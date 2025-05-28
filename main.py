import asyncio
import argparse
from three_commas_client import ThreeCommasClient
from grid_bot import GridBot
from dca_bot import DCABot
from config import GRID_BOT_CONFIG, DCA_BOT_CONFIG

async def main():
    parser = argparse.ArgumentParser(description='3Commas Trading Bot')
    parser.add_argument('--bot-type', choices=['grid', 'dca', 'all'], default='all',
                        help='Type of bot to run (grid, dca, or all)')
    parser.add_argument('--pair', type=str, help='Trading pair (e.g. BTC_USDT)')
    parser.add_argument('--account-id', type=int, help='3Commas account ID')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode without creating actual bots')
    
    args = parser.parse_args()
    
    client = ThreeCommasClient()
    
    # Update configs if pair is provided
    if args.pair:
        GRID_BOT_CONFIG['pair'] = args.pair
        DCA_BOT_CONFIG['pair'] = args.pair
    
    try:
        # Get account information
        accounts = client.get_accounts()
        print(f"Available accounts: {len(accounts)}")
        
        if len(accounts) == 0:
            print("\n⚠️ No exchange accounts connected to 3Commas!")
            print("Please follow these steps:")
            print("1. Log in to your 3Commas account")
            print("2. Go to 'My Exchanges' in the left sidebar")
            print("3. Click 'Connect Exchange' and follow the instructions")
            print("4. Come back and run this script again\n")
            return
        
        for account in accounts:
            print(f"Account: {account['name']} ({account['market_code']}), ID: {account['id']}")
        
        account_id = args.account_id
        if not account_id and accounts:
            account_id = accounts[0]['id']
            print(f"Using account ID: {account_id}")
        
        # Test mode notification
        if args.test_mode:
            print("\n*** RUNNING IN TEST MODE - NO ACTUAL BOTS WILL BE CREATED ***\n")
        
        # Create and start bots based on selected type
        if args.bot_type in ['grid', 'all']:
            grid_bot = GridBot(client, account_id)
            print(f"Grid Bot configuration: {grid_bot.config}")
            
            if not args.test_mode:
                grid_bot_data = await grid_bot.create_bot()
                if grid_bot_data:
                    bot_id = grid_bot_data.get('id')
                    if bot_id:
                        await grid_bot.start_bot(bot_id)
            else:
                print("Test mode: Grid Bot would be created with the above configuration")
        
        if args.bot_type in ['dca', 'all']:
            dca_bot = DCABot(client, account_id)
            print(f"DCA Bot configuration: {dca_bot.config}")
            
            if not args.test_mode:
                dca_bot_data = await dca_bot.create_bot()
                if dca_bot_data:
                    bot_id = dca_bot_data.get('id')
                    if bot_id:
                        await dca_bot.start_bot(bot_id)
            else:
                print("Test mode: DCA Bot would be created with the above configuration")
                    
        # Display active bots
        if not args.test_mode:
            active_bots = client.get_active_bots()
            print(f"\nActive bots: {len(active_bots)}")
            
            for bot in active_bots:
                print(f"Bot: {bot['name']}, Type: {bot['type']}, Pair: {bot['pairs']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())