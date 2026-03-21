## [​](https://docs.firecrawl.dev/webhooks/events\#quick-reference)  Quick Reference

| Event | Trigger |
| --- | --- |
| `crawl.started` | Crawl job begins processing |
| `crawl.page` | A page is scraped during a crawl |
| `crawl.completed` | Crawl job finishes and all pages have been processed |
| `batch_scrape.started` | Batch scrape job begins processing |
| `batch_scrape.page` | A URL is scraped during a batch scrape |
| `batch_scrape.completed` | All URLs in the batch have been processed |
| `extract.started` | Extract job begins processing |
| `extract.completed` | Extraction finishes successfully |
| `extract.failed` | Extraction fails |
| `agent.started` | Agent job begins processing |
| `agent.action` | Agent executes a tool (scrape, search, etc.) |
| `agent.completed` | Agent finishes successfully |
| `agent.failed` | Agent encounters an error |
| `agent.cancelled` | Agent job is cancelled by the user |

## [​](https://docs.firecrawl.dev/webhooks/events\#payload-structure)  Payload Structure

All webhook events share this structure:

Copy

```
{
  "success": true,
  "type": "crawl.page",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [...],
  "metadata": {}
}
```

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | Whether the operation succeeded |
| `type` | string | Event type (e.g. `crawl.page`) |
| `id` | string | Job ID |
| `data` | array | Event-specific data (see examples below) |
| `metadata` | object | Custom metadata from your webhook config |
| `error` | string | Error message (when `success` is `false`) |

## [​](https://docs.firecrawl.dev/webhooks/events\#crawl-events)  Crawl Events

### [​](https://docs.firecrawl.dev/webhooks/events\#crawl-started)  `crawl.started`

Sent when the crawl job begins processing.

Copy

```
{
  "success": true,
  "type": "crawl.started",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#crawl-page)  `crawl.page`

Sent for each page scraped. The `data` array contains the page content and metadata.

Copy

```
{
  "success": true,
  "type": "crawl.page",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "markdown": "# Page content...",\
      "metadata": {\
        "title": "Page Title",\
        "description": "Page description",\
        "url": "https://example.com/page",\
        "statusCode": 200,\
        "contentType": "text/html",\
        "scrapeId": "550e8400-e29b-41d4-a716-446655440001",\
        "sourceURL": "https://example.com/page",\
        "proxyUsed": "basic",\
        "cacheState": "hit",\
        "cachedAt": "2025-09-03T21:11:25.636Z",\
        "creditsUsed": 1\
      }\
    }\
  ],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#crawl-completed)  `crawl.completed`

Sent when the crawl job finishes and all pages have been processed.

Copy

```
{
  "success": true,
  "type": "crawl.completed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {}
}
```

## [​](https://docs.firecrawl.dev/webhooks/events\#batch-scrape-events)  Batch Scrape Events

### [​](https://docs.firecrawl.dev/webhooks/events\#batch_scrape-started)  `batch_scrape.started`

Sent when the batch scrape job begins processing.

Copy

```
{
  "success": true,
  "type": "batch_scrape.started",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#batch_scrape-page)  `batch_scrape.page`

Sent for each URL scraped. The `data` array contains the page content and metadata.

Copy

```
{
  "success": true,
  "type": "batch_scrape.page",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "markdown": "# Page content...",\
      "metadata": {\
        "title": "Page Title",\
        "description": "Page description",\
        "url": "https://example.com",\
        "statusCode": 200,\
        "contentType": "text/html",\
        "scrapeId": "550e8400-e29b-41d4-a716-446655440001",\
        "sourceURL": "https://example.com",\
        "proxyUsed": "basic",\
        "cacheState": "miss",\
        "cachedAt": "2025-09-03T23:30:53.434Z",\
        "creditsUsed": 1\
      }\
    }\
  ],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#batch_scrape-completed)  `batch_scrape.completed`

Sent when all URLs in the batch have been processed.

Copy

```
{
  "success": true,
  "type": "batch_scrape.completed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {}
}
```

## [​](https://docs.firecrawl.dev/webhooks/events\#extract-events)  Extract Events

### [​](https://docs.firecrawl.dev/webhooks/events\#extract-started)  `extract.started`

Sent when the extract job begins processing.

Copy

```
{
  "success": true,
  "type": "extract.started",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#extract-completed)  `extract.completed`

Sent when extraction finishes successfully. The `data` array contains the extracted data and usage info.

Copy

```
{
  "success": true,
  "type": "extract.completed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "success": true,\
      "data": { "siteName": "Example Site", "category": "Technology" },\
      "extractId": "550e8400-e29b-41d4-a716-446655440000",\
      "llmUsage": 0.0020118,\
      "totalUrlsScraped": 1,\
      "sources": {\
        "siteName": ["https://example.com"],\
        "category": ["https://example.com"]\
      }\
    }\
  ],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#extract-failed)  `extract.failed`

Sent when extraction fails. The `error` field contains the failure reason.

Copy

```
{
  "success": false,
  "type": "extract.failed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "error": "Failed to extract data: timeout exceeded",
  "metadata": {}
}
```

## [​](https://docs.firecrawl.dev/webhooks/events\#agent-events)  Agent Events

### [​](https://docs.firecrawl.dev/webhooks/events\#agent-started)  `agent.started`

Sent when the agent job begins processing.

Copy

```
{
  "success": true,
  "type": "agent.started",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#agent-action)  `agent.action`

Sent after each tool execution (scrape, search, etc.).

Copy

```
{
  "success": true,
  "type": "agent.action",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "creditsUsed": 5,\
      "action": "mcp__tools__scrape",\
      "input": {\
        "url": "https://example.com"\
      }\
    }\
  ],
  "metadata": {}
}
```

The `creditsUsed` value in `action` events is an **estimate** of the total
credits used so far. The final accurate credit count is only
available in the `completed`, `failed`, or `cancelled` events.

### [​](https://docs.firecrawl.dev/webhooks/events\#agent-completed)  `agent.completed`

Sent when the agent finishes successfully. The `data` array contains the extracted data and total credits used.

Copy

```
{
  "success": true,
  "type": "agent.completed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "creditsUsed": 15,\
      "data": {\
        "company": "Example Corp",\
        "industry": "Technology",\
        "founded": 2020\
      }\
    }\
  ],
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#agent-failed)  `agent.failed`

Sent when the agent encounters an error. The `error` field contains the failure reason.

Copy

```
{
  "success": false,
  "type": "agent.failed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "creditsUsed": 8\
    }\
  ],
  "error": "Max credits exceeded",
  "metadata": {}
}
```

### [​](https://docs.firecrawl.dev/webhooks/events\#agent-cancelled)  `agent.cancelled`

Sent when the agent job is cancelled by the user.

Copy

```
{
  "success": false,
  "type": "agent.cancelled",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "creditsUsed": 3\
    }\
  ],
  "metadata": {}
}
```

## [​](https://docs.firecrawl.dev/webhooks/events\#event-filtering)  Event Filtering

By default, you receive all events. To subscribe to specific events only, use the `events` array in your webhook config:

Copy

```
{
  "url": "https://your-app.com/webhook",
  "events": ["completed", "failed"]
}
```

This is useful if you only care about job completion and don’t need per-page updates.

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/webhooks/events.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/webhooks/events)

[Overview\\
\\
Previous](https://docs.firecrawl.dev/webhooks/overview) [Security\\
\\
Next](https://docs.firecrawl.dev/webhooks/security)

Ctrl+I