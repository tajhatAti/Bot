import time
from telethon import events

def register(client, uid):
    
    # ইনবক্স এবং গ্রুপ—সব জায়গায় এই কমান্ড ধরবে
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]ping$'))
    async def ping_cmd(e):
        start = time.time()
        
        # যদি কমান্ডটি তুই নিজে দিস, তাহলে মেসেজ এডিট হবে
        if getattr(e, 'sender_id', None) == uid:
            m = await e.edit("`Pinging...`")
        # আর যদি অন্য কেউ (ইনবক্স বা গ্রুপে) দেয়, তাহলে রিপ্লাই করবে
        else:
            m = await e.reply("`Pinging...`")
            
        latency = int((time.time() - start) * 1000)
        
        # ফাইনাল রেসপন্স
        await m.edit(f"🏓 **Pong!** 🫵\n🧭 **Latency:** `{latency} ms`")