<!-- Source: https://elevenlabs.io/docs/eleven-api/resources/webhooks -->

## Overview

Certain events within ElevenLabs can be configured to trigger webhooks, allowing external applications and systems to receive and process these events as they occur. Currently supported event types include:

| Event type | Description |
| --- | --- |
| `post_call_transcription` | A Agents Platform call has finished and analysis is complete |
| `voice_removal_notice` | A shared voice is scheduled to be removed |
| `voice_removal_notice_withdrawn` | A shared voice is no longer scheduled for removal |
| `voice_removed` | A shared voice has been removed and is no longer useable |

## Configuration

Webhooks can be created, disabled and deleted from the general settings page. For users within [Workspaces](https://elevenlabs.io/docs/overview/administration/workspaces/overview), only the workspace admins can configure the webhooks for the workspace.

![HMAC webhook configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/9ea298daac1c64eb43c802a12f7824e83accca44ba2edd1d01a39bcd62c0b9d6/assets/images/product-guides/administration/hmacwebhook.png)

After creation, the webhook can be selected to listen for events within product settings such as [Agents Platform](https://elevenlabs.io/docs/agents-platform/workflows/post-call-webhooks).

Webhooks can be disabled from the general settings page at any time. Webhooks that repeatedly fail are auto disabled if there are 10 or more consecutive failures and the last successful delivery was more than 7 days ago or has never been successfully delivered. Auto-disabled webhooks require re-enabling from the settings page. Webhooks can be deleted if not in use by any products.

## Integration

To integrate with webhooks, the listener should create an endpoint handler to receive the webhook event data POST requests. After validating the signature, the handler should quickly return HTTP 200 to indicate successful receipt of the webhook event, repeat failure to correctly return may result in the webhook becoming automatically disabled.
Each webhook event is dispatched only once, refer to the [API](https://elevenlabs.io/docs/api-reference/introduction) for methods to poll and get product specific data.

### Top-level fields

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Type of event |
| `data` | object | Data for the event |
| `event_timestamp` | string | When this event occurred |

## Example webhook payload

```
{
  "type": "post_call_transcription",
  "event_timestamp": 1739537297,
  "data": {
    "agent_id": "xyz",
    "conversation_id": "abc",
    "status": "done",
    "transcript": [\
      {\
        "role": "agent",\
        "message": "Hey there angelo. How are you?",\
        "tool_calls": null,\
        "tool_results": null,\
        "feedback": null,\
        "time_in_call_secs": 0,\
        "conversation_turn_metrics": null\
      },\
      {\
        "role": "user",\
        "message": "Hey, can you tell me, like, a fun fact about 11 Labs?",\
        "tool_calls": null,\
        "tool_results": null,\
        "feedback": null,\
        "time_in_call_secs": 2,\
        "conversation_turn_metrics": null\
      },\
      {\
        "role": "agent",\
        "message": "I do not have access to fun facts about Eleven Labs. However, I can share some general information about the company. Eleven Labs is an AI voice technology platform that specializes in voice cloning and text-to-speech...",\
        "tool_calls": null,\
        "tool_results": null,\
        "feedback": null,\
        "time_in_call_secs": 9,\
        "conversation_turn_metrics": {\
          "convai_llm_service_ttfb": {\
            "elapsed_time": 0.3704247010173276\
          },\
          "convai_llm_service_ttf_sentence": {\
            "elapsed_time": 0.5551181449554861\
          }\
        }\
      }\
    ],
    "metadata": {
      "start_time_unix_secs": 1739537297,
      "call_duration_secs": 22,
      "cost": 296,
      "deletion_settings": {
        "deletion_time_unix_secs": 1802609320,
        "deleted_logs_at_time_unix_secs": null,
        "deleted_audio_at_time_unix_secs": null,
        "deleted_transcript_at_time_unix_secs": null,
        "delete_transcript_and_pii": true,
        "delete_audio": true
      },
      "feedback": {
        "overall_score": null,
        "likes": 0,
        "dislikes": 0
      },
      "authorization_method": "authorization_header",
      "charging": {
        "dev_discount": true
      },
      "termination_reason": ""
    },
    "analysis": {
      "evaluation_criteria_results": {},
      "data_collection_results": {},
      "call_successful": "success",
      "transcript_summary": "The conversation begins with the agent asking how Angelo is, but Angelo redirects the conversation by requesting a fun fact about 11 Labs. The agent acknowledges they don't have specific fun facts about Eleven Labs but offers to provide general information about the company. They briefly describe Eleven Labs as an AI voice technology platform specializing in voice cloning and text-to-speech technology. The conversation is brief and informational, with the agent adapting to the user's request despite not having the exact information asked for."
    },
    "conversation_initiation_client_data": {
      "conversation_config_override": {
        "agent": {
          "prompt": null,
          "first_message": null,
          "language": "en"
        },
        "tts": {
          "voice_id": null
        }
      },
      "custom_llm_extra_body": {},
      "dynamic_variables": {
        "user_name": "angelo"
      }
    }
  }
}
```

## Authentication

It is important for the listener to validate all incoming webhooks. Webhooks currently support authentication via HMAC signatures. Set up HMAC authentication by:

- Securely storing the shared secret generated upon creation of the webhook
- Verifying the ElevenLabs-Signature header in your endpoint using the SDK

The ElevenLabs SDK provides a `constructEvent` method that handles signature verification, timestamp validation, and payload parsing.

###### Python

###### JavaScript

Example webhook handler using FastAPI:

```
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from elevenlabs.client import ElevenLabs
import os

load_dotenv()

app = FastAPI()
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

@app.post("/webhook")
async def receive_message(request: Request):
    payload = await request.body()
    signature = request.headers.get("elevenlabs-signature")

    try:
        event = elevenlabs.webhooks.construct_event(
            payload=payload.decode("utf-8"),
            signature=signature,
            secret=WEBHOOK_SECRET,
        )
    except Exception as e:
        return JSONResponse(content={"error": "Invalid signature"}, status_code=401)

    # Process the webhook event
    if event.type == "post_call_transcription":
        print(f"Received transcription: {event.data}")

    return {"status": "received"}
```
