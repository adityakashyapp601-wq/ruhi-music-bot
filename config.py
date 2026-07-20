"""
✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦ - Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Spotify Configuration (Optional)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# Admin IDs
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []

# Bot Settings
BOT_NAME = "✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦"
BOT_USERNAME = "RuhiMusicBot"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Music Settings
MAX_QUEUE_SIZE = 100
DOWNLOAD_DIR = "downloads"
