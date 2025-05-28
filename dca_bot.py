# filepath: c:\Users\USER\Desktop\New folder\dca_bot.py
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
            
            if not accounts or len(accounts) == 0:
                raise Exception("No exchange accounts found in your 3Commas account. Please connect an exchange in 3Commas first.")
                
            # Find account with the specified exchange
            for account in accounts:
                if account['market_code'].lower() == DEFAULT_EXCHANGE.lower():
                    self.account_id = account['id']
                    break
                    
            # If specified exchange not found but accounts exist, use the first available account
            if not self.account_id and accounts:
                self.account_id = accounts[0]['id']
                print(f"Warning: Exchange {DEFAULT_EXCHANGE} not found. Using {accounts[0]['market_code']} instead.")
                return
                
            if not self.account_id:
                raise Exception(f"No account found for exchange {DEFAULT_EXCHANGE}. Available exchanges: {', '.join([a['market_code'] for a in accounts])}")
    
    async def create_bot(self):
        """Create and start the DCA Bot"""
        if not self.account_id:
            await self.setup_account()
        
        print(f"Creating DCA Bot with config: {self.config}")
        
        bot = self.client.create_dca_bot(self.account_id, self.config)
        print(f"DCA Bot created: {bot.get('id')}")
        
        return bot
    
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
