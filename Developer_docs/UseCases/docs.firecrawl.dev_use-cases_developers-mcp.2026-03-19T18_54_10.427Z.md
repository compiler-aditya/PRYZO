Developers use Firecrawl’s MCP server to add web scraping to Claude Desktop, Cursor, and other AI coding assistants.

## [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#start-with-a-template)  Start with a Template

## MCP Server Firecrawl

Official MCP server - Add web scraping to Claude Desktop and Cursor

## Open Lovable

Build complete applications from any website instantly

**Get started with MCP in minutes.** Follow our [setup guide](https://github.com/firecrawl/firecrawl-mcp-server#installation) to integrate Firecrawl into Claude Desktop or Cursor.

## [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#how-it-works)  How It Works

Integrate Firecrawl directly into your AI coding workflow through Model Context Protocol. Once configured, your AI assistant gains access to a set of web scraping tools it can call on your behalf:

| Tool | What it does |
| --- | --- |
| **Scrape** | Extract content or structured data from a single URL |
| **Batch Scrape** | Extract content from multiple known URLs in parallel |
| **Map** | Discover all indexed URLs on a website |
| **Crawl** | Walk a site section and extract content from every page |
| **Search** | Search the web and optionally extract content from results |

Your assistant picks the right tool automatically — ask it to “read the Next.js docs” and it will scrape; ask it to “find all blog posts on example.com” and it will map then batch scrape.

## [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#why-developers-choose-firecrawl-mcp)  Why Developers Choose Firecrawl MCP

### [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#build-smarter-ai-assistants)  Build Smarter AI Assistants

Give your AI real-time access to documentation, APIs, and web resources. Reduce outdated information and hallucinations by providing your assistant with the latest data.

### [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#zero-infrastructure-required)  Zero Infrastructure Required

No servers to manage, no crawlers to maintain. Just configure once and your AI assistant can access websites instantly through the Model Context Protocol.

## [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#customer-stories)  Customer Stories

**Botpress**Discover how Botpress uses Firecrawl to streamline knowledge base population and improve developer experience.

**Answer HQ**Learn how Answer HQ uses Firecrawl to help businesses import website data and build intelligent support assistants.

## [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#faqs)  FAQs

Which AI assistants support MCP?

Currently, Claude Desktop and Cursor have native MCP support. More AI assistants are adding support regularly. You can also use the MCP SDK to build custom integrations.

Can I use MCP in VS Code or other IDEs?

VS Code and other IDEs can use MCP through community extensions or terminal integrations. Native support varies by IDE. Check our [GitHub repository](https://github.com/firecrawl/firecrawl-mcp-server) for IDE-specific setup guides.

How do I cache frequently accessed docs?

The MCP server automatically caches responses for 15 minutes. You can configure cache duration in your MCP server settings or implement custom caching logic.

Is there a rate limit for MCP requests?

MCP requests use your standard Firecrawl API rate limits. We recommend batching related requests and using caching for frequently accessed documentation.

How do I set up MCP with my Firecrawl API key?

Follow our [setup guide](https://github.com/firecrawl/firecrawl-mcp-server#installation) to configure MCP. You’ll need to add your Firecrawl API key to your MCP configuration file. The process takes just a few minutes.

## [​](https://docs.firecrawl.dev/use-cases/developers-mcp\#related-use-cases)  Related Use Cases

- [AI Platforms](https://docs.firecrawl.dev/use-cases/ai-platforms) \- Build AI-powered dev tools
- [Deep Research](https://docs.firecrawl.dev/use-cases/deep-research) \- Complex technical research
- [Content Generation](https://docs.firecrawl.dev/use-cases/content-generation) \- Generate documentation

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/use-cases/developers-mcp.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/use-cases/developers-mcp)

[Content Generation\\
\\
Previous](https://docs.firecrawl.dev/use-cases/content-generation) [Investment & Finance\\
\\
Next](https://docs.firecrawl.dev/use-cases/investment-finance)

⌘I