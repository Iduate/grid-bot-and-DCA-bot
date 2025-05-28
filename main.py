import asyncio
import argparse
from three_commas_client import ThreeCommasClient
from grid_bot import GridBot
from dca_bot import DCABot
from config import GRID_BOT_CONFIG, DCA_BOT_CONFIG, DEFAULT_EXCHANGE

async def main():
    parser = argparse.ArgumentParser(description='3Commas Trading Bot')
    parser.add_argument('--bot-type', choices=['grid', 'dca', 'all'], default='all',
                        help='Type of bot to run (grid, dca, or all)')
    parser.add_argument('--pair', type=str, help='Trading pair (e.g. BTC_ETH)')
    parser.add_argument('--account-id', type=int, help='3Commas account ID')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode without creating actual bots')
    
    args = parser.parse_args()
    
    print("\n🔄 Connecting to 3Commas API...")
    client = ThreeCommasClient()
    
    # Update configs if pair is provided
    if args.pair:
        GRID_BOT_CONFIG['pair'] = args.pair
        DCA_BOT_CONFIG['pair'] = args.pair
    
    try:
        # Fetch and display available trading pairs for reference
        print("📋 Fetching available trading pairs...")
        try:
            available_pairs = client.get_available_pairs('binance')
            if available_pairs:
                print(f"First 5 available pairs on Binance: {available_pairs[:5]}")
                print(f"Total available pairs: {len(available_pairs)}")
                
                # Check if the configured pair exists
                configured_pair = GRID_BOT_CONFIG['pair']
                if configured_pair in available_pairs:
                    print(f"✅ Pair '{configured_pair}' is valid")
                else:
                    print(f"⚠️ Warning: Pair '{configured_pair}' was not found in available pairs")
                    # Try to find similar pairs
                    similar_pairs = [p for p in available_pairs if configured_pair.split('_')[0] in p]
                    if similar_pairs:
                        print(f"Similar pairs found: {similar_pairs[:5]}")
                        print(f"Consider using one of these instead")
        except Exception as e:
            print(f"Note: Could not fetch available pairs: {e}")
        
        # Get account information
        print("\n📊 Checking exchange accounts...")
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
            account_type = account.get('type', 'Unknown')
            print(f"Account: {account['name']} ({account['market_code']}), Type: {account_type}, ID: {account['id']}")
        
        account_id = args.account_id
        if not account_id and accounts:
            # Try to find the account for the specified exchange
            for account in accounts:
                if account['market_code'].lower() == DEFAULT_EXCHANGE.lower():
                    account_id = account['id']
                    print(f"Found account for {DEFAULT_EXCHANGE}: {account['name']} (ID: {account_id})")
                    break
            
            # If no account found for DEFAULT_EXCHANGE, use first account
            if not account_id:
                account_id = accounts[0]['id']
                print(f"No account found for {DEFAULT_EXCHANGE}, using account: {accounts[0]['name']} (ID: {account_id})")
        
        # Test mode notification
        if args.test_mode:
            print("\n🧪 *** RUNNING IN TEST MODE - NO ACTUAL BOTS WILL BE CREATED ***\n")
        
        # Create and start bots based on selected type
        if args.bot_type in ['grid', 'all']:
            try:
                grid_bot = GridBot(client, account_id)
                print(f"Grid Bot configuration: {grid_bot.config}")
                
                if not args.test_mode:
                    try:
                        print("\n🔨 Creating Grid Bot...")
                        grid_bot_data = await grid_bot.create_bot()
                        if grid_bot_data:
                            bot_id = grid_bot_data.get('id')
                            if bot_id:
                                print(f"🚀 Starting Grid Bot (ID: {bot_id})...")
                                await grid_bot.start_bot(bot_id)
                                print(f"✅ Grid Bot successfully created and started!")
                    except Exception as grid_error:
                        print(f"❌ Grid Bot creation failed: {grid_error}")
                        print("\n⚠️ Troubleshooting tips:")
                        print("1. Verify your API keys have trading permissions")
                        print("2. Check that you have sufficient funds in your account")
                        print("3. Verify the trading pair is supported by your exchange")
                        print("4. Try adjusting the grid prices or quantity")
                else:
                    print("Test mode: Grid Bot would be created with the above configuration")
            except Exception as e:
                print(f"❌ Error setting up Grid Bot: {e}")
        
        if args.bot_type in ['dca', 'all']:
            try:
                dca_bot = DCABot(client, account_id)
                print(f"DCA Bot configuration: {dca_bot.config}")
                
                if not args.test_mode:
                    try:
                        print("\n🔨 Creating DCA Bot...")
                        dca_bot_data = await dca_bot.create_bot()
                        if dca_bot_data:
                            bot_id = dca_bot_data.get('id')
                            if bot_id:
                                print(f"🚀 Starting DCA Bot (ID: {bot_id})...")
                                await dca_bot.start_bot(bot_id)
                                print(f"✅ DCA Bot successfully created and started!")
                    except Exception as dca_error:
                        print(f"❌ DCA Bot creation failed: {dca_error}")
                        print("\n⚠️ Troubleshooting tips:")
                        print("1. Verify your API keys have trading permissions")
                        print("2. Check that you have sufficient funds in your account")
                        print("3. Verify the trading pair is supported by your exchange")
                        print("4. Try adjusting the base order volume or safety orders")
                else:
                    print("Test mode: DCA Bot would be created with the above configuration")
            except Exception as e:
                print(f"❌ Error setting up DCA Bot: {e}")
                    
        # Display active bots
        if not args.test_mode:
            try:
                print("\n📊 Checking active bots...")
                active_bots = client.get_active_bots()
                print(f"Active bots: {len(active_bots)}")
                
                if active_bots:
                    print("\nCurrent active bots:")
                    for bot in active_bots:
                        bot_type = bot.get('type', 'Unknown')
                        bot_pairs = bot.get('pairs', 'Unknown')
                        profit = bot.get('profit', {}).get('usd', 0)
                        print(f"Bot: {bot['name']}, Type: {bot_type}, Pair: {bot_pairs}, Profit: ${profit}")
                else:
                    print("No active bots found. The bots might still be initializing.")
            except Exception as bot_error:
                print(f"Could not retrieve active bots: {bot_error}")
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("\nPlease check:")
        print("1. Your API keys in the .env file")
        print("2. Your internet connection")
        print("3. The 3Commas service status")
        print("4. Run with --test-mode flag to check configuration without creating bots")

if __name__ == "__main__":
    asyncio.run(main())
