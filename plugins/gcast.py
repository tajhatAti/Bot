import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]gcast (.*)'))
    async def gcast_cmd(e):
        if not getattr(e, 'out', False): return
        
        text = e.pattern_match.group(1)
        m = await e.edit("`Broadcasting message...`")
        count = 0
        
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                try:
                    await client.send_message(dialog.id, text)
                    count += 1
                    await asyncio.sleep(0.5) # FloodWait এড়ানোর জন্য ডিলে
                except Exception:
                    pass
                    
        await m.edit(f"✅ **Broadcast complete in {count} chats!**")