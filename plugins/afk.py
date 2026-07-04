import time
from telethon import events

AFK_DATA = {"is_afk": False, "reason": "", "time": 0}

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]afk(?: |$)(.*)'))
    async def set_afk(e):
        if not getattr(e, 'out', False): return
        
        reason = e.pattern_match.group(1).strip()
        AFK_DATA["is_afk"] = True
        AFK_DATA["reason"] = reason if reason else "Not mentioned."
        AFK_DATA["time"] = time.time()
        
        await e.edit(f"💤 **I am now AFK.**\n**Reason:** `{AFK_DATA['reason']}`")

    @client.on(events.NewMessage(incoming=True))
    async def afk_reply(e):
        if not AFK_DATA["is_afk"]: return
        if not (e.is_private or e.mentioned): return
        
        afk_since = int(time.time() - AFK_DATA["time"])
        h, m = divmod(afk_since, 3600)
        m, s = divmod(m, 60)
        uptime_str = f"{h}h {m}m" if h > 0 else f"{m}m {s}s"
        
        msg = f"🛑 **I am currently offline!**\n\n📝 **Reason:** `{AFK_DATA['reason']}`\n⏱ **AFK Since:** `{uptime_str}`"
        await e.reply(msg)

    @client.on(events.NewMessage(outgoing=True))
    async def remove_afk(e):
        if AFK_DATA["is_afk"] and not e.text.startswith(('.afk', '!afk')):
            AFK_DATA["is_afk"] = False
            msg = await e.respond("✅ **I am back online! AFK mode disabled.**")
            time.sleep(3)
            await msg.delete()