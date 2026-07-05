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

# ── DUMMY WEB SERVER FOR RENDER (PORT 8080 FIX) ──
async def handle_render_ping(request):
    return web.Response(text="Bot is running perfectly on Render!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle_render_ping)])
    runner = web.AppRunner(app)
    await runner.setup()
    # সরাসরি কোডেই পোর্ট ৮০৮০ ফিক্সড করে বাইন্ড করা হলো
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("🟢 Render Port 8080 successfully opened and dummy server started.")

# ── DATABASE HANDLERS ──
def load_sessions():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return json.load(f)
        except: pass
    return []

def save_session(uid, session_str):
    data = load_sessions()
    # ডুপ্লিকেট সেশন এড়ানোর চেক
    if not any(item['uid'] == uid for item in data):
        data.append({"uid": uid, "session": session_str})
        with open(DB_FILE, 'w') as f: json.dump(data, f, indent=2)

# ── AUTOMATIC PLUGIN LOADER (১০০০ ফিচারের জন্য) ──
def register_plugins(client, uid):
    # plugins ফোল্ডারের সব ফাইল অটো-লোড করবে
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
@bot.on(events.NewMessage(pattern='/start', from_users=OWNER_ID))
async def start_cmd(e):
    await e.reply("⚡ **Multi-Session Userbot Controller Ready!**\n\nনিচের বাটনে ক্লিক করে তোমার পার্সোনাল অ্যাকাউন্ট কানেক্ট করো।", 
                  buttons=[[Button.inline("➕ Add New Account", data="add_account")]])

@bot.on(events.CallbackQuery(data=b'add_account'))
async def add_account_flow(e):
    if e.sender_id != OWNER_ID: return await e.answer("Access Denied.", alert=True)
    
    await e.edit("📱 তোমার টেলিগ্রাম নম্বরটি আন্তর্জাতিক ফরম্যাটে দাও (যেমন: `+88017XXXXXXXX`):")
    
    async with bot.conversation(e.sender_id, timeout=300) as conv:
        try:
            # ফোন নম্বর গ্রহণ
            phone_msg = await conv.get_response()
            phone = phone_msg.text.strip().replace(" ", "")
            
            await e.respond("`OTP কোড পাঠানো হচ্ছে...`")
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            
            code_request = await client.send_code_request(phone)
            await e.respond("📩 তোমার টেলিগ্রাম অ্যাপে পাঠানো OTP কোডটি দাও:")
            
            # ওটিপি কোড গ্রহণ
            otp_msg = await conv.get_response()
            otp = otp_msg.text.strip().replace(" ", "")
            
            try:
                await client.sign_in(phone, otp, phone_code_hash=code_request.phone_code_hash)
            except Exception as login_err:
                # যদি 2FA (Two-Factor Authentication) অন থাকে
                await e.respond("🔐 Two-Factor Authentication (2FA) পাসওয়ার্ডটি দাও:")
                pwd_msg = await conv.get_response()
                await client.sign_in(password=pwd_msg.text.strip())
            
            me = await client.get_me()
            uid = me.id
            sess_str = client.session.save()
            
            # মেমোরি ও ফাইল ডেটাবেজে সেভ
            save_session(uid, sess_str)
            SESSIONS[uid] = client
            
            # প্লাগিনস লোড করা
            register_plugins(client, uid)
            
            await e.respond(f"🎉 **লগইন সফল!**\n👤 User: **{me.first_name}** (ID: `{uid}`)\nএখন থেকে এই অ্যাকাউন্টে সব ইউজারবট ফিচার কাজ করবে।")
            
        except asyncio.TimeoutError:
            await e.respond("❌ সময় শেষ (Timeout)! আবার চেষ্টা করো।")
        except Exception as ex:
            await e.respond(f"❌ লগইন ব্যর্থ হয়েছে: `{ex}`")

# ── SYSTEM STARTUP ──
async def startup_process():
    # প্রথমে Render এর জন্য পোর্ট ৮০৮০ ওপেন করা
    await start_web_server()
    
    # পূর্বে সেভ থাকা সেশনগুলো ব্যাকগ্রাউন্ডে রানিং করা
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
        
