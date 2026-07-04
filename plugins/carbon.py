import urllib.request
import json
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]carbon (.*)'))
    async def generate_carbon(e):
        code = e.pattern_match.group(1).strip()
        if not code and e.is_reply:
            reply_msg = await e.get_reply_message()
            code = reply_msg.text
            
        if not code:
            return await e.edit("`Provide code text or reply to a text message.`")
            
        m = await e.edit("`Generating Carbon image...`") if getattr(e, 'out', False) else await e.reply("`Generating...`")
        
        try:
            # Ray.so API ব্যবহার করে কার্বন ইমেজ জেনারেট করা
            url = "https://rayso-api.vercel.app/api"
            data = json.dumps({"code": code, "theme": "breeze", "language": "python"}).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=15) as res:
                img_data = res.read()
                
            out_file = "/tmp/carbon.png"
            with open(out_file, "wb") as f:
                f.write(img_data)
                
            await client.send_file(e.chat_id, out_file, caption="💻 **Code snippet beautified via ****Ray.so**")
            await m.delete()
        except Exception as ex:
            await m.edit(f"❌ `Failed to generate image. Error: {ex}`")