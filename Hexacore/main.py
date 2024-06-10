import httpx
import time
import random

# Define the URL and headers for the requests
base_url = "https://hexacore-tg-api.onrender.com/api"
headers = {
    "Sec-Ch-Ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?0",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2OTg3MDE3NzUyLCJ1c2VybmFtZSI6InF5emFubm4iLCJ0aW1lc3RhbXAiOjE3MTY5NzcwNzYuMzUyNDM2fQ.6EfUu3msb6QreBSgi-fbAgGKOxgPad98YOkuT6bBHds",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36",
    "Sec-Ch-Ua-Platform": "Windows",
    "Accept": "*/*",
    "Origin": "https://ago-wallet.hexacore.io",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://ago-wallet.hexacore.io/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}

random_tap = random.randint(1,100)
payload = {
    "taps": random_tap
}

passes = {
    "name":"7_day"
}

user_id = "6987017752"

def auto_tap():
    try:
        response = httpx.post(f"{base_url}/mining-complete", headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Request successful: {response.text}")
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_level_info():
    try:
        response = httpx.get(f"{base_url}/level", headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except Exception as e:
        print(f"An error occurred while getting level info: {e}")
        return None

def upgrade_level():
    try:
        response = httpx.post(f"{base_url}/upgrade-level", headers=headers)
        if response.status_code == 200:
            print("Upgrade successful.")
        else:
            print(f"Upgrade failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while upgrading level: {e}")

def available_taps():
    try:
        response = httpx.post(f"{base_url}/available-taps", headers=headers)
        print(f"Checking Tap......")
        if response.status_code == 200:
            response.json()
            tab = response.get("available_taps")
            print(f"Tap Available : {tab}")
            return tab
        else:
            print(f"Check tap failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while upgrading level: {e}")

def balance():
    try:
        response = httpx.post(f"{base_url}/balance/{user_id}", headers=headers)
        if response.status_code == 200:
            response.json()
            balance = response.get("balance")
            return balance
        else:
            print(f"Check tap failed with status code {response.status_code}")

    except Exception as e:
        print(f"An error occurred while upgrading level: {e}")

def buy_passes():
    try:
        response = httpx.post(f"{base_url}/buy-tap-passes", headers=headers, json=passes)
        if response.status_code == 200:
            response.json()
            passes = response.get("success")
            return passes
        else:
            print(f"Check tap failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while upgrading level: {e}")

def get_passes():
    try:
        response = httpx.post(f"{base_url}/get-tap-passes", headers=headers)
        if response.status_code == 200:
            response.json()
            get_passes = response.get("active_tap_pass")
            return get_passes
        else:
            print(f"Check tap failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while upgrading level: {e}")    


def countdown_timer(seconds):
    while seconds > 0:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        print(f"Next request in {hours:02d}:{minutes:02d}:{seconds:02d} ", flush=True, end="\r")
        time.sleep(1)
        seconds -= 1
    print(" " * 40, flush=True, end="\r")

# Continuously check and upgrade level if possible
while True:
    auto_tap()
    balance()
    level_info = get_level_info()
    if level_info:
        next_data = level_info
        while next_data:
            if next_data.get("upgrade_available") == "true":
                upgrade_level()
                break
            next_data = next_data.get("next_data")

    # Wait for 30 seconds before checking again
    countdown_timer(30)
