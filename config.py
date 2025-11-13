import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

COMMAND_PREFIX = "/"
COLORS = {
    "primary": 0x7B2CBF,
    "success": 0x06A77D,
    "error": 0xFF0000,
}
