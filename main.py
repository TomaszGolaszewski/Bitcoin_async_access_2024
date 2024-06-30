# by Tomasz Golaszewski
# 2024.06.30
# Test program to check the possibility of asynchronously downloading Bitcoin data using the WebSocket protocol.

import asyncio
import websockets
import json

# sandbox:
# URI = "wss://ws-feed-public.sandbox.exchange.coinbase.com"
# production:
URI = "wss://ws-feed.exchange.coinbase.com"

async def websocket_listener():
    subscribe_message = json.dumps({
        "type": "subscribe",
        "channels": [
            {"name": "heartbeat", "product_ids": ["BTC-USD"]},
            {"name": "ticker", "product_ids": ["BTC-USD"]}
        ],
    })

    try:
        async with websockets.connect(URI, ping_interval=None) as websocket:
            await websocket.send(subscribe_message)
            while True:
                response = await websocket.recv()
                json_response = json.loads(response)
                response_type = json_response.get("type")
                if response_type == "ticker":
                    print(json_response.get("time"), ">>>", json_response.get("price") )
                elif response_type == "heartbeat":
                    print(json_response.get("time"), "...")
                else:
                    print(json_response)

    except websockets.exceptions.ConnectionClosedError:
        print('Connection closed with error, retrying...')
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed with OK")


if __name__ == '__main__':
    try:
        asyncio.run(websocket_listener())
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
    except:
        print("Something wrong...")