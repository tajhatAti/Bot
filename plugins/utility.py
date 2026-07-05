from telethon import events, utils
from telethon.errors import ChatAdminRequiredError
from asyncio import sleep

def register(client):
    prefixes = ['.', '/', '!']
    bot_username = client.me.username

    @client.on(events.NewMessage(
        pattern=f"(?i)^({'|'.join(prefixes)})([^\s]+)"))
    async def get_id(e):
        cmd = e.pattern_match.group(1)
        bot_cmd = f"{cmd}{bot_username}" if cmd != cmd.lower() else cmd

        sender = e.sender
        chat = e.chat
        replied = await e.get_reply_message()

        raw = f"👤 **Your ID:** `{sender.id}`\n💬 **Chat ID:** `{chat.id}`"

        if cmd == '.id' and e.is_private:
            raw += f"\n📊 **Your Phone:** {sender.phone or 'Private'}\n📝 **Your Name:** {sender.first_name or 'Unknown'}"

        if replied:
            raw += f"\n🎯 **Replied User ID:** `{replied.sender.id}`"

        if cmd != '.id' and replied:
            try:
                await client.forward_messages(
                    chat,
                    replied,
                    bot_username)
            except ChatAdminRequiredError:
                pass

        if getattr(e, 'out', False):
            await e.edit(raw)
        else:
            await e.reply(raw)

        await sleep(6)
        if not e.out and e.is_group:
            await e.delete()

    @client.on(events.NewMessage(pattern=r'(?i)^(\.|\!|#)(purge)$'))
    async def purge_msgs(e):
        sender = e.sender
        chat = e.chat
        replied = await e.get_reply_message()

        if not getattr(e, 'out', False): return

        if e.is_group:
            if not chat.admin_rights.delete_messages:
                return await e.edit("I don't have the required permissions!")

        if not replied:
            if getattr(e, 'out', False):
                await e.edit("Reply to a message to start purging!")
            else:
                await e.reply("Reply to a message to start purging!")
            return

        await e.edit("`Purging messages...`")
        messages = []
        async for msg in client.iter_messages(chat.id, min_id=replied.id - 1):
            messages.append(msg)
            if len(messages) >= 100:
                await client.delete_messages(chat.id, messages)
                messages.clear()

        if messages:
            await client.delete_messages(chat.id, messages)

        msg = await e.respond("🧹 **Purge Complete!**")
        await sleep(6)
        if not e.out:
            await msg.delete()