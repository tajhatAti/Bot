import os
import asyncio
import logging
import json
import glob
import importlib
from aiohttp import web
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# ── CONFIGURATION ──
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
DB_FILE = "sessions.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# মাস্টার বট ইনিশিয়ালাইজেশন
bot = TelegramClient('master_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
SESSIONS = {} 
USER_STATES = {}  # ওটিপি এবং নম্বরের স্টেট ধরে রাখার জন্য গ্লোবাল ডিকশনারি

# ── DUMMY WEB SERVER FOR RENDER (PORT 8080 FIX) ──
async def handle_render_ping(request):
    return web.Response(text="Bot is running perfectly on Render!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle_render_ping)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("🟢 Render Port 8080 successfully opened.")

# ── DATABASE HANDLERS ──
def load_sessions():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return json.load(f)
        except: pass
    return []

def save_session(uid, session_str):
    data = load_sessions()
    if not any(item['uid'] == uid for item in data):
        data.append({"uid": uid, "session": session_str})
        with open(DB_FILE, 'w') as f: json.dump(data, f, indent=2)

# ── AUTOMATIC PLUGIN LOADER ──
def register_plugins(client, uid):
    for file in glob.glob("plugins/*.py"):
        name = os.path.basename(file)[:-3]
        try:
            module = importlib.import_module(f"plugins.{name}")
            if hasattr(module, "register"):
                module.register(client, uid)
                logger.info(f"Successfully loaded plugin: {name} for UID: {uid}")
        except Exception as e:
            logger.error(f"Failed to load plugin {name}: {e}")

# ── MASTER BOT HANDLERS ──
@bot.on(events.NewMessage(pattern=r'(?i)^/start$', from_users=OWNER_ID))
async def start_cmd(e):
    USER_STATES.pop(e.sender_id, None) # রিসেট স্টেট
    await e.reply("⚡ **Multi-Session Userbot Controller Ready!**\n\nনতুন অ্যাকাউন্ট যোগ করতে নিচের বাটনে ক্লিক করো অথবা সরাসরি `/add` কমান্ড দাও।", 
                  buttons=[[Button.inline("➕ Add New Account", data="add_account")]])

@bot.on(events.NewMessage(pattern=r'(?i)^/add$', from_users=OWNER_ID))
async def add_cmd(e):
    USER_STATES[e.sender_id] = {"step": "input_phone"}
    await e.reply("📱 তোমার টেলিগ্রাম নম্বরটি আন্তর্জাতিক ফরম্যাটে দাও (যেমন: `+88017XXXXXXXX`):")

@bot.on(events.CallbackQuery(data=b'add_account'))
async def add_account_callback(e):
    if e.sender_id != OWNER_ID: 
        return await e.answer("Access Denied.", alert=True)
    USER_STATES[e.sender_id] = {"step": "input_phone"}
    await e.edit("📱 তোমার টেলিগ্রাম নম্বরটি আন্তর্জাতিক ফরম্যাটে দাও (যেমন: `+88017XXXXXXXX`):")

# ── STATE MANAGEMENT INPUT HANDLER ──
@bot.on(events.NewMessage(from_users=OWNER_ID))
async def handle_steps(e):
    if e.text.startswith('/'): return
    state = USER_STATES.get(e.sender_id)
    if not state: return

    step = state.get("step")

    # স্টেপ ১: ফোন নম্বর ইনপুট নেওয়া
    if step == "input_phone":
        phone = e.text.strip().replace(" ", "")
        m = await e.reply("`OTP কোড পাঠানো হচ্ছে...`")
        try:
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            code_request = await client.send_code_request(phone)
            
            # পরবর্তী স্টেপের জন্য ডাটা স্টোর
            USER_STATES[e.sender_id] = {
                "step": "input_otp",
                "phone": phone,
                "phone_code_hash": code_request.phone_code_hash,
                "client": client
            }
            await m.edit("An OTP message has been sent to your Telegram app.\n\n📩 ওটিপি কোডটি দাও:")
        except Exception as ex:
            USER_STATES.pop(e.sender_id, None)
            await m.edit(f"❌ কোড পাঠাতে ব্যর্থ: `{ex}`\nআবার শুরু করতে `/add` দাও।")

    # স্টেপ ২: ওটিপি ইনপুট নেওয়া
    elif step == "input_otp":
        otp = e.text.strip().replace(" ", "")
        client = state["client"]
        phone = state["phone"]
        phone_code_hash = state["phone_code_hash"]
        
        m = await e.reply("`যাচাই করা হচ্ছে...`")
        try:
            try:
                await client.sign_in(phone, otp, phone_code_hash=phone_code_hash)
            except Exception as login_err:
                # যদি টু-ফ্যাক্টর অথেনটিকেশন (2FA) লাগে
                USER_STATES[e.sender_id]["step"] = "input_password"
                await m.edit("🔐 তোমার অ্যাকাউন্টে Two-Factor Authentication (2FA) অন আছে।\n\nতোমার ক্লাউড পাসওয়ার্ডটি দাও:")
                return
            
            # সফল লগইন প্রসেস
            await process_successful_login(e, client, m)

        except Exception as ex:
            USER_STATES.pop(e.sender_id, None)
            await m.edit(f"❌ লগইন ব্যর্থ: `{ex}`\nআবার চেষ্টা করতে `/add` দাও।")

    # স্টেপ ৩: টু-ফ্যাক্টর পাসওয়ার্ড ইনপুট নেওয়া
    elif step == "input_password":
        pwd = e.text.strip()
        client = state["client"]
        m = await e.reply("`পাসওয়ার্ড চেক করা হচ্ছে...`")
        try:
            await client.sign_in(password=pwd)
            await process_successful_login(e, client, m)
        except Exception as ex:
            USER_STATES.pop(e.sender_id, None)
            await m.edit(f"❌ পাসওয়ার্ড ভুল বা ত্রুটি ঘটেছে: `{ex}`\nআবার শুরু করতে `/add` দাও।")

async def process_successful_login(event, client, status_msg):
    me = await client.get_me()
    uid = me.id
    sess_str = client.session.save()
    
    save_session(uid, sess_str)
    SESSIONS[uid] = client
    
    register_plugins(client, uid)
    USER_STATES.pop(event.sender_id, None)
    await status_msg.edit(f"🎉 **লগইন সফল!**\n👤 অ্যাকাউন্ট: **{me.first_name}** (ID: `{uid}`)\n\nইউজারবট এখন সচল।")

# ── SYSTEM STARTUP ──
async def startup_process():
    await start_web_server()
    saved_data = load_sessions()
    logger.info(f"Found {len(saved_data)} saved sessions to load.")
    
    for item in saved_data:
        uid = item['uid']
        sess = item['session']
        try:
            cl = TelegramClient(StringSession(sess), API_ID, API_HASH)
            await cl.start()
            SESSIONS[uid] = cl
            register_plugins(cl, uid)
            logger.info(f"✅ Auto-started session for UID: {uid}")
        except Exception as e:
            logger.error(f"❌ Failed to auto-start session for UID {uid}: {e}")

# রান লুপ ম্যানেজার
loop = asyncio.get_event_loop()
loop.run_until_complete(startup_process())

logger.info("🚀 Master Controller Bot is fully deployed and active!")
bot.run_until_disconnected()
        
