"""Episode script generation using Gemini — turns story + context into a production-ready script."""

import json
from google import genai
from config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-2.5-flash"


async def generate_episode_script(
    anonymized_text: str,
    time_capsule: dict,
    similar_stories: list[dict],
    category: str,
    emotion: str,
    title: str,
) -> dict:
    """Generate a full episode script with audio directions.

    Returns:
        {
            "sections": [{"speaker": "narrator"|"story", "text": str}],
            "sound_effects": [{"description": str, "duration": float, "timing": str}],
            "music": {"description": str, "mood": str},
            "voice_direction": str
        }
    """
    # Build context strings
    tc_facts = "\n".join(f"- {f}" for f in time_capsule.get("facts", []))
    tc_cultural = "\n".join(f"- {f}" for f in time_capsule.get("cultural_context", []))
    tc_stats = "\n".join(f"- {f}" for f in time_capsule.get("statistics", []))
    similar_count = len(similar_stories)

    era = time_capsule.get("era")
    era_line = f"This story is set around {era}." if era else "No specific era mentioned."

    response = client.models.generate_content(
        model=MODEL,
        contents=f"""Write a produced audio episode script for Voiceless — an anonymous storytelling platform.

TITLE: "{title}"
CATEGORY: {category}
EMOTION: {emotion}
{era_line}

THE ANONYMIZED STORY:
{anonymized_text}

TIME CAPSULE CONTEXT (from Firecrawl web research):
Facts: {tc_facts if tc_facts else "None available"}
Cultural context: {tc_cultural if tc_cultural else "None available"}
Statistics: {tc_stats if tc_stats else "None available"}

SIMILAR STORIES FOUND: {similar_count} people wrote publicly about a similar experience.

---

SCRIPT STRUCTURE — SINGLE FIRST-PERSON SPEAKER (no narrator):

The ENTIRE episode is spoken by ONE person — the storyteller themselves. They tell their own story,
weave in context, and close with a reflection. Everything is in FIRST PERSON ("I", "me", "my").

1. OPENING: 2-3 sentences. The storyteller sets the scene using time capsule context in their own words.
   Example: "It was 2012. I remember the economy was still recovering... 400,000 small businesses
   had closed that year. Mine was about to become one of them."

2. STORY: The main anonymized text adapted for audio.
   - Keep FIRST PERSON throughout: "I remember...", "I felt...", "I didn't know..."
   - Add ElevenLabs audio tags: [gentle], [heavy], [hopeful], [trembling], [whispered]
   - Add ellipses for trailing thoughts...
   - Add [pause] markers between heavy moments
   - Adapt written text to spoken cadence (shorter sentences, natural breath points)
   - Mark intimate confessions with [whispered]
   - You can split the story into 2-3 sections for natural pacing

3. CONTEXT WEAVE: The storyteller naturally weaves in statistics or facts from the time capsule.
   Example: "I didn't know it then, but {similar_count} other people were going through the exact same thing."

4. CLOSING: The storyteller reflects and closes.
   Example: "If you're listening to this... and something felt familiar... just know — you're not alone."

ALL sections use speaker: "story". Do NOT use speaker: "narrator" at all.

SOUND EFFECTS: 1-3 ambient sounds that match the story's mood and era.
Each: description (for ElevenLabs SFX API), duration (seconds), timing (when to play).

MUSIC: One background track description and mood.

Respond as JSON only:
{{
  "sections": [
    {{"speaker": "story", "text": "[gentle] It was 2012. I remember the economy was still shaking... 400,000 small businesses had closed that year. Mine was about to become one of them."}},
    {{"speaker": "story", "text": "[heavy] I remember the last customer who walked in... I stood behind the counter, watching them leave. [pause] I knew it was over."}},
    {{"speaker": "story", "text": "[whispered] I locked the door for the last time... and I just stood there. [pause] I didn't know it then, but so many other people were standing in front of their own locked doors that same year."}},
    {{"speaker": "story", "text": "[hopeful] If you're listening to this... and something felt familiar... you're not alone. None of us are."}}
  ],
  "sound_effects": [
    {{"description": "shop bell ringing gently then silence", "duration": 3.0, "timing": "after section 1"}}
  ],
  "music": {{"description": "solo piano gentle melancholy reflective", "mood": "grief"}},
  "voice_direction": "Quiet measured voice slightly low like someone speaking at 2 AM"
}}""",
    )

    try:
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(raw)
    except (json.JSONDecodeError, IndexError):
        # Fallback: simple two-section script
        return {
            "sections": [
                {"speaker": "story", "text": anonymized_text},
                {"speaker": "story", "text": "If you're listening to this and something felt familiar... you're not alone."},
            ],
            "sound_effects": [],
            "music": {"description": "gentle ambient piano", "mood": emotion},
            "voice_direction": "Warm measured voice with emotional depth",
        }
