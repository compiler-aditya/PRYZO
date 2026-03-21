<!-- Source: https://elevenlabs.io/docs/eleven-api/quickstart -->

By the end of this guide you will have a working script that sends a text string to the ElevenLabs API and plays the returned audio through your speakers. You will learn how to authenticate with an API key, install the SDK, and make your first text-to-speech request.

For guides covering other capabilities — streaming, voice cloning, speech-to-text — see the [Tutorials](https://elevenlabs.io/docs/eleven-api/guides/cookbooks) section.

Use the [ElevenLabs text-to-speech skill](https://github.com/elevenlabs/skills/tree/main/text-to-speech) to generate speech from your AI coding assistant:

```
npx skills add elevenlabs/skills --skill text-to-speech
```

## Using the Text to Speech API

[1](https://elevenlabs.io/docs/eleven-api/quickstart#create-an-api-key)

### Create an API key

[Create an API key in the dashboard here](https://elevenlabs.io/app/settings/api-keys), which you’ll use to securely [access the API](https://elevenlabs.io/docs/api-reference/authentication).

Store the key as a managed secret and pass it to the SDKs either as a environment variable via an `.env` file, or directly in your app’s configuration depending on your preference.

.env

```
ELEVENLABS_API_KEY=<your_api_key_here>
```

[2](https://elevenlabs.io/docs/eleven-api/quickstart#install-the-sdk)

### Install the SDK

We’ll also use the `dotenv` library to load our API key from an environment variable.

PythonTypeScript

```
pip install elevenlabs
pip install python-dotenv
```

To play the audio through your speakers, you may be prompted to install [MPV](https://mpv.io/)
and/or [ffmpeg](https://ffmpeg.org/).

[3](https://elevenlabs.io/docs/eleven-api/quickstart#make-your-first-request)

### Make your first request

Create a new file named `example.py` or `example.mts`, depending on your language of choice and add the following code:

PythonTypeScript

```
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

audio = elevenlabs.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # "George" - browse voices at elevenlabs.io/app/voice-library
    model_id="eleven_v3",
    output_format="mp3_44100_128",
)

play(audio)
```

[4](https://elevenlabs.io/docs/eleven-api/quickstart#run-the-code)

### Run the code

PythonTypeScript

```
python example.py
```

You should hear the audio play through your speakers.

## Next steps

[Stream audio\\
\\
Reduce latency by streaming audio as it generates rather than waiting for the complete file](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/streaming) [Browse voices\\
\\
Explore 5,000+ voices and swap the example voice ID for one that fits your use case](https://elevenlabs.io/app/voice-library) [Clone a voice\\
\\
Create a custom voice from a short audio recording](https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/instant-voice-cloning)
