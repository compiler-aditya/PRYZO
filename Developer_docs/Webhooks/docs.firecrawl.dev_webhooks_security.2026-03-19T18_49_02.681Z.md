Firecrawl signs every webhook request using HMAC-SHA256. Verifying signatures ensures requests are authentic and haven’t been tampered with.

## [​](https://docs.firecrawl.dev/webhooks/security\#secret-key)  Secret Key

Your webhook secret is available in the [Advanced tab](https://www.firecrawl.dev/app/settings?tab=advanced) of your account settings. Each account has a unique secret used to sign all webhook requests.

Keep your webhook secret secure and never expose it publicly. If you believe your secret has been compromised, regenerate it immediately from your account settings.

## [​](https://docs.firecrawl.dev/webhooks/security\#signature-verification)  Signature Verification

Each webhook request includes an `X-Firecrawl-Signature` header:

Copy

```
X-Firecrawl-Signature: sha256=abc123def456...
```

### [​](https://docs.firecrawl.dev/webhooks/security\#how-to-verify)  How to Verify

1. Extract the signature from the `X-Firecrawl-Signature` header
2. Get the raw request body (before parsing)
3. Compute HMAC-SHA256 using your secret key
4. Compare signatures using a timing-safe function

### [​](https://docs.firecrawl.dev/webhooks/security\#implementation)  Implementation

Node/Express

Python/Flask

Copy

```
import crypto from 'crypto';
import express from 'express';

const app = express();

// Use raw body parser for signature verification
app.use('/webhook/firecrawl', express.raw({ type: 'application/json' }));

app.post('/webhook/firecrawl', (req, res) => {
  const signature = req.get('X-Firecrawl-Signature');
  const webhookSecret = process.env.FIRECRAWL_WEBHOOK_SECRET;

  if (!signature || !webhookSecret) {
    return res.status(401).send('Unauthorized');
  }

  // Extract hash from signature header
  const [algorithm, hash] = signature.split('=');
  if (algorithm !== 'sha256') {
    return res.status(401).send('Invalid signature algorithm');
  }

  // Compute expected signature
  const expectedSignature = crypto
    .createHmac('sha256', webhookSecret)
    .update(req.body)
    .digest('hex');

  // Verify signature using timing-safe comparison
  if (!crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(expectedSignature, 'hex'))) {
    return res.status(401).send('Invalid signature');
  }

  // Parse and process verified webhook
  const event = JSON.parse(req.body);
  console.log('Verified Firecrawl webhook:', event);

  res.status(200).send('ok');
});

app.listen(3000, () => console.log('Listening on 3000'));
```

## [​](https://docs.firecrawl.dev/webhooks/security\#best-practices)  Best Practices

### [​](https://docs.firecrawl.dev/webhooks/security\#always-verify-signatures)  Always Verify Signatures

Never process a webhook without verifying its signature first:

Copy

```
app.post('/webhook', (req, res) => {
  if (!verifySignature(req)) {
    return res.status(401).send('Unauthorized');
  }
  processWebhook(req.body);
  res.status(200).send('OK');
});
```

### [​](https://docs.firecrawl.dev/webhooks/security\#use-timing-safe-comparisons)  Use Timing-Safe Comparisons

Standard string comparison can leak timing information. Use `crypto.timingSafeEqual()` in Node.js or `hmac.compare_digest()` in Python.

### [​](https://docs.firecrawl.dev/webhooks/security\#use-https)  Use HTTPS

Always use HTTPS for your webhook endpoint to ensure payloads are encrypted in transit.

[Suggest edits](https://github.com/firecrawl/firecrawl-docs/edit/main/webhooks/security.mdx) [Raise issue](https://github.com/firecrawl/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/webhooks/security)

[Event Types\\
\\
Previous](https://docs.firecrawl.dev/webhooks/events) [Testing\\
\\
Next](https://docs.firecrawl.dev/webhooks/testing)

Ctrl+I