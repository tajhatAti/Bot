import os
import importlib
import asyncio
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
import config

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Asyncio Loop ফিক্স
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Render 24/7 Uptime-এর জন্য ডামি ওয়েব সার্ভার
async def handle_ping(reader, writer):
    await reader.read(100)
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
    await writer.drain()
    writer.close()

async def start_server():
    await asyncio.start_server(handle_ping, '0.0.0.0', config.PORT)
    logger.info(f"🟢 Web server started on port {config.PORT}")

# ক্লায়েন্ট সেটআপ
client = TelegramClient(StringSession(config.STRING_SESSION), config.API_ID, config.API_HASH)

# ডাইনামিক প্লাগিন লোডার
def load_plugins():
    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)
        logger.info("📁 Created plugins directory.")
        return

    count = 0
    # plugins ফোল্ডারের সব .py ফাইল স্ক্যান করবে
    for file in os.listdir(plugin_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = f"{plugin_dir}.{file[:-3]}"
            try:
                module = importlib.import_module(module_name)
                # প্রতিটি প্লাগিনে register() ফাংশন থাকতে হবে
                if hasattr(module, "register"):
                    module.register(client)
                    count += 1
            except Exception as e:
                logger.error(f"❌ Failed to load {file}: {e}")
                
    logger.info(f"✅ Successfully loaded {count} plugins.")

async def main():
    await start_server()
    await client.connect()
    
    if not await client.is_user_authorized():
        logger.error("❌ Invalid Session String! Please check Environment Variables.")
        return
        
    logger.info("⚡ Modular Userbot is Alive and Running!")
    
    # লগইন সফল হলে প্লাগিন লোড করবে
    load_plugins()
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    loop.run_until_complete(main())
