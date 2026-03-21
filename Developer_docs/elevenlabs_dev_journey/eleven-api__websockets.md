<!-- Source: https://elevenlabs.io/docs/eleven-api/websockets -->

WebSocket streaming is a method of sending and receiving data over a single, long-lived connection. This method is useful for real-time applications where you need to stream audio data as it becomes available.

If you want to quickly test out the latency (time to first byte) of a WebSocket connection to the ElevenLabs text-to-speech API, you can install `elevenlabs-latency` via `npm` and follow the instructions [here](https://www.npmjs.com/package/elevenlabs-latency?activeTab=readme).

WebSockets can be used with the Text to Speech and Agents Platform products. This guide will
demonstrate how to use them with the Text to Speech API. WebSockets are not available for the
`eleven_v3` model.

## Requirements

- An ElevenLabs account with an API key (here’s how to [find your API key](https://elevenlabs.io/docs/api-reference/authentication)).
- Python or Node.js (or another JavaScript runtime) installed on your machine

## Setup

Install required dependencies:

PythonTypeScript

```
pip install python-dotenv
pip install websockets
```

Next, create a `.env` file in your project directory and add your API key:

.env

```
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

## Initiate the websocket connection

After choosing a voice from the Voice Library and the text to speech model you wish to use, initiate a WebSocket connection to the text to speech API.

text-to-speech-websocket.pytext-to-speech-websocket.ts

```
import os
from dotenv import load_dotenv
import websockets

# Load the API key from the .env file
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

voice_id = 'Xb7hH8MSUJpSbSDYk0k2'

# For use cases where latency is important, we recommend using the 'eleven_flash_v2_5' model.
model_id = 'eleven_flash_v2_5'

async def text_to_speech_ws_streaming(voice_id, model_id):
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model_id}"

    async with websockets.connect(uri) as websocket:
       ...
```

## Send the input text

Once the WebSocket connection is open, set up voice settings first. Next, send the text message to the API.

text-to-speech-websocket.pytext-to-speech-websocket.ts

```
async def text_to_speech_ws_streaming(voice_id, model_id):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": False},
            "generation_config": {
                "chunk_length_schedule": [120, 160, 250, 290]
            },
            "xi_api_key": ELEVENLABS_API_KEY,
        }))

        text = "The twilight sun cast its warm golden hues upon the vast rolling fields, saturating the landscape with an ethereal glow. Silently, the meandering brook continued its ceaseless journey, whispering secrets only the trees seemed privy to."
        await websocket.send(json.dumps({"text": text}))

        # Send empty string to indicate the end of the text sequence which will close the WebSocket connection
        await websocket.send(json.dumps({"text": ""}))
```

## Save the audio to file

Read the incoming message from the WebSocket connection and write the audio chunks to a local file.

text-to-speech-websocket.pytext-to-speech-websocket.ts

```
import asyncio

async def write_to_local(audio_stream):
    """Write the audio encoded in base64 string to a local mp3 file."""

    with open(f'./output/test.mp3', "wb") as f:
        async for chunk in audio_stream:
            if chunk:
                f.write(chunk)

async def listen(websocket):
    """Listen to the websocket for audio data and stream it."""

    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("audio"):
                yield base64.b64decode(data["audio"])
            elif data.get('isFinal'):
                break

        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            break

async def text_to_speech_ws_streaming(voice_id, model_id):
    async with websockets.connect(uri) as websocket:
          ...
          # Add listen task to submit the audio chunks to the write_to_local function
          listen_task = asyncio.create_task(write_to_local(listen(websocket)))

          await listen_task

asyncio.run(text_to_speech_ws_streaming(voice_id, model_id))
```

## Run the script

You can run the script by executing the following command in your terminal. An mp3 audio file will be saved in the `output` directory.

PythonTypeScript

```
python text-to-speech-websocket.py
```

## Advanced configuration

The use of WebSockets comes with some advanced settings that you can use to fine-tune your real-time audio generation.

### Buffering

When generating real-time audio, two important concepts should be taken into account: Time To First Byte (TTFB) and Buffering. To produce high quality audio and deduce context, the model requires a certain threshold of input text. The more text that is sent in a WebSocket connection, the better the audio quality. If the threshold is not met, the model will add the text to a buffer and generate audio once the buffer is full.

In terms of latency, TTFB is the time it takes for the first byte of audio to be sent to the client. This is important because it affects the perceived latency of the audio. As such, you might want to control the buffer size to balance between quality and latency.

To manage this, you can use the `chunk_length_schedule` parameter when either initializing the WebSocket connection or when sending text. This parameter is an array of integers that represent the number of characters that will be sent to the model before generating audio. For example, if you set `chunk_length_schedule` to `[120, 160, 250, 290]`, the model will generate audio after 120, 160, 250, and 290 characters have been sent, respectively.

Here’s an example of how this works with the default settings for `chunk_length_schedule`:

![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/077efc232570b0f92355aed2d6766b66bba815e335466e81cd64f8dfcce10ada/assets/images/developer-guides/buffering-explainer.jpg)

In the above diagram, audio is only generated after the second message is sent to the server. This is because the first message is below the threshold of 120 characters, while the second message brings the total number of characters above the threshold. The third message is above the threshold of 160 characters, so audio is immediately generated and returned to the client.

You can specify a custom value for `chunk_length_schedule` when initializing the WebSocket connection or when sending text.

PythonTypeScript

```
await websocket.send(json.dumps({
    "text": text,
    "generation_config": {
        # Generate audio after 50, 120, 160, and 290 characters have been sent
        "chunk_length_schedule": [50, 120, 160, 290]
    },
    "xi_api_key": ELEVENLABS_API_KEY,
}))
```

In the case that you want force the immediate return of the audio, you can use `flush: true` to clear out the buffer and force generate any buffered text. This can be useful, for example, when you have reached the end of a document and want to generate audio for the final section.

![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/84011e01024effe1bba1556f0007c7947165a0101bce3a41f8b955d1a9788a9c/assets/images/developer-guides/buffering-flush-explainer.jpg)

This can be specified on a per-message basis by setting `flush: true` in the message.

PythonTypeScript

```
await websocket.send(json.dumps({"text": "Generate this audio immediately.", "flush": True}))
```

In addition, closing the websocket will automatically force generate any buffered text.

### Voice settings

When initializing the WebSocket connections, you can specify the voice settings for the subsequent generations. This allows you to control the speed, stability, and other voice characteristics of the generated audio.

PythonTypeScript

```
await websocket.send(json.dumps({
    "text": text,
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": False},
}))
```

This can be overridden on a per-message basis by specifying a different `voice_settings` in the message.

### Pronunciation dictionaries

You can use pronunciation dictionaries to control the pronunciation of specific words or phrases. This can be useful for ensuring that certain words are pronounced correctly or for adding emphasis to certain words or phrases.

Unlike `voice_settings` and `generation_config`, pronunciation dictionaries must be specified in the “Initialize Connection” message. See the [API Reference](https://elevenlabs.io/docs/api-reference/text-to-speech/v-1-text-to-speech-voice-id-stream-input#send.Initialize%20Connection.pronunciation_dictionary_locators) for more information.

When using phoneme-based pronunciation dictionaries with WebSockets, you must add `enable_ssml_parsing=true` as a query parameter to the WebSocket URI. For example:

```
wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model_id}&enable_ssml_parsing=true
```

## Best practice

- We suggest using the default setting for `chunk_length_schedule` in `generation_config`.
- When developing a real-time conversational agent application, we advise using `flush: true` along with the text at the end of conversation turn to ensure timely audio generation.
- If the default setting doesn’t provide optimal latency for your use case, you can modify the `chunk_length_schedule`. However, be mindful that reducing latency through this adjustment may come at the expense of quality.

## Tips

- The WebSocket connection will automatically close after 20 seconds of inactivity. To keep the connection open, you can send a single space character `" "`. Please note that this string must include a space, as sending a fully empty string, `""`, will close the WebSocket.
- Send an empty string to close the WebSocket connection after sending the last text message.
- You can use `alignment` to get the word-level timestamps for each word in the text. This can be useful for aligning the audio with the text in a video or for other applications that require precise timing. See the [API Reference](https://elevenlabs.io/docs/api-reference/text-to-speech/v-1-text-to-speech-voice-id-stream-input#receive.Audio%20Output.alignment) for more information.

## Next steps

[TTS streaming\\
\\
Use HTTP streaming when input text is available up-front rather than generated in real time.](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/streaming) [Latency optimization\\
\\
Reduce time-to-first-audio with model selection, voice choice, and geographic routing.](https://elevenlabs.io/docs/eleven-api/guides/how-to/best-practices/latency-optimization)
