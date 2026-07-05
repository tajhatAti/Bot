import urllib.request
import json
from telethon import events, utils
from datetime import datetime

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]/?(?:@)?([a-zA-Z0-9_]+)?\s*wiki (\S*)'))
    async def wiki_search(e):
        sender = await e.client.get_entity(e.sender_id)
        if e.is_private and e.sender_id == await client.get_me():
            m = await e.edit("`Searching Wikipedia...`")
        else:
            m = await e.reply(f"`Searching for '{e.pattern_match.group(2)}'...`")

        try:
            query = e.pattern_match.group(2).replace(" ", "%20")
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
                
            title = data.get("title", "Unknown")
            extract = data.get("extract", "No description found.")
            page = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            
            wiki_text = f"🏛 **{title}**\n\n📖 `{extract}`\n\n🔗 [Read More on Wikipedia]({page})"
            await m.edit(wiki_text, link_preview=False, delete_after=datetime.utcnow() + datetime.timedelta(seconds=6))
            
        except Exception:
            await m.edit("❌ `Topic not found or network error.`")