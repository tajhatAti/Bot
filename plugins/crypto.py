import urllib.request
import json
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]crypto(?: |$)(.*)'))
    async def crypto_price(e):
        coin = e.pattern_match.group(1).strip().lower()
        if not coin: 
            coin = "toncoin" # Default
            
        m = await e.edit("`Fetching market data...`") if getattr(e, 'out', False) else await e.reply("`Fetching...`")
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
                
            if coin in data:
                price = data[coin]['usd']
                await m.edit(f"🪙 **{coin.capitalize()} Live Price:**\n💵 `${price}`")
            else:
                await m.edit("❌ `Coin not found. Use full names like bitcoin, ethereum, the-open-network.`")
        except Exception as ex:
            await m.edit(f"❌ `Error: {ex}`")