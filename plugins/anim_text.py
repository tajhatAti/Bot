import asyncio
from telethon import events
from telethon.errors import FloodWaitError

def register(client):
    prefixes = ['.', '/', '!']
    bot_username = client.get_me().username
    
    @client.on(events.NewMessage(pattern=f'(?i)^({"".join(prefixes)}{bot_username}?:?)?.*(hack|magic)$'))
    async def animation(e):
        if not getattr(e, 'out', False): return
        sender = await e.get_sender()
        if sender.id == client.get_me().id:
            msg = await e.edit('')
        else:
            reply = await e.reply('')
            await asyncio.sleep(2)
            msg = reply
        
        if 'hack' in e.text:
            animation_frames = [
                "🟢 `Initializing hacking tools...`",
                "🟡 `Bypassing Telegram security protocols...`",
                "🔴 `Extracting target's IP address... [████░░░░░░] 40%`",
                "🔴 `Decrypting chat database... [███████░░░] 70%`",
                "🔵 `Uploading data to local server... [██████████] 100%`",
                "✅ **System breached successfully!**\n\n🎯 **Target Data:**\nIP: `192.168.1.104`\nDevice: `Android 14`"
            ]
            for frame in animation_frames:
                try:
                    await msg.edit(frame)
                    await asyncio.sleep(1)
                except FloodWaitError:
                    await asyncio.sleep(10)
                    continue
        elif 'magic' in e.text:
            frames = ["(>‿◠)✌", "ᕙ(`▿´)ᕗ", "༼ つ ◕_◕ ༽つ", "(▀Ĺ̯▀ )", "✅ **Magic Loaded!**"]
            for frame in frames:
                try:
                    await msg.edit(frame)
                    await asyncio.sleep(1)
                except FloodWaitError:
                    await asyncio.sleep(10)
                    continue
        await asyncio.sleep(6)
        await msg.delete()