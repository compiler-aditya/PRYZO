Integrate Firecrawl with LlamaIndex to build AI applications with vector search and embeddings powered by web content.

## [​](https://docs.firecrawl.dev/developer-guides/llm-sdks-and-frameworks/llamaindex\#setup)  Setup

Copy

```
npm install llamaindex @llamaindex/openai @mendable/firecrawl-js
```

Create `.env` file:

Copy

```
FIRECRAWL_API_KEY=your_firecrawl_key
OPENAI_API_KEY=your_openai_key
```

> **Note:** If using Node < 20, install `dotenv` and add `import 'dotenv/config'` to your code.

## [​](https://docs.firecrawl.dev/developer-guides/llm-sdks-and-frameworks/llamaindex\#rag-with-vector-search)  RAG with Vector Search

This example demonstrates how to use LlamaIndex with Firecrawl to crawl a website, create embeddings, and query the content using RAG.

Copy

```
import Firecrawl from '@mendable/firecrawl-js';
import { Document, VectorStoreIndex, Settings } from 'llamaindex';
import { OpenAI, OpenAIEmbedding } from '@llamaindex/openai';

Settings.llm = new OpenAI({ model: "gpt-4o" });
Settings.embedModel = new OpenAIEmbedding({ model: "text-embedding-3-small" });

const firecrawl = new Firecrawl({ apiKey: process.env.FIRECRAWL_API_KEY });
const crawlResult = await firecrawl.crawl('https://firecrawl.dev', {
  limit: 10,
  scrapeOptions: { formats: ['markdown'] }
});
console.log(`Crawled ${crawlResult.data.length } pages`);

const documents = crawlResult.data.map((page: any, i: number) =>
  new Document({
    text: page.markdown,
    id_: `page-${i}`,
    metadata: { url: page.metadata?.sourceURL }
  })
);

const index = await VectorStoreIndex.fromDocuments(documents);
console.log('Vector index created with embeddings');

const queryEngine = index.asQueryEngine();
const response = await queryEngine.query({ query: 'What is Firecrawl and how does it work?' });

console.log('\nAnswer:', response.toString());
```

For more examples, check the [LlamaIndex documentation](https://ts.llamaindex.ai/).

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/developer-guides/llm-sdks-and-frameworks/llamaindex.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/developer-guides/llm-sdks-and-frameworks/llamaindex)

[LangGraph\\
\\
Previous](https://docs.firecrawl.dev/developer-guides/llm-sdks-and-frameworks/langgraph) [Mastra\\
\\
Next](https://docs.firecrawl.dev/developer-guides/llm-sdks-and-frameworks/mastra)

⌘I