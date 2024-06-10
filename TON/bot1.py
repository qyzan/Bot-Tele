import time
import requests

# URL for the POST request
post_url = "https://toncatapult.com/user/claim-ton"

cookie = 'g_state={"i_l":0}; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzcxNSwiaWF0IjoxNzE3ODYzNDM5fQ.ZrjIRuL5wgaj0RJ_RJ5qyPNuh4IAx3WYZyXQk2xqsSo.CEYdMzrGpZAnGSjMPl0En18vXi5zKdF80wIhqnOhnSE'

cookies = [
    'g_state={"i_l":0}; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzczMSwiaWF0IjoxNzE3ODYzNzE5fQ.FgudnzozI91KWvpBkZzLl-kcetIgdK1YUDK-5mT-cbM.%2FtnD0NmGh%2F9vK3mmqRdefsabqdVP7%2FUEC4QFO7mL1Yk',
    'g_state={"i_l":0}; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzcxNSwiaWF0IjoxNzE3ODYzNDM5fQ.ZrjIRuL5wgaj0RJ_RJ5qyPNuh4IAx3WYZyXQk2xqsSo.CEYdMzrGpZAnGSjMPl0En18vXi5zKdF80wIhqnOhnSE',
    'g_state={"i_l":0}; g_csrf_token=aa44adcf601aee0c; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzY1MSwiaWF0IjoxNzE3ODY1NjQyfQ.W2VtnZ2Z2vJAywJh36FK9N4ynf3wpTGgiaRetNO33es.KOY9VHLDTFqt2qk3QU3%2FrXV7ZH1Xwd9uySm3J5iX3LQ',
    'g_state={"i_l":0}; g_csrf_token=1edb1148a961ad8f; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Nzg3OSwiaWF0IjoxNzE3ODY2MTE3fQ.1XpNBH_mzPLrmbFKHwsMGXEyNsLfWW_smYSBF3T8hkc.AHwIweEX6WNPtG40hrEilN5z%2BzNqdFQc0SfCys9%2BFgY',
    'g_state={"i_l":0}; g_csrf_token=39554d8b685e6a52; __task_to_earn-f__token=s%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Nzk5OCwiaWF0IjoxNzE3ODY3ODU5fQ.TgtkRD3QWxPaVwslrkmERZkG3UW596_sBWP_7evhbfE.IX%2BtAVpuI1Owl3AWBEb4Zl%2FsjX8K5jgIiGmy3arZyyQ'
]

# Headers for the POST request
headers = {
    "Cookie": cookie,
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
def wait_with_countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Waiting for {i} seconds...", end="\r")
        time.sleep(1)
    print("")

# Infinite loop to send requests every 2 minutes
while True:
    # Send the POST request
    response = requests.post(post_url, headers=headers, data=data)
    
    # Print the status code and response text
    response_json = response.json()

    if response_json.get("message") == "Please wait for 2 minutes before claiming again":
        wait_time = 2 * 60  # 2 minutes in seconds
        print("Server responded with a wait message. Waiting for 2 minutes before trying again.")
    else:
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        wait_time = 2 * 60  # If no wait message, wait a shorter period (e.g., 10 seconds)

    # Wait before the next request
    wait_with_countdown(wait_time)
    
    print("Sending the next request...")
