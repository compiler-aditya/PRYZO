"""Story quality scoring and moment evaluation using Gemini."""

import json
from google import genai
from config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-2.5-flash"


async def score_story(text: str, source_type: str = "user_blog") -> dict:
    """Score a story on emotional depth, universality, and originality.

    Returns:
        {
            "emotional_depth": int (1-10),
            "universality": int (1-10),
            "originality": int (1-10),
            "category": str,
            "emotion": str,
            "is_ai_probability": float (0-1),
            "title_suggestion": str,
            "passes": bool
        }
    """
    response = client.models.generate_content(
        model=MODEL,
        contents=f"""Score this text for Voiceless — a platform that turns human-written content into audio episodes.

We accept a WIDE range of human writing: personal stories, philosophical essays, scientific reflections,
expert knowledge sharing, opinion pieces, creative writing, cultural commentary, poetry, technical deep-dives
written with passion, memoirs, travel writing, and more.

Rate on three dimensions (1-10):

1. HUMAN_VOICE: Is this genuinely written by a human with a personal perspective?
   Score HIGH (7-10) for:
   - Personal stories with real emotion
   - Expert writing where the author's passion/experience shows through
   - Philosophical or intellectual essays with a distinct viewpoint
   - Scientific writing that shares wonder, curiosity, or hard-won insight
   - Poetry, creative writing, cultural commentary
   - Opinion pieces with genuine conviction
   Score LOW (1-3) for:
   - Auto-generated product pages, SEO spam, marketing copy
   - Generic corporate content with no human voice
   - Random website pages (navigation menus, terms of service, landing pages)
   - Pure data dumps or tables with no narrative
   - AI-generated filler content

2. SUBSTANCE: Does this have real depth — emotional, intellectual, or experiential?
   Score HIGH for: deep personal reflection, rigorous analysis, hard-won wisdom,
   unique expertise, genuine philosophical inquiry, vivid storytelling
   Score LOW for: shallow listicles, recycled motivational quotes, surface-level takes,
   content that says nothing new

3. ORIGINALITY: Is this a fresh or authentic perspective?
   Score HIGH for: unique life experiences, novel arguments, specialist knowledge,
   unconventional viewpoints, distinctive writing voice
   Score LOW for: generic advice, cliches, content indistinguishable from a thousand other posts

Also determine:
- CATEGORY: exactly one of: loss, love, identity, work, family, fear, joy, change, regret, hope, philosophy, science, craft, culture, wisdom
- EMOTION: exactly one of: grief, joy, anger, nostalgia, fear, peace, love, regret, wonder, conviction, curiosity
- IS_AI: probability this was written by AI (0.0 = definitely human, 1.0 = definitely AI).
  Score HIGH if it reads like ChatGPT output (generic, hedging, overly balanced, no personal voice).
  Score LOW if it has quirks, strong opinions, specific experiences, or distinctive style.
- IS_BLOG: is this actual blog/essay/article content written by a person? (true/false)
  false if it's a product page, navigation page, terms of service, landing page, API docs, etc.
- TITLE: suggest a short evocative title (3-6 words, no quotes)

Respond as JSON only, no markdown:
{{"human_voice": 8, "substance": 9, "originality": 7, "category": "philosophy", "emotion": "wonder", "is_ai_probability": 0.1, "is_blog": true, "title_suggestion": "The Weight of Knowing"}}

TEXT:
{text}""",
    )

    try:
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
        result = json.loads(raw)
    except (json.JSONDecodeError, IndexError):
        return {
            "human_voice": 0,
            "substance": 0,
            "originality": 0,
            "category": "hope",
            "emotion": "peace",
            "is_ai_probability": 0.5,
            "is_blog": False,
            "title_suggestion": "Untitled",
            "passes": False,
        }

    # Map new field names back to legacy names for compatibility
    result.setdefault("emotional_depth", result.get("human_voice", 0))
    result.setdefault("universality", result.get("substance", 0))

    is_blog = result.get("is_blog", True)
    total = result.get("human_voice", 0) + result.get("substance", 0) + result.get("originality", 0)

    # Skip is_blog check for direct user submissions — they're not blog posts
    blog_ok = is_blog if source_type == "user_blog" else True

    result["passes"] = (
        blog_ok
        and total >= 10
        and result.get("is_ai_probability", 1.0) < 0.85
    )

    return result


async def score_stories_batch(posts: list[dict]) -> list[tuple[dict, dict]]:
    """Score multiple blog posts and return sorted by quality.

    Args:
        posts: List of {"url": str, "title": str, "text": str}

    Returns:
        List of (post, score) tuples sorted by total score descending
    """
    scored = []
    for post in posts:
        score = await score_story(post["text"])
        if score["passes"]:
            scored.append((post, score))

    scored.sort(
        key=lambda x: x[1]["emotional_depth"] + x[1]["universality"] + x[1]["originality"],
        reverse=True,
    )
    return scored


async def evaluate_moment(text: str) -> dict:
    """Evaluate if a life moment is meaningful enough to publish.

    Returns:
        {
            "approved": bool,
            "score": float,
            "guidance": str | None,
            "emotion": str,
            "category": str
        }
    """
    response = client.models.generate_content(
        model=MODEL,
        contents=f"""Evaluate if this is a meaningful life moment worth sharing on an anonymous storytelling platform.

MEANINGFUL (score 6-10):
- Real emotional inflection points ("Today I forgave someone I swore I never would")
- Moments of realization, loss, joy, courage, vulnerability
- Something that would make a stranger stop scrolling and listen

NOT MEANINGFUL (score 1-5):
- Daily routine ("went to gym", "had coffee", "worked late")
- Generic status updates ("feeling tired", "busy day")
- Mundane observations without emotional weight

If the score is below 6, write a gentle redirect message. NOT rejection — encouragement to dig deeper. Examples:
- "Thanks for sharing. Was there a specific moment today that surprised you or made you feel something unexpected?"
- "What was the one thing about today that you'll still remember next week?"

Respond as JSON only, no markdown:
{{"score": 7.5, "is_meaningful": true, "guidance": null, "emotion": "peace", "category": "change"}}

TEXT:
{text}""",
    )

    try:
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
        result = json.loads(raw)
    except (json.JSONDecodeError, IndexError):
        return {"approved": True, "score": 6.0, "guidance": None, "emotion": "peace", "category": "hope"}

    return {
        "approved": result.get("is_meaningful", False),
        "score": result.get("score", 0),
        "guidance": result.get("guidance"),
        "emotion": result.get("emotion", "peace"),
        "category": result.get("category", "hope"),
    }
