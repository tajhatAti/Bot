from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

def register(client):
    # Ban Rights
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

    @client.on(events.NewMessage(pattern=r'(?i)^[.!]ban$'))
    async def ban_user(e):
        if not getattr(e, 'out', False): return
        if not e.is_group:
            return await e.edit("`This command is for groups only.`")
            
        reply_msg = await e.get_reply_message()
        if not reply_msg:
            return await e.edit("`Reply to a user to ban them.`")
            
        await e.edit("`Processing ban request...`")
        try:
            user = await client.get_entity(reply_msg.sender_id)
            await client(EditBannedRequest(e.chat_id, user.id, BANNED_RIGHTS))
            await e.edit(f"🔨 **Banned!**\n**User:** [{user.first_name}](tg://user?id={user.id})\n**Chat:** `{e.chat.title}`")
        except Exception as ex:
            await e.edit(f"❌ **Error:** `{str(ex)}`")