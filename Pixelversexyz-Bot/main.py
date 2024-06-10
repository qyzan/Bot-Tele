import requests
import time
import sys
import json
from loguru import logger

# Set up the logger with custom formatting and color
logger.remove()  # Remove default handler
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")

# The URL for the API endpoint
url = 'https://api-clicker.pixelverse.xyz/api/'
secret = '210bed50035d30b059d57ac222693dff00b42e969a0b1db5bbe4fa6604c19df3'
tgId = '6938110450'
userid = 'qyzann'
data = 'user=%7B%22id%22%3A6938110450%2C%22first_name%22%3A%22Khairul%22%2C%22last_name%22%3A%22.%22%2C%22username%22%3A%22qyzann%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=-1979330427079370649&chat_type=sender&auth_date=1717643435&hash=5df4cffccd751e9f2e06fd37f80087b0a22857b1eb6ed8f1e66545db075bbade'
headers = {
    'Secret': secret,
    'Sec-Ch-Ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Username': userid,
    'Tg-Id': tgId,
    'Initdata': data,
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://sexyzbot.pxlvrs.io',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://sexyzbot.pxlvrs.io/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Priority': 'u=1, i',
}

def make_request(method, endpoint, headers, data=None):
    while True:
        try:
            if method == 'GET':
                response = requests.get(url + endpoint, headers=headers)
            elif method == 'POST':
                response = requests.post(url + endpoint, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                logger.error(f"Bad Request (400) encountered for {url + endpoint}. Skipping this ID.")
                return None  # Return None to indicate the specific 400 error should skip to the next pet
            else:
                logger.error(f"Request failed: {e}. Retrying...")
                time.sleep(2)  # Wait for 2 seconds before retrying

def get_user_data(headers):
    logger.info("Getting user data...")
    return make_request('GET', 'users', headers)

def get_pets(headers):
    logger.info("Getting pets...")
    return make_request('GET', 'pets', headers)

def select_pet(headers, pet_id):
    logger.info(f"Selecting pet with id: {pet_id}")
    return make_request('POST', f'pets/user-pets/{pet_id}/select', headers)

def claim_pet_energy(headers):
    logger.info("Claiming pet energy")
    return make_request('POST', 'mining/claim', headers)

def level_up_pet(headers, pet_id):
    logger.info(f"Leveling up pet with id: {pet_id}")
    return make_request('POST', f'pets/user-pets/{pet_id}/level-up', headers)

def main():
    logger.info("Starting the clicker bot... with telegramUserId:" + tgId)

    try:
        while True:
            currentPetId = ""
            
            # Get user data
            user_data = get_user_data(headers)
            if user_data and '"telegramUserId"' in user_data:
                currentPetId = user_data['updatedAt']['id']

            # Get pets
            pets_data = get_pets(headers)
            list_pet = pets_data['data']
            logger.info("found " + str(len(list_pet)) + " pets")

            # Loop through pets
            for pet in list_pet:
                user_pet = pet['userPet']
                id_pet = user_pet['id']

                # Select pet
                pet_selected = select_pet(headers, id_pet)
                if pet_selected is None:
                    continue  # Skip to the next pet if a 400 error occurred

                currentPetId = id_pet
                # Get user data with current pet
                user_data = get_user_data(headers)
                if user_data:
                    clicks_count = user_data['clicksCount']
                    pet = user_data['pet']
                    pet_name = pet['pet']['name']
                    pet_energy = pet['energy']
                    level = pet['level']
                    level_up_price = pet['levelUpPrice']

                    logger.info(f"Pet name: {pet_name} - Energy: {pet_energy} - Level: {level} - Level up price: {level_up_price} - Coin: {clicks_count}")

                    if pet_energy > 0:
                        # Click pet
                        claim_response = claim_pet_energy(headers)
                        if claim_response:
                            next_claim = claim_response['nextFullRestorationDate']
                            claim_amount = claim_response['claimedAmount']
                            logger.success(f"Pet clicked, next claim: {next_claim}\n Coint Amount: {claim_amount}")
                            logger.info("Sleeping for 30 mnt")
                            time.sleep(1800)
                        else:
                            logger.info("Claim pet failed")

                    user_data = get_user_data(headers)
                    clicks_count = int(user_data['clicksCount'])

                    if clicks_count > level_up_price:
                        # Level up pet
                        level_up_response = level_up_pet(headers, id_pet)
                        if level_up_response:
                            level = level_up_response['level']
                            level_up_price = level_up_response['levelUpPrice']
                            clicks_count -= level_up_price
                            logger.success(f"Pet level up to {level}, next level price: {level_up_price}")
                        else:
                            break
                else:
                    logger.error(f"Error selecting pet: {user_data}")
                    time.sleep(1)

    except KeyboardInterrupt:
        print("Loop interrupted. Stopping...")

if __name__ == "__main__":
    main()
