import urllib.request
import json
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]git (.*)'))
    async def github_info(e):
        username = e.pattern_match.group(1).strip()
        m = await e.edit("`Fetching GitHub profile...`") if getattr(e, 'out', False) else await e.reply("`Fetching...`")
        
        try:
            url = f"https://api.github.com/users/{username}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
            
            info = (f"🐙 **GitHub Profile:** [{data['login']}]({data['html_url']})\n\n"
                    f"👤 **Name:** {data.get('name', 'N/A')}\n"
                    f"📝 **Bio:** {data.get('bio', 'N/A')}\n"
                    f"🏢 **Company:** {data.get('company', 'N/A')}\n"
                    f"📍 **Location:** {data.get('location', 'N/A')}\n"
                    f"📦 **Public Repos:** {data['public_repos']}\n"
                    f"👥 **Followers:** {data['followers']} | **Following:** {data['following']}")
            
            if data.get('avatar_url'):
                await client.send_file(e.chat_id, data['avatar_url'], caption=info)
                await m.delete()
            else:
                await m.edit(info)
        except Exception as ex:
            await m.edit(f"❌ `User not found or Error: {ex}`")