import time
import requests

# headers["authorization"] = f"Bearer {token}"

def send_request(clicks, balance, balance_from_clicks):
    # Current timestamp
    current_timestamp = int(time.time())
    new_time = str(current_timestamp)

    data = {
        "id": 9323049,
        "clicks": clicks, 
        "energy": 1,  # Tetap sama seperti sebelumnya
        "balance": balance,
        "balance_from_clicks": balance_from_clicks,
        "last_click_at": current_timestamp
    }

    # Headers for the GET request
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en,en-US;q=0.9,id-ID;q=0.8,id;q=0.7",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTMyMzA0OSwiaWF0IjoxNzE3OTI5OTQxLCJleHAiOjE3MTc5MzA4NDF9.lKOmvl5J3R_3A4Oay1fM5jbFSxPH9v9upEF2MV5lPLk",
        "Origin": "https://alohomora-bucket-fra1-prod-frontend-static.fra1.cdn.digitaloceanspaces.com",
        "Referer": "https://alohomora-bucket-fra1-prod-frontend-static.fra1.cdn.digitaloceanspaces.com/",
        "Sec-Ch-Ua": '"Android WebView";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G570Y Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.164 Mobile Safari/537.36",
        "X-Requested-With": "org.telegram.messenger"
    }

    # URL for the GET request
    get_url = "https://starfish-app-fknmx.ondigitalocean.app/wapi/api/users/9323049?timestamp="+ new_time +"&hash=query_id=AAHv9Ko-AwAAAO_0qj5hfJk4&user={%22id%22:7493842159,%22first_name%22:%22Qyzan%22,%22last_name%22:%22.%22,%22language_code%22:%22en%22,%22allows_write_to_pm%22:true}&auth_date=1717926806&hash=6ac13569df10b3b76c5976ba93e17fc1b61ca264bb450b08996474a1235e13a5"

    # Send the GET request
    get_response = requests.put(get_url, json=data, headers=headers)
    get_data = get_response.json()
    coin = get_data.get("balance")
    energy = get_data.get("energy")
    name = get_data.get("telegram_username")
    click = get_data.get("clicks")
    print(f"Name : {name}")
    print(f"Current Balance: {coin}")
    print(f"Current Energy: {energy}")
    print(f"Click : {click}")
    print("-"*80)

# Initial values
clicks = 2035
balance = 123054632
balance_from_clicks = 123055632

while True:  # Loop indefinitely
    try:
        send_request(clicks, balance, balance_from_clicks)
        clicks += 1  # Increment clicks by 1 each time
        balance += 2  # Increment balance by 2 each time
        balance_from_clicks += 2  # Increment balance_from_clicks by 2 each time
        time.sleep(3)  # Wait for 1 second before sending the next request

    except KeyboardInterrupt:
        print("Loop terminated by user.")
        break

    except Exception as e:
        print(f"An error occurred: {e}")
        break
