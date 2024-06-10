import requests
import time
import json

# URL and headers for the request
url = 'https://tgames.bcsocial.net/panel/users/login'
claim_url = 'https://tgames.bcsocial.net/panel/games/claim'
data ='d967013396fb9bef82d9a03526e782a0424a2878ea813a85f6daccfbab4e7ce0'
date = '1717958690'
cookie = 'ci_session=vogqaue80fakhdu62s646cttg5i2jf2g; __cf_bm=zJJOiT.kPAp5eSe4VJ1LJWgDM3jz0C87fUoDYaz_xmQ-1717958014-1.0.1.1-TLfF59CewqHn0x0HNU4gWNJpjNPyVA.EE5DIX7atHQNqngxyq2o2H1WtELUDEkozcul8GgNIm.lp.Y2K5tv.hQ'

headers = {
    'Host': 'tgames.bcsocial.net',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
    'Content-Type': 'application/json',
    'Cookie': cookie,
    'Origin': 'https://tgames.bcsocial.net',
    'Priority': 'u=1, i',
    'Referer': 'https://tgames.bcsocial.net/game',
    'Sec-Ch-Ua': '"Android WebView";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Platform': '"Android"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G570Y Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6422.165 Mobile Safari/537.36',
    'X-Requested-With': 'org.telegram.messenger'
}

# Initial payload
payload = {
    "gameId": 1,
    "initData": {
        "query_id": "AAHyKYsdAwAAAPIpix3l84Ye",
        "user": "{\"id\":6938110450,\"first_name\":\"Khairul\",\"last_name\":\".\",\"username\":\"qyzann\",\"language_code\":\"en\",\"allows_write_to_pm\":true}",
        "auth_date": date,
        "hash": data
    },
    "externalId": 6938110450,
    "username": "qyzann",
    "firstName": "Khairul",
    "language": "en",
    "lastName": ".",
    "refId": ""
}

claim_payload = {}

def make_request(url,payload):
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def main():
    while True:
        response_data = make_request(url,payload)
        if response_data['code'] == 0 and response_data['message'] == 'ok':
            data = response_data['data']
            balance = data['balance']
            balanceFTN = data['balanceFTN']
            username = data['username']
            walletAddress = data['walletAddress']
            ftnRate = data['ftnRate']
            nextClaimTime = data['nextClaimTime']
            
            print(f"Username: {username}")
            print(f"Balance: {balance}")
            print(f"BalanceFTN: {balanceFTN}")
            print(f"WalletAddress: {walletAddress}")
            print(f"FTN Rate: {ftnRate}")
            print(f"Next claim in: {nextClaimTime} seconds")
            
            time.sleep(nextClaimTime)
            claim_response_data = make_request(claim_url, claim_payload)
            if claim_response_data and claim_response_data['code'] == 0 and claim_response_data['message'] == 'ok':
                print("Claim successful:", claim_response_data)
            else:
                print("Error in claim response:", claim_response_data)
        else:
            print("Error in response:", response_data)
            break

if __name__ == "__main__":
    main()
