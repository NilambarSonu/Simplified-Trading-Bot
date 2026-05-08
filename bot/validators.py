from bot.logging_config import logger

def validate_order_params(symbol, side, order_type, quantity, price=None):
    """Validates basic order parameters."""
    if not symbol:
        raise ValueError("Symbol is required (e.g., BTCUSDT)")
    
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")
    
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0")
    except ValueError:
        raise ValueError("Quantity must be a valid number")
        
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be greater than 0")
        except ValueError:
            raise ValueError("Price must be a valid number")
            
    return True
