import os
import asyncio
import logging
import json
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# ── CONFIG ──
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

logging.basicConfig(level=logging.INFO)
bot = TelegramClient('master_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

SESSIONS = {} # {uid: client_instance}
DB_FILE = "sessions.json"

def load_sessions():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return []

def save_session(uid, session_str):
    data = load_sessions()
    data.append({"uid": uid, "session": session_str})
    with open(DB_FILE, 'w') as f: json.dump(data, f)

# ── LOGIN LOGIC ──
@bot.on(events.NewMessage(pattern='/start', from_users=OWNER_ID))
async def start(e):
    await e.reply("বট রেডি! নতুন অ্যাকাউন্ট যোগ করতে `/add` কমান্ড দাও।", 
                  buttons=[[Button.inline("➕ Add Account", data="add")]])

@bot.on(events.CallbackQuery(data=b'add'))
async def add_acc(e):
    await e.edit("টেলিগ্রাম নম্বর দাও (যেমন: +88017...):")
    async with bot.conversation(e.sender_id) as conv:
        phone = await conv.get_response()
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()
        code = await client.send_code_request(phone.text)
        await e.respond("OTP কোড দাও:")
        otp = await conv.get_response()
        await client.sign_in(phone.text, otp.text, phone_code_hash=code.phone_code_hash)
        
        sess_str = client.session.save()
        save_session((await client.get_me()).id, sess_str)
        SESSIONS[(await client.get_me()).id] = client
        await e.respond("✅ লগইন সফল!")

# ── DYNAMIC PLUGIN LOADER (১০০০ ফিচারের জন্য) ──
def register_plugins(client, uid):
    # এখানে তোর plugins ফোল্ডারের ফাইলগুলো লোড করবি
    # এই ফাংশনটি এখন থেকে আর এডিট করতে হবে না
    pass 

# ── BOOTUP ──
async def startup():
    for item in load_sessions():
        cl = TelegramClient(StringSession(item['session']), API_ID, API_HASH)
        await cl.start()
        SESSIONS[item['uid']] = cl
        register_plugins(cl, item['uid'])
        logging.info(f"Loaded session for {item['uid']}")

loop = asyncio.get_event_loop()
loop.run_until_complete(startup())
logging.info("Master Bot is running...")
bot.run_until_disconnected()