import asyncio
from telethon import events

def register(client):
    async def fake_action(e):
        if sender := getattr(e, 'sender_id', None) == client.uid:
            await e.edit(message="Action applied...", delete_in=6)
        else:
            await e.reply(message="Action applied...", reply_to=e.id, delete_in=6)
        
        action_map = {
            'typing': 'typing',
            'video': 'record-video',
            'audio': 'record-audio',
            'photo': 'photo'
        }
        
        action = e.pattern_match.group(1).lower()
        try:
            # 6 সেকেন্ডের জন্য ফেইক অ্যাকশন দেখাবে
            await client.action(e.chat_id, action_map[action])
            await asyncio.sleep(6)
        except Exception:
            pass
    client.on(events.NewMessage(pattern=r'(?i)^(?:\.|/|!)?\s*@\w+?.\s?action (typing|video|audio|photo)', incoming=True)) \
        .add_handler(fake_action)