import urllib.request
import json
import asyncio
from telethon import events, helpers

def register(client, uid):
    @client.on(events.NewMessage(pattern=r'(?i)(?:\.(?:/|!))\s*(?:@?(?P<username>[^ ]+|))?\s*(?:\.(?:/|!))? (.*)'))
    async def generate_carbon(event):
        username = event.pattern_match.group('username')
        if username:
            username = f'@{username}'
        
        code = event.pattern_match.group(1).strip()
        if not code and event.is_reply:
            reply_msg = await event.get_reply_message()
            code = reply_msg.text
            
        if not code:
            return await (event.edit("`Provide code text or reply to a text message.`") if event.sender_id == int(client.me.id) else event.reply("`Provide code text or reply to a text message.`"))
        
        m = await (event.edit("`Generating Carbon image...`") if event.sender_id == int(client.me.id) else event.reply("`Generating...`"))
        
        try:
            url = "https://rayso-api.vercel.app/api"
            data = json.dumps({"code": code, "theme": "breeze", "language": "python"}).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=15) as res:
                img_data = res.read()
                
            out_file = "/tmp/carbon.png"
            with open(out_file, "wb") as f:
                f.write(img_data)
                
            await client.send_file(event.chat_id, out_file, caption=f"💻 **Code snippet beautified via ****Ray.so**")
            await asyncio.sleep(6)
            await (event.delete() if event.sender_id == int(client.me.id) else (m.delete()))
        except Exception as ex:
            await (event.edit(f"❌ `Failed to generate image. Error: {ex}`") if event.sender_id == int(client.me.id) else (m.edit(f"❌ `Failed to generate image. Error: {ex}`")))