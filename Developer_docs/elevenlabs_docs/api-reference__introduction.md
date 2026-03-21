<!-- Source: https://elevenlabs.io/docs/api-reference/introduction -->

## Installation

You can interact with the API through HTTP or Websocket requests from any language, via our official Python bindings or our official Node.js libraries.

To install the official Python bindings, run the following command:

```
pip install elevenlabs
```

To install the official Node.js library, run the following command in your Node.js project directory:

```
npm install @elevenlabs/elevenlabs-js
```

## Tracking generation costs

Access response headers to retrieve generation metadata including character costs.

PythonJavaScript

```
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="your_api_key")

# Get raw response with headers
response = client.text_to_speech.with_raw_response.convert(
    text="Hello, world!",
    voice_id="voice_id"
)

# Access character cost from headers
char_cost = response.headers.get("x-character-count")
request_id = response.headers.get("request-id")
audio_data = response.data
```

The raw response provides access to:

- Response data - The actual API response content
- HTTP headers - Metadata including character costs and request IDs
