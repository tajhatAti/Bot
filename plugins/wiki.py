import urllib.request
import json
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]wiki (.*)'))
    async def wiki_search(e):
        query = e.pattern_match.group(1).replace(" ", "%20")
        m = await e.edit("`Searching Wikipedia...`") if getattr(e, 'out', False) else await e.reply("`Searching...`")
        
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
                
            title = data.get("title", "Unknown")
            desc = data.get("extract", "No description found.")
            link = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            
            wiki_text = f"🏛 **{title}**\n\n📖 `{desc}`\n\n🔗 [Read More on Wikipedia]({link})"
            await m.edit(wiki_text, link_preview=False)
            
        except Exception:
            await m.edit("❌ `Topic not found or network error.`")