"""Celery task: Full episode production pipeline.

Flow: score → anonymize → enrich → script → produce → upload → publish
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
from datetime import datetime, timezone
from tasks.celery_app import celery

logger = logging.getLogger(__name__)


def _run(coro):
    """Run an async function from sync Celery task."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery.task(bind=True, max_retries=2)
def produce_episode_task(self, story_id: str, raw_text: str, source_type: str, gender: str = "neutral"):
    """Full production pipeline for a story."""
    from models.database import get_db
    from services.scorer import score_story
    from services.anonymizer import anonymize_text
    from services.timecapsule import build_time_capsule
    from services.matcher import find_similar_stories
    from services.scriptwriter import generate_episode_script
    from services.producer import produce_episode
    from services.agent_setup import create_reflection_agent
    from config import settings

    db = get_db()

    try:
        # Step 1: Score the story
        db.table("stories").update({"status": "anonymizing"}).eq("id", story_id).execute()
        score = _run(score_story(raw_text, source_type))
        total = score.get("human_voice", 0) + score.get("substance", 0) + score.get("originality", 0)
        logger.info(
            "Score for %s: total=%d/30 (voice=%s, substance=%s, orig=%s) "
            "ai_prob=%.2f is_blog=%s passes=%s source_type=%s",
            story_id, total,
            score.get("human_voice"), score.get("substance"), score.get("originality"),
            score.get("is_ai_probability", 0), score.get("is_blog"), score.get("passes"), source_type,
        )

        if not score["passes"]:
            # Build a human-readable rejection reason
            total = score.get("human_voice", 0) + score.get("substance", 0) + score.get("originality", 0)
            reasons = []
            if not score.get("is_blog", True):
                reasons.append("This doesn't appear to be a blog post or personal writing.")
            if score.get("is_ai_probability", 0) >= 0.7:
                reasons.append("This appears to be AI-generated content.")
            if total < 10 and not reasons:
                reasons.append(f"The content scored {total}/30 on our quality check (minimum 10 needed). Try submitting something with more personal depth or a stronger point of view.")
            reason = " ".join(reasons) if reasons else "The content didn't meet our quality threshold. Try submitting something more personal or with deeper substance."

            db.table("stories").update({
                "status": "rejected",
                "quality_score": score,
                "status_reason": reason,
            }).eq("id", story_id).execute()
            return {"status": "rejected", "reason": reason}

        # Step 2: Anonymize
        anonymized = _run(anonymize_text(raw_text))

        db.table("stories").update({
            "anonymized_text": anonymized,
            "category": score["category"],
            "emotion": score["emotion"],
            "quality_score": score,
            "title": score.get("title_suggestion", "Untitled"),
            "status": "enriching",
        }).eq("id", story_id).execute()

        # Step 3: Enrich with time capsule + similar stories
        time_capsule = _run(build_time_capsule(anonymized, score["category"]))
        similar = _run(find_similar_stories(anonymized, score["category"], score["emotion"]))

        db.table("stories").update({
            "time_capsule": time_capsule,
            "similar_stories": [s for s in similar],
            "status": "scripting",
        }).eq("id", story_id).execute()

        # Step 4: Generate episode script
        title = score.get("title_suggestion", "Untitled")
        script = _run(generate_episode_script(
            anonymized, time_capsule, similar,
            score["category"], score["emotion"], title,
        ))

        db.table("stories").update({
            "episode_script": str(script),
            "status": "producing",
        }).eq("id", story_id).execute()

        # Step 5: Produce audio (single first-person voice, no narrator)
        audio_bytes, duration = _run(produce_episode(script, score["emotion"], gender))

        # Step 6: Upload to Google Cloud Storage
        from google.cloud import storage as gcs
        if settings.GCS_KEY_FILE:
            gcs_client = gcs.Client.from_service_account_json(settings.GCS_KEY_FILE)
        else:
            gcs_client = gcs.Client()  # uses ADC on Cloud Run
        bucket = gcs_client.bucket(settings.GCS_BUCKET)
        blob = bucket.blob(f"episodes/{story_id}.mp3")
        blob.upload_from_string(audio_bytes, content_type="audio/mpeg")
        audio_url = f"https://storage.googleapis.com/{settings.GCS_BUCKET}/episodes/{story_id}.mp3"

        # Step 7: Create reflection agent (optional — won't block publishing)
        agent_id = None
        try:
            agent_id = _run(create_reflection_agent(
                story_id=story_id,
                title=title,
                category=score["category"],
                emotion=score["emotion"],
                anonymized_text=anonymized,
                time_capsule=time_capsule,
                similar_count=len(similar),
            ))
        except Exception:
            pass  # Agent creation is nice-to-have, not required

        # Step 8: Publish
        db.table("stories").update({
            "audio_url": audio_url,
            "audio_duration_secs": duration,
            "status": "published",
            "published_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", story_id).execute()

        return {"status": "published", "story_id": story_id, "agent_id": agent_id}

    except Exception as exc:
        # Build user-friendly error reason
        error_msg = str(exc)
        if "quota_exceeded" in error_msg or "credits" in error_msg.lower():
            reason = "Audio generation temporarily unavailable — our voice synthesis quota has been reached. Your story is saved and will be produced when quota resets."
        elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            reason = "Production timed out. We'll retry automatically."
        else:
            reason = "Something went wrong during production. We'll retry automatically."

        status = "failed" if self.request.retries >= self.max_retries else "pending"
        db.table("stories").update({
            "status": status,
            "status_reason": reason,
        }).eq("id", story_id).execute()
        raise self.retry(exc=exc, countdown=60)
