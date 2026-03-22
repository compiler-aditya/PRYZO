"""Blog scraping and CC-licensed content discovery using Firecrawl.

Handles major blog platforms:
- WordPress (.com and self-hosted)
- Blogspot / Blogger (JS-heavy, uses feed fallback)
- Medium
- Substack
- Ghost
- Hugo / Jekyll / static site generators
- Tumblr
- Wix / Squarespace
- Paul Graham-style custom HTML sites
- Generic sites with RSS/Atom feeds
- Any direct article URL
"""

import re
import asyncio
import html as html_mod
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin
import httpx
from firecrawl import FirecrawlApp
from config import settings

fc = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)

# URL path segments that are NOT articles (navigation/utility pages)
SKIP_SEGMENTS = {
    "about", "contact", "privacy", "terms", "login", "signup", "register",
    "search", "tags", "categories", "archive", "author", "feed", "feeds", "rss",
    "sitemap", "wp-admin", "wp-login", "cart", "checkout", "account",
    "subscribe", "unsubscribe", "cookie", "legal", "faq", "help",
    "tag", "category", "page", "comments", "trackback", "wp-json",
    "wp-content", "wp-includes", "cdn-cgi", "api", "static", "assets",
    "media", "uploads", "images", "img", "css", "js", "fonts",
}

# File extensions that are never articles
SKIP_EXTENSIONS = re.compile(
    r"\.(css|js|png|jpg|jpeg|gif|svg|ico|pdf|zip|xml|json|woff2?|ttf|eot|mp[34]|wav|webp|avif)$",
    re.IGNORECASE,
)

# Platform-specific feed paths (ordered by likelihood)
_FEED_PATHS = [
    "/feeds/posts/default",       # Blogspot / Blogger
    "/feed",                      # WordPress, Substack, Dev.to
    "/rss",                       # Ghost, Tumblr
    "/rss/",                      # Ghost variant
    "/feed.xml",                  # Jekyll
    "/atom.xml",                  # Atom (Jekyll, Hugo)
    "/index.xml",                 # Hugo
    "/blog/feed",                 # WordPress with /blog prefix
    "/blog/rss",                  # Ghost with /blog prefix
    "/?feed=rss2",                # WordPress fallback
    "/rss.xml",                   # Generic
]


def _normalize_url(url: str) -> str:
    """Ensure URL has a protocol and is clean."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")


def _get_base_url(url: str) -> str:
    """Extract base URL (scheme + host)."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _detect_platform(url: str) -> str | None:
    """Detect blog platform from URL patterns."""
    host = urlparse(url).netloc.lower()
    if "blogspot.com" in host or "blogger.com" in host:
        return "blogger"
    if "medium.com" in host:
        return "medium"
    if "substack.com" in host or ".substack." in host:
        return "substack"
    if "tumblr.com" in host:
        return "tumblr"
    if "ghost.io" in host:
        return "ghost"
    if "wordpress.com" in host or "wp.com" in host:
        return "wordpress"
    if "wixsite.com" in host or "wix.com" in host:
        return "wix"
    if "squarespace.com" in host:
        return "squarespace"
    if "hashnode.dev" in host or "hashnode.com" in host:
        return "hashnode"
    if "dev.to" in host:
        return "devto"
    return None


def _is_index_page(url: str) -> bool:
    """Detect index/listing pages that aren't actual articles."""
    parsed = urlparse(url)
    path = parsed.path.lower().rstrip("/")
    filename = path.split("/")[-1] if "/" in path else path

    index_names = {
        "index.html", "index.htm", "articles.html", "articles.htm",
        "blog.html", "posts.html", "archive.html", "archives.html",
        "essays.html", "writing.html", "all.html", "list.html",
        "index", "articles", "blog", "posts", "archive", "archives",
        "essays", "writing", "blog-posts", "all-posts",
    }
    return filename in index_names or path in ("", "/")


def _is_useful_url(url: str) -> bool:
    """Filter out navigation/utility pages that aren't articles."""
    parsed = urlparse(url)
    path = parsed.path.lower().rstrip("/")
    segments = [s for s in path.split("/") if s]

    # Skip if any segment is a known non-article page
    for seg in segments:
        if seg in SKIP_SEGMENTS:
            return False

    # Skip asset/file URLs
    if SKIP_EXTENSIONS.search(path):
        return False

    # Skip fragment-only URLs
    if not path or path == "/":
        return False

    # Need at least some path depth (filters out bare domain matches)
    if len(segments) == 0:
        return False

    return True


async def scrape_blog_posts(blog_url: str, limit: int = 50) -> list[dict]:
    """Scrape posts from a blog URL or a single article URL.

    Multi-strategy approach:
    1. Try Firecrawl map() to discover article URLs
    2. Try extracting links from the page HTML
    3. Scrape discovered articles with Firecrawl
    4. If scraping fails (JS-heavy sites), fall back to RSS/Atom feed
    5. For single article URLs, scrape directly

    Handles all major platforms: WordPress, Blogspot, Medium, Substack,
    Ghost, Hugo, Jekyll, Tumblr, Wix, Squarespace, custom sites.
    """
    blog_url = _normalize_url(blog_url)
    scrape_cap = min(limit, 5)
    platform = _detect_platform(blog_url)
    is_likely_article = _is_likely_article_url(blog_url)

    # If URL looks like a specific article, try scraping it directly first
    if is_likely_article:
        post = await _scrape_one(blog_url)
        if post:
            return [post]
        # Scrape failed — try feed fallback for JS-heavy sites
        posts = await _scrape_via_feed(blog_url, scrape_cap)
        if posts:
            return posts
        return []

    # For known JS-heavy platforms, skip straight to feed
    if platform in ("blogger", "wix"):
        posts = await _scrape_via_feed(blog_url, scrape_cap)
        if posts:
            return posts

    # Step 1: Discover article URLs
    discovered = await _discover_urls(blog_url, limit)

    # Step 2: If discovery found multiple URLs, scrape them
    if len(discovered) > 1:
        filtered = _filter_article_urls(discovered)

        if filtered:
            posts = await _scrape_batch(filtered[:scrape_cap])
            if posts:
                return posts

        # Scraping all failed — try feed
        posts = await _scrape_via_feed(blog_url, scrape_cap)
        if posts:
            return posts

    # Step 3: Scrape the submitted URL directly
    post = await _scrape_one(blog_url)
    if post:
        return [post]

    # Step 4: Last resort — try feed
    posts = await _scrape_via_feed(blog_url, scrape_cap)
    if posts:
        return posts

    return []


def _is_likely_article_url(url: str) -> bool:
    """Heuristic: is this URL a specific article rather than a blog root/index?"""
    parsed = urlparse(url)
    path = parsed.path.lower().rstrip("/")

    # Root URL or empty path = not an article
    if not path or path == "/":
        return False

    # Known index pages
    if _is_index_page(url):
        return False

    segments = [s for s in path.split("/") if s]

    # URLs with date-like patterns are almost always articles
    # e.g., /2024/03/my-post, /2024/my-post.html
    if any(re.match(r"^\d{4}$", s) for s in segments):
        return True

    # URLs ending in .html/.htm are usually articles on static sites
    if path.endswith((".html", ".htm")):
        return True

    # URLs with slugs (long path segments with hyphens) are likely articles
    # e.g., /my-great-blog-post, /p/the-title-of-my-article
    last = segments[-1] if segments else ""
    if "-" in last and len(last) > 10:
        return True

    # Medium/Substack article patterns: /@user/slug or /p/slug
    if any(s.startswith("@") for s in segments):
        return True
    if "p" in segments and len(segments) >= 2:
        return True

    return False


def _filter_article_urls(urls: list[str]) -> list[str]:
    """Deduplicate and filter URLs to only likely article pages."""
    seen = set()
    filtered = []
    for url in urls:
        normalized = _normalize_url(url)
        # Normalize www vs non-www
        key = normalized.replace("://www.", "://")
        if key not in seen and _is_useful_url(normalized) and not _is_index_page(normalized):
            seen.add(key)
            filtered.append(normalized)
    return filtered


async def _discover_urls(blog_url: str, limit: int) -> list[str]:
    """Discover article URLs using multiple strategies."""
    # Strategy 1: Firecrawl map (works for most sites)
    try:
        map_result = fc.map(url=blog_url, limit=limit)
        if map_result and map_result.links:
            urls = [link.url if hasattr(link, 'url') else str(link) for link in map_result.links]
            unique = set(urls)
            if len(unique) > 2:
                return list(unique)[:limit]
    except Exception:
        pass

    # Strategy 2: Scrape page and extract links
    try:
        result = fc.scrape(url=blog_url, formats=["links"])
        if result and result.links:
            parsed_base = urlparse(blog_url)
            base_domain = parsed_base.netloc.replace("www.", "")
            same_domain = []
            for link in result.links:
                link_str = str(link)
                parsed = urlparse(link_str)
                link_domain = parsed.netloc.replace("www.", "")
                if link_domain == base_domain and _is_useful_url(link_str):
                    same_domain.append(link_str)
            if len(same_domain) > 1:
                return same_domain[:limit]
    except Exception:
        pass

    return []


async def _scrape_batch(urls: list[str]) -> list[dict]:
    """Scrape multiple URLs in parallel."""
    tasks = [_scrape_one(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return [p for p in results if p]


async def _scrape_one(url: str) -> dict | None:
    """Scrape a single URL with fallback strategies."""
    # Try 1: main content only (cleanest)
    post = await _scrape_with_options(url, only_main_content=True)
    if post:
        return post

    # Try 2: full page (catches content that main-content filter misses)
    post = await _scrape_with_options(url, only_main_content=False)
    if post:
        return post

    return None


async def _scrape_with_options(url: str, only_main_content: bool = True) -> dict | None:
    """Single scrape attempt with given options."""
    try:
        kwargs = {"url": url, "formats": ["markdown"]}
        if only_main_content:
            kwargs["only_main_content"] = True

        result = fc.scrape(**kwargs)

        if not result or not result.markdown:
            return None

        text = _clean_markdown(result.markdown)

        if len(text) < 150:
            return None

        title = "Untitled"
        if result.metadata:
            title = getattr(result.metadata, "title", None) or "Untitled"

        return {
            "url": url,
            "title": title,
            "text": text,
        }
    except Exception:
        return None


async def _scrape_via_feed(blog_url: str, limit: int) -> list[dict]:
    """Fetch and parse RSS/Atom feed directly (bypasses Firecrawl).

    Works for JS-heavy sites where Firecrawl can't render content:
    Blogspot, Wix, and any site with a standard feed.
    """
    parsed = urlparse(blog_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    platform = _detect_platform(blog_url)

    # Platform-specific feed ordering for faster discovery
    feed_paths = list(_FEED_PATHS)
    if platform == "blogger":
        feed_paths = ["/feeds/posts/default"] + [p for p in feed_paths if p != "/feeds/posts/default"]
    elif platform in ("wordpress", None):
        feed_paths = ["/feed", "/?feed=rss2", "/blog/feed"] + [p for p in feed_paths if p not in ("/feed", "/?feed=rss2", "/blog/feed")]
    elif platform == "ghost":
        feed_paths = ["/rss/", "/rss"] + [p for p in feed_paths if p not in ("/rss/", "/rss")]
    elif platform == "substack":
        feed_paths = ["/feed"] + feed_paths

    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        for feed_path in feed_paths:
            feed_url = base + feed_path
            try:
                resp = await client.get(feed_url)
                if resp.status_code != 200 or len(resp.text) < 200:
                    continue

                content_type = resp.headers.get("content-type", "")
                # Verify it's actually a feed, not an HTML page
                if "html" in content_type and "xml" not in content_type and "<rss" not in resp.text[:500] and "<feed" not in resp.text[:500]:
                    continue

                posts = _parse_feed_xml(resp.text, base)
                if posts:
                    return posts[:limit]
            except Exception:
                continue
    return []


def _parse_feed_xml(xml_text: str, base_url: str) -> list[dict]:
    """Parse RSS or Atom feed XML into post dicts."""
    posts = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    # Collect all namespace URIs used in the document
    atom_ns = "http://www.w3.org/2005/Atom"
    content_ns = "http://purl.org/rss/1.0/modules/content/"

    # Find entries (Atom) or items (RSS)
    entries = (
        root.findall(f".//{{{atom_ns}}}entry") or
        root.findall(".//entry") or
        root.findall(".//item") or
        root.findall(".//channel/item") or
        []
    )

    for entry in entries:
        # --- Title ---
        title = (
            _xt(entry, f"{{{atom_ns}}}title") or
            _xt(entry, "title") or
            "Untitled"
        )

        # --- Content (try multiple tags) ---
        content = (
            _xt(entry, f"{{{atom_ns}}}content") or
            _xt(entry, f"{{{content_ns}}}encoded") or
            _xt(entry, "content:encoded") or
            _xt(entry, "content") or
            _xt(entry, f"{{{atom_ns}}}summary") or
            _xt(entry, "description") or
            _xt(entry, "summary") or
            ""
        )

        # --- Link ---
        link = _extract_link(entry, atom_ns)

        # --- Clean content to plain text ---
        text = re.sub(r"<[^>]+>", " ", content)
        text = html_mod.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) < 100:
            continue

        posts.append({
            "url": link or base_url,
            "title": title.strip(),
            "text": text[:5000],
        })

    return posts


def _xt(el: ET.Element, tag: str) -> str | None:
    """Get text content of a child element (handles namespaced and plain tags)."""
    child = el.find(tag)
    if child is not None:
        # Some feeds put content in CDATA which ET reads as .text
        return child.text or ""
    return None


def _extract_link(entry: ET.Element, atom_ns: str) -> str:
    """Extract the article link from a feed entry."""
    # Atom: <link rel="alternate" href="..." />
    for link_tag in [f"{{{atom_ns}}}link", "link"]:
        for link_el in entry.findall(link_tag):
            rel = link_el.get("rel", "alternate")
            href = link_el.get("href", "")
            if rel == "alternate" and href:
                return href

    # RSS: <link>text</link>
    link_el = entry.find("link")
    if link_el is not None and link_el.text:
        return link_el.text.strip()

    # Atom: <id> as fallback (Blogger uses tag: URIs but sometimes has URLs)
    id_el = entry.find(f"{{{atom_ns}}}id") or entry.find("id") or entry.find("guid")
    if id_el is not None and id_el.text and id_el.text.startswith("http"):
        return id_el.text.strip()

    return ""


def _clean_markdown(md: str) -> str:
    """Clean scraped markdown of common junk."""
    lines = md.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()

        # Skip empty table rows and separator rows
        if re.match(r"^\|[\s\-|]*\|?$", stripped):
            continue

        # Skip lines that are only images/links/pipes (handles nested markdown too)
        text_only = re.sub(r"!?\[.*?\]\(.*?\)", "", stripped)  # remove images/links
        text_only = re.sub(r"\[|\]|\(|\)", "", text_only)       # stray brackets
        text_only = re.sub(r"https?://\S+", "", text_only)      # bare URLs
        text_only = text_only.replace("|", "").replace("-", "").strip()
        if stripped and len(text_only) < 5:
            continue

        # Skip horizontal rules
        if re.match(r"^[\-\*_]{3,}$", stripped):
            continue

        # Skip "Skip to main content" links
        if "skip to main content" in stripped.lower():
            continue

        # Skip common nav/footer junk
        if stripped.lower() in ("menu", "navigation", "search", "home", "close"):
            continue

        # Extract content from table cells (PG-style sites wrap text in tables)
        if stripped.startswith("|") and "<br>" in stripped:
            # Pull text out of table cell, convert <br> to newlines
            cell_text = re.sub(r"^\|?\s*", "", stripped).rstrip("|").strip()
            # Remove leading image markdown
            cell_text = re.sub(r"^!?\[.*?\]\(.*?\)\s*", "", cell_text)
            cell_text = cell_text.replace("<br>", "\n")
            if cell_text.strip():
                cleaned.append(cell_text)
                continue

        cleaned.append(line)

    text = "\n".join(cleaned).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


async def scrape_single_post(url: str) -> dict | None:
    """Scrape a single blog post and extract content + license info."""
    url = _normalize_url(url)
    return await _scrape_one(url)


async def discover_cc_blogs() -> list[dict]:
    """Use Firecrawl Agent to discover CC-licensed personal blogs."""
    try:
        result = fc.agent(
            prompt="""Find personal blogs published under Creative Commons licenses
(CC-BY, CC-BY-SA, CC0, or public domain). Focus on blogs about personal
experiences, emotions, life changes, loss, love, fear, identity, growth.

Target sources:
- zenhabits.net (explicitly uncopyrighted/public domain)
- raptitude.com (CC-BY)
- WordPress blogs with CC license metadata
- Medium posts published under CC
- Personal domains with CC declarations in footer

For each blog found, return:
- The blog URL
- The detected license type
- A brief description of the content

Return at least 10 blogs.""",
            schema={
                "type": "object",
                "properties": {
                    "blogs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string"},
                                "license": {"type": "string"},
                                "description": {"type": "string"},
                            },
                        },
                    },
                },
            },
            max_credits=2500,
        )

        if result and hasattr(result, "data") and result.data:
            blogs = result.data.get("blogs", []) if isinstance(result.data, dict) else []
            return blogs
    except Exception:
        pass
    return []


def verify_license(attributes: dict) -> str | None:
    """Verify CC license from scraped page attributes."""
    valid_licenses = {
        "creativecommons.org/publicdomain/zero": "CC0",
        "creativecommons.org/licenses/by/": "CC-BY",
        "creativecommons.org/licenses/by-sa/": "CC-BY-SA",
        "creativecommons.org/licenses/by-nc/": "CC-BY-NC",
    }

    for key, values in attributes.items():
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if not isinstance(value, str):
                continue
            value_lower = value.lower()
            for pattern, license_type in valid_licenses.items():
                if pattern in value_lower:
                    return license_type

    return None
