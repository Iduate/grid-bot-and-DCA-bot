import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 3Commas API configuration
API_URL = os.getenv('3COMMAS_API_URL')
API_KEY = os.getenv('3COMMAS_API_KEY')
API_SECRET = os.getenv('3COMMAS_SECRET')

# Bot configuration
DEFAULT_EXCHANGE = 'binance'  # Change this to your preferred exchange
DEFAULT_MARKET_CODE = 'BTC_USDT'  # Default trading pair

# Grid Bot configuration
GRID_BOT_CONFIG = {
    'name': 'Auto Grid Bot',
    'pair': DEFAULT_MARKET_CODE,
    'upper_price': None,  # Will be set dynamically
    'lower_price': None,  # Will be set dynamically
    'quantity_per_grid': 0.001,  # Adjust based on your capital
    'grids_count': 20,
    'leverage_type': 'spot',  # 'spot', 'cross', or 'isolated'
    'leverage_custom_value': 1,
}

# DCA Bot configuration
DCA_BOT_CONFIG = {
    'name': 'Auto DCA Bot',
    'pair': DEFAULT_MARKET_CODE,
    'base_order_volume': 10,  # in USD
    'safety_order_volume': 20,  # in USD
    'max_safety_orders': 5,
    'max_active_safety_orders': 3,
    'martingale_volume_coefficient': 1.5,  # Increase each safety order by this factor
    'martingale_step_coefficient': 1.0,  # Price deviation to open a safety order
    'take_profit': 1.5,  # Take profit percentage
    'safety_order_step_percentage': 2.5,  # Price deviation to open a safety order
    'strategy': 'long',  # 'long' or 'short'
}
