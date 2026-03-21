Add web scraping and search capabilities to Claude Code with Firecrawl MCP.

## [​](https://docs.firecrawl.dev/developer-guides/mcp-setup-guides/claude-code\#quick-setup)  Quick Setup

### [​](https://docs.firecrawl.dev/developer-guides/mcp-setup-guides/claude-code\#1-get-your-api-key)  1\. Get Your API Key

Sign up at [firecrawl.dev/app](https://firecrawl.dev/app) and copy your API key.

### [​](https://docs.firecrawl.dev/developer-guides/mcp-setup-guides/claude-code\#2-add-firecrawl-mcp-server)  2\. Add Firecrawl MCP Server

**Option A: Remote hosted URL (recommended)**

Copy

```
claude mcp add firecrawl --url https://mcp.firecrawl.dev/your-api-key/v2/mcp
```

**Option B: Local (npx)**

Copy

```
claude mcp add firecrawl -e FIRECRAWL_API_KEY=your-api-key -- npx -y firecrawl-mcp
```

Replace `your-api-key` with your actual Firecrawl API key.Done! You can now search and scrape the web from Claude Code.

## [​](https://docs.firecrawl.dev/developer-guides/mcp-setup-guides/claude-code\#quick-demo)  Quick Demo

Try these in Claude Code:**Search the web:**

Copy

```
Search for the latest Next.js 15 features
```

**Scrape a page:**

Copy

```
Scrape firecrawl.dev and tell me what it does
```

**Get documentation:**

Copy

```
Find and scrape the Stripe API docs for payment intents
```

Claude will automatically use Firecrawl’s search and scrape tools to get the information.

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/developer-guides/mcp-setup-guides/claude-code.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/developer-guides/mcp-setup-guides/claude-code)

[MCP Web Search & Scrape in ChatGPT\\
\\
Previous](https://docs.firecrawl.dev/developer-guides/mcp-setup-guides/chatgpt) [MCP Web Search & Scrape in Cursor\\
\\
Next](https://docs.firecrawl.dev/developer-guides/mcp-setup-guides/cursor)

Ctrl+I