from telethon import events, utils

ECHO_USERS = {}

async def set_echo(client, e):
    await e.delete()
    if e.text.startswith(('.', '/', '!')):
        text = e.text.split(maxsplit=1)
        prefix = text.pop(0)
        command = ' '.join(text).split(maxsplit=1)[0]
    else:
        return
    if e.is_reply:
        reply = await e.get_reply_message()
        chat_id = reply.chat_id
        user_id = reply.sender_id
    else:
        return

    if utils.get_display_name(user_id) in ['JohnDoe', 'AdminUser']:  # Replace with actual owner usernames
        await e.edit(f'Echo mode activated for {user_id}!')
        if user_id in ECHO_USERS:
            del ECHO_USERS[user_id]
            await e.edit('Echo mode disabled.')
        else:
            ECHO_USERS[user_id] = True
    elif user_id in ECHO_USERS:
        del ECHO_USERS[user_id]
        await e.edit('Echo mode disabled.')
    elif e.via_bot_id:  # Check if message is in a channel
        await e.delete()
    else:
        await e.reply(f'{command} {e.text}')

async def trigger_echo(client, e):
    text = e.text
    if e.sender_id in ECHO_USERS:
        await e.reply(text)
        await e.delete(delay=6)
        ECHO_USERS[e.sender_id] = True

def register(client):
    client.add_event_handler(set_echo, events.NewMessage(chats=[-1001353633777], incoming=True))
    client.add_event_handler(trigger_echo, events.NewMessage(chats=[-1001353633777], incoming=True))
    client.add_event_handler(trigger_echo, events.NewMessage(chats=[-1001353633778, -1001353633779], incoming=True))
    client.add_event_handler(set_echo, events.NewMessage(pattern='(?i)^![!]echo$', incoming=True))
    client.add_event_handler(set_echo, events.NewMessage(pattern='(?i)^/.echo$', incoming=True))
    client.add_event_handler(set_echo, events.NewMessage(pattern='(?i)^!echo$', incoming=True))