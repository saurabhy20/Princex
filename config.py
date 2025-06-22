# config.py - Configuration settings
import os

class Config:
    # Telegram API credentials
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    SESSION_STRING = os.getenv("SESSION_STRING", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", None)  # Optional assistant bot
    
    # Plugin configurations
    PLUGINS_DIR = "plugins"
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", 0))  # For logging
    OWNER_ID = int(os.getenv("OWNER_ID", 0))  # Bot owner ID
    
    # AI services
    OPENAI_KEY = os.getenv("OPENAI_KEY", "")
    SCREENSHOT_API_KEY = os.getenv("SCREENSHOT_API_KEY", "")
    
    # Welcome plugin settings
    WELCOME_ENABLED = os.getenv("WELCOME_ENABLED", "true").lower() == "true"
    WELCOME_GROUP = int(os.getenv("WELCOME_GROUP", 0))
    
    # Security
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]

config = Config()
