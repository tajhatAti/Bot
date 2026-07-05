import os
import time
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from telethon import events

def register(client):
    @client.on(events.NewMessage(
        incoming=True,
        pattern=r'(?i)(?:\.|\/|!)?(?:\s*([\w.-]+)\s*)?(?:(?:\.|\/|!|) )(.*)'
    ))
    async def google_search(event):
        prefix = event.pattern_match.group(1) if event.pattern_match.group(1) else None
        username = prefix.split()[0] if prefix else None
        query = ' '.join(event.pattern_match.group(2,).replace(prefix, '').replace(username, '').split())

        if hasattr(event.message.reply_to_msg, 'sender'):
            msg = await event.message.reply_to_msg.edit(f"🔍 **Google Search Results for:** `[{prefix}{username}]{query}`")
        else:
            msg = await event.reply(f"🔍 **Google Search Results for:** `[{prefix}{username}]{query}`")

        try:
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            from urllib.request import Request, urlopen
            req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urlopen(req, timeout=10) as res:
                soup = BeautifulSoup(res.read(), 'html.parser')
            results = []
            for g in soup.find_all('div', class_='tF23um'): 
                anchor = g.find('a')
                title = g.find('h3')
                if anchor and title:
                    results.append(f"🔗 [{title.text}]({anchor['href']})")
                if len(results) >= 3:
                    break
            if results:
                output = "\n\n".join(results)
                await msg.edit(output, link_preview=False)
            else:
                await msg.edit("❌ `No results found.`")
        except Exception as ex:
            await msg.edit(f"❌ `Error: {ex}`")
        finally:
            time.sleep(6)
            await msg.delete()