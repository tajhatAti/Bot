import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]hack$'))
    async def hack_anim(e):
        if not getattr(e, 'out', False): return
        
        animation_frames = [
            "🟢 `Initializing hacking tools...`",
            "🟡 `Bypassing Telegram security protocols...`",
            "🔴 `Extracting target's IP address... [████░░░░░░] 40%`",
            "🔴 `Decrypting chat database... [███████░░░] 70%`",
            "🔵 `Uploading data to local server... [██████████] 100%`",
            "✅ **System breached successfully!**\n\n🎯 **Target Data:**\nIP: `192.168.1.104`\nDevice: `Android 14`"
        ]
        
        m = await e.edit(animation_frames[0])
        for frame in animation_frames[1:]:
            await asyncio.sleep(0.8) # Smooth delay
            await m.edit(frame)

    @client.on(events.NewMessage(pattern=r'(?i)^[.!]magic$'))
    async def magic_anim(e):
        if not getattr(e, 'out', False): return
        
        frames = ["(>‿◠)✌", "ᕙ(`▿´)ᕗ", "༼ つ ◕_◕ ༽つ", "(▀Ĺ̯▀ )", "✅ **Magic Loaded!**"]
        m = await e.edit(frames[0])
        for frame in frames[1:]:
            await asyncio.sleep(0.5)
            await m.edit(frame)