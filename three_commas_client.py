import hashlib
import hmac
import json
import time
from urllib.parse import urlencode
import requests
from py3cw.request import Py3CW

from config import API_URL, API_KEY, API_SECRET

class ThreeCommasClient:
    def __init__(self):
        # Using py3cw library for API calls
        self.client = Py3CW(
            key=API_KEY,
            secret=API_SECRET,
            request_options={
                'request_timeout': 30,
                'nr_of_retries': 3,
                'retry_status_codes': [500, 502, 503, 504]
            }
        )
        
    def get_accounts(self):
        """Get all accounts (exchanges) connected to 3Commas"""
        error, accounts = self.client.request(
            entity='accounts',
            action=''
        )
        if error:
            raise Exception(f"Error getting accounts: {error}")
        return accounts
    
    def get_market_pairs(self, market_code):
        """Get all available pairs for a specific market"""
        error, pairs = self.client.request(
            entity='accounts',
            action='market_pairs',
            payload={
                'market_code': market_code
            }
        )
        if error:
            raise Exception(f"Error getting market pairs: {error}")
        return pairs
    
    def get_currency_rate(self, pair):
        """Get current rate for a currency pair"""
        error, rate = self.client.request(
            entity='accounts',
            action='currency_rates',
            payload={
                'pair': pair
            }
        )
        if error:
            raise Exception(f"Error getting currency rate: {error}")
        return rate
    
    def create_grid_bot(self, account_id, config):
        """Create a Grid Bot with the specified configuration"""
        payload = {
            'account_id': account_id,
            'name': config['name'],
            'pair': config['pair'],
            'upper_price': config['upper_price'],
            'lower_price': config['lower_price'],
            'quantity_per_grid': config['quantity_per_grid'],
            'grids_count': config['grids_count'],
            'leverage_type': config['leverage_type'],
            'leverage_custom_value': config['leverage_custom_value'],
        }
        
        error, bot = self.client.request(
            entity='grid_bots',
            action='create',
            payload=payload
        )
        if error:
            raise Exception(f"Error creating grid bot: {error}")
        return bot
    
    def create_dca_bot(self, account_id, config):
        """Create a DCA Bot with the specified configuration"""
        payload = {
            'account_id': account_id,
            'name': config['name'],
            'pair': config['pair'],
            'base_order_volume': config['base_order_volume'],
            'safety_order_volume': config['safety_order_volume'],
            'max_safety_orders': config['max_safety_orders'],
            'max_active_safety_orders': config['max_active_safety_orders'],
            'martingale_volume_coefficient': config['martingale_volume_coefficient'],
            'martingale_step_coefficient': config['martingale_step_coefficient'],
            'take_profit': config['take_profit'],
            'safety_order_step_percentage': config['safety_order_step_percentage'],
            'strategy': config['strategy'],
            'active': True
        }
        
        error, bot = self.client.request(
            entity='bots',
            action='create_bot',
            payload=payload
        )
        if error:
            raise Exception(f"Error creating DCA bot: {error}")
        return bot
    
    def start_bot(self, bot_id):
        """Start a bot by ID"""
        error, response = self.client.request(
            entity='bots',
            action='enable',
            action_id=str(bot_id)
        )
        if error:
            raise Exception(f"Error starting bot: {error}")
        return response
    
    def stop_bot(self, bot_id):
        """Stop a bot by ID"""
        error, response = self.client.request(
            entity='bots',
            action='disable',
            action_id=str(bot_id)
        )
        if error:
            raise Exception(f"Error stopping bot: {error}")
        return response
    
    def get_bot_deals(self, bot_id):
        """Get deals for a specific bot"""
        error, deals = self.client.request(
            entity='bots',
            action='deals',
            payload={
                'bot_id': bot_id,
                'limit': 50
            }
        )
        if error:
            raise Exception(f"Error getting bot deals: {error}")
        return deals
    
    def get_market_info(self, pair):
        """Get market information for a pair"""
        error, info = self.client.request(
            entity='accounts',
            action='market_info',
            payload={
                'pair': pair
            }
        )
        if error:
            raise Exception(f"Error getting market info: {error}")
        return info
        
    def get_active_bots(self):
        """Get all active bots"""
        error, bots = self.client.request(
            entity='bots',
            action='',
            payload={
                'limit': 100,
                'scope': 'enabled'
            }
        )
        if error:
            raise Exception(f"Error getting active bots: {error}")
        return bots
