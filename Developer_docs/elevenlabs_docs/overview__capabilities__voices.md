<!-- Source: https://elevenlabs.io/docs/overview/capabilities/voices -->

## Overview

ElevenLabs provides models for voice creation & customization. The platform supports a wide range of voice options, including voices from our extensive [voice library](https://elevenlabs.io/app/voice-library), voice cloning, and artificially designed voices using text prompts.

### Voice types

- **Community**: Voices shared by the community from the ElevenLabs [voice library](https://elevenlabs.io/docs/creative-platform/voices/voice-library).
- **Cloned**: Custom voices created using instant or professional [voice cloning](https://elevenlabs.io/docs/creative-platform/voices/voice-cloning).
- **Voice design**: Artificially designed voices created with the [voice design](https://elevenlabs.io/docs/creative-platform/voices/voice-design) tool.
- **Default**: Pre-designed, high-quality voices optimized for general use.

Voices that you personally own, either created with Instant Voice Cloning, Professional Voice
Cloning, or Voice Design, can be used for [Voice\\
Remixing](https://elevenlabs.io/docs/overview/capabilities/voice-remixing).

#### Community

The [voice library](https://elevenlabs.io/docs/creative-platform/voices/voice-library) contains over 10,000 voices shared by the ElevenLabs community. Use it to:

- Discover unique voices shared by the ElevenLabs community.
- Add voices to your personal collection.
- Share your own voice clones for cash rewards when other paid subscribers use it.

Share your voice with the community, set your terms, and earn cash rewards when others use it.
We’ve paid out over **$14M** already.

The voice library is not available via the API to free tier users.

[Products\\
\\
Learn how to use voices from the voice library](https://elevenlabs.io/docs/creative-platform/voices/voice-library)

#### Cloned

Clone your own voice from 30-second samples with Instant Voice Cloning, or create hyper-realistic voices using Professional Voice Cloning.

- **Instant Voice Cloning**: Quickly replicate a voice from short audio samples.
- **Professional Voice Cloning**: Generate professional-grade voice clones with extended training audio.

Voice-captcha technology is used to verify that professional voice clones are created from your own voice samples.

A Creator plan or higher is required to create professional voice clones.

[Products\\
\\
Learn how to create instant & professional voice clones](https://elevenlabs.io/docs/creative-platform/voices/voice-cloning) [Instant Voice Cloning\\
\\
Clone a voice instantly](https://elevenlabs.io/docs/developers/guides/cookbooks/voices/instant-voice-cloning) [Professional Voice Cloning\\
\\
Create a perfect voice clone](https://elevenlabs.io/docs/developers/guides/cookbooks/voices/professional-voice-cloning)

#### Voice design

With [Voice Design](https://elevenlabs.io/docs/creative-platform/voices/voice-design), you can create entirely new voices by specifying attributes like age, gender, accent, and tone. Generated voices are ideal for:

- Realistic voices with nuanced characteristics.
- Creative character voices for games and storytelling.

The voice design tool creates 3 voice previews, simply provide:

- A **voice description** between 20 and 1000 characters.
- A **text** to preview the voice between 100 and 1000 characters.

##### Voice design with Eleven v3

Using the [Eleven v3 model](https://elevenlabs.io/docs/overview/models#eleven-v3), voices that are capable of a wide range of emotion can be designed via a prompt.

Using v3 gets you the following benefits:

- More natural and versatile voice generation.
- Better control over voice characteristics.
- Audio tags supported in Preview generations.
- Backward compatibility with v2 models.

[Products\\
\\
Learn how to craft voices from a single prompt.](https://elevenlabs.io/docs/creative-platform/voices/voice-design) [Developers\\
\\
Integrate voice design into your application.](https://elevenlabs.io/docs/developers/guides/cookbooks/voices/voice-design)

#### Default

Our curated set of default voices is optimized for core use cases. These voices are:

- **Reliable**: Available long-term.
- **Consistent**: Carefully crafted and quality-checked for performance.
- **Model-ready**: Fine-tuned on new models upon release.

Default voices are available to all users via the **My Voices** tab in the [voice lab\\
dashboard](https://elevenlabs.io/app/voice-lab). Default voices were previously referred to as
`premade` voices. The latter term is still used when accessing default voices via the API.

### Managing voices

All voices can be managed through **My Voices**, where you can:

- Search, filter, and categorize voices
- Add descriptions and custom tags
- Organize voices for quick access

Learn how to manage your voice collection in [My Voices documentation](https://elevenlabs.io/docs/creative-platform/voices/voice-library#my-voices).

- **Search and Filter**: Find voices using keywords or tags.
- **Preview Samples**: Listen to voice demos before adding them to **My Voices**.
- **Add to Collection**: Save voices for easy access in your projects.

> **Tip**: Try searching by specific accents or genres, such as “Australian narration” or “child-like character.”

### Supported languages

All ElevenLabs voices support multiple languages. Experiment by converting phrases like `Hello! こんにちは! Bonjour!` into speech to hear how your own voice sounds across different languages.

ElevenLabs supports voice creation in 32 languages. Match your voice selection to your target region for the most natural results.

- **Default Voices**: Optimized for multilingual use.
- **Generated and Cloned Voices**: Accent fidelity depends on input samples or selected attributes.

Our multilingual v2 models support 29 languages:

_English (USA, UK, Australia, Canada), Japanese, Chinese, German, Hindi, French (France, Canada), Korean, Portuguese (Brazil, Portugal), Italian, Spanish (Spain, Mexico), Indonesian, Dutch, Turkish, Filipino, Polish, Swedish, Bulgarian, Romanian, Arabic (Saudi Arabia, UAE), Czech, Greek, Finnish, Croatian, Malay, Slovak, Danish, Tamil, Ukrainian & Russian._

Flash v2.5 supports 32 languages - all languages from v2 models plus:

_Hungarian, Norwegian & Vietnamese_

[Learn more about our models](https://elevenlabs.io/docs/overview/models)

## Key facts

- **Instant Voice Cloning**: Created from short audio samples (30 seconds or more); available on most plans
- **Professional Voice Cloning**: Requires extended training audio for highest fidelity; requires a Creator plan or higher
- **Voice sharing**: Professional Voice Clones can be shared publicly in the Voice Library; Instant Voice Clones and Generated Voices cannot
- **Generated Voices**: Created from text descriptions via Voice Design — suited for unique characters in games, animations, and creative storytelling
