from telethon import events, utils

def register(client):
    @client.on(events.NewMessage(
        pattern=r'(?i)((?<!\.)\.(?!\.)|(?<!\\/)\/(?!\/)|(?<!\!)!\(?!\.)\s*?)\s*?(?:\s*([^\s]+))?\s*:?\s*alive$'
    ))
    async def alive_cmd(e):
        text = "**⚡ Userbot is perfectly running on Modular Architecture!**"
        sender = await e.get_sender()
        client_id = utils.get_peer_id(sender)
        bot_id = (await client.get_me()).id
        
        if client_id == bot_id:
            await e.edit(text)
        else:
            await e.reply(text)
        
        await asyncio.sleep(6)
        await e.delete()