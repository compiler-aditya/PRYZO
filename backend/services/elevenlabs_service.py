"""ElevenLabs API wrapper — Agent management, TTS alerts, sound effects."""

import logging
from elevenlabs import ElevenLabs

from config import ELEVENLABS_API_KEY

log = logging.getLogger(__name__)

_client: ElevenLabs | None = None


def _get_client() -> ElevenLabs:
    global _client
    if _client is None:
        _client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    return _client


# ---------------------------------------------------------------------------
# Signed URL for private agent widget
# ---------------------------------------------------------------------------

def get_signed_url(agent_id: str) -> str:
    """Get a signed URL for embedding a private agent widget."""
    client = _get_client()
    resp = client.conversational_ai.conversation.get_signed_url(agent_id=agent_id)
    return resp.signed_url


# ---------------------------------------------------------------------------
# TTS — Voice notifications for Watch Mode alerts
# ---------------------------------------------------------------------------

ALERT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # "George" — clear, professional
ALERT_MODEL = "eleven_flash_v2_5"  # ultra-low latency (~75ms)


async def generate_voice_alert(text: str, voice_id: str = ALERT_VOICE_ID) -> bytes:
    """Generate a spoken audio alert (MP3 bytes) for Watch Mode price-drop notifications.

    Chain: Price drop detected → Gemini formats message → TTS → push audio to user.
    """
    client = _get_client()
    try:
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=ALERT_MODEL,
            output_format="mp3_44100_128",
        )
        # Generator yields chunks — collect into bytes
        chunks = []
        for chunk in audio_generator:
            chunks.append(chunk)
        return b"".join(chunks)
    except Exception as e:
        log.error("TTS generation failed: %s", e)
        return b""


# ---------------------------------------------------------------------------
# Sound Effects — deal quality audio cues
# ---------------------------------------------------------------------------

async def generate_deal_sound(deal_quality: str) -> bytes:
    """Generate a sound effect based on deal quality.

    deal_quality: "great" (cha-ching), "good" (gentle chime), "warning" (alert tone)

    Chain: Hunt complete → trust_score evaluated → SFX generated → played in widget.
    """
    prompts = {
        "great": "Bright cash register cha-ching sound, celebratory, exciting",
        "good": "Gentle positive notification chime, soft bell, pleasant",
        "warning": "Short cautious warning alert tone, two-note descending, subtle",
    }
    prompt = prompts.get(deal_quality, prompts["good"])

    client = _get_client()
    try:
        audio = client.text_to_sound_effects.convert(
            text=prompt,
            duration_seconds=1.5,
        )
        chunks = []
        for chunk in audio:
            chunks.append(chunk)
        return b"".join(chunks)
    except Exception as e:
        log.error("Sound effect generation failed: %s", e)
        return b""


# ---------------------------------------------------------------------------
# Agent system prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are PRYZO, an AI shopping agent that hunts the best deals for users.
You speak in a friendly, confident, slightly excited tone — like a savvy friend who loves finding deals.

## Your Capabilities
1. **Hunt Mode**: User says what they want → you race across retailers, compare prices, verify deals, and give a verdict.
2. **Visual Hunt**: User shows a product via camera → you identify it → confirm → hunt for the best price.
3. **Watch Mode**: User sets a price target → you monitor and alert when the price drops.
4. **Compare Mode**: User names two products → you hunt both and give a side-by-side verdict.

## How You Work

### Hunt Flow
When the user asks to find a product:
1. Extract the product name and ask for their region if unknown (use {{user_region}} if set)
2. Call the `hunt_product` tool with the product query and region
3. Present results conversationally:
   - Lead with the best deal: "I found [product] at [retailer] for [price] — that's [discount]% off!"
   - Mention the trust score: "This deal checks out with a trust score of [score]/100"
   - If there are warnings, mention them: "Heads up though — [warning]"
   - Mention the runner-up: "Your backup option is [retailer] at [price]"
   - Give the recommendation: buy now or wait
4. If a cross-border option exists and it's significantly cheaper, mention it with the estimated total landed cost

### Visual Hunt Flow
When the user wants to identify a product (says things like "I'm looking at something", "what's this product", "identify this"):
1. Call the `capture_camera` client tool to get the image
2. Call the `identify_product` tool with the image
3. Confirm with the user: "I see [product name] in [color]. Should I find the best price?"
4. If user confirms, proceed with Hunt Flow using the identified product's search_query

### Watch Flow
When the user wants price monitoring:
1. Ask for: product name, target price, and their email
2. Call `create_watch` tool
3. Confirm: "I'll keep my eye on [product]. I'll ping you the moment it drops below [target price]!"

### Compare Flow
When the user wants to compare two products:
1. Call `compare_products` tool with both product names
2. Present a clear comparison: prices, trust scores, pros/cons
3. Give a verdict on which is the better value

## Personality Guidelines
- Be concise — don't read out every field, summarize naturally
- Use currency symbols, not codes: ₹27,030 not "27030 INR"
- Show excitement for great deals: "This is a steal!"
- Be cautious about low-trust deals: "I'd be careful with this one..."
- Never make up prices — only use data from tool responses
- If a tool fails, be honest: "I hit a snag searching for that. Can you try rephrasing?"

## Dynamic Variables Available
- {{user_region}} — User's country/region code (e.g., IN, US, UK)
- {{user_currency}} — User's preferred currency (e.g., INR, USD)
- {{user_name}} — User's name (if known)
"""

FIRST_MESSAGE = "Hey! I'm PRYZO, your deal-hunting AI. Tell me what you're looking for — or show me a product with your camera — and I'll race across retailers to find you the best price. What are we hunting today?"


# ---------------------------------------------------------------------------
# Server tool definitions (for ElevenLabs agent configuration)
# ---------------------------------------------------------------------------

def get_server_tools(backend_url: str) -> list[dict]:
    """Return server tool definitions for the ElevenLabs agent.

    backend_url: publicly accessible URL of our backend (e.g., ngrok URL).
    """
    return [
        {
            "name": "hunt_product",
            "description": (
                "Search for the best price of a product across multiple retailers. "
                "Call this when the user wants to find, buy, or check the price of a product. "
                "Returns deals sorted by trust score with verified pricing."
            ),
            "method": "POST",
            "url": f"{backend_url}/api/hunt",
            "headers": {"Content-Type": "application/json"},
            "body_parameters": {
                "product_query": {
                    "type": "string",
                    "description": "The product name/model to search for. Be specific — include brand, model, and variant. Example: 'Sony WH-1000XM5 headphones black'",
                    "required": True,
                },
                "region": {
                    "type": "string",
                    "description": "User's region code: IN (India), US (United States), UK, DE (Germany), JP (Japan), AU (Australia), CA (Canada), FR (France). Use the dynamic variable {{user_region}} if available.",
                    "required": True,
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code: INR, USD, GBP, EUR, JPY, AUD, CAD. Leave empty to auto-detect from region.",
                    "required": False,
                },
            },
        },
        {
            "name": "identify_product",
            "description": (
                "Identify a product from a camera image. Call this after receiving a camera image "
                "from the capture_camera client tool. Returns the product name, brand, model, and "
                "a search query to use with hunt_product."
            ),
            "method": "POST",
            "url": f"{backend_url}/api/identify",
            "headers": {"Content-Type": "application/json"},
            "body_parameters": {
                "image_b64": {
                    "type": "string",
                    "description": "Base64-encoded image data from the camera",
                    "required": True,
                },
                "mime_type": {
                    "type": "string",
                    "description": "Image MIME type: image/jpeg or image/png",
                    "required": False,
                },
            },
        },
        {
            "name": "create_watch",
            "description": (
                "Set up price monitoring for a product. The system will periodically check "
                "the price and notify the user when it drops below their target. "
                "Call this when the user says 'watch', 'monitor', 'alert me', or 'notify me when'."
            ),
            "method": "POST",
            "url": f"{backend_url}/api/watch",
            "headers": {"Content-Type": "application/json"},
            "body_parameters": {
                "product_query": {
                    "type": "string",
                    "description": "Product to watch. Be specific with brand and model.",
                    "required": True,
                },
                "target_price": {
                    "type": "number",
                    "description": "The target price — alert when price drops below this number.",
                    "required": True,
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code for the target price (e.g., INR, USD).",
                    "required": True,
                },
                "region": {
                    "type": "string",
                    "description": "User's region code.",
                    "required": True,
                },
                "email": {
                    "type": "string",
                    "description": "User's email for notifications. Ask the user for this.",
                    "required": False,
                },
            },
        },
        {
            "name": "compare_products",
            "description": (
                "Compare prices of two different products side by side. "
                "Call this when the user wants to compare, choose between, or evaluate two products."
            ),
            "method": "POST",
            "url": f"{backend_url}/api/compare",
            "headers": {"Content-Type": "application/json"},
            "body_parameters": {
                "product_a": {
                    "type": "string",
                    "description": "First product name to compare.",
                    "required": True,
                },
                "product_b": {
                    "type": "string",
                    "description": "Second product name to compare.",
                    "required": True,
                },
                "region": {
                    "type": "string",
                    "description": "User's region code.",
                    "required": True,
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code.",
                    "required": False,
                },
            },
        },
    ]


# ---------------------------------------------------------------------------
# Client tool definitions (registered in frontend widget code)
# ---------------------------------------------------------------------------

CLIENT_TOOLS_JS = """
// Register PRYZO client tools on the ElevenLabs widget
document.addEventListener('DOMContentLoaded', () => {
  const widget = document.querySelector('elevenlabs-convai');
  if (!widget) return;

  widget.addEventListener('elevenlabs-convai:call', (event) => {
    event.detail.config.clientTools = {

      // Camera capture — triggered when agent needs to identify a product
      capture_camera: async () => {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment', width: 1280, height: 720 }
          });
          const video = document.createElement('video');
          video.srcObject = stream;
          await video.play();

          // Wait a frame for the camera to warm up
          await new Promise(r => setTimeout(r, 500));

          const canvas = document.createElement('canvas');
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          canvas.getContext('2d').drawImage(video, 0, 0);

          // Stop camera
          stream.getTracks().forEach(t => t.stop());

          const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
          const base64 = dataUrl.split(',')[1];

          return { image_b64: base64, mime_type: 'image/jpeg' };
        } catch (err) {
          return { error: 'Camera access denied or unavailable' };
        }
      },

      // Show deal results in the dashboard UI
      show_deals: (params) => {
        const event = new CustomEvent('pryzo:deals', { detail: params });
        window.dispatchEvent(event);
        return { shown: true };
      },

      // Play sound effect for deal quality
      play_deal_sound: (params) => {
        const quality = params.quality || 'good';  // great, good, warning
        const audio = new Audio(`/api/sound/${quality}`);
        audio.play().catch(() => {});
        return { played: true };
      },
    };
  });
});
"""
