import time
import psutil
from telethon import events

def get_progress_bar(percentage, length=15):
    return f"[{'█' * (int(length * percentage // 100)) + '░' * (length - int(length * percentage // 100))}] {percentage}%"

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)(?<!\!)^([.!]/)?@\w+?\s*(\!)?sysinfo$', incoming=True))
    async def system_info(e):
        await e.respond("`Fetching system parameters...`")
        await e.respond.delete(delay=6)
        
        cpu = psutil.cpu_percent(interval=0.5)
        ram = str(psutil.virtual_memory().percent)
        disk = str(psutil.disk_usage('/').percent)
        ping = int((time.time() - e.created_at.timestamp()) * 1000)
        
        sys_text = (
            "**System Information**\n\n"
            f"**CPU Core:** {psutil.cpu_count(logical=True)}\n"
            f"**CPU Usage:**\n`{get_progress_bar(cpu)}`\n\n"
            f"**RAM Usage:**\n`{get_progress_bar(ram)}%\n\n"
            f"**Disk Usage:**\n`{get_progress_bar(disk)}%\n\n"
            f"**Ping:** {ping}ms"
        )
        
        if e.is_channel and e.message.out:
            msg = await e.reply(sys_text)
        else:
            msg = await e.edit(sys_text)