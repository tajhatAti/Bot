from telethon import events
import math

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^[.!]calc (.*)'))
    async def calculator(e):
        expr = e.pattern_match.group(1).strip()
        m = await e.edit("`Calculating...`") if getattr(e, 'out', False) else await e.reply("`Calculating...`")
        
        # সুরক্ষার জন্য নির্দিষ্ট ক্যারেক্টার ছাড়া বাকি সব ব্লক করা হলো
        allowed_chars = "0123456789+-*/().[] ** sqrt log sin cos tan pi e "
        if not all(c in allowed_chars or c.isspace() for c in expr):
            return await m.edit("❌ `Invalid characters in expression!`")
            
        try:
            # math মডিউলের ফাংশনগুলো ইভ্যালুয়েশনে পাস করা হচ্ছে
            safe_dict = {
                "abs": abs, "round": round,
                "sqrt": math.sqrt, "log": math.log,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "pi": math.pi, "e": math.e
            }
            result = eval(expr, {"__builtins__": None}, safe_dict)
            await m.edit(f"📊 **Math Expression:**\n`{expr}`\n\n✅ **Result:**\n`{result}`")
        except Exception as ex:
            await m.edit(f"❌ **Error:** `{str(ex)}`")