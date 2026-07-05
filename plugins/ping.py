import time
from telethon import events

# এই register ফাংশনটি থাকতেই হবে, না হলে main.py এটাকে লোড করতে পারবে না
def register(client, uid):
    
    # কমান্ডের প্যাটার্ন: .ping বা !ping
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]ping$'))
    async def ping_cmd(e):
        # এই লাইনটি নিশ্চিত করবে যে শুধু তুই (তোর কানেক্ট করা একাউন্ট) কমান্ড দিতে পারবি
        if getattr(e, 'sender_id', None) != uid: 
            return 
            
        start = time.time()
        m = await e.reply("`Pinging...`") if e.sender_id != uid else await e.edit("`Pinging...`")
        latency = int((time.time() - start) * 1000)
        
        await m.edit(f"🏓 **Pong!**\n🧭 **Latency:** `{latency} ms`")
        
