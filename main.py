# by Tomasz Golaszewski
# 2024.06.30
# Test program to check the possibility of asynchronously downloading Bitcoin data
# using the WebSocket protocol.

import asyncio
import json
import websockets

# sandbox:
# URI = "wss://ws-feed-public.sandbox.exchange.coinbase.com"
# production:
URI = "wss://ws-feed.exchange.coinbase.com"

async def websocket_listener(product_ids: list[str]):
    """The method takes as parameters a list of products to subscribe to. 
    Then it establishes a connection using a websocket and listens for received messages. 
    Finally, it displays the current price of the subscribed products on the screen.
    """
    subscribe_message = json.dumps({
        "type": "subscribe",
        "channels": [
            {"name": "ticker", "product_ids": product_ids}
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
                else:
                    print(json_response)

    except websockets.exceptions.ConnectionClosedError as e:
        print('Connection closed with error: ' + str(e))
    except websockets.exceptions.ConnectionClosedOK as e:
        print("Connection closed correctly with message: " + str(e))


async def websocket_unsubscribe(product_ids: list[str]):
    """The method takes as parameters a list of products to unsubscribe from.
    """

    subscribe_message = json.dumps({
        "type": "unsubscribe",
        "channels": [
            {"name": "ticker", "product_ids": product_ids}
        ],
    })
    try:
        async with websockets.connect(URI, ping_interval=None) as websocket:
            await websocket.send(subscribe_message)
            response = await websocket.recv()
            json_response = json.loads(response)
            print(json_response)
    except websockets.exceptions.ConnectionClosedError as e:
        print('Connection closed during unsubscribing with error: ' + str(e))
    except websockets.exceptions.ConnectionClosedOK as e:
        print("Connection closed during unsubscribing correctly with message: " + str(e))


if __name__ == '__main__':
    product_list = ["BTC-USD"]
    try:
        asyncio.run(websocket_listener(product_list))
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
        asyncio.run(websocket_unsubscribe(product_list))
    except:
        print("Something wrong...")
