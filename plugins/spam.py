import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]spam (\d+) (.*)'))
    async def spam_cmd(e):
        if not getattr(e, 'out', False): return
        try:
            count = int(e.pattern_match.group(1))
            text = e.pattern_match.group(2)
            await e.delete()
            for _ in range(count):
                await client.send_message(e.chat_id, text)
                await asyncio.sleep(0.2)
        except Exception as ex:
            await client.send_message(e.chat_id, f"❌ `Error: {ex}`")

    @client.on(events.NewMessage(pattern=r'(?i)^[.!]dspam (\d+) (\d+) (.*)'))
    async def dspam_cmd(e):
        if not getattr(e, 'out', False): return
        try:
            delay = float(e.pattern_match.group(1))
            count = int(e.pattern_match.group(2))
            text = e.pattern_match.group(3)
            await e.delete()
            for _ in range(count):
                await client.send_message(e.chat_id, text)
                await asyncio.sleep(delay)
        except Exception as ex:
            await client.send_message(e.chat_id, f"❌ `Error: {ex}`")