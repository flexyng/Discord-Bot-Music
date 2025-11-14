import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "discord_music_bot")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "es")

COMMAND_PREFIX = "!"
OWNER_IDS = [int(oid) for oid in os.getenv("OWNER_IDS", "").split(",") if oid.strip()] if os.getenv("OWNER_IDS") else []

COLORS = {
    "primary": 0x7B2CBF,
    "success": 0x06A77D,
    "error": 0xFF0000,
    "premium": 0xFFD700,
    "warning": 0xFFA500,
}

SUPPORTED_LANGUAGES = {
    "es": "Español",
    "en": "English",
    "ar": "العربية",
    "pt": "Português"
}

PREMIUM_FEATURES = {
    "unlimited_playlists": {"free": 5, "premium": None},
    "unlimited_queue": {"free": 50, "premium": None},
    "advanced_analytics": {"free": False, "premium": True},
    "custom_prefix": {"free": False, "premium": True},
    "priority_support": {"free": False, "premium": True},
    "ad_free": {"free": False, "premium": True},
}
