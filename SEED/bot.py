import requests
import time
from datetime import datetime, timedelta
import pytz

def countdown(seconds):
    """Display a countdown timer for the specified number of seconds."""
    while seconds > 0:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds_left = divmod(remainder, 60)
        print(f"Next request in: {hours:02}:{minutes:02}:{seconds_left:02}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()  # New line for readability

def get_local_time(utc_time_str):
    """Convert UTC time string to local time."""
    # Parse the UTC time string
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Set the timezone to UTC
    utc_time = utc_time.replace(tzinfo=pytz.UTC)
    # Convert to local time
    local_time = utc_time.astimezone()
    return local_time

post_url = "https://elb.seeddao.org/api/v1/seed/claim"
get_url = "https://elb.seeddao.org/api/v1/profile"
headers = {
    "Sec-Ch-Ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
    "Accept": "application/json, text/plain, */*",
    "Sec-Ch-Ua-Mobile": "?1",
    "Telegram-Data": 'query_id=AAHyKYsdAwAAAPIpix33kcu0&user={"id":6938110450,"first_name":"Khairul","last_name":".","username":"qyzann","language_code":"id","allows_write_to_pm":true}&auth_date=1717959828&hash=64f375bc7755993fe7542da61384b17feb7d3fab857ff79494266f357cb5fe5c',
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Mobile Safari/537.36",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Origin": "https://cf.seeddao.org",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://cf.seeddao.org/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}

while True:
    try:
        # Send POST request
        post_response = requests.post(post_url, headers=headers)
        if post_response.status_code == 400:
            print("Too Early Claim")
            
        print(f"POST Response status code: {post_response.status_code}")
        print(f"POST Response text: {post_response.text}")

        # Send GET request
        get_response = requests.get(get_url, headers=headers)
        print(f"GET Response status code: {get_response.status_code}")

        if get_response.status_code == 200:
            response_data = get_response.json()
            name = response_data['data']['name']
            upgrades = response_data['data']['upgrades']
            last_claim_utc = response_data['data']['last_claim']

            print(f"Name: {name}")
            for upgrade in upgrades:
                cost = upgrade['cost']
                print(f"Upgrade Cost: {cost}")

            # Convert last_claim to local time
            last_claim_local = get_local_time(last_claim_utc)
            print(f"Last Claim (Local Time): {last_claim_local}")

            # Calculate the next claim time (3 hours after last_claim)
            next_claim_time = last_claim_local + timedelta(hours=3)
            print(f"Next Claim Time (Local Time): {next_claim_time}")

            # Calculate the countdown duration in seconds
            current_time = datetime.now(last_claim_local.tzinfo)
            countdown_duration = (next_claim_time - current_time).total_seconds()

            # Ensure the countdown is not negative
            if countdown_duration > 0:
                countdown(int(countdown_duration))
            else:
                print("The next claim time has already passed. Sending next request immediately.")
        else:
            print(f"Failed to get data. Status code: {get_response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Reconnecting...")
        time.sleep(10)  # Wait for 10 seconds before attempting to reconnect

    # Wait for the next request cycle if countdown was skipped
    time.sleep(1)
