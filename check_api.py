# 3Commas API Check Script
# This script validates your 3Commas API connection and checks if your trading pairs are valid.

import asyncio
import requests  # Added import for HTTP requests
from three_commas_client import ThreeCommasClient
from config import GRID_BOT_CONFIG, DCA_BOT_CONFIG, DEFAULT_EXCHANGE

async def main():
    print("\n🔍 3Commas API Connection Checker")
    print("================================\n")
    
    try:
        print("🔄 Connecting to 3Commas API...")
        client = ThreeCommasClient()
        
        # Test API connection
        try:
            accounts = client.get_accounts()
            print(f"✅ API Connection successful! Found {len(accounts)} connected exchanges.")
            
            if len(accounts) == 0:
                print("\n⚠️ No exchange accounts connected to 3Commas!")
                print("Please follow these steps:")
                print("1. Log in to your 3Commas account")
                print("2. Go to 'My Exchanges' in the left sidebar")
                print("3. Click 'Connect Exchange' and follow the instructions")
                print("4. Come back and run this script again\n")
                return
            
            print("\n📊 Connected Exchanges:")
            for account in accounts:
                account_type = account.get('type', 'Unknown')
                print(f"- {account['name']} ({account['market_code']}), Type: {account_type}, ID: {account['id']}")
            
            # Get exchange from config
            print(f"\n🔍 Checking exchange: {DEFAULT_EXCHANGE}")
            exchange_found = False
            for account in accounts:
                if account['market_code'].lower() == DEFAULT_EXCHANGE.lower():
                    exchange_found = True
                    print(f"✅ Exchange '{DEFAULT_EXCHANGE}' found with account ID: {account['id']}")
                    break
            
            if not exchange_found:
                print(f"❌ Exchange '{DEFAULT_EXCHANGE}' not found among your connected exchanges!")
                print(f"Please update DEFAULT_EXCHANGE in config.py to one of: {', '.join([a['market_code'] for a in accounts])}")
            
            # Check trading pairs
            pairs_to_check = [GRID_BOT_CONFIG['pair'], DCA_BOT_CONFIG['pair']]
            unique_pairs = list(set(pairs_to_check))
            
            print(f"\n🔍 Checking trading pairs: {', '.join(unique_pairs)}")
            
            for exchange_account in accounts:
                exchange = exchange_account['market_code']
                print(f"\nChecking pairs on {exchange}...")
                
                try:
                    available_pairs = client.get_available_pairs(exchange)
                    if available_pairs:
                        print(f"Found {len(available_pairs)} available pairs on {exchange}")
                        
                        for pair in unique_pairs:
                            if pair in available_pairs:
                                print(f"✅ Pair '{pair}' is valid on {exchange}")
                            else:
                                print(f"❌ Pair '{pair}' NOT FOUND on {exchange}")
                                # Try to find similar pairs
                                if '_' in pair:
                                    base_currency = pair.split('_')[0]
                                    similar_pairs = [p for p in available_pairs if p.startswith(f"{base_currency}_")][:5]
                                    if similar_pairs:
                                        print(f"   Similar pairs you could use: {', '.join(similar_pairs)}")
                except Exception as e:
                    print(f"Error checking pairs on {exchange}: {e}")
            
            # Test price fetching
            print("\n🔍 Testing price fetching...")
            for pair in unique_pairs:
                try:
                    print(f"Fetching price for {pair}...")
                    rate_data = client.get_currency_rate(pair)
                    if rate_data and 'last' in rate_data:
                        print(f"✅ Price for {pair}: {rate_data['last']}")
                        
                        # For BTC_ETH, also check if we can calculate it from BTC/USDT and ETH/USDT
                        if pair in ['BTC_ETH', 'BTCETH']:
                            try:
                                print("   Verifying with direct calculation from BTCUSDT and ETHUSDT...")
                                headers = {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                                }
                                btc_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", headers=headers)
                                eth_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT", headers=headers)
                                
                                if btc_response.status_code == 200 and eth_response.status_code == 200:
                                    btc_data = btc_response.json()
                                    eth_data = eth_response.json()
                                    
                                    if 'price' in btc_data and 'price' in eth_data:
                                        btc_price = float(btc_data['price'])
                                        eth_price = float(eth_data['price'])
                                        binance_calculated_rate = btc_price / eth_price
                                        
                                        print(f"   ✅ Binance prices - BTC/USDT: {btc_price}, ETH/USDT: {eth_price}")
                                        print(f"   ✅ Calculated price from Binance: {binance_calculated_rate}")
                                        
                                        # Check if the calculated rate is close to the direct rate
                                        direct_rate = float(rate_data['last'])
                                        diff_percent = abs((binance_calculated_rate - direct_rate) / direct_rate * 100)
                                        
                                        if diff_percent < 5:
                                            print(f"   ✅ Rates match within {diff_percent:.2f}% difference")
                                        else:
                                            print(f"   ⚠️ Rates differ by {diff_percent:.2f}% - this might indicate an issue")
                                    else:
                                        print("   ⚠️ Missing price data in Binance response")
                                else:
                                    print(f"   ⚠️ Could not get data from Binance API: BTC status {btc_response.status_code}, ETH status {eth_response.status_code}")
                            except Exception as calc_error:
                                print(f"   ⚠️ Could not verify with calculation: {calc_error}")
                    else:
                        print(f"❌ Could not get price for {pair}: Missing 'last' in response")
                except Exception as e:
                    print(f"❌ Error fetching price for {pair}: {e}")
                    
                    # Try direct calculation for BTC_ETH when the main method fails
                    if pair in ['BTC_ETH', 'BTCETH']:
                        print("   Attempting direct calculation from BTCUSDT and ETHUSDT as fallback...")
                        try:
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                            }
                            btc_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", headers=headers)
                            eth_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT", headers=headers)
                            
                            if btc_response.status_code == 200 and eth_response.status_code == 200:
                                btc_data = btc_response.json()
                                eth_data = eth_response.json()
                                
                                if 'price' in btc_data and 'price' in eth_data:
                                    btc_price = float(btc_data['price'])
                                    eth_price = float(eth_data['price'])
                                    binance_calculated_rate = btc_price / eth_price
                                    
                                    print(f"   ✅ FALLBACK - BTC/USDT: {btc_price}, ETH/USDT: {eth_price}")
                                    print(f"   ✅ FALLBACK calculated price for BTC_ETH: {binance_calculated_rate}")
                                    print("      You can use this price for your grid bot configuration")
                                else:
                                    print("   ⚠️ Missing price data in Binance response")
                            else:
                                print(f"   ⚠️ Could not get data from Binance API: BTC status {btc_response.status_code}, ETH status {eth_response.status_code}")
                        except Exception as calc_error:
                            print(f"   ❌ Fallback calculation also failed: {calc_error}")
                            print("   ℹ️ Using default price estimate for BTC_ETH: 15.0")
                            print("      This is just an approximation - please verify current market price")
            
            print("\n✅ API check completed!")
            
        except Exception as e:
            print(f"❌ API connection error: {e}")
            print("\nPlease check:")
            print("1. Your API keys in the .env file")
            print("2. Your internet connection")
            print("3. The 3Commas service status")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
