<!-- Source: https://elevenlabs.io/docs/eleven-api/resources/agent-tooling -->

## Overview

Agent tooling includes reusable skills and local integrations that help you automate ElevenLabs workflows in developer tools and assistants.

## Agent skills

Agent Skills are reusable building blocks for common ElevenLabs workflows. They follow the Agent Skills specification and can be used with compatible coding assistants. Install the skills with:

```
npx skills add elevenlabs/skills
```

The official collection is hosted in the [elevenlabs/skills](https://github.com/elevenlabs/skills) repository.
Open each skill for a prompt you can paste into your assistant after installing the skills.

###### Text to speech

Convert text to speech using ElevenLabs voices.

```
Use the text to speech skill to generate audio for the script below.
Model: eleven_v3
Voice: "Juniper" (or default).
Output: Save the MP3 file locally and return the file path.
Script: "Welcome to ElevenLabs. Today we will walk through the new agent tooling."
```

###### Speech to text

Transcribe audio to text with timestamps.

```
Use the speech to text skill to transcribe the audio file path/to/file.mp3.
Return a transcript that contains speaker IDs and timestamps at the start of each paragraph.
```

###### Realtime speech to text

Stream live transcription with low latency.

```
Use the speech to text skill to start a real-time transcription session for microphone input.
Model: scribe_v2_realtime.
Stream partial transcripts and return committed transcripts with word-level timestamps.
```

###### Agents

Build conversational voice agents.

```
Use the Agents skill to create a voice agent named "Support Concierge".
Persona: friendly, concise, asks clarifying questions when needed.
Goals: answer pricing questions and route enterprise leads to sales.
```

###### Sound effects

Generate sound effects from text prompts.

```
Use the Sound effects skill to generate a 3-second effect: "Wooden door creaks open, then a soft slam."
Output WAV at 48 kHz and return the file path.
```

###### Music

Generate music tracks from prompts.

```
Use the Music skill to generate a 30-second instrumental loop.
Style: lo-fi hip hop, warm, chill.
BPM: 80. No vocals.
Return the audio file path.
```

###### Setup API key

Get and configure an ElevenLabs API key.

```
How do I get my ElevenLabs API key?
```

## ElevenLabs MCP server

The ElevenLabs MCP server is a local Model Context Protocol server for the ElevenLabs platform. It runs on your machine so tools like Claude and Cursor can call ElevenLabs APIs through simple prompts.

[ElevenLabs MCP\\
\\
Install and run the MCP server locally.](https://github.com/elevenlabs/elevenlabs-mcp)
