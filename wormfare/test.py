import os
import sys
import requests
def get_me(token):
    headers = {
        'Sec-Ch-Ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
        'Accept': 'application/json, text/plain, */*',
        'X-Api-Key': '9m60AhO1I9JmrYIsWxMnThXbF3nDW4GHFA1rde5PKzJmRA9Dv6LZ2YXSM6vvwigC',
        'Content-Type': 'application/json',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
        'Origin': 'https://clicker.wormfare.com',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://clicker.wormfare.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': 'u=1, i',
        'Sec-Ch-Ua-Platform': '"Android"'
    }
    headers["Authorization"] = f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjY5ODcwMTc3NTIsImlhdCI6MTcxNjczMzkzNiwiZXhwIjoxODQyODc3OTM2fQ.qsxsPPQiY9UZ9vMz5sdZKQevsuv8rvMAv_isB1lginQ"  # Corrected header key
    print (headers)
    res = requests.get("https://elcevb3oz4.execute-api.eu-central-1.amazonaws.com/user/profile", headers=headers)
    
    # Print response for debugging purposes
    print(res)
    print(res.text)
    
    if res.status_code == 200:
        data = res.json()
        name = data.get("username")
        score = data.get("score")
        last_update = data.get("lastUpdateTimestamp")
        energy_left = data.get("energyLeft")
        
        print(f"Username: {name}")
        print(f"Score: {score}")
        print(f"Last Update Timestamp: {last_update}")
        print(f"Energy Left: {energy_left}")
        
        return True
    elif res.status_code == 401:
        print("Unauthorized: Please check your token.")
    else:
        print(f"Failed to fetch data. HTTP status code: {res.status_code}")
        
    return False
if __name__ == "__main__":
    # Example usage
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjY5ODcwMTc3NTIsImlhdCI6MTcxNjczMzkzNiwiZXhwIjoxODQyODc3OTM2fQ.qsxsPPQiY9UZ9vMz5sdZKQevsuv8rvMAv_isB1lginQ"
    get_me(token)
