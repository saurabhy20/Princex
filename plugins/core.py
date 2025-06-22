# plugins/core.py - Core functionality
from datetime import datetime
from telethon import events

async def register_handlers(client, bot):
    # System info command
    @client.on(events.NewMessage(pattern=r'\.sysinfo'))
    async def sysinfo_handler(event):
        start = datetime.now()
        await event.edit("🖥️ **System Information**\n`Collecting data...`")
        end = datetime.now()
        response_time = (end - start).microseconds / 1000
        
        # System stats
        import psutil
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        
        await event.edit(
            f"🖥️ **System Information**\n\n"
            f"⏱️ **Response Time:** `{response_time}ms`\n"
            f"🧠 **CPU Usage:** `{cpu_usage}%`\n"
            f"💾 **Memory Usage:** `{mem_usage}%`\n"
            f"🌐 **Platform:** `Fly.io`"
        )
