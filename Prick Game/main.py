import json
import time
import random
import ssl
import websocket
from colorama import *
import threading

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL

def generate_timestamps(count, interval_ms):
    """
    Generates a list of Unix timestamps in milliseconds.

    :param count: Number of timestamps to generate.
    :param interval_ms: Interval between timestamps in milliseconds.
    :return: List of timestamps in milliseconds.
    """
    current_time = int(time.time() * 1000)
    return [current_time + i * interval_ms for i in range(count)]

def on_message(ws, message):
    x = json.loads(message)
    data = x.get("data")
    while True:
        data = {"action":"up_energy","data":5000}
        ws.send(json.dumps(data))
        print(f"Energy Full!!")
        countdown_timer(10)  # 1 hour countdown
        
        taps_count = 500
        timestamps = generate_timestamps(taps_count, 200)
        data = {
            "action": "tap",
            "data": timestamps
        }
        ws.send(json.dumps(data))
        print(f"{biru}Data sent: {taps_count} Tap {reset}")
        print("-"*80)
        new_data = x.get("data")
        user = new_data.get("username")
        balance = new_data.get("balance")
        energy = new_data.get("energy")
        clicks = new_data.get("clicks")

        print(f"{merah}Received data sent:\nUser : {user}\nBalance : {balance}\nEnergy : {energy}\nClick : {clicks}")
        print("-"*80)
        countdown_timer(10)
        send_request()
        # Wait before sending the next set of data


def on_error(ws, error):
    print(f"{merah}Error: {error}{reset}")

def on_close(ws):
    print(f"{merah}Connection closed{reset}")

def on_open(ws):
    print(f"{hijau}Connection opened{reset}")

banner = f"""
{putih}AUTO BOT {hijau}PRICK 

{putih}By: {hijau}t.me/qyzannn
{putih}Github: {hijau}@qyzan

{hijau}Message: {putih}Don't Forget To Claim Everyday!
"""
print(banner)

def send_request():
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://api.prick.lol/ws",
        header=[
            "Upgrade: websocket",
            "Origin: https://app.prick.lol",
            "User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Mobile Safari/537.36",
            "Accept-Encoding: gzip, deflate, br",
            "Accept-Language: en-US,en;q=0.9",
            "Sec-WebSocket-Protocol: 6938110450",
            "Pragma: no-cache",
            "Cache-Control: no-cache"
        ],
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        time_format = f"Next request in {mins:02d}:{secs:02d} "
        print(time_format, end="\r", flush=True)
        time.sleep(1)
        seconds -= 1
    print("Reconnecting now...")

# Send the request initially
send_request()
