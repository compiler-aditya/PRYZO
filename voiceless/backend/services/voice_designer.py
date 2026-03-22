"""Voice selection using ElevenLabs premade voices (no paid voice-creation required)."""

import random
from elevenlabs.client import ElevenLabs
from config import settings

client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

# Premade voices mapped by gender + emotion
# These are free voices available on all ElevenLabs plans

MALE_VOICES = {
    "grief":     ("SAz9YHcvj6GT2YYXdXww", "River - Relaxed, Neutral"),
    "joy":       ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
    "anger":     ("IKne3meq5aSn9XLyUdCD", "Charlie - Deep, Confident"),
    "nostalgia": ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
    "fear":      ("CwhRBWXzGAHq8TQ4Fs17", "Roger - Laid-Back, Casual"),
    "peace":     ("CwhRBWXzGAHq8TQ4Fs17", "Roger - Laid-Back, Casual"),
    "love":      ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
    "regret":    ("SAz9YHcvj6GT2YYXdXww", "River - Relaxed, Neutral"),
    "wonder":    ("bIHbv24MWmeRgasZH58o", "Will - Relaxed"),
    "conviction":("IKne3meq5aSn9XLyUdCD", "Charlie - Deep, Confident"),
    "curiosity": ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
}

FEMALE_VOICES = {
    "grief":     ("EXAVITQu4vr4xnSDxMaL", "Sarah - Mature, Reassuring"),
    "joy":       ("cgSgspJ2msm6clMCkdW9", "Jessica - Playful, Bright"),
    "anger":     ("XrExE9yKIg1WjnnlVkGX", "Matilda - Professional"),
    "nostalgia": ("EXAVITQu4vr4xnSDxMaL", "Sarah - Mature, Reassuring"),
    "fear":      ("Xb7hH8MSUJpSbSDYk0k2", "Alice - Clear, Engaging"),
    "peace":     ("EXAVITQu4vr4xnSDxMaL", "Sarah - Mature, Reassuring"),
    "love":      ("cgSgspJ2msm6clMCkdW9", "Jessica - Playful, Bright"),
    "regret":    ("EXAVITQu4vr4xnSDxMaL", "Sarah - Mature, Reassuring"),
    "wonder":    ("Xb7hH8MSUJpSbSDYk0k2", "Alice - Clear, Engaging"),
    "conviction":("XrExE9yKIg1WjnnlVkGX", "Matilda - Professional"),
    "curiosity": ("Xb7hH8MSUJpSbSDYk0k2", "Alice - Clear, Engaging"),
}

# Neutral defaults (used when gender not specified)
NEUTRAL_VOICES = {
    "grief":     ("SAz9YHcvj6GT2YYXdXww", "River - Relaxed, Neutral"),
    "joy":       ("cgSgspJ2msm6clMCkdW9", "Jessica - Playful, Bright"),
    "anger":     ("IKne3meq5aSn9XLyUdCD", "Charlie - Deep, Confident"),
    "nostalgia": ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
    "fear":      ("EXAVITQu4vr4xnSDxMaL", "Sarah - Mature, Reassuring"),
    "peace":     ("CwhRBWXzGAHq8TQ4Fs17", "Roger - Laid-Back, Casual"),
    "love":      ("cgSgspJ2msm6clMCkdW9", "Jessica - Playful, Bright"),
    "regret":    ("SAz9YHcvj6GT2YYXdXww", "River - Relaxed, Neutral"),
    "wonder":    ("Xb7hH8MSUJpSbSDYk0k2", "Alice - Clear, Engaging"),
    "conviction":("IKne3meq5aSn9XLyUdCD", "Charlie - Deep, Confident"),
    "curiosity": ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
}

# Pool of voices for random user profiles
USER_VOICE_POOL = [
    ("CwhRBWXzGAHq8TQ4Fs17", "Roger - Laid-Back"),
    ("EXAVITQu4vr4xnSDxMaL", "Sarah - Mature"),
    ("IKne3meq5aSn9XLyUdCD", "Charlie - Deep"),
    ("SAz9YHcvj6GT2YYXdXww", "River - Relaxed"),
    ("cjVigY5qzO86Huf0OWal", "Eric - Smooth"),
    ("bIHbv24MWmeRgasZH58o", "Will - Relaxed"),
    ("Xb7hH8MSUJpSbSDYk0k2", "Alice - Clear"),
    ("XrExE9yKIg1WjnnlVkGX", "Matilda - Professional"),
    ("cgSgspJ2msm6clMCkdW9", "Jessica - Bright"),
]


async def create_emotion_matched_voice(emotion: str, gender: str = "neutral") -> tuple[str, str]:
    """Pick a premade voice matched to emotion and gender.

    Args:
        emotion: Primary emotion of the story
        gender: "male", "female", or "neutral"

    Returns (voice_id, voice_description)
    """
    if gender == "male":
        voice_map = MALE_VOICES
    elif gender == "female":
        voice_map = FEMALE_VOICES
    else:
        voice_map = NEUTRAL_VOICES

    voice_id, description = voice_map.get(emotion, voice_map.get("peace", NEUTRAL_VOICES["peace"]))
    return voice_id, description


async def create_random_voice() -> tuple[str, str]:
    """Pick a random premade voice for an anonymous user profile."""
    voice_id, description = random.choice(USER_VOICE_POOL)
    return voice_id, description
