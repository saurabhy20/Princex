# main.py - Entry point for Prince-X Userbot
import logging
import asyncio
import sys
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Prince-X")

# Initialize clients
client = TelegramClient(
    StringSession(config.SESSION_STRING),
    config.API_ID,
    config.API_HASH
)

bot = None
if config.BOT_TOKEN:
    bot = TelegramClient('bot', config.API_ID, config.API_HASH)

# Plugin loader
def load_plugins():
    plugin_count = 0
    for filename in os.listdir(config.PLUGINS_DIR):
        if filename.endswith('.py') and not filename.startswith('_'):
            plugin_name = filename[:-3]
            try:
                plugin_path = f"{config.PLUGINS_DIR}.{plugin_name}"
                __import__(plugin_path)
                
                module = sys.modules[plugin_path]
                if hasattr(module, 'register_handlers'):
                    module.register_handlers(client, bot)
                
                plugin_count += 1
                logger.info(f"Loaded plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error loading {plugin_name}: {str(e)}")
    return plugin_count

# Startup notification
async def send_startup_message():
    me = await client.get_me()
    message = (
        "🚀 **Prince-X Userbot Activated!**\n\n"
        f"👑 **User:** [{me.first_name}](tg://user?id={me.id})\n"
        f"🔌 **Plugins Loaded:** {load_plugins()}\n"
        "📅 **System Status:** Operational\n\n"
        "_Report issues @PrinceXSupport_"
    )
    
    if config.LOG_CHANNEL:
        await client.send_message(config.LOG_CHANNEL, message)
    else:
        logger.info("No LOG_CHANNEL set, skipping startup message")

# Core commands
@client.on(events.NewMessage(pattern=r'\.ping'))
async def ping_handler(event):
    from datetime import datetime
    start = datetime.now()
    await event.edit("🏓 `Pong!`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"🏓 **Pong!**\n`{ms:.2f}ms`")

@client.on(events.NewMessage(pattern=r'\.alive'))
async def alive_handler(event):
    await event.reply("💫 **Prince-X is Alive!**\n`Version 2.0 • Free Server`")

# Main function
async def main():
    await client.start()
    logger.info("Prince-X Client Started")
    
    if bot:
        await bot.start(bot_token=config.BOT_TOKEN)
        logger.info("Assistant Bot Started")
    
    await send_startup_message()
    logger.info("Startup process completed")
    
    # Keep running
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
