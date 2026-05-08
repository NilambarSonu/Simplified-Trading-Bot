import argparse
import sys
import json
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_order_params
from bot.logging_config import logger
from bot.utils import Colors

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Place command
    place_parser = subparsers.add_parser("place", help="Place an order")
    place_parser.add_argument("--symbol", required=True, help="Trading symbol, e.g., BTCUSDT")
    place_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="BUY or SELL")
    place_parser.add_argument("--order-type", default="MARKET", choices=["MARKET", "LIMIT"], help="MARKET or LIMIT")
    place_parser.add_argument("--quantity", required=True, type=float, help="Quantity to trade")
    place_parser.add_argument("--price", type=float, help="Price for LIMIT orders")

    args = parser.parse_args()

    if args.command == "place":
        try:
            # 1. Validate Input
            validate_order_params(args.symbol, args.side, args.order_type, args.quantity, args.price)
            
            # 2. Initialize Client and Order Manager
            print(f"{Colors.OKBLUE}Initializing Binance Client...{Colors.ENDC}")
            binance_client = BinanceClient()
            order_manager = OrderManager(binance_client)
            
            # 3. Print Summary
            print(f"\n{Colors.BOLD}{Colors.HEADER}--- Order Summary ---{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Symbol:   {Colors.ENDC}{args.symbol.upper()}")
            print(f"{Colors.OKCYAN}Side:     {Colors.ENDC}{args.side.upper()}")
            print(f"{Colors.OKCYAN}Type:     {Colors.ENDC}{args.order_type.upper()}")
            print(f"{Colors.OKCYAN}Quantity: {Colors.ENDC}{args.quantity}")
            print(f"{Colors.OKCYAN}Price:    {Colors.ENDC}{args.price if args.price else 'N/A'}")
            print(f"{Colors.BOLD}{Colors.HEADER}----------------------{Colors.ENDC}\n")
            
            # 4. Place Order
            response = order_manager.place_futures_order(
                args.symbol, args.side, args.order_type, args.quantity, args.price
            )
            
            # 5. Display Success Result
            print(f"{Colors.BOLD}{Colors.OKGREEN}✅ Order placed successfully!{Colors.ENDC}")
            print(f"\n{Colors.UNDERLINE}Order Response Details:{Colors.ENDC}")
            print(f"{Colors.OKBLUE}{json.dumps(response, indent=4)}{Colors.ENDC}")

        except ValueError as ve:
            print(f"\n{Colors.FAIL}❌ Validation Error: {ve}{Colors.ENDC}")
            sys.exit(1)
        except Exception as e:
            print(f"\n{Colors.FAIL}❌ Error: {e}{Colors.ENDC}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
