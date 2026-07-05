import asyncio
from telethon import events, functions, utils
from telethon import __version__

def register(client):
    client.prefixes = ['.','/', '!']

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        for prefix in client.prefixes:
            if event.raw_text.startswith(prefix) and event.raw_text.split(prefix)[1].split(' ')[0] != event.message.sender.username:
                if event.is_sender_banned:
                    await event.edit("You are banned!")
                elif event.is_sender_muted:
                    await event.edit("You are muted!")

                message_id = event.message.id
                command = event.pattern_match.group(0).replace(prefix, '').split(' ')[0]
                args = event.pattern_match.group(0).replace(prefix, '').split(' ')[1:]
                bot_username = client.username
                
                if command == 'gcast':
                    if event.is_channel or event.is_group:
                        m = await event.reply("`Broadcasting message...`")
                        count = 0
                        
                        async for dialog in client.iter_dialogs():
                            if dialog.is_group or dialog.is_channel:
                                try:
                                    await client.send_message(dialog.id, ' '.join([bot_username, ' ', message_id, ' ', command, ' ', ' '.join(args)]))
                                    m_reply = await client.send_message(dialog.id, command)
                                    await utils.wait(event.client, m_reply.delete, timeout=6)
                                    count += 1
                                    await asyncio.sleep(0.5)
                                except Exception:
                                    pass
                        await m.edit(f"✅ **Broadcast complete in {count} chats!**")
                        await event.delete()
                    else:
                        await event.reply("Only in groups and channels.")
                else:
                    await event.reply("Unknown command.")
                
                await asyncio.sleep(6)
                await utils.wait(event.client, m.edit, new_text=f"✅ **Broadcast complete in 0 chats!**")
                await utils.wait(event.client, m.delete)
                await event.delete()