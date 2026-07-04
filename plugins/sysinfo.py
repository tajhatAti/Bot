import time
import psutil
from telethon import events

def get_progress_bar(percentage, length=15):
    filled = int(length * percentage // 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {percentage}%"

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]sysinfo$'))
    async def system_info(e):
        start_time = time.time()
        m = await e.edit("`Fetching system parameters...`") if getattr(e, 'out', False) else await e.reply("`Fetching...`")
        
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        ping = int((time.time() - start_time) * 1000)
        
        sys_text = (
            "💻 **System Information**\n\n"
            f"**CPU Core:** {psutil.cpu_count(logical=True)}\n"
            f"**CPU Usage:**\n`{get_progress_bar(cpu)}`\n\n"
            f"**RAM Usage:**\n`{get_progress_bar(ram)}`\n\n"
            f"**Disk Usage:**\n`{get_progress_bar(disk)}`\n\n"
            f"⚡ **Ping:** `{ping}ms`"
        )
        
        await m.edit(sys_text)