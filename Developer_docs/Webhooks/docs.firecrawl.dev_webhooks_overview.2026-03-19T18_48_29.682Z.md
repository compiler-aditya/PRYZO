Webhooks let you receive real-time notifications as your operations progress, instead of polling for status.

## [​](https://docs.firecrawl.dev/webhooks/overview\#supported-operations)  Supported Operations

| Operation | Events |
| --- | --- |
| Crawl | `started`, `page`, `completed` |
| Batch Scrape | `started`, `page`, `completed` |
| Extract | `started`, `completed`, `failed` |
| Agent | `started`, `action`, `completed`, `failed`, `cancelled` |

## [​](https://docs.firecrawl.dev/webhooks/overview\#configuration)  Configuration

Add a `webhook` object to your request:

JSON

Copy

```
{
  "webhook": {
    "url": "https://your-domain.com/webhook",
    "metadata": {
      "any_key": "any_value"
    },
    "events": ["started", "page", "completed", "failed"]
  }
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | string | Yes | Your endpoint URL (HTTPS) |
| `headers` | object | No | Custom headers to include |
| `metadata` | object | No | Custom data included in payloads |
| `events` | array | No | Event types to receive (default: all) |

## [​](https://docs.firecrawl.dev/webhooks/overview\#usage)  Usage

### [​](https://docs.firecrawl.dev/webhooks/overview\#crawl-with-webhook)  Crawl with Webhook

cURL

Copy

```
curl -X POST https://api.firecrawl.dev/v2/crawl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev",
      "limit": 100,
      "webhook": {
        "url": "https://your-domain.com/webhook",
        "metadata": {
          "any_key": "any_value"
        },
        "events": ["started", "page", "completed"]
      }
    }'
```

### [​](https://docs.firecrawl.dev/webhooks/overview\#batch-scrape-with-webhook)  Batch Scrape with Webhook

cURL

Copy

```
curl -X POST https://api.firecrawl.dev/v2/batch/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "urls": [\
        "https://example.com/page1",\
        "https://example.com/page2",\
        "https://example.com/page3"\
      ],
      "webhook": {
        "url": "https://your-domain.com/webhook",
        "metadata": {
          "any_key": "any_value"
        },
        "events": ["started", "page", "completed"]
      }
    }'
```

## [​](https://docs.firecrawl.dev/webhooks/overview\#timeouts-&-retries)  Timeouts & Retries

Your endpoint must respond with a `2xx` status within **10 seconds**.If delivery fails (timeout, non-2xx, or network error), Firecrawl retries automatically:

| Retry | Delay after failure |
| --- | --- |
| 1st | 1 minute |
| 2nd | 5 minutes |
| 3rd | 15 minutes |

After 3 failed retries, the webhook is marked as failed and no further attempts are made.

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/webhooks/overview.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/webhooks/overview)

[Firecrawl + Dify\\
\\
Previous](https://docs.firecrawl.dev/developer-guides/workflow-automation/dify) [Event Types\\
\\
Next](https://docs.firecrawl.dev/webhooks/events)

⌘I