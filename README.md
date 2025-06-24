# 🪙 PrimeTrade AI Bot – Binance Futures Testnet

A simplified Python-based crypto trading bot that lets you place Binance Futures USDT-M orders via both command-line and a lightweight Streamlit UI. Built as part of a Junior Python Developer assignment.

---

## ✨ Features

- 🔐 Secure API credential handling (manual or .env)
- ✅ Supports Market, Limit, Stop, and Stop-Market order types
- 🔄 Buy/Sell support for USDT-M pairs (e.g., BTCUSDT)
- 📊 Real-time open order viewing in UI
- 📦 Command-line interface: run_bot.py
- 🖥️ Streamlit-based frontend: app.py
- 📜 Logging of API responses & errors (bot.log)
- ⚙️ Built using official Binance API (python-binance)

---

## 🧰 Project Structure

├── app.py # Streamlit UI
├── run_bot.py # CLI interface
├── trading_bot/ # Bot logic
│ └── bot.py
├── requirements.txt # Python dependencies
├── bot.log # Log of API interactions



---

## 🚀 Quick Start

1. 🔁 Clone the repo
```bash
git clone https://github.com/SS-Hossain/primetrade-ai-bot.git
cd primetrade-ai-bot
```

## 🐍 Create & activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
## 📦 Install dependencies
```bash
pip install -r requirements.txt
```

## 🔑 Set your API key and secret (manually in the UI or via .env file):
# .env
```
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
```
## Run the App
🖥️ GUI (Streamlit):
```bash
streamlit run app.py
```

🖥️ CLI:
```bash
python run_bot.py
```

## 🧪 Testnet Setup
- Registered on Binance Futures Testnet
- Used base URL: https://testnet.binancefuture.com
- Credentials generated from Testnet


## 📁 Logs
All bot activity is logged in bot.log, including:

- Order requests
- Binance API responses
- Errors & exceptions

## 🧠 Bonus Features
- 🔘 View all open orders in real-time (via Streamlit UI)
- ⚠️ Handles input validation and order failures gracefully

