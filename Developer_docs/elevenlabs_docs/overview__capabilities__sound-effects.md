<!-- Source: https://elevenlabs.io/docs/overview/capabilities/sound-effects -->

## Overview

ElevenLabs [sound effects](https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert) API turns text descriptions into high-quality audio effects with precise control over timing, style and complexity. The model understands both natural language and audio terminology, enabling you to:

- Generate cinematic sound design for films & trailers
- Create custom sound effects for games & interactive media
- Produce Foley and ambient sounds for video content

Listen to an example:

## Usage

Sound effects are generated using text descriptions & two optional parameters:

- **Duration**: Set a specific length for the generated audio (in seconds)
  - Default: Automatically determined based on the prompt
  - Range: 0.1 to 30 seconds
  - Cost: 40 credits per second when duration is specified
- **Looping**: Enable seamless looping for sound effects longer than 30 seconds
  - Creates sound effects that can be played on repeat without perceptible start/end points
  - Perfect for atmospheric sounds, ambient textures, and background elements
  - Example: Generate 30s of ‘soft rain’ then loop it endlessly for atmosphere in audiobooks, films, games
- **Prompt influence**: Control how strictly the model follows the prompt
  - High: More literal interpretation of the prompt
  - Low: More creative interpretation with added variations

[Products\\
\\
Step-by-step guide for using sound effects in ElevenLabs.](https://elevenlabs.io/docs/creative-platform/playground/sound-effects) [Developers\\
\\
Learn how to integrate sound effects into your application.](https://elevenlabs.io/docs/developers/guides/cookbooks/sound-effects) [API reference\\
\\
Full API reference for the Sound Effects endpoint.](https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert)

### Prompting guide

#### Simple effects

For basic sound effects, use clear, concise descriptions:

- “Glass shattering on concrete”
- “Heavy wooden door creaking open”
- “Thunder rumbling in the distance”

#### Complex sequences

For multi-part sound effects, describe the sequence of events:

- “Footsteps on gravel, then a metallic door opens”
- “Wind whistling through trees, followed by leaves rustling”
- “Sword being drawn, then clashing with another blade”

#### Musical elements

The API also supports generation of musical components:

- ”90s hip-hop drum loop, 90 BPM”
- “Vintage brass stabs in F minor”
- “Atmospheric synth pad with subtle modulation”

#### Audio terminology

Common terms that can enhance your prompts:

- **Impact**: Collision or contact sounds between objects, from subtle taps to dramatic crashes
- **Whoosh**: Movement through air effects, ranging from fast and ghostly to slow-spinning or rhythmic
- **Ambience**: Background environmental sounds that establish atmosphere and space
- **One-shot**: Single, non-repeating sound
- **Loop**: Repeating audio segment
- **Stem**: Isolated audio component
- **Braam**: Big, brassy cinematic hit that signals epic or dramatic moments, common in trailers
- **Glitch**: Sounds of malfunction, jittering, or erratic movement, useful for transitions and sci-fi
- **Drone**: Continuous, textured sound that creates atmosphere and suspense

## Key facts

- **Maximum duration**: 30 seconds per generation
- **Output formats**: MP3 for all effects; WAV at 48 kHz for non-looping effects
- **Looping effects**: Designed for seamless repeat playback — no audible start or end point
- **Musical elements**: Drum loops, bass lines, and melodic samples can be generated; for full music production use the [Music](https://elevenlabs.io/docs/overview/capabilities/music) API
