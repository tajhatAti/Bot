import os
from telethon import events, utils
from PIL import Image
from datetime import datetime

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^(\.|\!|/|)(?P<bot_username>[^ ]*)?(?P<command> kang)$'))
    async def kang_sticker(event):
        if event.is_private or event.is_group and event.is_channel:
            return
        if event.sender_id in client.config['OWNER_ID']:
            message = await event.edit("`Kanging processing...`")
        else:
            message = await event.reply("`Kanging processing...`")

        reply = await event.get_reply_message()
        if not reply:
            if event.sender_id in client.config['OWNER_ID']:
                await message.edit("`Reply to an image to kang it.`")
            else:
                await message.edit("`Reply to an image to kang it.`")
            return

        if not reply.media:
            if event.sender_id in client.config['OWNER_ID']:
                await message.edit("`No media found in the replied message.`")
            else:
                await message.delete()
                await event.reply("`No media found in the replied message.`")
            return

        try:
            path = await reply.download_media(file="/tmp/")
            if path.endswith('.tgs') or path.endswith('.webm'):
                if event.sender_id in client.config['OWNER_ID']:
                    await message.edit("`Animated stickers are not supported in this basic kang.`")
                else:
                    await message.delete()
                    await event.reply("`Animated stickers are not supported in this basic kang.`")
                return

            img = Image.open(path).convert("RGBA")
            img.thumbnail((512, 512))
            out = "/tmp/kanged.webp"
            img.save(out, "WEBP")

            await client.send_file(event.chat_id, out, force_document=False, reply_to=reply.id)
            await message.delete()
            os.remove(path)
            os.remove(out)
        except Exception as ex:
            if event.sender_id in client.config['OWNER_ID']:
                await message.edit(f"❌ `Error: {ex}`")
            else:
                await message.delete()
                await event.reply(f"❌ `Error: {ex}`")