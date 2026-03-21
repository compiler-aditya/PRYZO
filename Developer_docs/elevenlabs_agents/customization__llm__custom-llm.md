<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm -->

Custom LLM allows you to connect your conversations to your own LLM via an external endpoint.
ElevenLabs also supports [natively integrated LLMs](https://elevenlabs.io/docs/agents-platform/customization/llm)

**Custom LLMs** let you bring your own OpenAI API key or run an entirely custom LLM server.

## Overview

By default, we use our own internal credentials for popular models like OpenAI. To use a custom LLM server, it must align with one of the following OpenAI-compatible request/response structures:

- [Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create) (`/v1/chat/completions`)
- [Responses API](https://platform.openai.com/docs/api-reference/responses/create) (`/v1/responses`)

The Responses API is OpenAI’s newer API format that supports additional features. Both API formats
are fully supported for custom LLM integration.

The following guides cover both use cases:

1. **Bring your own OpenAI key**: Use your own OpenAI API key with our platform.
2. **Custom LLM server**: Host and connect your own LLM server implementation.

You’ll learn how to:

- Store your OpenAI API key in ElevenLabs
- Host a server that replicates OpenAI’s [Chat Completions](https://platform.openai.com/docs/api-reference/chat/create) or [Responses](https://platform.openai.com/docs/api-reference/responses/create) endpoint
- Direct ElevenLabs to your custom endpoint
- Pass extra parameters to your LLM as needed

## Using your own OpenAI key

To integrate a custom OpenAI key, create a secret containing your OPENAI\_API\_KEY:

[1](https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm#step)

Navigate to the “Secrets” page and select “Add Secret”

![Add Secret](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/4b886cb2e6c49585bf0512aef1a4611041984e6760f794a1938c0db623ffc0f9/assets/images/conversational-ai/byollm-1.png)

[2](https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm#step-1)

Choose “Custom LLM” from the dropdown menu.

![Choose custom llm](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/45ec75f558a5c8e5070bd3170d96cbc54ef63e15d9f04ac472a45854a22a17ac/assets/images/conversational-ai/byollm-2.png)

[3](https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm#step-2)

Enter the URL, your model, and the secret you created.

![Enter url](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/1f519bdd2dff09797d00c893f4c40cfb525809a751b7c5381121b019a587c42e/assets/images/conversational-ai/byollm-3.png)

[4](https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm#step-3)

Set “Custom LLM extra body” to true.

![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/55beb285e9c446ef2e2a137c9260eda55c55c0ef6c8bee0198f82c0931e3642f/assets/images/conversational-ai/byollm-4.png)

## Custom LLM Server

To bring a custom LLM server, set up a compatible server endpoint using OpenAI’s style. You can implement either the Chat Completions API (`/v1/chat/completions`) or the Responses API (`/v1/responses`).

Both endpoints must return responses in SSE (Server-Sent Events) format with `Content-Type: text/event-stream`.

###### Chat Completions API

###### Responses API

The Chat Completions API uses the `/v1/chat/completions` endpoint.

Each chunk must be formatted as `data: {json}\n\n` and the stream must end with `data: [DONE]\n\n`.

Here’s an example server implementation:

```
import json
import os
import fastapi
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
import uvicorn
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

app = fastapi.FastAPI()
oai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    model: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    user_id: Optional[str] = None

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest) -> StreamingResponse:
    oai_request = request.dict(exclude_none=True)
    if "user_id" in oai_request:
        oai_request["user"] = oai_request.pop("user_id")

    chat_completion_coroutine = await oai_client.chat.completions.create(**oai_request)

    async def event_stream():
        try:
            async for chunk in chat_completion_coroutine:
                # Convert the ChatCompletionChunk to a dictionary before JSON serialization
                chunk_dict = chunk.model_dump()
                yield f"data: {json.dumps(chunk_dict)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            yield f"data: {json.dumps({'error': 'Internal error occurred!'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8013)
```

Run this code or your own server code.

![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/8032697eeac9a62bb084feb13ab05294df2fee44f14a97897f0b7c10ffee813c/assets/images/conversational-ai/byollm-5.png)

### Setting Up a Public URL for Your Server

To make your server accessible, create a public URL using a tunneling tool like ngrok:

```
ngrok http --url=<Your url>.ngrok.app 8013
```

![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/16d139cc2889d46e026c8aa7578fcdcd8d228dbe0f4df245091ea6de2ceb345a/assets/images/conversational-ai/byollm-6.png)

### Configuring Elevenlabs CustomLLM

Now let’s make the changes in Elevenlabs

![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/b2fbcd2f14c477820bb0c8b4a75823041cdab84fa1a6c1abad61ba59fc9b123e/assets/images/conversational-ai/byollm-8.png)

![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/281a99a47b35c59fd264ae7515f2cbc312577ed4079726947ede8ca218fd8f0d/assets/images/conversational-ai/byollm-7.png)

Direct your server URL to ngrok endpoint, setup “Limit token usage” to 5000 and set “Custom LLM extra body” to true.

You can start interacting with ElevenAgents with your own LLM server

## Optimizing for slow processing LLMs

If your custom LLM has slow processing times (perhaps due to agentic reasoning or pre-processing requirements) you can improve the conversational flow by implementing **buffer words** in your streaming responses. This technique helps maintain natural speech prosody while your LLM generates the complete response.

### Buffer words

When your LLM needs more time to process the full response, return an initial response ending with `"... "` (ellipsis followed by a space). This allows the Text to Speech system to maintain natural flow while keeping the conversation feeling dynamic.
This creates natural pauses that flow well into subsequent content that the LLM can reason longer about. The extra space is crucial to ensure that the subsequent content is not appended to the ”…” which can lead to audio distortions.

### Implementation

Here’s how to modify your custom LLM server to implement buffer words:

server.pyserver.ts

```
@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest) -> StreamingResponse:
    oai_request = request.dict(exclude_none=True)
    if "user_id" in oai_request:
        oai_request["user"] = oai_request.pop("user_id")

    async def event_stream():
        try:
            # Send initial buffer chunk while processing
            initial_chunk = {
                "id": "chatcmpl-buffer",
                "object": "chat.completion.chunk",
                "created": 1234567890,
                "model": request.model,
                "choices": [{\
                    "delta": {"content": "Let me think about that... "},\
                    "index": 0,\
                    "finish_reason": None\
                }]
            }
            yield f"data: {json.dumps(initial_chunk)}\n\n"

            # Process the actual LLM response
            chat_completion_coroutine = await oai_client.chat.completions.create(**oai_request)

            async for chunk in chat_completion_coroutine:
                chunk_dict = chunk.model_dump()
                yield f"data: {json.dumps(chunk_dict)}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            yield f"data: {json.dumps({'error': 'Internal error occurred!'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

## System tools integration

Your custom LLM can trigger [system tools](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools) to control conversation flow and state. These tools are automatically included in the `tools` parameter of your chat completion requests when configured in your agent.

### How system tools work

1. **LLM Decision**: Your custom LLM decides when to call these tools based on conversation context
2. **Tool Response**: The LLM responds with function calls in standard OpenAI format
3. **Backend Processing**: ElevenLabs processes the tool calls and updates conversation state

For more information on system tools, please see [our guide](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools)

### Available system tools

###### End call

**Purpose**: Automatically terminate conversations when appropriate conditions are met.

**Trigger conditions**: The LLM should call this tool when:

- The main task has been completed and user is satisfied
- The conversation reached natural conclusion with mutual agreement
- The user explicitly indicates they want to end the conversation

**Parameters**:

- `reason` (string, required): The reason for ending the call
- `message` (string, optional): A farewell message to send to the user before ending the call

**Function call format**:

```
{
  "type": "function",
  "function": {
    "name": "end_call",
    "arguments": "{\"reason\": \"Task completed successfully\", \"message\": \"Thank you for using our service. Have a great day!\"}"
  }
}
```

**Implementation**: Configure as a system tool in your agent settings. The LLM will receive detailed instructions about when to call this function.

Learn more: [End call tool](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/end-call)

###### Language detection

**Purpose**: Automatically switch to the user’s detected language during conversations.

**Trigger conditions**: The LLM should call this tool when:

- User speaks in a different language than the current conversation language
- User explicitly requests to switch languages
- Multi-language support is needed for the conversation

**Parameters**:

- `reason` (string, required): The reason for the language switch
- `language` (string, required): The language code to switch to (must be in supported languages list)

**Function call format**:

```
{
  "type": "function",
  "function": {
    "name": "language_detection",
    "arguments": "{\"reason\": \"User requested Spanish\", \"language\": \"es\"}"
  }
}
```

**Implementation**: Configure supported languages in agent settings and add the language detection system tool. The agent will automatically switch voice and responses to match detected languages.

Learn more: [Language detection tool](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/language-detection)

###### Agent transfer

**Purpose**: Transfer conversations between specialized AI agents based on user needs.

**Trigger conditions**: The LLM should call this tool when:

- User request requires specialized knowledge or different agent capabilities
- Current agent cannot adequately handle the query
- Conversation flow indicates need for different agent type

**Parameters**:

- `reason` (string, optional): The reason for the agent transfer
- `agent_number` (integer, required): Zero-indexed number of the agent to transfer to (based on configured transfer rules)

**Function call format**:

```
{
  "type": "function",
  "function": {
    "name": "transfer_to_agent",
    "arguments": "{\"reason\": \"User needs billing support\", \"agent_number\": 0}"
  }
}
```

**Implementation**: Define transfer rules mapping conditions to specific agent IDs. Configure which agents the current agent can transfer to. Agents are referenced by zero-indexed numbers in the transfer configuration.

Learn more: [Agent transfer tool](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/agent-transfer)

###### Transfer to human

**Purpose**: Seamlessly hand off conversations to human operators when AI assistance is insufficient.

**Trigger conditions**: The LLM should call this tool when:

- Complex issues requiring human judgment
- User explicitly requests human assistance
- AI reaches limits of capability for the specific request
- Escalation protocols are triggered

**Parameters**:

- `reason` (string, optional): The reason for the transfer
- `transfer_number` (string, required): The phone number to transfer to (must match configured numbers)
- `client_message` (string, required): Message read to the client while waiting for transfer
- `agent_message` (string, required): Message for the human operator receiving the call

**Function call format**:

```
{
  "type": "function",
  "function": {
    "name": "transfer_to_number",
    "arguments": "{\"reason\": \"Complex billing issue\", \"transfer_number\": \"+15551234567\", \"client_message\": \"I'm transferring you to a billing specialist who can help with your account.\", \"agent_message\": \"Customer has a complex billing dispute about order #12345 from last month.\"}"
  }
}
```

**Implementation**: Configure transfer phone numbers and conditions. Define messages for both customer and receiving human operator. Works with both Twilio and SIP trunking.

Learn more: [Transfer to human tool](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/transfer-to-human)

###### Skip turn

**Purpose**: Allow the agent to pause and wait for user input without speaking.

**Trigger conditions**: The LLM should call this tool when:

- User indicates they need a moment (“Give me a second”, “Let me think”)
- User requests pause in conversation flow
- Agent detects user needs time to process information

**Parameters**:

- `reason` (string, optional): Free-form reason explaining why the pause is needed

**Function call format**:

```
{
  "type": "function",
  "function": {
    "name": "skip_turn",
    "arguments": "{\"reason\": \"User requested time to think\"}"
  }
}
```

**Implementation**: No additional configuration needed. The tool simply signals the agent to remain silent until the user speaks again.

Learn more: [Skip turn tool](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/skip-turn)

###### Voicemail detection

**Parameters**:

- `reason` (string, required): The reason for detecting voicemail (e.g., “automated greeting detected”, “no human response”)

**Function call format**:

```
{
  "type": "function",
  "function": {
    "name": "voicemail_detection",
    "arguments": "{\"reason\": \"Automated greeting detected with request to leave message\"}"
  }
}
```

Learn more: [Voicemail detection tool](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/voicemail-detection)

### Example Request with System Tools

When system tools are configured, your custom LLM will receive requests that include the tools in the standard OpenAI format:

```
{
  "messages": [\
    {\
      "role": "system",\
      "content": "You are a helpful assistant. You have access to system tools for managing conversations."\
    },\
    {\
      "role": "user",\
      "content": "I think we're done here, thanks for your help!"\
    }\
  ],
  "model": "your-custom-model",
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": true,
  "tools": [\
    {\
      "type": "function",\
      "function": {\
        "name": "end_call",\
        "description": "Call this function to end the current conversation when the main task has been completed...",\
        "parameters": {\
          "type": "object",\
          "properties": {\
            "reason": {\
              "type": "string",\
              "description": "The reason for the tool call."\
            },\
            "message": {\
              "type": "string",\
              "description": "A farewell message to send to the user along right before ending the call."\
            }\
          },\
          "required": ["reason"]\
        }\
      }\
    },\
    {\
      "type": "function",\
      "function": {\
        "name": "language_detection",\
        "description": "Change the conversation language when the user expresses a language preference explicitly...",\
        "parameters": {\
          "type": "object",\
          "properties": {\
            "reason": {\
              "type": "string",\
              "description": "The reason for the tool call."\
            },\
            "language": {\
              "type": "string",\
              "description": "The language to switch to. Must be one of language codes in tool description."\
            }\
          },\
          "required": ["reason", "language"]\
        }\
      }\
    },\
    {\
      "type": "function",\
      "function": {\
        "name": "skip_turn",\
        "description": "Skip a turn when the user explicitly indicates they need a moment to think...",\
        "parameters": {\
          "type": "object",\
          "properties": {\
            "reason": {\
              "type": "string",\
              "description": "Optional free-form reason explaining why the pause is needed."\
            }\
          },\
          "required": []\
        }\
      }\
    }\
  ]
}
```

Your custom LLM must support function calling to use system tools. Ensure your model can generate
proper function call responses in OpenAI format.

# Additional Features

###### Custom LLM Parameters

You may pass additional parameters to your custom LLM implementation.

###### Python

[1](https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm#define-the-extra-parameters)

### Define the Extra Parameters

Create an object containing your custom parameters:

```
from elevenlabs.conversational_ai.conversation import Conversation, ConversationConfig

extra_body_for_convai = {
    "UUID": "123e4567-e89b-12d3-a456-426614174000",
    "parameter-1": "value-1",
    "parameter-2": "value-2",
}

config = ConversationConfig(
    extra_body=extra_body_for_convai,
)
```

[2](https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm#update-the-llm-implementation)

### Update the LLM Implementation

Modify your custom LLM code to handle the additional parameters:

```
import json
import os
import fastapi
from fastapi.responses import StreamingResponse
from fastapi import Request
from openai import AsyncOpenAI
import uvicorn
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

app = fastapi.FastAPI()
oai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    model: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    user_id: Optional[str] = None
    elevenlabs_extra_body: Optional[dict] = None

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest) -> StreamingResponse:
    oai_request = request.dict(exclude_none=True)
    print(oai_request)
    if "user_id" in oai_request:
        oai_request["user"] = oai_request.pop("user_id")

    if "elevenlabs_extra_body" in oai_request:
        oai_request.pop("elevenlabs_extra_body")

    chat_completion_coroutine = await oai_client.chat.completions.create(**oai_request)

    async def event_stream():
        try:
            async for chunk in chat_completion_coroutine:
                chunk_dict = chunk.model_dump()
                yield f"data: {json.dumps(chunk_dict)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            yield f"data: {json.dumps({'error': 'Internal error occurred!'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8013)
```

### Example Request

With this custom message setup, your LLM will receive requests in this format:

```
{
  "messages": [\
    {\
      "role": "system",\
      "content": "\n  <Redacted>"\
    },\
    {\
      "role": "assistant",\
      "content": "Hey I'm currently unavailable."\
    },\
    {\
      "role": "user",\
      "content": "Hey, who are you?"\
    }\
  ],
  "model": "gpt-4o",
  "temperature": 0.5,
  "max_tokens": 5000,
  "stream": true,
  "elevenlabs_extra_body": {
    "UUID": "123e4567-e89b-12d3-a456-426614174000",
    "parameter-1": "value-1",
    "parameter-2": "value-2"
  }
}
```
