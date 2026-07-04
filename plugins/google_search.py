import urllib.request
from bs4 import BeautifulSoup
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]google (.*)'))
    async def google_search(e):
        query = e.pattern_match.group(1).strip()
        m = await e.edit("`Searching Google...`") if getattr(e, 'out', False) else await e.reply("`Searching...`")
        
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            
            with urllib.request.urlopen(req, timeout=10) as res:
                soup = BeautifulSoup(res.read(), 'html.parser')
                
            results = []
            for g in soup.find_all('div', class_='tF23um'): # গুগলের সার্চ রেজাল্ট ক্লাসের ডিভ
                anchor = g.find('a')
                title = g.find('h3')
                if anchor and title:
                    results.append(f"🔗 [{title.text}]({anchor['href']})")
                if len(results) >= 3:
                    break
                    
            if results:
                output = f"🔍 **Google Search Results for:** `{query}`\n\n" + "\n\n".join(results)
                await m.edit(output, link_preview=False)
            else:
                await m.edit("❌ `No results found.`")
        except Exception as ex:
            await m.edit(f"❌ `Error: {ex}`")