import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]tagall(?: |$)(.*)'))
    async def tagall_cmd(e):
        if not getattr(e, 'out', False): return
        if not e.is_group: 
            return await e.edit("`This command is only for groups!`")
            
        msg = e.pattern_match.group(1) or "Wake up everyone!"
        await e.delete()
        
        users = []
        async for user in client.iter_participants(e.chat_id):
            if not user.bot:
                users.append(f"[{user.first_name}](tg://user?id={user.id})")
                
        chunk_size = 5
        for i in range(0, len(users), chunk_size):
            text = f"📢 **{msg}**\n\n" + "\n".join(users[i:i+chunk_size])
            try:
                await client.send_message(e.chat_id, text)
                await asyncio.sleep(2)
            except Exception:
                break