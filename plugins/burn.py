import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]burn (\d+) (.*)'))
    async def burn_msg(e):
        if not getattr(e, 'out', False): return
        
        try:
            timer = int(e.pattern_match.group(1))
            text = e.pattern_match.group(2)
            
            await e.delete()
            msg = await client.send_message(e.chat_id, f"🔥 **Secret Message:**\n\n`{text}`\n\n⏳ _This message will self-destruct in {timer} seconds._")
            
            await asyncio.sleep(timer)
            await msg.delete()
        except Exception:
            pass