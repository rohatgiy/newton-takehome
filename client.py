import asyncio
from websockets.asyncio.client import connect
import json

async def send_message():
	uri = "ws://localhost:8765"
	async with connect(uri) as websocket:
		message = {
			"event": "subscribe",
			"channel": "rates"
		}
		await websocket.send(json.dumps(message))
		while True:
			raw_res = await websocket.recv()
			res = json.loads(raw_res)
			print(res)


if __name__ == '__main__':
	asyncio.run(send_message())