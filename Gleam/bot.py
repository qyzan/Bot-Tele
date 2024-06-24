import requests
import json
import time
from colorama import init, Fore, Style

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL

banner = f"""
    {putih}AUTO Claim {hijau}GLEAM 
    
    {putih}By: {hijau}qyzan
    {putih}Github: {hijau}https://github.com/qyzan
    
    {hijau}Message: {putih}Dont Forget To Claim Every Day
        """
print(banner)
# Function to read the contents of a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Load payload from a file
payload_file_path = 'payload.json'  # Update this with the actual file path
payload = read_file(payload_file_path)

# Load cookies from a file
cookies_file_path = 'cookies.txt'  # Update this with the actual file path
cookie = read_file(cookies_file_path)

def countdown(seconds):
    """Display a countdown timer for the specified number of seconds."""
    while seconds > 0:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds_left = divmod(remainder, 60)
        print(f"Next in: {hours:02}:{minutes:02}:{seconds_left:02}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()


def login():
    # Set the headers
    headers = {
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Ngrok-Skip-Browser-Warning": "69420",
        "Accept-Language": "en-US",
        "Cookie": cookie,
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://app.gleam.bot",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.gleam.bot/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }

    # Set the URL
    url = "https://prod-api.gleam.bot/api/v1/accounts/auth"

    # Send the POST request
    response = requests.post(url, headers=headers, data=payload)

    # Print the response
    data = response.json()
    username = data['account']['username']
    id = data['account']['id']
    for balance in data['balances']:
        if balance['currency'] == 'GLEAM':
            amount_gleam = float(balance['amount'])  # Ubah ke float jika diperlukan
            break
    
    print(f'{putih}-'*80)
    print(f"{hijau}Id User : {putih}{id}")
    print(f"{hijau}Login as : {putih}{username}")
    print(f"{hijau}Balance GLEAM : {putih}{amount_gleam}")

    if response.status_code == 200:
        return response.json().get('token'), headers  # Adjust based on actual response structure
    else:
        raise Exception("Failed to obtain authorization token")
    
def CheckEnergy(auth_token, headers):
    # Extract initData from payload
    payload = json.loads(read_file(payload_file_path))
    init_data = payload['initData']

    # Update headers with the authorization token
    headers["Authorization"] = f"Bearer {auth_token}"

    # Set the URL for the second request
    url_claim = "https://prod-api.gleam.bot/api/v1/accounts/energy/refill/claim"
    url_start = "https://prod-api.gleam.bot/api/v1/accounts/energy/refill/start"

    # Create the payload for the second request
    new_payload = {
        "initData": init_data
    }

    # Send the second POST request
    claim = requests.post(url=url_claim, headers=headers, json=new_payload)
    start = requests.post(url=url_start, headers=headers, json=new_payload)
    data = claim.json()
    message = data.get('message')

    # Print the response
    if claim.status_code == 200:
        print(f"{hijau}Success to Claim Energy : {putih}{claim.status_code}")
    if start.status_code == 200:
        print(f"{hijau}Success to Start Energy : {putih}{claim.status_code}")
    else:
        print(f'{merah}Energi Sedang Proses Refill {claim.status_code}')

def checkProject(auth_token, headers):
    headers["Authorization"] = f"Bearer {auth_token}"
    url = 'https://prod-api.gleam.bot/api/v1/projects/list'
    
    response = requests.get(url, headers=headers)
    data = response.json()
    slugs = [project.get('slug') for project in data.get('projects', [])]
    return(slugs)
    

def quest(auth_token,slug):
    payload = json.loads(read_file(payload_file_path))
    init_data = payload['initData']
    new_payload = {
        "initData": init_data
    }
    headers["Authorization"] = f"Bearer {auth_token}"

    for project in slug:
        url = f'https://prod-api.gleam.bot/api/v1/projects/{project}/quests'
        print(f'{putih}-'*80)
        print(f'{hijau}Start Quest {project} ......')
        countdown(3)
        a = requests.get(url, headers=headers)
        if a.status_code == 200:
            json_data = a.json()
            quest_ids = [quest['id'] for quest in json_data.get('quests', [])]
            for quest_id in quest_ids:
                url_check = f"https://prod-api.gleam.bot/api/v1/quests/{quest_id}/check"
                url_start = f"https://prod-api.gleam.bot/api/v1/quests/{quest_id}/start"
                url_claim = f"https://prod-api.gleam.bot/api/v1/quests/{quest_id}/claim"
                
                response = requests.post(url=url_start, headers=headers, json=new_payload)
                data = response.json()
                message = data.get('message')
                title = data['quest']['title']
                if response.status_code == 200:
                    start = requests.post(url=url_check, headers=headers, json=new_payload)
                    if start.status_code == 200:
                        print(f'{hijau}Success to Start Quest : {putih}{title} - {start.status_code}')
                    claim = requests.post(url=url_claim, headers=headers, json=new_payload)
                    if claim.status_code == 200:
                        print(f'{hijau}Success to Claim Quest : {putih}{title} - {claim.status_code}')
                    print(f'{putih}-'*80)

                elif message == "Insufficient energy." :
                    print(f'{merah}Energi Habis Bro..')
                    CheckEnergy(auth_token, headers)
                    countdown(10800)
                    break
                elif message == 'This quest has already been processed or completed.':
                    print(f'{biru}This quest has already been processed or completed.')
                    print(f'{hijau}Next Request....')
                    continue
                else:
                    print(response.status_code)
                    continue              

while True:
    try:
        # Login and obtain token, headers
        token, headers = login()

        # Fetch project slugs
        slug = checkProject(token, headers)

        # Perform quests
        quest(token, slug)

    except Exception as e:
        print(f'Error: {str(e)}')
