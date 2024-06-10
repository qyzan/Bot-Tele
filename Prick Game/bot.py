import websocket
import ssl
import time
import json
import random
def generate_timestamps(count, interval_ms):
    """
    Generates a list of Unix timestamps in milliseconds.

    :param count: Number of timestamps to generate.
    :param interval_ms: Interval between timestamps in milliseconds.
    :return: List of timestamps in milliseconds.
    """
    current_time = int(time.time() * 1000)
    return [current_time + i * interval_ms for i in range(count)]

# Example: Generate 10 timestamps with a 200 ms interval between them

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    while True:
        taps_count = random.choice(range(8, 25, 8))
        timestamps = generate_timestamps(taps_count, 200)
        data = {
            "action": "tap",
            "data": timestamps
        }
        ws.send(json.dumps(data))
        print("Data sent:", data)
        message = on_message()
        new_message = json.load(message)
        

        time.sleep(random.uniform(1, 3))
        # Simulate waiting before sending the next set of data

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://swagerbyfalio.com/prick/ws",
        header=[
            "Upgrade: websocket",
            "Origin: https://app.prick.lol",
            "User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Mobile Safari/537.36",
            "Accept-Encoding: gzip, deflate, br",
            "Accept-Language: en-US,en;q=0.9",
            "Sec-WebSocket-Protocol: 6987017752",
            "Pragma: no-cache",
            "Cache-Control: no-cache"
        ],
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
