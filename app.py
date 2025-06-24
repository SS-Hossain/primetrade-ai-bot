import streamlit as st
from trading_bot.bot import BasicBot
import os
import requests
import time

# Read API keys from environment or input manually
api_key = os.getenv("BINANCE_API_KEY", "")
api_secret = os.getenv("BINANCE_API_SECRET", "")

st.set_page_config(page_title="Binance Futures Bot", layout="wide")
st.title("🚀 Binance Futures Testnet Trading Bot")

# Sidebar for credentials
st.sidebar.header("🔐 API Credentials")
api_key = st.sidebar.text_input("API Key", api_key)
api_secret = st.sidebar.text_input("API Secret", api_secret, type="password")

if api_key and api_secret:
    bot = BasicBot(api_key, api_secret, testnet=True)

    st.subheader("📋 Place an Order")

    symbol = st.text_input("📈 Symbol", "BTCUSDT")
    side = st.selectbox("🟢 Side", ["BUY", "SELL"])
    order_type = st.selectbox("📘 Order Type", ["MARKET", "LIMIT", "STOP", "STOP_MARKET"])
    quantity = st.number_input("🔢 Quantity", min_value=0.001, value=0.001, step=0.001, format="%.6f")

    price = None
    stop_price = None

    if order_type in ["LIMIT", "STOP"]:
        price = st.number_input("💰 Price", min_value=0.0, step=1.0)
    if order_type in ["STOP", "STOP_MARKET"]:
        stop_price = st.number_input("🛑 Stop Price", min_value=0.0, step=1.0)

    col1, col2 = st.columns([1, 1])
    submit_clicked = col1.button("✅ Submit Order")
    view_clicked = col2.button("📄 View Open Orders")

    def get_open_orders():
        try:
            server_time = requests.get(f"{bot.base_url}/fapi/v1/time").json()["serverTime"]
            params = {
                "symbol": symbol,
                "timestamp": server_time
            }
            query = bot.sign_payload(params)
            headers = {"X-MBX-APIKEY": api_key}
            response = requests.get(f"{bot.base_url}/fapi/v1/openOrders?{query}", headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.text}
        except Exception as e:
            return {"error": str(e)}

    if submit_clicked:
        try:
            order = bot.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )
            st.success("✅ Order submitted successfully!")
            st.json(order)

            # Live status tracking
            if order and "orderId" in order:
                st.info("⏳ Tracking order status for 30 seconds...")
                placeholder = st.empty()
                for i in range(30):
                    time.sleep(1)
                    try:
                        server_time = requests.get(f"{bot.base_url}/fapi/v1/time").json()["serverTime"]
                        params = {
                            "symbol": symbol,
                            "orderId": order["orderId"],
                            "timestamp": server_time
                        }
                        query = bot.sign_payload(params)
                        headers = {"X-MBX-APIKEY": api_key}
                        status_response = requests.get(f"{bot.base_url}/fapi/v1/order?{query}", headers=headers)
                        if status_response.status_code == 200:
                            data = status_response.json()
                            placeholder.info(f"📌 Status: {data['status']}")
                            if data["status"] == "FILLED":
                                placeholder.success("🎯 Order filled!")
                                break
                        else:
                            placeholder.error(f"Failed to get status: {status_response.text}")
                            break
                    except Exception as err:
                        placeholder.error(f"⚠️ Error while checking status: {err}")
                        break

        except Exception as e:
            st.error(f"❌ Failed to submit order: {e}")

    if view_clicked:
        st.subheader("📄 Open Orders")
        open_orders = get_open_orders()
        if "error" in open_orders:
            st.error(f"❌ Error: {open_orders['error']}")
        elif open_orders:
            st.json(open_orders)
        else:
            st.info("📭 No open orders found.")

else:
    st.warning("Please enter your API credentials to begin.")
