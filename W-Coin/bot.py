import time
import requests
import json

hash='query_id=AAHv9Ko-AwAAAO_0qj5hfJk4&user={%22id%22:7493842159,%22first_name%22:%22Qyzan%22,%22last_name%22:%22.%22,%22language_code%22:%22en%22,%22allows_write_to_pm%22:true}&auth_date=1717926806&hash=6ac13569df10b3b76c5976ba93e17fc1b61ca264bb450b08996474a1235e13a5'

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en,en-US;q=0.9,id-ID;q=0.8,id;q=0.7",
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

def login():
    post_url = "https://starfish-app-fknmx.ondigitalocean.app/wapi/api/auth/local?hash="+hash
    auth_data = {"identifier":"7493842159","password":"7493842159"}
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://alohomora-bucket-fra1-prod-frontend-static.fra1.cdn.digitaloceanspaces.com",
        "Referer": "https://alohomora-bucket-fra1-prod-frontend-static.fra1.cdn.digitaloceanspaces.com/",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i",
        "Sec-Ch-Ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Ch-Ua-Mobile": "?1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Mobile Safari/537.36"
    }
    post_response = requests.post(post_url, json=auth_data, headers=headers)
    res = post_response.json()
    auth = res.get("jwt")
    if auth:
        print ("Success Login!!!")
        with open("auth_token", "w") as token_file:
            json.dump({"jwt": auth}, token_file)
    return auth

def get_token():
    try:
        with open("auth_token", "r") as token_file:
            data = json.load(token_file)
            return data.get("jwt")
    except FileNotFoundError:
        return None

def send_request(clicks, balance, balance_from_clicks,energy):
    current_timestamp = int(time.time())
    token = get_token()
    headers["Authorization"] = f"Bearer {token}"
    data = {
        "id": 9323049,
        "clicks": clicks,
        "energy": energy,
        "balance": balance,
        "balance_from_clicks": balance_from_clicks,
        "last_click_at": current_timestamp
    }
    get_url = f"https://starfish-app-fknmx.ondigitalocean.app/wapi/api/users/9323049?timestamp={current_timestamp}&hash={hash}"
    get_response = requests.put(get_url, json=data, headers=headers)
    if get_response.status_code == 401:
        login()
        token2 = get_token()
        headers["Authorization"] = f"Bearer {token2}"
        get_response = requests.put(get_url, json=data, headers=headers)
        get_data = get_response.json()
        coin = get_data.get("balance")
        energy = get_data.get("energy")
        name = get_data.get("telegram_username")
        click = get_data.get("clicks")
    else:
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

def get_me():
    current_timestamp = int(time.time())
    token = get_token()
    headers["Authorization"] = f"Bearer {token}"
    get_url = f"https://starfish-app-fknmx.ondigitalocean.app/wapi/api/users/me?timestamp={current_timestamp}&hash={hash}"
    get_response = requests.get(get_url, headers=headers)
    if get_response.status_code == 401:
        login()
        token1 = get_token()
        headers["Authorization"] = f"Bearer {token1}"
        get_response = requests.get(get_url, headers=headers)
        print(get_response)
        get_data = get_response.json()
        clicks = get_data.get("clicks")  # Default to 0 if None
        balance = get_data.get("balance")  # Default to 0 if None
        energy = get_data.get("energy")  # Default to 0 if None
        with open("user_data.json", "w") as data_file:
            json.dump({"clicks": clicks, "balance": balance, "energy": energy}, data_file)
    else:
        get_data = get_response.json()
        clicks = get_data.get("clicks")  # Default to 0 if None
        balance = get_data.get("balance")  # Default to 0 if None
        energy = get_data.get("energy")  # Default to 0 if None
        with open("user_data.json", "w") as data_file:
            json.dump({"clicks": clicks, "balance": balance, "energy": energy}, data_file)

login()
get_me()
with open("user_data.json", "r") as user_file:
    data = json.load(user_file)
    clicks = int(data.get("clicks"))
    balance = int(data.get("balance"))
    balance_from_clicks = int(data.get("balance"))
    energy = int(data.get("energy"))

while True:
    try:
        send_request(clicks, balance, balance_from_clicks,energy)
        clicks += 100
        balance += 100
        balance_from_clicks += 100
        time.sleep(3)
    except KeyboardInterrupt:
        print("Loop terminated by user.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
