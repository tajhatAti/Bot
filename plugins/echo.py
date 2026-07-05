import asyncio
from telethon import events

# গ্লোবাল ডিকশনারি কোন কোন ইউজারের মেসেজ ইকো হবে তা ট্র্যাক রাখতে
ECHO_USERS = {}

def register(client, uid):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!][\s]*[^\s]+$', re.IGNORECASE))
    async def set_echo(e):
        if not getattr(e, 'out', False): return
        if not e.is_reply:
            m = await e.reply('Reply to a user to activate echo mode.')
        else:
            reply = await e.get_reply_message()
            user_id = reply.sender_id
            
            if user_id in ECHO_USERS:
                del ECHO_USERS[user_id]
                m = await e.edit('📴 **Echo mode disabled for this user.**')
            else:
                ECHO_USERS[user_id] = True
                m = await e.edit('💡 **Echo mode enabled! I will copy everything they say.**')
        
        if getattr(e, 'sender_id', None) == uid:
            m = await e.edit(m)
        else:
            m = m

    @client.on(events.NewMessage(incoming=True))
    async def trigger_echo(e):
        if getattr(e, 'sender_id', None) == uid:
            m = await e.reply(e.text)
        else:
            m = await e.reply(e.text)
        
        if e.sender_id in ECHO_USERS and e.text:
            await asyncio.sleep(6)
            try:
                await m.delete()
            except:
                pass