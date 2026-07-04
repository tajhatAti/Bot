from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]alive$'))
    async def alive_cmd(e):
        text = "**⚡ Userbot is perfectly running on Modular Architecture!**"
        
        if getattr(e, 'out', False):
            await e.edit(text)
        else:
            await e.reply(text)