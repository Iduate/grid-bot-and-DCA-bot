# 3Commas Trading Bots

This project implements Grid and DCA (Dollar-Cost Averaging) trading bots using the 3Commas API.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure the bots:
   - Edit the `.env` file with your 3Commas API credentials
   - Adjust bot settings in `config.py`

## Usage

Run all bots:
```
python main.py
```

Run only Grid bot:
```
python main.py --bot-type grid
```

Run only DCA bot:
```
python main.py --bot-type dca
```

Test mode (no actual bots will be created):
```
python main.py --test-mode
```

Specify a trading pair:
```
python main.py --pair BTC_USDT
```

Specify an account ID:
```
python main.py --account-id 12345678
```

## Bot Types

### Grid Bot
The Grid Bot creates a grid of buy and sell orders within a price range. It profits from price fluctuations within the range by buying low and selling high.

### DCA Bot
The DCA (Dollar-Cost Averaging) Bot implements a strategy that makes an initial purchase and then creates additional buy orders (safety orders) at lower prices if the market goes down, reducing the average purchase price.

## Configuration

You can adjust the bot configurations in the `config.py` file:

- `GRID_BOT_CONFIG`: Settings for the Grid Bot
- `DCA_BOT_CONFIG`: Settings for the DCA Bot

## Security

Your API credentials are stored in the `.env` file, which should never be shared or committed to a repository. The `.env` file is loaded by the application at runtime.
