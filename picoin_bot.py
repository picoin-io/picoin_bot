import os
import requests
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Enable Debug Logging
logging.basicConfig(level=logging.INFO)

# 🔑 Secure API Keys & Bot Configuration
API_TOKEN = os.getenv("API_TOKEN")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")
BSC_CONTRACT = os.getenv("BSC_CONTRACT")

# ✅ Ensure API Token is provided
if not API_TOKEN:
    raise ValueError("❌ Bot API token is missing! Please check your .env file.")

# ✅ Initialize Bot & Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 🔍 Fetch PiCoin Price from GeckoTerminal
def get_pi_price():
    url = "https://api.geckoterminal.com/api/v2/networks/bsc/pools/0xe9c7347605cfce6a302cd8c76b4665f1f3f8d1c1"
    response = requests.get(url)
    data = response.json()
    
    try:
        price = data["data"]["attributes"]["base_token_price_usd"]
        return f"🚀 PiCoin Latest Price: ${price}"
    except:
        return "⚠️ Unable to fetch PiCoin price. Please try again later."

# 🎉 Welcome New Members
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

# 📊 Handle /price Command
@dp.message(F.text.lower() == "/price")
async def send_price(message: Message):
    price = get_pi_price()
    await message.reply(price)

# 🚫 Auto-Delete Spam (Anti-Advertising)
@dp.message(F.text.lower().contains("http"), F.from_user.is_bot == False)
async def delete_spam(message: Message):
    await message.delete()
    await message.reply("⚠️ External advertising links are not allowed!")

# ✅ Start Bot
async def main():
    print("🚀 Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# 🛠 Fix Windows `asyncio` Issue
if __name__ == "__main__":
    import sys
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
