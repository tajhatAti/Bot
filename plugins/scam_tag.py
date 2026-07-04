from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]scam (.*)'))
    async def fake_scam(e):
        if not getattr(e, 'out', False): return
        text = e.pattern_match.group(1)
        
        # টেলিগ্রামের আসল স্ক্যাম ট্যাগের মতো একটি টেক্সট ফরম্যাট তৈরি করবে
        scam_text = f"⚠️ **⚠️ WARNING: This user is flagged as a** `[ SCAM ]` **by community reports.**\n\n💬 **Message:** {text}"
        await e.edit(scam_text)