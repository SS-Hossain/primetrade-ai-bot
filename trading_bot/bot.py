
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
import logging

# Logging config
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        logging.info("✅ Direct REST mode: Binance Testnet client initialized.")

    def sign_payload(self, data: dict):
        query_string = urlencode(data)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return query_string + f"&signature={signature}"

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            # Get server time for accurate timestamp
            server_time = requests.get(f"{self.base_url}/fapi/v1/time").json()["serverTime"]

            data = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
                "timestamp": server_time,
                "recvWindow": 10000
            }

            if order_type == "LIMIT":
                data["price"] = price
                data["timeInForce"] = "GTC"

            elif order_type == "STOP_MARKET":
                data["stopPrice"] = stop_price
                data["closePosition"] = False
                data["timeInForce"] = "GTC"

            elif order_type == "STOP":
                data["stopPrice"] = stop_price
                data["price"] = price
                data["timeInForce"] = "GTC"

            final_query = self.sign_payload(data)
            headers = {"X-MBX-APIKEY": self.api_key}
            response = requests.post(f"{self.base_url}/fapi/v1/order", headers=headers, data=final_query)

            if response.status_code == 200:
                order = response.json()
                logging.info(f"✅ Order placed: {order}")
                print("✅ Order executed:", order)
            else:
                logging.error(f"❌ API Error: {response.text}")
                print("❌ API Error:", response.text)

        except Exception as e:
            logging.error(f"❌ Request error: {e}")
            print("❌ Request error:", e)
