# main.py - Entry point for Prince-X Userbot
import os
import sys
import logging
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION_STRING, BOT_TOKEN, PLUGINS_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Prince-X")

# Client initialization
client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)

if BOT_TOKEN:
    bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
else:
    bot = None

# Load plugins dynamically
def load_plugins():
    plugin_count = 0
    for filename in os.listdir(PLUGINS_DIR):
        if filename.endswith('.py') and not filename.startswith('_'):
            plugin_name = filename[:-3]
            try:
                # Import plugin module
                plugin_path = f"plugins.{plugin_name}"
                __import__(plugin_path)
                
                # Register handlers if defined
                module = sys.modules[plugin_path]
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(client, bot)
                
                plugin_count += 1
                logger.info(f"Loaded plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error loading {plugin_name}: {str(e)}")
    return plugin_count

# Startup message
async def send_startup_message():
    me = await client.get_me()
    message = (
        "🚀 **Prince-X Userbot Activated!**\n\n"
        f"👑 **User:** [{me.first_name}](tg://user?id={me.id})\n"
        f"🔌 **Plugins Loaded:** {load_plugins()}\n"
        "📅 **System Status:** Operational\n\n"
        "_Report issues @PrinceXSupport_"
    )
    
    if bot:
        await bot.send_message("me", message)
    else:
        await client.send_message("me", message)

# Core commands
@client.on(events.NewMessage(pattern=r'\.ping'))
async def ping_handler(event):
    start = datetime.now()
    await event.edit("🏓 `Pong!`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"🏓 **Pong!**\n`{ms}ms`")

@client.on(events.NewMessage(pattern=r'\.alive'))
async def alive_handler(event):
    await event.reply("💫 **Prince-X is Alive!**\n`Version 2.0 • Fly.io`")

# Main function
async def main():
    await client.start()
    logger.info("Prince-X Client Started")
    
    if bot:
        await bot.start()
        logger.info("Assistant Bot Started")
    
    await send_startup_message()
    logger.info("Startup message sent")
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
