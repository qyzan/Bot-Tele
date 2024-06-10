import time
import requests
from bs4 import BeautifulSoup
import schedule
# URL for the POST request
post_url = "https://toncatapult.com/user/claim-ton"
balance_url = "https://toncatapult.com/user/dashboard"
wd_url = "https://toncatapult.com/user/withdrawal"

# List of cookies for the POST request
cookies = [
    'g_state={"i_l":0}; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzczMSwiaWF0IjoxNzE3ODYzNzE5fQ.FgudnzozI91KWvpBkZzLl-kcetIgdK1YUDK-5mT-cbM.%2FtnD0NmGh%2F9vK3mmqRdefsabqdVP7%2FUEC4QFO7mL1Yk',
    'g_state={"i_l":0}; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzcxNSwiaWF0IjoxNzE3ODYzNDM5fQ.ZrjIRuL5wgaj0RJ_RJ5qyPNuh4IAx3WYZyXQk2xqsSo.CEYdMzrGpZAnGSjMPl0En18vXi5zKdF80wIhqnOhnSE',
    'g_state={"i_l":0}; g_csrf_token=aa44adcf601aee0c; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzY1MSwiaWF0IjoxNzE3ODY1NjQyfQ.W2VtnZ2Z2vJAywJh36FK9N4ynf3wpTGgiaRetNO33es.KOY9VHLDTFqt2qk3QU3%2FrXV7ZH1Xwd9uySm3J5iX3LQ',
    'g_state={"i_l":0}; g_csrf_token=1edb1148a961ad8f; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Nzg3OSwiaWF0IjoxNzE3ODY2MTE3fQ.1XpNBH_mzPLrmbFKHwsMGXEyNsLfWW_smYSBF3T8hkc.AHwIweEX6WNPtG40hrEilN5z%2BzNqdFQc0SfCys9%2BFgY',
    'g_state={"i_l":0}; g_csrf_token=39554d8b685e6a52; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Nzk5OCwiaWF0IjoxNzE3ODY3ODU5fQ.TgtkRD3QWxPaVwslrkmERZkG3UW596_sBWP_7evhbfE.IX%2BtAVpuI1Owl3AWBEb4Zl%2FsjX8K5jgIiGmy3arZyyQ',
    'g_state={"i_l":0}; g_csrf_token=e92e20ecccd31d04; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA2MTUsImlhdCI6MTcxNzg5MTU2NH0.p2DkMAwEZPYmZhanvA8TkHV7EeYPcvpePDP5XworZFM.XBQWJsiGrbWa%2Bg4ck1ZbMAqsUQpndC2YZRwFDpbg5HM',
    'g_state={"i_l":0}; g_csrf_token=e255355744b34bdd; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA2MTksImlhdCI6MTcxNzg5MTY4OH0.DCbFs_B9C7WG8xmn6OWyIsyuvamJegAVSGwMg69FF6k.WPtP%2FHsNHBzJqXUZERa4wcHgdBwlfrWU%2FLrqV3B3TKE',
    'g_state={"i_l":0}; g_csrf_token=73d18540e71900e7; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA2MjEsImlhdCI6MTcxNzg5MTcyMX0._FyNnDkzjqJl2YzmV-BwKMUcws1Z3SNCjlWxiQKv7E0.hLPH05yTywzEuKckXmLRO1s4%2F1%2FR9rQNvL1y4GdpDVI',
    'g_state={"i_l":0}; g_csrf_token=6a239470dee54778; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA2MzEsImlhdCI6MTcxNzg5MTc1M30.7XBS_TfchopWloUQB4nPrQkZykBoz53pGPxnGinuwNY.ClSblpsBlzmrMiStJy9rGtZYZteN2nn1kQsIiZDbTE4',
    'g_state={"i_l":0}; g_csrf_token=a88369c865fbd87; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA2MzMsImlhdCI6MTcxNzg5MTc4NH0.t0GMy_x7EmV5qyetXt7fPjh2DpCZoHETpdp2Cd7t_lk.hYGHyf7PNx7udoN4uvJ7XhO9XY4Mpb5NGaa88mnmDRg'
]

# Headers template for the POST request
headers_template = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Accept": "*/*",
    "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Origin": "https://toncatapult.com",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Te": "trailers",
    "Connection": "keep-alive"
}

# Data for the POST request
data = "{}"

# Function to wait for a specified number of seconds with countdown
def wait_with_countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Waiting for {i} seconds...", end="\r")
        time.sleep(1)
    print("")

# Function to extract Activities Balance from HTML
def extract_activities_balance(html):
    soup = BeautifulSoup(html, 'html.parser')
    activities_balance_tag = soup.find('h6', string='Activities Balance')
    if activities_balance_tag:
        balance_value_tag = activities_balance_tag.find_next('h1')
        if balance_value_tag:
            return balance_value_tag.text.strip()
    return None

def Name(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Temukan input dengan atribut readonly di dalam form
    strong_tag = soup.find('strong')

# Jika tag <strong> ditemukan
    if strong_tag:
        # Mengambil teks di dalam tag <strong>
        invitation_code = strong_tag.text
        return invitation_code.strip()
    else:
        return None

def withdrawal(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Mencari tag <input> dengan id 'activities_balance'
    input_tag = soup.find('input', {'id': 'activities_balance'})

    # Jika tag <input> ditemukan
    if input_tag and 'value' in input_tag.attrs:
        # Mengambil nilai dari atribut 'value'
        activities_balance = input_tag['value']
        return activities_balance.strip()
    else:
        return None

def perform_auto_withdrawal():
    cookie = cookies[cookie_index]
    headers = headers_template.copy()
    headers["Cookie"] = cookie
    
    try:
        wd_res = requests.get(url=wd_url, headers=headers)
        if wd_res.status_code == 200:
            html_content = wd_res.text
            wd_balance = withdrawal(html_content)
            if wd_balance:
                print(f"wd_balance: {wd_balance}")

            # Perform the POST request for withdrawal
            data = {"type":"act","amount": wd_balance}
    
            auto_wd = requests.post(url=wd_url, data=data, headers=headers)
            print(f"Auto withdrawal response: {auto_wd.text}")
        else:
            print(f"Failed to retrieve withdrawal page. Status Code: {wd_res.status_code}")
    except requests.ConnectionError as e:
        print("Connection error occurred during withdrawal:", e)

def rotate_cookie(cookie_index):
    return (cookie_index + 1) % len(cookies)


schedule.every().day.at("00:00").do(perform_auto_withdrawal)
# Infinite loop to send requests
cookie_index = 0
while True:
    # Rotate cookie
    cookie = cookies[cookie_index]
    headers = headers_template.copy()
    headers["Cookie"] = cookie
    
    try:
        # Send the POST request
        response = requests.post(post_url, headers=headers, data=data)
        response1 = requests.get(url=balance_url, headers=headers)
        wd_res = requests.get(url=wd_url, headers=headers)
        auto_wd = requests.post(url=wd_res, headers=headers)

        if response1.status_code == 200:
            html_content = response1.text
            activities_balance = extract_activities_balance(html_content)
            nama = Name(html_content)
            if nama:
                print(f"Account : {nama}")
            if activities_balance:
                print(f"Activities Balance: {activities_balance}")
        # Parse the response JSON
        response_json = response.json()
        
        # Check if we need to wait for 2 minutes before trying again
        if response_json.get("message") == "Please wait for 2 minutes before claiming again":
            wait_time = 2 * 60  # 2 minutes in seconds
            print("Server responded with a wait message. Waiting for 2 minutes before trying again.")
        else:
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            wait_time = 3  # If no wait message, wait a shorter period (e.g., 10 seconds)
            
    except requests.ConnectionError as e:
        print("Connection error occurred:", e)
        wait_time = 30  # Wait 30 seconds before retrying on connection error

    # Move to the next cookie for the next request
    cookie_index = rotate_cookie(cookie_index)

    # Wait before the next request
    wait_with_countdown(wait_time)
    # Check the schedule
    schedule.run_pending()

    print("Sending the next request...")
    print("-"*80)


    
