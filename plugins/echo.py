from telethon import events

# গ্লোবাল ডিকশনারি কোন কোন ইউজারের মেসেজ ইকো হবে তা ট্র্যাক রাখতে
ECHO_USERS = {}

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]echo$'))
    async def set_echo(e):
        if not getattr(e, 'out', False): return
        if not e.is_reply:
            return await e.edit("`Reply to a user to activate echo mode.`")
            
        reply = await e.get_reply_message()
        user_id = reply.sender_id
        
        if user_id in ECHO_USERS:
            del ECHO_USERS[user_id]
            await e.edit("📴 **Echo mode disabled for this user.**")
        else:
            ECHO_USERS[user_id] = True
            await e.edit("💡 **Echo mode enabled! I will copy everything they say.**")

    @client.on(events.NewMessage(incoming=True))
    async def trigger_echo(e):
        if e.sender_id in ECHO_USERS:
            if e.text:
                await e.reply(e.text)