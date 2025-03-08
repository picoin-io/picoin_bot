import os
import requests
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Enable Debug Logging
logging.basicConfig(level=logging.INFO)

# ✅ Retrieve API keys and configurations from environment variables
API_TOKEN = os.getenv("API_TOKEN")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")
BSC_CONTRACT = os.getenv("BSC_CONTRACT")

# ✅ Validate API token
if not API_TOKEN:
    raise ValueError("❌ API_TOKEN is missing! Check your environment variables.")

# ✅ Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ✅ Function to fetch the latest PiCoin price
def get_pi_price():
    url = "https://api.geckoterminal.com/api/v2/networks/bsc/pools/0xe9c7347605cfce6a302cd8c76b4665f1f3f8d1c1"
    try:
        response = requests.get(url)
        data = response.json()
        price = data["data"]["attributes"]["base_token_price_usd"]
        return f"🚀 PiCoin Latest Price: ${price}"
    except Exception as e:
        logging.error(f"Error fetching PiCoin price: {e}")
        return "⚠️ Unable to fetch PiCoin price. Please try again later."

# ✅ Welcome new members to the group
@dp.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    for new_member in message.new_chat_members:
        await message.reply(
            f"👋 Welcome {new_member.full_name} to the PiCoin Global Community! 🚀\n\n"
            f"🔗 Official Website: https://www.picoin.io\n"
            f"📢 Official Announcements: https://x.com/Picoin_io\n"
            f"💰 Trade PiCoin: https://pancakeswap.finance/?outputCurrency={BSC_CONTRACT}\n\n"
            f"💡 Type /price to check the latest price!"
        )

# ✅ Handle /price command
@dp.message(F.text.lower() == "/price")
async def send_price(message: Message):
    price = get_pi_price()
    await message.reply(price)

# ✅ Auto-delete spam messages (anti-advertising)
@dp.message(F.text.lower().contains("http"), F.from_user.is_bot == False)
async def delete_spam(message: Message):
    await message.delete()
    await message.reply("⚠️ External advertising links are not allowed!")

# ✅ Keep bot alive to prevent Railway from sleeping
async def keep_bot_alive():
    while True:
        try:
            await bot.send_message(CHAT_ID, "🚀 Bot is still running!")
            logging.info("Sent heartbeat message to prevent Railway from sleeping.")
        except Exception as e:
            logging.error(f"Error in keep_bot_alive: {e}")
        await asyncio.sleep(600)  # Every 10 minutes

# ✅ Start the bot
async def main():
    logging.info("🚀 Bot is starting...")
    asyncio.create_task(keep_bot_alive())  # Start the heartbeat function
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# ✅ Fix Windows `asyncio` issue
if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("🛑 Bot stopped.")
