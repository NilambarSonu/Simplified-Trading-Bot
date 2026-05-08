import os
import hmac
import hashlib
import time
import json
import urllib.request
import urllib.parse
from bot.logging_config import logger
from bot.utils import load_dotenv

load_dotenv()

class BinanceClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.time_offset = 0
        
        if not self.api_key or not self.api_secret:
            logger.error("API Key and Secret must be provided in .env file")
            raise ValueError("Missing API credentials")
        
        # Synchronize time with Binance
        self.sync_time()
        logger.info("Binance Client (Standard Lib) initialized with time sync")

    def sync_time(self):
        """Fetches server time and calculates offset to avoid 'recvWindow' errors."""
        try:
            url = f"{self.BASE_URL}/fapi/v1/time"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))
                server_time = data['serverTime']
                local_time = int(time.time() * 1000)
                self.time_offset = server_time - local_time
                logger.info(f"Time synchronized. Offset: {self.time_offset}ms")
        except Exception as e:
            logger.error(f"Failed to sync time: {e}")
            self.time_offset = 0

    def _get_timestamp(self):
        return int(time.time() * 1000) + self.time_offset

    def _sign(self, query_string):
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def request(self, method, endpoint, params=None):
        if params is None:
            params = {}
        
        # Use synchronized timestamp and a larger recvWindow
        params["timestamp"] = self._get_timestamp()
        params["recvWindow"] = 10000  # Increase window to 10 seconds for reliability
        
        # Create query string
        query_string = urllib.parse.urlencode(params)
        
        # Add signature
        signature = self._sign(query_string)
        query_string += f"&signature={signature}"
        
        url = f"{self.BASE_URL}{endpoint}"
        if method == "GET":
            url += f"?{query_string}"
            data = None
        else:
            data = query_string.encode("utf-8")

        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("X-MBX-APIKEY", self.api_key)
        
        logger.info(f"Request: {method} {url}")
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = response.read().decode("utf-8")
                logger.info(f"Response: {res_data}")
                return json.loads(res_data)
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode("utf-8")
            logger.error(f"HTTP Error {e.code}: {error_msg}")
            try:
                return json.loads(error_msg)
            except:
                raise Exception(f"HTTP Error {e.code}: {error_msg}")
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
