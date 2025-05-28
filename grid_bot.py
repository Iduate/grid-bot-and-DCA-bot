import time
from three_commas_client import ThreeCommasClient
from config import GRID_BOT_CONFIG, DEFAULT_EXCHANGE

class GridBot:
    def __init__(self, client, account_id=None, config=None):
        """
        Initialize the Grid Bot
        
        Args:
            client: ThreeCommasClient instance
            account_id: 3Commas account ID
            config: Grid bot configuration
        """
        self.client = client
        self.account_id = account_id
        self.config = config or GRID_BOT_CONFIG.copy()
        
    async def setup_account(self):
        """Find and set account ID if not provided"""
        if not self.account_id:
            accounts = self.client.get_accounts()
            # Find account with the specified exchange
            for account in accounts:
                if account['market_code'].lower() == DEFAULT_EXCHANGE.lower():
                    self.account_id = account['id']
                    break
            if not self.account_id:
                raise Exception(f"No account found for exchange {DEFAULT_EXCHANGE}")
    
    async def calculate_grid_prices(self, margin_percent=5):
        """Calculate grid prices based on current market price"""
        rate_data = self.client.get_currency_rate(self.config['pair'])
        current_price = float(rate_data.get('last', 0))
        
        if not current_price:
            raise Exception(f"Failed to get current price for {self.config['pair']}")
        
        # Calculate upper and lower prices with margin_percent above and below current price
        upper_price = current_price * (1 + margin_percent / 100)
        lower_price = current_price * (1 - margin_percent / 100)
        
        self.config['upper_price'] = round(upper_price, 2)
        self.config['lower_price'] = round(lower_price, 2)
        
        print(f"Grid price range: {self.config['lower_price']} - {self.config['upper_price']}")
    
    async def create_bot(self):
        """Create and start the Grid Bot"""
        if not self.account_id:
            await self.setup_account()
            
        if not self.config['upper_price'] or not self.config['lower_price']:
            await self.calculate_grid_prices()
        
        print(f"Creating Grid Bot with config: {self.config}")
        
        bot = self.client.create_grid_bot(self.account_id, self.config)
        print(f"Grid Bot created: {bot.get('id')}")
        
        return bot
    
    async def start_bot(self, bot_id):
        """Start the Grid Bot"""
        result = self.client.start_bot(bot_id)
        print(f"Grid Bot started: {result}")
        return result
    
    async def stop_bot(self, bot_id):
        """Stop the Grid Bot"""
        result = self.client.stop_bot(bot_id)
        print(f"Grid Bot stopped: {result}")
        return result
