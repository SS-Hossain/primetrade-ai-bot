from trading_bot.bot import BasicBot
from dotenv import load_dotenv
import os
from trading_bot.bot import BasicBot

# Load keys from .env
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# # CLI Inputs for order
# symbol = input("📈 Symbol (e.g., BTCUSDT): ").upper()
# side = input("🟢 Side (BUY/SELL): ").upper()
# order_type = input("📘 Order Type (MARKET/LIMIT): ").upper()
# quantity = float(input("🔢 Quantity: "))

# price = None
# if order_type == "LIMIT":
#     price = input("💰 Price: ")

# # Run bot
# bot = BasicBot(api_key, api_secret)
# bot.place_order(symbol, side, order_type, quantity, price)



bot = BasicBot(api_key, api_secret, testnet=True)

symbol = input("📈 Symbol (e.g., BTCUSDT): ").upper()
side = input("🟢 Side (BUY/SELL): ").upper()
order_type = input("📘 Order Type (MARKET/LIMIT/STOP/STOP_MARKET): ").upper()
quantity = float(input("🔢 Quantity: "))

price = None
stop_price = None

# Ask for price if required
if order_type in ["LIMIT", "STOP"]:
    price = input("💰 Price: ").strip()
    if price:
        price = float(price)

# Ask for stop price if required
if order_type in ["STOP", "STOP_MARKET"]:
    stop_price = input("🛑 Stop Price: ").strip()
    if stop_price:
        stop_price = float(stop_price)

# Place order using bot
bot.place_order(symbol, side, order_type, quantity, price=price, stop_price=stop_price)