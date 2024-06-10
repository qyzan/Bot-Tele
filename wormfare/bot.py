import os
import sys
import json
import time
import random
import requests
import datetime
from data import data_string
from urllib.parse import unquote
from colorama import init, Fore, Style
from base64 import b64decode

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL

class ConfigModel:
    def __init__(self, interval: int, sleep: int, min_energy: int, start_range: int, end_range: int):
        self.interval = interval
        self.sleep = sleep
        self.min_energy = min_energy
        self.start_range = start_range
        self.end_range = end_range

class Onchain:
    def __init__(self):
        self.headers = {
            'Sec-Ch-Ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
            'Accept': 'application/json, text/plain, */*',
            'X-Api-Key': '9m60AhO1I9JmrYIsWxMnThXbF3nDW4GHFA1rde5PKzJmRA9Dv6LZ2YXSM6vvwigC',
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
            'X-Api-Key': '9m60AhO1I9JmrYIsWxMnThXbF3nDW4GHFA1rde5PKzJmRA9Dv6LZ2YXSM6vvwigC'
        }
        self.has_recovery = False
        self.parsed_data = None

    def log(self, message):
        year, mon, day, hour, minute, second, a, b, c = time.localtime()
        mon = str(mon).zfill(2)
        hour = str(hour).zfill(2)
        minute = str(minute).zfill(2)
        second = str(second).zfill(2)
        print(f"{biru}[{year}-{mon}-{day} {hour}:{minute}:{second}] {message}")

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def parser_data(self, data):
        # Decode the URL-encoded string
        decoded_data = unquote(data)
        
        # Store the formatted data
        self.parsed_data = {"initData": decoded_data}
        return self.parsed_data

    def is_expired(self, token):
        header, payload, sign = token.split(".")
        depayload = b64decode(payload + "==").decode("utf-8")
        jepayload = json.loads(depayload)
        exp = jepayload["exp"]
        now = int(time.time())
        if now > int(exp):
            return True
        return False

    def refresh_token(self):
        data = open("")

    def main(self):
        banner = f"""
    {putih}AUTO Claim {hijau}WORMFARE BOT 
    
    {putih}By: {hijau}Qyzan
    {putih}Github: {hijau}Cari Surang
    
    {hijau}Message: {putih}
        """
        if len(sys.argv) <= 1:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        if not os.path.exists("data"):
            self.log(f"{merah}'data' file is not found!")
            open("data", "a")

        data = open("data", "r").read()
        if len(data) <= 0:
            self.log(f"{kuning}please fill 'data' file with your telegram data!")
            sys.exit()

        if not os.path.exists("token"):
            self.log(f"{kuning}token file is not found!")
            open("token", "a")
        token = open("token", "r").read()
        if len(token) <= 0:
            self.login(data)
            token = open("token", "r").read()

        if self.is_expired(token):
            self.login(data)
            token = open("token", "r").read()
        
        token = open("token", "r").read()
        config = json.loads(open("config.json").read())
        interval = config["interval"]
        sleep = config["sleep"]
        min_energy = config["min_energy"]
        click_range = config["click_range"]
        start = click_range["start"]
        end = click_range["end"]
        cfg = ConfigModel(interval, sleep, min_energy, start, end)
        if int(start) > int(end):
            self.log(f"{merah}the value of click range end must be higher than start value!")
            sys.exit()
        self.get_me(token)
        print("~" * 50)
        while True:
            if self.is_expired(token):
                self.login(data)
                token = open("token", "r").read()

            self.click(token, cfg)
            print("~" * 50)
            self.countdown(cfg.interval)

    def get_me(self, token):
        headers = self.headers
        headers["authorization"] = f"Bearer {token}"
        res = self.http("https://elcevb3oz4.execute-api.eu-central-1.amazonaws.com/user/profile", headers=headers)
        if res.status_code == 200:
            name = res.json()["username"]
            score = res.json()["score"]
            lastupdate = res.json()["lastUpdateTimestamp"]
            refill = res.json()["energyLeft"]
            wallet = res.json()["walletAddress"]
            rank = res.json()["rank"]
            if refill >= 1:
                self.has_recovery = True

            self.log(f"{hijau}login as : {putih}{name}")
            self.log(f"{hijau}wallet address: {putih}{wallet}")
            self.log(f"{hijau}rank : {putih}{rank}")
            return True

        self.log(f"{merah}failed fetch data info!, http status code: {kuning}{res.status_code}")
        return False

    def click(self, token: str, cfg: ConfigModel):
        _click = random.randint(cfg.start_range, cfg.end_range)
        now = datetime.datetime.now()
        times = int(now.timestamp() * 1000)
        data = {"amount": _click, "startTimestamp": times}
        headers = self.headers
        headers["authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json"
        headers["content-length"] = str(len(json.dumps(data)))
        res = self.http(
            "https://elcevb3oz4.execute-api.eu-central-1.amazonaws.com/game/save-clicks",
            headers,
            json.dumps(data),
        )
       
        if '"score"' in res.text:
            clicks = res.json()["totalEarnedScore"]
            energy = res.json()["energyLeft"]
            coins = res.json()["score"]
            self.log(f"{hijau}total Score: {putih}{clicks}")
            self.log(f"{hijau}total coin: {putih}{coins}")
            self.log(f"{hijau}total click: {putih}{_click}")
            self.log(f"{hijau}remaining energy: {putih}{energy}")
            if cfg.min_energy >= int(energy):
                if self.has_recovery:
                    value = json.dumps({"type": "full_energy"})
                    headers["content-length"] = str(len(value))
                    self.http("https://elcevb3oz4.execute-api.eu-central-1.amazonaws.com/game/activate-daily-boost",
                              headers=headers,
                              data=value,
                    )
                    self.has_recovery = False
                    return True

                self.countdown(cfg.sleep)

            return True
        
        self.log(f"{merah}failed to click, http status code: {kuning}{res.status_code}")
        return False

    def login(self, data):
        self.parser_data(data)
        data = self.parsed_data
        headers = self.headers
        headers["content-length"] = str(len(json.dumps(data)))
        while True:
            res = self.http(
                "https://elcevb3oz4.execute-api.eu-central-1.amazonaws.com/auth/login", headers, json.dumps(data)
            )
            if res.status_code == 200:
                token = res.json()["accessToken"]
                self.log(f"{hijau}success login!")
                open("token", "w").write(token)
                return True
                self.log(res.status_code)

            self.log(f"{merah}failed login with http status code: {kuning}{res.status_code}")
            self.log(f"{kuning}trying login again!")
            continue

    def http(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url, headers=headers)
                    open('.http_request.log', 'a').write(res.text + '\n')
                    return res

                res = requests.post(url, headers=headers, data=data)
                open('.http_request.log', 'a').write(res.text + '\n')
                return res
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.SSLError):
                self.log(f"{merah}connection error!")

if __name__ == "__main__":
    try:
        app = Onchain()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
