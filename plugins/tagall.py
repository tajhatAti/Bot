import asyncio
from telethon import events

def register(client):
    prefixes = ('.', '/', '!')
    bot_username = '@yourbotusername'

    @client.on(events.NewMessage(pattern=(
        f'(?i)^({prefixes[0]}|{prefixes[1]}|{prefixes[2]})({bot_username}| )?(.*)')))
    async def tagall_cmd(e):
        if not e.is_group:
            return await e.reply("`This command is only for groups!`")
            
        if e.sender_id in [client.id, await client.get_me().id]:
            m = await e.edit(f'📢 {e.message.text}')
        else:
            m = await e.reply(f'📢 {e.message.text}')
        
        await asyncio.sleep(6)
        
        if e.sender_id in [client.id, await client.get_me().id]:
            await m.edit('')
            await m.delete()
        else:
            await m.delete()
                
        msg = e.pattern_match.group(3) or "Wake up everyone!"
        users = []
        async for user in client.iter_participants(e.chat_id):
            if not user.bot:
                users.append(f"[{user.first_name}](tg://user?id={user.id})")
                
        chunk_size = 5
        for i in range(0, len(users), chunk_size):
            text = f"**{msg}**\n\n" + "\n".join(users[i:i+chunk_size])
            try:
                await client.send_message(e.chat_id, text)
                await asyncio.sleep(2)
            except Exception:
                break