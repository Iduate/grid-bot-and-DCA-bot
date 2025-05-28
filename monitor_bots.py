# 3Commas Bot Monitor
# This script monitors the performance of your active bots on 3Commas

import asyncio
import time
from three_commas_client import ThreeCommasClient

async def main():
    print("\n📊 3Commas Bot Monitor")
    print("====================\n")
    
    client = ThreeCommasClient()
    
    try:
        # Get account information
        accounts = client.get_accounts()
        print(f"Connected accounts: {len(accounts)}")
        
        for account in accounts:
            print(f"- {account['name']} ({account['market_code']})")
        
        # Monitor bots
        await monitor_bots(client)
        
    except Exception as e:
        print(f"Error: {e}")

async def monitor_bots(client, refresh_interval=60, iterations=None):
    """
    Monitor active bots and display their performance
    
    Args:
        client: ThreeCommasClient instance
        refresh_interval: Time in seconds between refreshes
        iterations: Number of times to refresh (None for infinite)
    """
    iteration = 0
    try:
        while iterations is None or iteration < iterations:
            iteration += 1
            
            print("\n" + "="*70)
            print(f"📊 Bot Status (Refresh #{iteration}) - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*70)
            
            # Get active bots
            active_bots = client.get_active_bots()
            print(f"\nActive bots: {len(active_bots)}")
            
            if not active_bots:
                print("No active bots found!")
            else:
                # Display bot information
                for bot in active_bots:
                    bot_id = bot.get('id', 'Unknown')
                    bot_name = bot.get('name', 'Unknown')
                    bot_type = bot.get('type', 'Unknown')
                    bot_pair = bot.get('pairs', 'Unknown')
                    profit_usd = bot.get('profit', {}).get('usd', 0)
                    profit_percent = bot.get('profit', {}).get('percent', 0)
                    
                    print(f"\nBot: {bot_name} (ID: {bot_id})")
                    print(f"Type: {bot_type}")
                    print(f"Pair: {bot_pair}")
                    print(f"Profit: ${profit_usd} ({profit_percent}%)")
                    
                    # Get recent deals for this bot
                    try:
                        deals = client.get_bot_deals(bot_id)
                        print(f"Recent deals: {len(deals)}")
                        
                        for i, deal in enumerate(deals[:3]):  # Show only last 3 deals
                            deal_id = deal.get('id', 'Unknown')
                            deal_status = deal.get('status', 'Unknown')
                            deal_profit = deal.get('final_profit', 'Unknown')
                            deal_created_at = deal.get('created_at', 'Unknown')
                            
                            print(f"  Deal {i+1}: ID {deal_id}, Status: {deal_status}, Profit: {deal_profit}")
                    except Exception as e:
                        print(f"  Could not get deals: {e}")
            
            if iterations is None or iteration < iterations:
                print(f"\nRefreshing in {refresh_interval} seconds... (Press Ctrl+C to exit)")
                await asyncio.sleep(refresh_interval)
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"Error during monitoring: {e}")

if __name__ == "__main__":
    asyncio.run(main())
