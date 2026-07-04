from telethon import events
import time

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]ping$'))
    async def ping_cmd(e):
        start = time.time()
        
        # নিজের মেসেজ হলে এডিট করবে, অন্যের হলে রিপ্লাই দেবে
        if getattr(e, 'out', False):
            m = await e.edit("`Pinging...`")
        else:
            m = await e.reply("`Pinging...`")
            
        latency = int((time.time() - start) * 1000)
        await m.edit(f"🏓 **Pong!**\nLatency: `{latency}ms`")
