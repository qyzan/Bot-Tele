import httpx
import json
import time
import random
import hashlib
import os
from colorama import *

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL

# Define the URL and headers for the request
url = "https://api-gw-tg.memefi.club/graphql"
headers = {
    "Sec-Ch-Ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?1",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY2NTYyMzZlZDBiYzMwYjk4N2EzZmJiMiIsInVzZXJuYW1lIjoibm90X3Byb3ZpZGVkIn0sInNlc3Npb25JZCI6IjY2NjJiMmI1NmE4ODNiNTNkNTkzZTBmNiIsInN1YiI6IjY2NTYyMzZlZDBiYzMwYjk4N2EzZmJiMiIsImlhdCI6MTcxNzc0NDMwOSwiZXhwIjoxNzE4MzQ5MTA5fQ.SOPRFjNRH1Q2Q3QhJnZnH-C6Ls1web-FYyLr4bi9xSw",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Mobile Safari/537.36",
    "Sec-Ch-Ua-Platform": "Android",
    "Origin": "https://tg-app.memefi.club",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://tg-app.memefi.club/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}

with open('payload.json', 'r') as file:
    payload = json.load(file)

def generate_nonce():
    return hashlib.sha256(os.urandom(32)).hexdigest()

def send_request():
    # Generate a random tapsCount that is a multiple of 8, between desired range, e.g., 8 and 800
    taps_count = random.choice(range(8, 25, 8))
    nonce = generate_nonce()
    
    # Update the payload with the generated nonce and tapsCount
    payload["variables"]["payload"]["nonce"] = nonce
    payload["variables"]["payload"]["tapsCount"] = taps_count
    
    try:
        response = httpx.post(url, headers=headers, json=payload)
        response_json = response.json()
        with open('.http_request.log', 'a') as log_file:
            log_file.write(f"Request payload: {json.dumps(payload)}\n")
            log_file.write(f"Response: {response.text}\n")
        
        # Extract and print only the currentEnergy and coinsAmount from the response
        data = response_json.get("data", {}).get("telegramGameProcessTapsBatch", {})
        current_energy = data.get("currentEnergy")
        coins_amount = data.get("coinsAmount")
        print("-"*80)
        print(f"{hijau}tapsCount: {putih}{taps_count}\n{hijau}nonce: {putih}{nonce}\n{hijau}currentEnergy: {putih}{current_energy}\n{hijau}coinsAmount: {putih}{coins_amount}")
        return current_energy
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        print(f"Next request in {mins:02d}:{secs:02d} ", flush=True, end="\r")
        time.sleep(1)
        seconds -= 1

def boost_energi():
    try:
        with open('boost.json', 'r') as file:
            payload_boost = json.load(file)

        response = httpx.post(url, headers=headers, json=payload_boost)
        response_json = response.json()
        with open('.http_request.log', 'a') as log_file:
            log_file.write(f"Request payload: {json.dumps(payload)}\n")
            log_file.write(f"ResponseBoost: {response.text}\n")
        # Extract and print only the currentEnergy and coinsAmount from the response
        if "errors" in response.text:
            with open('checkdata.json', 'r') as file:
                payload_check = json.load(file)
            check_data = httpx.post(url, headers=headers, json=payload_check)
            check_data_json = check_data.json()
            data = check_data_json.get("data", {}).get("telegramGameGetConfig", {})
            current_energy = data.get("currentEnergy")
            print(f"{hijau}Recharge Limit")

        elif "data" in response.text:
            boost = response_json.get("data", {}).get("freeBoosts", {})
            boost_coin = boost.get("currentTurboAmount")
            boost_refill = boost.get("currentRefillEnergyAmount")
            print(f'{hijau}Success Claim Recharge')
            
            print(f"Current Turbo :{boost_coin}, Don't Forget To Claim In Your Phone!!, Wait Untill Next Update")
            print(f"Current Refill :{boost_refill}, Don't Forget To Claim")
        else:
            print(f"Failed to Claim Refill {response.status_code}")
            
            # Re-fetch data after using boost
        return current_energy
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def next_boss():
    try:
        with open('nextboss.json', 'r') as file:
            payload_nextboos = json.load(file)

        response = httpx.post(url, headers=headers, json=payload_nextboos)
        if response.status_code == 200:
            print(f'{hijau}Success To Next Boss')
        else:
            print(f"Failed to Next Boss {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
def claim_rewardBoss():
    try:
        with open('claimboss.json', 'r') as file:
            payload_claimboos = json.load(file)

        response = httpx.post(url, headers=headers, json=payload_claimboos)
        if response.status_code == 200:
            print(f'{hijau}Success To Claim Reward Boss')
        else:
            print(f"Failed to Claim Reward Boss {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

def healthBoss():
    try:
        response = httpx.post(url, headers=headers, json=payload)
        response_json = response.json()
        boss = response_json.get("data", {}).get("telegramGameProcessTapsBatch", {}).get("currentBoss")
        boss_health = boss.get("currentHealth")
        print("-"*80)
        print(f"{kuning}HealthBoss: {boss_health}")
        return boss_health

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# Send the request repeatedly
banner = f"""
{putih}AUTO BOT {hijau}MemeFi 

{putih}By: {hijau}t.me/qyzannn
{putih}Github: {hijau}@qyzan

{hijau}Message: {putih}Don't Forget To Claim Everyday !
    """
print (banner)

while True:
    current_energy = send_request()
    random_time = random.randint(1,10)
    countdown_timer(random_time)
    boss_health = healthBoss()
    if current_energy is None:
        send_request()
    elif current_energy <= 100:
        boost_energi()
        if current_energy <= 100:
            print("-"*80)
            print(f"{merah}Current energy is 100, sleeping for 16 minutes.")
            countdown_timer(960)  # Sleep for 30 minutes
    elif boss_health == 0:
        claim_rewardBoss()
        time.sleep(3)
        next_boss()
    else:
       # Adjust the sleep duration as needed for regular requests
        random_time = random.randint(1,10)
        countdown_timer(random_time)
        # If there was an error and current_energy is None, wait a short period before retrying
    
