# plugins/core.py - Essential utilities
from datetime import datetime
from telethon import events
import psutil, os

async def register_handlers(client, bot):
    # System info command
    @client.on(events.NewMessage(pattern=r'\.sys'))
    async def sysinfo_handler(event):
        start = datetime.now()
        message = await event.reply("📊 **Collecting system data...**")
        end = datetime.now()
        resp_time = (end - start).microseconds / 1000
        
        # System stats
        cpu_usage = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        await message.edit(
            f"🖥️ **Prince-X System Report**\n\n"
            f"⏱️ **Response Time:** `{resp_time:.2f}ms`\n"
            f"🧠 **CPU Usage:** `{cpu_usage}%`\n"
            f"💾 **Memory:** `{mem.used/1024/1024:.1f}MB/{mem.total/1024/1024:.1f}MB`\n"
            f"💽 **Disk:** `{disk.used/1024/1024:.1f}MB/{disk.total/1024/1024:.1f}MB`\n"
            f"🐍 **Python:** `{sys.version.split()[0]}`\n"
            f"⚡ **Uptime:** `{datetime.now() - start_time}`"
        )
    
    # Server restart command
    @client.on(events.NewMessage(pattern=r'\.restart'))
    async def restart_handler(event):
        await event.reply("🔄 **Restarting Prince-X Userbot...**")
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    # Ping command
    @client.on(events.NewMessage(pattern=r'\.ping'))
    async def ping_handler(event):
        start = datetime.now()
        message = await event.reply("🏓")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await message.edit(f"🏓 **Pong!**\n`{ms:.2f}ms`")

# Global start time for uptime calculation
start_time = datetime.now()
