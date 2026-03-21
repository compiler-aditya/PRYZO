Academic researchers and analysts use Firecrawl’s deep research mode to aggregate data from hundreds of sources automatically.

## [​](https://docs.firecrawl.dev/use-cases/deep-research\#start-with-a-template)  Start with a Template

[**Fireplexity** \\
\\
Blazing-fast AI search with real-time citations](https://github.com/firecrawl/fireplexity)

[**Firesearch** \\
\\
Deep research agent with LangGraph and answer validation](https://github.com/firecrawl/firesearch)

[**Open Researcher** \\
\\
Visual AI research assistant for comprehensive analysis](https://github.com/firecrawl/open-researcher)

**Choose from multiple research templates.** Clone, configure your API key, and start researching.

## [​](https://docs.firecrawl.dev/use-cases/deep-research\#how-it-works)  How It Works

Build powerful research tools that transform scattered web data into comprehensive insights. The core pattern is a **search → scrape → analyze → repeat** loop: use Firecrawl’s search API to discover relevant sources, scrape each source for full content, then feed the results into an LLM to synthesize findings and identify follow-up queries.

1

[Navigate to header](https://docs.firecrawl.dev/use-cases/deep-research#)

Search for sources

Use the `/search` endpoint to find relevant pages for your research topic.

Python

Node.js

Copy

```
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

results = firecrawl.search(
    "recent advances in quantum computing",
    limit=5,
    scrape_options={"formats": ["markdown", "links"]}
)
```

2

[Navigate to header](https://docs.firecrawl.dev/use-cases/deep-research#)

Scrape discovered pages

Extract full content from each result to get detailed information with citations.

Python

Node.js

Copy

```
for result in results:
    doc = firecrawl.scrape(result["url"], formats=["markdown"])
    # Feed doc content into your LLM for analysis
```

3

[Navigate to header](https://docs.firecrawl.dev/use-cases/deep-research#)

Analyze and iterate

Use an LLM to synthesize findings, identify gaps, and generate follow-up queries. Repeat the loop until your research question is fully answered.

## [​](https://docs.firecrawl.dev/use-cases/deep-research\#why-researchers-choose-firecrawl)  Why Researchers Choose Firecrawl

### [​](https://docs.firecrawl.dev/use-cases/deep-research\#accelerate-research-from-weeks-to-hours)  Accelerate Research from Weeks to Hours

Build automated research systems that discover, read, and synthesize information from across the web. Create tools that deliver comprehensive reports with full citations, eliminating manual searching through hundreds of sources.

### [​](https://docs.firecrawl.dev/use-cases/deep-research\#ensure-research-completeness)  Ensure Research Completeness

Reduce the risk of missing critical information. Build systems that follow citation chains, discover related sources, and surface insights that traditional search methods miss.

## [​](https://docs.firecrawl.dev/use-cases/deep-research\#research-tool-capabilities)  Research Tool Capabilities

- **Iterative Exploration**: Build tools that automatically discover related topics and sources
- **Multi-Source Synthesis**: Combine information from hundreds of websites
- **Citation Preservation**: Maintain full source attribution in your research outputs
- **Intelligent Summarization**: Extract key findings and insights for analysis
- **Trend Detection**: Identify patterns across multiple sources

## [​](https://docs.firecrawl.dev/use-cases/deep-research\#faqs)  FAQs

How can I build research tools with Firecrawl?

Use Firecrawl’s crawl and search APIs to build iterative research systems. Start with search results, extract content from relevant pages, follow citation links, and aggregate findings. Combine with LLMs to synthesize comprehensive research reports.

Can Firecrawl handle academic and scientific websites?

Yes. Firecrawl can extract data from open-access research papers, academic websites, and publicly available scientific publications. It preserves formatting, citations, and technical content critical for research work.

How do I ensure research data accuracy?

Firecrawl maintains source attribution and extracts content exactly as presented on websites. All data includes source URLs and timestamps, ensuring full traceability for research purposes.

Can I use Firecrawl for longitudinal studies?

Yes. Set up scheduled crawls to track how information changes over time. This is perfect for monitoring trends, policy changes, or any research requiring temporal data analysis.

How does Firecrawl handle large-scale research projects?

Our crawling infrastructure scales to handle thousands of sources simultaneously. Whether you’re analyzing entire industries or tracking global trends, Firecrawl provides the data pipeline you need.

## [​](https://docs.firecrawl.dev/use-cases/deep-research\#related-use-cases)  Related Use Cases

- [AI Platforms](https://docs.firecrawl.dev/use-cases/ai-platforms) \- Build AI research assistants
- [Content Generation](https://docs.firecrawl.dev/use-cases/content-generation) \- Research-based content
- [Competitive Intelligence](https://docs.firecrawl.dev/use-cases/competitive-intelligence) \- Market research

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/use-cases/deep-research.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/use-cases/deep-research)

[SEO Platforms\\
\\
Previous](https://docs.firecrawl.dev/use-cases/seo-platforms) [Product & E-commerce\\
\\
Next](https://docs.firecrawl.dev/use-cases/product-ecommerce)

Ctrl+I