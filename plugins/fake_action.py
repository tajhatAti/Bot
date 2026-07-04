import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]action (typing|video|audio|photo)$'))
    async def fake_action(e):
        if not getattr(e, 'out', False): return
        
        action = e.pattern_match.group(1).lower()
        await e.delete()
        
        action_map = {
            'typing': 'typing',
            'video': 'record-video',
            'audio': 'record-audio',
            'photo': 'photo'
        }
        
        try:
            # ১০ সেকেন্ডের জন্য ফেইক অ্যাকশন দেখাবে
            async with client.action(e.chat_id, action_map[action]):
                await asyncio.sleep(10)
        except Exception:
            pass