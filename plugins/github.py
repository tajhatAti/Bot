import telethon
import json
import time
from telethon.errors import ChatSendInlineForbiddenError, ChatSendMediaForbiddenError
from telethon.tl import functions
from urllib.request import urlopen, Request
from telethon.utils import get_display_name

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^((?:\.{1}|\!|\/)\s?[\w\.]{1,32})?\s?[\w\.]{1,32}\s*$'))
    async def github_info(event):
        try:
            message = event.message
            sender = await event.get_sender()
            chat = event.chat
            if sender.id == await client.get_me().id:
                m = await event.edit("`Fetching GitHub profile...`")
            else:
                m = await event.reply("`Fetching...`")

            username = event.pattern_match.group(2).strip()
            url = f"https://api.github.com/users/{username}"
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode("utf-8"))
            info = (f"🐙 **GitHub Profile:** [{data['login']}]({data['html_url']})\n\n"
                    f"👤 **Name:** {data.get('name', 'N/A')}\n"
                    f"📝 **Bio:** {data.get('bio', 'N/A')}\n"
                    f"🏢 **Company:** {data.get('company', 'N/A')}\n"
                    f"📍 **Location:** {data.get('location', 'N/A')}\n"
                    f"📦 **Public Repos:** {data['public_repos']}\n"
                    f"👥 **Followers:** {data['followers']} | **Following:** {data['following']}")
            if data.get('avatar_url'):
                try:
                    await client.send_file(chat.id, data['avatar_url'], caption=info)
                except ChatSendMediaForbiddenError:
                    await m.edit(info)
                    await client(functions.messages.DeleteHistoryRequest(peer=chat.id, max_id=0, revoke=True))
                    await m.delete()
                else:
                    await m.delete()
                    await client(functions.messages.DeleteHistoryRequest(peer=chat.id, max_id=0, revoke=True))
            else:
                await m.edit(info)
                await time.sleep(6)
                await m.delete()
                try:
                    await client(functions.messages.DeleteHistoryRequest(peer=chat.id, max_id=0, revoke=True))
                except telethon.errors.BadRequestError:
                    pass
        except Exception as ex:
            await m.edit(f"❌ `User not found or Error: {ex}`")