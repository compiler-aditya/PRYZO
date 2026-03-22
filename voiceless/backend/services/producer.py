"""Audio production pipeline — takes a script and produces a full episode using ElevenLabs."""

import io
import tempfile
from pathlib import Path
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs
from config import settings

client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)


async def produce_episode(script: dict, emotion: str, gender: str = "neutral") -> tuple[bytes, int]:
    """Produce a full audio episode from a script using a single voice.

    Args:
        script: {sections, sound_effects, music, voice_direction}
        emotion: Story emotion for voice matching
        gender: "male", "female", or "neutral"

    Returns:
        (audio_bytes, duration_secs)
    """
    # Pick a single voice matched to emotion + gender (no narrator)
    from services.voice_designer import create_emotion_matched_voice
    voice_id, _ = await create_emotion_matched_voice(emotion, gender)

    # Generate speech for each section — all with the same voice
    speech_segments = []
    for section in script["sections"]:
        text = section["text"]
        audio_bytes = _generate_speech(voice_id, text, emotion)
        segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
        speech_segments.append(segment)

    # Generate sound effects
    sfx_segments = []
    for effect in script.get("sound_effects", []):
        try:
            sfx_bytes = _generate_sound_effect(
                effect["description"],
                effect.get("duration", 3.0),
            )
            sfx = AudioSegment.from_mp3(io.BytesIO(sfx_bytes))
            sfx_segments.append(sfx)
        except Exception:
            continue

    # Combine speech segments with short pauses
    combined = AudioSegment.silent(duration=500)  # 0.5s intro silence
    for i, segment in enumerate(speech_segments):
        combined += segment
        if i < len(speech_segments) - 1:
            combined += AudioSegment.silent(duration=1000)

    # Overlay sound effects at approximate positions
    if sfx_segments:
        total_speech_ms = len(combined)
        for i, sfx in enumerate(sfx_segments):
            position = int(total_speech_ms * (i + 1) / (len(sfx_segments) + 1))
            sfx = sfx - 10
            combined = combined.overlay(sfx, position=position)

    # Trailing silence
    combined += AudioSegment.silent(duration=2000)

    # Export
    output = io.BytesIO()
    combined.export(output, format="mp3", bitrate="128k")
    audio_bytes = output.getvalue()
    duration_secs = len(combined) // 1000

    return audio_bytes, duration_secs


async def produce_moment(text: str, voice_id: str) -> tuple[bytes, int]:
    """Produce a short audio clip for a life moment."""
    audio_bytes = _generate_speech(voice_id, text, "peace")
    segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))

    try:
        ambient_bytes = _generate_sound_effect(
            "soft ambient room tone warm quiet",
            duration=min(len(segment) / 1000 + 1, 30),
        )
        ambient = AudioSegment.from_mp3(io.BytesIO(ambient_bytes))
        ambient = ambient - 18
        while len(ambient) < len(segment):
            ambient += ambient
        ambient = ambient[:len(segment)]
        segment = segment.overlay(ambient)
    except Exception:
        pass

    final = AudioSegment.silent(duration=300) + segment + AudioSegment.silent(duration=1000)

    output = io.BytesIO()
    final.export(output, format="mp3", bitrate="128k")
    return output.getvalue(), len(final) // 1000


def _generate_speech(voice_id: str, text: str, emotion: str) -> bytes:
    """Generate speech audio using ElevenLabs TTS."""
    stability = 0.3 if emotion in ("grief", "fear", "regret") else 0.5
    similarity = 0.8

    audio_generator = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=settings.TTS_MODEL,
        output_format="mp3_44100_128",
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity,
        },
    )

    audio_bytes = b""
    for chunk in audio_generator:
        audio_bytes += chunk

    return audio_bytes


def _generate_sound_effect(description: str, duration: float = 3.0) -> bytes:
    """Generate a sound effect using ElevenLabs SFX API."""
    duration = min(max(duration, 0.5), 30.0)

    result = client.text_to_sound_effects.convert(
        text=description,
        duration=duration,
    )

    audio_bytes = b""
    for chunk in result:
        audio_bytes += chunk

    return audio_bytes
