# config.py - Configuration settings
import os

API_ID = int(os.getenv("API_ID", 12345))
API_HASH = os.getenv("API_HASH", "your_api_hash")
SESSION_STRING = os.getenv("SESSION_STRING", "your_session_string")
BOT_TOKEN = os.getenv("BOT_TOKEN", None)  # Optional assistant bot
PLUGINS_DIR = "plugins"
