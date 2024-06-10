import requests
import time
import json

# URL and headers for the POST request
url_tap = "https://api.hamsterkombat.io/clicker/tap"
url_boosts_for_buy = "https://api.hamsterkombat.io/clicker/boosts-for-buy"
url_buy_boost = "https://api.hamsterkombat.io/clicker/buy-boost"
url_sync = "https://api.hamsterkombat.io/clicker/sync"

auth = "Bearer 1717944365980kYNjXkYZzawvCuEVsF7BGP4rANOFscGhD4v1G9vkOG0NX1njEOfXYfCdYDCKbrDC6938110450"
headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
    "Connection": "keep-alive",
    "Host": "api.hamsterkombat.io",
    "Origin": "https://hamsterkombat.io",
    "Referer": "https://hamsterkombat.io/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G570Y Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.165 Mobile Safari/537.36",
    "X-Requested-With": "org.telegram.messenger",
    "accept": "application/json",
    "authorization": auth,
    "content-type": "application/json",
    "sec-ch-ua": '"Android WebView";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"'
}

def sync():
    response = requests.post(url_sync, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        sync = response_json.get("clickerUser", {})
        available_taps = sync.get("availableTaps", 0)
        return available_taps
    else:
        print(f"Failed to get sync: {response.status_code}, {response.text}")
        return 0

# Function to send the POST request and print desired data
def send_post_request():
    tap = sync()
    timestamp = int(time.time())  # Current timestamp
    data = {
        "count": 1000,
        "availableTaps": tap,
        "timestamp": timestamp
    }
    response = requests.post(url_tap, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        clicker_user = response_json.get("clickerUser", {})
        user_id = clicker_user.get("id", "")
        total_coins = clicker_user.get("totalCoins", 0)
        balance_coins = clicker_user.get("balanceCoins", 0)
        level = clicker_user.get("level", 0)
        available_taps = clicker_user.get("availableTaps", 0)
        
        print(f"ID: {user_id}")
        print(f"Total Coins: {total_coins}")
        print(f"Balance Coins: {balance_coins}")
        print(f"Level: {level}")
        print(f"Available Taps: {available_taps}")
        print("-"*80)
        boost_for_buy(balance_coins)
    else:
        print(f"Failed to get a tap: {response.status_code}, {response.text}")

# Function to check and buy boost if conditions are met
def boost_for_buy(balance_coins):
    response = requests.post(url_boosts_for_buy, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        boosts = response_json.get("boostsForBuy", [])
        for boost in boosts:
            boost_id = boost.get("id")
            boost_price = boost.get("price", 0)
            cooldown_seconds = boost.get("cooldownSeconds", 0)
            level = boost.get("level", 0)
            print(f"Boost ID: {boost_id}, Price: {boost_price}, Cooldown: {cooldown_seconds}")

            if boost_id == "BoostMaxTaps":
                if boost_price <= balance_coins:
                    buy_boost(boost_id)
                else:
                    print(f"Balance coins do not match the price of {boost_id}. Balance Coins: {balance_coins}, Boost Price: {boost_price}")
                    print("-"*80)
            elif boost_id == "BoostEarnPerTap":
                if boost_price <= balance_coins:
                    buy_boost(boost_id)
                else:
                    print(f"Balance coins do not match the price of {boost_id}. Balance Coins: {balance_coins}, Boost Price: {boost_price}")
                    print("-"*80)
            elif boost_id == "BoostFullAvailableTaps":
                if cooldown_seconds == 0:
                    if level <= 5:
                        buy_boost(boost_id)
                    else:
                        print("Limit Boost Full Energy...")
                        print("-"*80)
                else:
                    print(f"Boost {boost_id} is in cooldown. Cooldown Seconds: {cooldown_seconds}")
                    print("-"*80)
            else:
                print(f"Unknown boost ID: {boost_id}")
    else:
        print(f"Failed to get boosts for buy: {response.status_code}, {response.text}")

def buy_boost(boost_id):
    timestamp = int(time.time())  # Current timestamp
    buy_data = {
        "boostId": boost_id,
        "timestamp": timestamp
    }
    buy_response = requests.post(url_buy_boost, headers=headers, data=json.dumps(buy_data))
    if buy_response.status_code == 200:
        print(f"{boost_id} purchased successfully.")
    else:
        print(f"Failed to purchase {boost_id}: {buy_response.status_code}, {buy_response.text}")

# Delay between requests in seconds
def countdown(timer):
    while timer:
        mins, secs = divmod(timer, 60)
        timer_format = '{:02d}:{:02d}'.format(mins, secs)
        print(timer_format, end='\r')
        time.sleep(1)
        timer -= 1
    
    print("Next Request....")

# Send repeated POST requests
while True:
    taps = sync()
    if taps <= 100:
        print(f"Energy not available: {taps}")
        print(f'Countdown time! Let\'s get a coffee!')
        countdown(900)

    send_post_request()
    countdown(3)
