from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import re

def register(client):
    BANNED_RIGHTS = ChatBannedRights(
        until_date=None,
        view_messages=True,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True
    )

    @client.on(events.NewMessage(pattern=r'(?i)^(\.\/)!?ban\s[@!]?(\w*)$'))
    async def ban_user(e):
        if not getattr(e, 'out', False): return
        if not e.is_group:
            return await e.edit("`This command is for groups only.`")
            
        reply_msg = await e.get_reply_message()
        if not reply_msg:
            return await e.edit("`Reply to a user to ban them.`")

        prefix = re.search(r'(?i)^(\.\/)!?', e.text).group(0)
        bot_username = re.search(r'(?i)^(\.\/)!?(\w*)', e.text).group(2)

        await e.reply(f"{prefix}{bot_username} **Processing ban request...**")

        user = await client.get_entity(reply_msg.sender_id)
        try:
            await client(EditBannedRequest(e.chat_id, user.id, BANNED_RIGHTS))
            await e.client.edit_message(e.chat_id, e.reply_to_msg_id, f"{prefix}{bot_username} 🔨 **Banned!**\n**User:** [{user.first_name}](tg://user?id={user.id})\n**Chat:** `{e.chat.title}`")
        except Exception as ex:
            await e.client.edit_message(e.chat_id, e.reply_to_msg_id, f"{prefix}{bot_username} ❌ **Error:** `{str(ex)}`")

        await e.client.delete_messages(e.chat.id, [e.reply_to_msg_id, e.reply_to_msg_id + 1])
        await asyncio.sleep(6)