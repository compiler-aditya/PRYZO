## [​](https://docs.firecrawl.dev/webhooks/testing\#local-development)  Local Development

Since webhooks need to reach your server from the internet, you’ll need to expose your local development server publicly.

### [​](https://docs.firecrawl.dev/webhooks/testing\#using-cloudflare-tunnels)  Using Cloudflare Tunnels

[Cloudflare Tunnels](https://github.com/cloudflare/cloudflared/releases) provide a free way to expose your local server without opening firewall ports:

Copy

```
cloudflared tunnel --url localhost:3000
```

You’ll get a public URL like `https://abc123.trycloudflare.com`. Use this in your webhook config:

Copy

```
{
  "url": "https://abc123.trycloudflare.com/webhook"
}
```

## [​](https://docs.firecrawl.dev/webhooks/testing\#troubleshooting)  Troubleshooting

### [​](https://docs.firecrawl.dev/webhooks/testing\#webhooks-not-arriving)  Webhooks Not Arriving

- **Endpoint not accessible** \- Verify your server is publicly reachable and firewalls allow incoming connections
- **Using HTTP** \- Webhook URLs must use HTTPS
- **Wrong events** \- Check the `events` filter in your webhook config

### [​](https://docs.firecrawl.dev/webhooks/testing\#signature-verification-failing)  Signature Verification Failing

The most common cause is using the parsed JSON body instead of the raw request body.

Copy

```
// Wrong - using parsed body
const signature = crypto
  .createHmac('sha256', secret)
  .update(JSON.stringify(req.body))
  .digest('hex');

// Correct - using raw body
app.use('/webhook', express.raw({ type: 'application/json' }));
app.post('/webhook', (req, res) => {
  const signature = crypto
    .createHmac('sha256', secret)
    .update(req.body) // Raw buffer
    .digest('hex');
});
```

### [​](https://docs.firecrawl.dev/webhooks/testing\#other-issues)  Other Issues

- **Wrong secret** \- Verify you’re using the correct secret from your [account settings](https://www.firecrawl.dev/app/settings?tab=advanced)
- **Timeout errors** \- Ensure your endpoint responds within 10 seconds

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/webhooks/testing.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/webhooks/testing)

[Security\\
\\
Previous](https://docs.firecrawl.dev/webhooks/security) [Use Cases\\
\\
Next](https://docs.firecrawl.dev/use-cases/overview)

⌘I