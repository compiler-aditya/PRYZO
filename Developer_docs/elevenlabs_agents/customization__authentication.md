<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/authentication -->

Secure Your Agents: Allowlists & Signed URL Authentication - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Secure Your Agents: Allowlists & Signed URL Authentication](https://www.youtube.com/watch?v=8hZ4IWL7iqw)

ElevenLabs

Search

Watch later

Share

Copy link

Info

Shopping

Tap to unmute

If playback doesn't begin shortly, try restarting your device.

Full screen is unavailable. [Learn More](https://support.google.com/youtube/answer/6276924)

More videos

## More videos

You're signed out

Videos you watch may be added to the TV's watch history and influence TV recommendations. To avoid this, cancel and sign in to YouTube on your computer.

CancelConfirm

Share

Include playlist

An error occurred while retrieving sharing information. Please try again later.

[Watch on](https://www.youtube.com/watch?v=8hZ4IWL7iqw&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 8:47

•Live

•

## Overview

When building conversational agents, you may need to restrict access to certain agents or conversations. ElevenLabs provides multiple authentication mechanisms to ensure only authorized users can interact with your agents.

## Authentication methods

ElevenLabs offers two primary methods to secure your conversational agents:

[Signed URLs\\
\\
Generate temporary authenticated URLs for secure client-side connections without exposing API\\
keys.](https://elevenlabs.io/docs/eleven-agents/customization/authentication#using-signed-urls) [Allowlists\\
\\
Restrict access to specific domains or hostnames that can connect to your agent.](https://elevenlabs.io/docs/eleven-agents/customization/authentication#using-allowlists)

## Using signed URLs

Signed URLs are the recommended approach for client-side applications. This method allows you to authenticate users without exposing your API key.

The guides below uses the [JS client](https://www.npmjs.com/package/@elevenlabs/client) and
[Python SDK](https://github.com/elevenlabs/elevenlabs-python/).

### How signed URLs work

1. Your server requests a signed URL from ElevenLabs using your API key.
2. ElevenLabs generates a temporary token and returns a signed WebSocket URL.
3. Your client application uses this signed URL to establish a WebSocket connection.
4. The signed URL expires after 15 minutes.

Never expose your ElevenLabs API key client-side.

### Generate a signed URL via the API

To obtain a signed URL, make a request to the `get_signed_url` [endpoint](https://elevenlabs.io/docs/agents-platform/api-reference/conversations/get-signed-url) with your agent ID:

PythonJavaScriptBash

```
# Server-side code using the Python SDK
from elevenlabs.client import ElevenLabs
async def get_signed_url():
    try:
        elevenlabs = ElevenLabs(api_key="your-api-key")
        response = await elevenlabs.conversational_ai.conversations.get_signed_url(agent_id="your-agent-id")
        return response.signed_url
    except Exception as error:
        print(f"Error getting signed URL: {error}")
        raise
```

The curl response has the following format:

```
{
  "signed_url": "wss://api.elevenlabs.io/v1/convai/conversation?agent_id=your-agent-id&conversation_signature=your-token"
}
```

### Connecting to your agent using a signed URL

Retrieve the server generated signed URL from the client and use the signed URL to connect to the websocket.

PythonJavaScript

```
# Client-side code using the Python SDK
from elevenlabs.conversational_ai.conversation import (
    Conversation,
    AudioInterface,
    ClientTools,
    ConversationInitiationData
)
import os
from elevenlabs.client import ElevenLabs
api_key = os.getenv("ELEVENLABS_API_KEY")

elevenlabs = ElevenLabs(api_key=api_key)

conversation = Conversation(
  client=elevenlabs,
  agent_id=os.getenv("AGENT_ID"),
  requires_auth=True,
  audio_interface=AudioInterface(),
  config=ConversationInitiationData()
)

async def start_conversation():
  try:
    signed_url = await get_signed_url()
    conversation = Conversation(
      client=elevenlabs,
      url=signed_url,
    )

    conversation.start_session()
  except Exception as error:
    print(f"Failed to start conversation: {error}")
```

### Signed URL expiration

Signed URLs are valid for 15 minutes. The conversation session can last longer, but the conversation must be initiated within the 15 minute window.

## Using allowlists

Allowlists provide a way to restrict access to your conversational agents based on the origin domain. This ensures that only requests from approved domains can connect to your agent.

### How allowlists work

1. You configure a list of approved hostnames for your agent.
2. When a client attempts to connect, ElevenLabs checks if the request’s origin matches an allowed hostname.
3. If the origin is on the allowlist, the connection is permitted; otherwise, it’s rejected.

### Configuring allowlists

Allowlists are configured as part of your agent’s authentication settings. You can specify up to 10 unique hostnames that are allowed to connect to your agent.

### Example: setting up an allowlist

PythonJavaScript

```
from elevenlabs.client import ElevenLabs
import os
from elevenlabs.types import *

api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key=api_key)

agent = elevenlabs.conversational_ai.agents.create(
  conversation_config=ConversationalConfig(
    agent=AgentConfig(
      first_message="Hi. I'm an authenticated agent.",
    )
  ),
  platform_settings=AgentPlatformSettingsRequestModel(
  auth=AuthSettings(
    enable_auth=False,
    allowlist=[\
      AllowlistItem(hostname="example.com"),\
      AllowlistItem(hostname="app.example.com"),\
      AllowlistItem(hostname="localhost:3000")\
      ]
    )
  )
)
```

## Choosing an authentication method

Configure one authentication method per agent:

1. Use signed URLs (`enable_auth`) for authenticated client sessions.
2. Use allowlists (`allowlist`) for hostname-based access control.

Do not configure signed URLs and allowlists together on the same agent. Choose the method that
matches your deployment model.

### Example: signed URLs only

Use `enable_auth` without an `allowlist`:

PythonJavaScript

```
from elevenlabs.client import ElevenLabs
import os
from elevenlabs.types import *

api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key=api_key)

agent = elevenlabs.conversational_ai.agents.create(
  conversation_config=ConversationalConfig(
    agent=AgentConfig(
      first_message="Hi. I require a signed URL.",
    )
  ),
  platform_settings=AgentPlatformSettingsRequestModel(
    auth=AuthSettings(
      enable_auth=True
    )
  )
)
```

### Example: allowlist only

Use `allowlist` without enabling signed URLs:

PythonJavaScript

```
from elevenlabs.client import ElevenLabs
import os
from elevenlabs.types import *

api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs = ElevenLabs(api_key=api_key)

agent = elevenlabs.conversational_ai.agents.create(
  conversation_config=ConversationalConfig(
    agent=AgentConfig(
      first_message="Hi. I only accept approved hostnames.",
    )
  ),
  platform_settings=AgentPlatformSettingsRequestModel(
    auth=AuthSettings(
      allowlist=[\
        AllowlistItem(hostname="example.com"),\
        AllowlistItem(hostname="app.example.com"),\
      ]
    )
  )
)
```

## FAQ

###### Can I use the same signed URL for multiple users?

This is possible but we recommend generating a new signed URL for each user session.

###### What happens if the signed URL expires during a conversation?

If the signed URL expires (after 15 minutes), any WebSocket connection created with that signed
url will **not** be closed, but trying to create a new connection with that signed URL will
fail.

###### Can I restrict access to specific users?

The signed URL mechanism only verifies that the request came from an authorized source. To
restrict access to specific users, implement user authentication in your application before
requesting the signed URL.

###### Is there a limit to how many signed URLs I can generate?

There is no specific limit on the number of signed URLs you can generate.

###### How do allowlists handle subdomains?

Allowlists perform exact matching on hostnames. If you want to allow both a domain and its
subdomains, you need to add each one separately (e.g., “example.com” and “app.example.com”).

###### Do I need to use both authentication methods?

No. Configure either signed URLs or an allowlist for each agent. For client-side
applications, signed URLs are the recommended default.

###### What other security measures should I implement?

Beyond signed URLs and allowlists, consider implementing:

- User authentication before requesting signed URLs
- Rate limiting on API requests
- Usage monitoring for suspicious patterns
- Proper error handling for auth failures
