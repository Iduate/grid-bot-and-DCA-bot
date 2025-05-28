import time
from three_commas_client import ThreeCommasClient
from config import DCA_BOT_CONFIG, DEFAULT_EXCHANGE

class DCABot:
    def __init__(self, client, account_id=None, config=None):
        """
        Initialize the DCA Bot
        
        Args:
            client: ThreeCommasClient instance
            account_id: 3Commas account ID
            config: DCA bot configuration
        """
        self.client = client
        self.account_id = account_id
        self.config = config or DCA_BOT_CONFIG.copy()
        
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
    
    async def create_bot(self):
        """Create and start the DCA Bot"""
        if not self.account_id:
            await self.setup_account()
        
        print(f"Creating DCA Bot with config: {self.config}")
        
        try:
            bot = self.client.create_dca_bot(self.account_id, self.config)
            print(f"DCA Bot created: {bot.get('id')}")
            return bot
        except Exception as e:
            print(f"Error creating DCA Bot: {str(e)}")
            print("Troubleshooting suggestions:")
            print("1. Check if your API key has trading permissions")
            print("2. Verify you have sufficient funds in your account")
            print("3. Ensure your trading pair is correctly formatted")
            print("4. Try adjusting safety order parameters to match exchange requirements")
            raise
    
    async def start_bot(self, bot_id):
        """Start the DCA Bot"""
        result = self.client.start_bot(bot_id)
        print(f"DCA Bot started: {result}")
        return result
    
    async def stop_bot(self, bot_id):
        """Stop the DCA Bot"""
        result = self.client.stop_bot(bot_id)
        print(f"DCA Bot stopped: {result}")
        return result
    
    async def get_deals(self, bot_id):
        """Get deals for the DCA Bot"""
        deals = self.client.get_bot_deals(bot_id)
        return deals