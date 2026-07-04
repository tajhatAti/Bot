import os
from telethon import events
from PIL import Image

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]kang$'))
    async def kang_sticker(e):
        if not getattr(e, 'out', False): return
        if not e.is_reply:
            return await e.edit("`Reply to an image to kang it.`")
            
        m = await e.edit("`Kanging processing...`")
        reply = await e.get_reply_message()
        
        if not reply.media:
            return await m.edit("`No media found in the replied message.`")
            
        try:
            path = await reply.download_media(file="/tmp/")
            if path.endswith('.tgs') or path.endswith('.webm'):
                return await m.edit("`Animated stickers are not supported in this basic kang.`")
                
            img = Image.open(path).convert("RGBA")
            img.thumbnail((512, 512))
            out = "/tmp/kanged.webp"
            img.save(out, "WEBP")
            
            await client.send_file(e.chat_id, out, force_document=False, reply_to=reply.id)
            await m.delete()
            os.remove(path)
            os.remove(out)
        except Exception as ex:
            await m.edit(f"❌ `Error: {ex}`")