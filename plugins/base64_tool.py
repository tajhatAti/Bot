import base64
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]encode (.*)'))
    async def encode_b64(e):
        text = e.pattern_match.group(1).strip()
        m = await e.edit("`Encoding...`") if getattr(e, 'out', False) else await e.reply("`Encoding...`")
        
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        encoded_str = encoded_bytes.decode('utf-8')
        await m.edit(f"🔒 **Encoded Message:**\n`{encoded_str}`")

    @client.on(events.NewMessage(pattern=r'(?i)^[.!]decode (.*)'))
    async def decode_b64(e):
        text = e.pattern_match.group(1).strip()
        m = await e.edit("`Decoding...`") if getattr(e, 'out', False) else await e.reply("`Decoding...`")
        
        try:
            decoded_bytes = base64.b64decode(text.encode('utf-8'))
            decoded_str = decoded_bytes.decode('utf-8')
            await m.edit(f"🔓 **Decoded Message:**\n`{decoded_str}`")
        except Exception:
            await m.edit("❌ `Invalid Base64 string!`")