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
            if not self.account_id and accounts:
                # If no account found for DEFAULT_EXCHANGE but accounts exist, use the first one
                self.account_id = accounts[0]['id']
                print(f"No account found for exchange {DEFAULT_EXCHANGE}, using account: {accounts[0]['name']}")
            if not self.account_id:
                raise Exception(f"No account found for exchange {DEFAULT_EXCHANGE}")
    
    async def calculate_grid_prices(self, margin_percent=5):
        """Calculate grid prices based on current market price"""
        try:
            print(f"Fetching current price for {self.config['pair']}...")
            
            # Try to get rate with current pair format
            try:
                rate_data = self.client.get_currency_rate(self.config['pair'])
                current_price = float(rate_data.get('last', 0))
            except Exception as rate_error:
                print(f"Error with initial rate fetch: {str(rate_error)}")
                
                # Try alternative pair format
                alt_pair = self.config['pair'].replace('_', '') if '_' in self.config['pair'] else f"{self.config['pair'][:3]}_{self.config['pair'][3:]}"
                print(f"Trying alternative pair format: {alt_pair}")
                
                try:
                    rate_data = self.client.get_currency_rate(alt_pair)
                    current_price = float(rate_data.get('last', 0))
                except Exception as alt_error:
                    print(f"Error with alternative rate fetch: {str(alt_error)}")
                    current_price = 0
            
            if not current_price:
                raise Exception(f"Failed to get current price for {self.config['pair']}")
            
            print(f"Current price for {self.config['pair']}: {current_price}")
            
            # Calculate upper and lower prices with margin_percent above and below current price
            upper_price = current_price * (1 + margin_percent / 100)
            lower_price = current_price * (1 - margin_percent / 100)
            
            self.config['upper_price'] = round(upper_price, 8)  # More precision for crypto
            self.config['lower_price'] = round(lower_price, 8)
            
            print(f"Grid price range: {self.config['lower_price']} - {self.config['upper_price']}")
            return True
        except Exception as e:
            print(f"Error calculating grid prices: {str(e)}")
            # Set some default values if price fetching fails
            print("Using default price range based on the trading pair")
            
            # Get the base and quote currency
            pair = self.config['pair']
            if '_' in pair:
                base, quote = pair.split('_')
            else:
                # Try to split without underscore (like BTCETH)
                if len(pair) >= 6:  # Most crypto symbols are 3 chars each
                    base = pair[:3]
                    quote = pair[3:6]
                else:
                    base = pair[:len(pair)//2]
                    quote = pair[len(pair)//2:]
            
            print(f"Base currency: {base}, Quote currency: {quote}")
            
            # Set default prices based on the pair
            if base == 'BTC' and quote == 'USDT':
                self.config['upper_price'] = 30000
                self.config['lower_price'] = 28000
            elif base == 'ETH' and quote == 'USDT':
                self.config['upper_price'] = 2000
                self.config['lower_price'] = 1800
            elif base == 'BTC' and quote == 'ETH':
                self.config['upper_price'] = 15.5
                self.config['lower_price'] = 14.5
            elif base == 'ETH' and quote == 'BTC':
                self.config['upper_price'] = 0.07
                self.config['lower_price'] = 0.065
            else:
                self.config['upper_price'] = 100
                self.config['lower_price'] = 90
                
            print(f"Default grid price range: {self.config['lower_price']} - {self.config['upper_price']}")
            return False
    
    async def create_bot(self):
        """Create and start the Grid Bot"""
        if not self.account_id:
            await self.setup_account()
            
        if not self.config['upper_price'] or not self.config['lower_price']:
            await self.calculate_grid_prices()
        
        print(f"Creating Grid Bot with config: {self.config}")
        
        try:
            bot = self.client.create_grid_bot(self.account_id, self.config)
            print(f"Grid Bot created: {bot.get('id')}")
            return bot
        except Exception as e:
            print(f"Error creating Grid Bot: {str(e)}")
            print("Troubleshooting suggestions:")
            print("1. Check if your API key has trading permissions")
            print("2. Verify you have sufficient funds in your account")
            print("3. Ensure your trading pair is correctly formatted")
            print("4. Try adjusting grid parameters to match exchange requirements")
            raise
    
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