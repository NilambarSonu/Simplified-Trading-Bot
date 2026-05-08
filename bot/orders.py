from bot.logging_config import logger

class OrderManager:
    def __init__(self, client):
        self.client = client

    def place_futures_order(self, symbol, side, order_type, quantity, price=None):
        """
        Places an order on Binance Futures (USDT-M).
        """
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }

        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        logger.info(f"Attempting to place {order_type} {side} order for {quantity} {symbol}")
        
        # Endpoint for USDT-M Futures Order
        endpoint = "/fapi/v1/order"
        response = self.client.request("POST", endpoint, params)
        
        # If the response contains 'code', it's likely an error from Binance
        if "code" in response and response.get("code") != 200:
            error_msg = response.get("msg", "Unknown error")
            logger.error(f"Order failed: {error_msg} (Code: {response.get('code')})")
            raise Exception(f"Binance Error: {error_msg}")

        logger.info(f"Order placed successfully: {response.get('orderId')}")
        return response
