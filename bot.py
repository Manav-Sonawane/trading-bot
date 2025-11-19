import os
import time
import httpx
import logging
from dotenv import load_dotenv
from utils import sign_params, mask_sensitive

load_dotenv()
logger = logging.getLogger("binance_bot")

class BasicBot:
    def __init__(self, api_key: str, api_secret: str, base_url: str = None, testnet = True):
        if not api_key or not api_secret:
            raise ValueError("API key adn secret are required")
        
        self.api_key = api_key
        self.api_secret = api_secret

        self.base_url = base_url or os.getenv("BINANCE_TESTNET_BASE")
        if not self.base_url:
            raise ValueError("Base URL not provided and not found in environment variables")
        
        self.http = httpx.Client(
            timeout=10.0,
            headers={"X-MBX-APIKEY": self.api_key}
        )

        logger.info(f"Bot initialized (testnet={testnet}) using {self.base_url}")

    def _request(self, method: str, path: str, params: dict):
        url = self.base_url.rstrip("/") + path

        signed = sign_params(params, self.api_secret)
        
        attempts = 0
        max_attempts = 3
        backoff = 0.5

        while attempts < max_attempts:
            try:
                safe_params = mask_sensitive(signed)
                logger.debug(f"REQUEST -> {method.upper()} {url} params={safe_params}")

                if method.upper() == "GET":
                    resp = self.http.post(url, params=list(sorted(signed.items())))

                elif method.upper() == "POST":
                    resp = self.http.post(url, params=list(sorted(signed.items())))

                elif method.upper() == "DELETE":
                    resp = self.http.post(url, params=list(sorted(signed.items())))

                else:
                    resp = self.http.post(url, params=list(sorted(signed.items())))

            
                logger.debug(f"RESPONSE <- {resp.status_code} {resp.text}")

                resp.raise_for_status()
                return resp.json()
            
            except httpx.HTTPStatusError as e:
                err_body = e.response.text
                logger.error(f"Binance response error: {err_body}")
                raise

            except httpx.RequestError as e:
                attempts += 1
                logger.warning(f"Network error: {e}. Retrying {attempts}/{max_attempts}...")
                time.sleep(backoff)
                backoff *= 2

        raise ConnectionError("Failed after multiple networks retries")

    def place_order(self, symbol: str, side: str, quantity: float,
                    ord_type: str = "MARKET", price: float = None,
                    time_in_force: str = None, reduce_only: bool = False):

        symbol = symbol.upper()
        side = side.upper()
        ord_type = ord_type.upper()

        if side not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")

        if ord_type not in ("MARKET", "LIMIT"):
            raise ValueError("ord_type must be MARKET or LIMIT")

        if quantity is None or quantity <= 0:
            raise ValueError("quantity must be > 0")
        
        if ord_type == "MARKET" and quantity < 0.0001:
            raise ValueError("Quantity is unrealistically low for MARKET order")
    
        if ord_type == "LIMIT":
            if time_in_force not in ("GTC", "IOC", "FOK"):
                raise ValueError("Invalid timeInForce")


        params = {
            "symbol": symbol,
            "side": side,
            "type": ord_type,
            "quantity": format(quantity, 'f'),
            "recvWindow": 5000
        }

        if ord_type == "LIMIT":
            if price is None or price <= 0:
                raise ValueError("LIMIT order requires price > 0")

            params["price"] = price
            params["timeInForce"] = time_in_force or "GTC"   # GTC is default

        if reduce_only:
            params["reduceOnly"] = "true"

        return self._request("POST", "/fapi/v1/order", params)
        
    def get_order(self, symbol: str, order_id: int):
        symbol = symbol.upper()
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        return self._request("GET", "/fapi/v1/order", params)
    
    def cancel_order(self, symbol: str, order_id: int):
        symbol = symbol.upper()
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        return self._request("DELETE", "/fapi/v1/order", params)
    
    def sanity_check(self, symbol: str, quantity: float, price: float = None):

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if price is not None and price <= 0:
            raise ValueError("Price must be > 0 for LIMIT orders")

        # optional but recommended:
        # check symbol format
        if not symbol.isalnum():
            raise ValueError("Invalid symbol")

        return True

