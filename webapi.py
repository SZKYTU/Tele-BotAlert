from dotenv import load_dotenv
import websockets
import asyncio
import json
import os


load_dotenv()


async def cryptocompare():
    url = os.getenv("URL")
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({
            "action": "SubAdd",
            "subs": ["2~Coinbase~BTC~USD"],
        }))

        async def loop():
            while True:
                try:
                    data = await websocket.recv()
                except websockets.ConnectionClosed:
                    break
                try:
                    data = json.loads(data)
                    if len(data) == 16:
                        BTC_price = data["PRICE"]
                        print(BTC_price)
                        crypto_name = data["FROMSYMBOL"]
                    else:
                        pass
                except ValueError:
                    print(data)
            return BTC_price, crypto_name


class SocketData:
    def __init__(self, price, crypto):
        self.price = cryptocompare.BTC_price
        self.crypto = cryptocompare.crypto_name


asyncio.get_event_loop().run_until_complete(cryptocompare())
