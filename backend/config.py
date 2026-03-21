import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
HUNT_AGENT_ID = os.getenv("HUNT_AGENT_ID", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pryzo.db")
BACKEND_SECRET = os.getenv("BACKEND_SECRET", "dev-secret")

# SMTP for Watch Mode email alerts
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Web Push (VAPID)
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "")
