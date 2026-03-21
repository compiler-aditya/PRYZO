<!-- Source: https://elevenlabs.io/docs/overview/capabilities/voice-changer -->

The Best AI Voice Changer (Full Tutorial) - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[The Best AI Voice Changer (Full Tutorial)](https://www.youtube.com/watch?v=d3B3BiCmczc)

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

[Watch on](https://www.youtube.com/watch?v=d3B3BiCmczc&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 3:10

•Live

•

## Overview

ElevenLabs [voice changer](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert) API lets you transform any source audio (recorded or uploaded) into a different, fully cloned voice without losing the performance nuances of the original. It’s capable of capturing whispers, laughs, cries, accents, and subtle emotional cues to achieve a highly realistic, human feel and can be used to:

- Change any voice while preserving emotional delivery and nuance
- Create consistent character voices across multiple languages and recording sessions
- Fix or replace specific words and phrases in existing recordings

Explore our [voice library](https://elevenlabs.io/voice-library) to find the perfect voice for your project.

[Products\\
\\
Step-by-step guide for using voice changer in ElevenLabs.](https://elevenlabs.io/docs/creative-platform/playground/voice-changer) [Developers\\
\\
Learn how to integrate voice changer into your application.](https://elevenlabs.io/docs/developers/guides/cookbooks/voice-changer) [API reference\\
\\
Full API reference for the Voice Changer endpoint.](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert)

## Supported languages

Our multilingual v2 models support 29 languages:

_English (USA, UK, Australia, Canada), Japanese, Chinese, German, Hindi, French (France, Canada), Korean, Portuguese (Brazil, Portugal), Italian, Spanish (Spain, Mexico), Indonesian, Dutch, Turkish, Filipino, Polish, Swedish, Bulgarian, Romanian, Arabic (Saudi Arabia, UAE), Czech, Greek, Finnish, Croatian, Malay, Slovak, Danish, Tamil, Ukrainian & Russian._

The `eleven_english_sts_v2` model only supports English.

## Key facts

- **Maximum segment length**: 5 minutes — split longer recordings into chunks
- **Billing**: 1,000 characters per minute of processed audio
- **Background noise**: Use `remove_background_noise=true` to minimize environmental sounds in the output
- **Model recommendation**: `eleven_multilingual_sts_v2` often outperforms `eleven_english_sts_v2` even for English content
- **Custom voices**: Any cloned or designed voice in your library can be used as the output voice; provide its `voice_id`
