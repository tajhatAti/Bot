from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]id$'))
    async def get_id(e):
        reply = await e.get_reply_message()
        out = f"👤 **Your ID:** `{e.sender_id}`\n💬 **Chat ID:** `{e.chat_id}`"
        
        if reply:
            out += f"\n🎯 **Replied User ID:** `{reply.sender_id}`"
            if reply.forward:
                out += f"\n📤 **Forwarded From ID:** `{reply.forward.sender_id or reply.forward.chat_id}`"
                
        if getattr(e, 'out', False):
            await e.edit(out)
        else:
            await e.reply(out)

    @client.on(events.NewMessage(pattern=r'(?i)^[.!]purge$'))
    async def purge_msgs(e):
        if not getattr(e, 'out', False): return
        reply = await e.get_reply_message()
        if not reply:
            return await e.edit("`Reply to a message to start purging.`")
            
        await e.edit("`Purging messages...`")
        messages = []
        async for msg in client.iter_messages(e.chat_id, min_id=reply.id - 1):
            messages.append(msg)
            if len(messages) >= 100:
                await client.delete_messages(e.chat_id, messages)
                messages.clear()
        
        if messages:
            await client.delete_messages(e.chat_id, messages)
            
        msg = await e.respond("🧹 **Purge Complete!**")
        await __import__('asyncio').sleep(3)
        await msg.delete()