# 3Commas Trading Bots

A Python-based implementation of Grid Bot and DCA Bot for cryptocurrency trading using the 3Commas API.

## Features

- **Grid Bot**: Creates and manages a grid trading strategy with configurable parameters
- **DCA Bot**: Creates and manages a dollar-cost averaging strategy with safety orders
- **Test Mode**: Safely verify configurations without creating actual bots
- **Robust Error Handling**: Gracefully handles API issues, missing accounts, and invalid pairs
- **Price Fetching**: Multiple fallback mechanisms for retrieving accurate price data
- **Account Discovery**: Automatically finds and uses the correct exchange account

## Requirements

- Python 3.6+
- 3Commas account with API access
- Connected exchange (Binance, KuCoin, etc.)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/3commas-trading-bots.git
cd 3commas-trading-bots
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory with your 3Commas API credentials:
```
3COMMAS_API_URL=https://api.3commas.io
3COMMAS_API_KEY=your_api_key_here
3COMMAS_SECRET=your_api_secret_here
```

## Configuration

Edit the `config.py` file to customize bot settings:

### General Settings
- `DEFAULT_EXCHANGE`: Your preferred exchange (e.g., 'binance', 'kucoin')
- `DEFAULT_MARKET_CODE`: Default trading pair (e.g., 'BTC_ETH')

### Grid Bot Settings
- `name`: Bot name
- `pair`: Trading pair
- `quantity_per_grid`: Amount to buy/sell per grid
- `grids_count`: Number of grids
- `leverage_type`: 'spot', 'cross', or 'isolated'
- `leverage_custom_value`: Leverage value (1 for spot)

### DCA Bot Settings
- `name`: Bot name
- `pair`: Trading pair
- `base_order_volume`: Initial order size in USD
- `safety_order_volume`: Safety order size in USD
- `max_safety_orders`: Maximum number of safety orders
- `max_active_safety_orders`: Maximum number of active safety orders
- `martingale_volume_coefficient`: Volume multiplier for each safety order
- `martingale_step_coefficient`: Price deviation multiplier
- `take_profit`: Take profit percentage
- `safety_order_step_percentage`: Price deviation for safety orders
- `strategy`: 'long' or 'short'

## Usage

### Check API Connection First (Recommended)
```
python check_api.py
```

### Test Mode (Recommended for initial setup)
```
python main.py --test-mode
```

### Create Bots
```
python main.py
```

### Create Specific Bot Type
```
python main.py --bot-type grid  # Only create Grid Bot
python main.py --bot-type dca   # Only create DCA Bot
```

### Specify Trading Pair
```
python main.py --pair BTC_USDT
```

### Specify Account
```
python main.py --account-id 12345678
```

### Monitor Bot Performance
```
python monitor_bots.py
```

## Troubleshooting

### Connection Issues
- Verify your API keys in the `.env` file
- Check your internet connection
- Verify the 3Commas service is operational

### Bot Creation Failures
- Ensure your API keys have trading permissions
- Verify you have sufficient funds in your account
- Check that the trading pair is supported by your exchange
- Try adjusting the grid prices, quantities or other parameters

### Price Fetching Issues
- The script will attempt multiple methods to fetch prices
- If all methods fail, default values will be used based on the trading pair
- You can manually set upper_price and lower_price in config.py

## Architecture

- `main.py`: Entry point script for creating bots
- `check_api.py`: Script to validate API connection and trading pairs
- `monitor_bots.py`: Script to monitor bot performance
- `three_commas_client.py`: API client for 3Commas
- `grid_bot.py`: Grid Bot implementation
- `dca_bot.py`: DCA Bot implementation
- `config.py`: Configuration settings
- `.env`: API credentials file (not included in repository)

## Disclaimer

This software is for educational purposes only. Use at your own risk. Cryptocurrency trading involves significant risk and can result in the loss of your invested capital. The authors are not responsible for any financial losses incurred while using this software.

## License

MIT License