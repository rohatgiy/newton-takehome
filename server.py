from dotenv import load_dotenv
import os
import asyncio
import websockets
import json
import requests
import time

load_dotenv()
KRAKEN_URI = os.getenv('KRAKEN_URI')
REFETCH_INTERVAL = 10

assets = [
	"BTC", "ETH", "LTC", "XRP", "BCH", "USDC", "XMR", "XLM",
	"USDT", "DOGE", "LINK", "MATIC", "UNI", "COMP", "AAVE", "DAI",
	"SUSHI", "SNX", "CRV", "DOT", "YFI", "MKR", "PAXG", "ADA", "BAT", "ENJ",
	"AXS", "DASH", "EOS", "BAL", "KNC", "ZRX", "SAND", "GRT", "QNT", "ETC",
	"ETHW", "1INCH", "CHZ", "CHR", "SUPER", "OMG", "FTM", "MANA",
	"SOL", "ALGO", "LUNC", "UST", "ZEC", "XTZ", "REN", "UMA", "SHIB",
	"LRC", "ANKR", "EGLD", "AVAX", "GALA", "ALICE", "ATOM",
	"DYDX", "STORJ", "CTSI", "BAND", "ENS", "RNDR", "MASK", "APE"]

special_assets = {
	'LUNC': 'LUNA',
	'RNDR': 'RENDER'
}

kraken_pair_to_readable = {
	'XXBTZUSD': 'BTCUSD',
}

clients = {}
prev_prices = {}
last_fetch = 0

def get_prices():
	global last_fetch
	timestamp = time.time()
	if timestamp - last_fetch <= REFETCH_INTERVAL:
		return [price for _, price in prev_prices.items()]
	last_fetch = timestamp
	url = f'{KRAKEN_URI}/Ticker'
	params = {
		'pair': ','.join([f'{special_assets[asset]}USD' if asset in special_assets else f'{asset}USD' for asset in assets])
	}
	headers = {
		'accept': 'application/json',
	}
	req = requests.get(url, headers=headers, params=params)
	res = req.json()
	if res['error']:
		return res['error']
	data = res['result']

	ret = []
	
	for pair_name, pair_data in data.items():
		symbol = pair_name if pair_name not in kraken_pair_to_readable else kraken_pair_to_readable[pair_name]
		ask = pair_data['a'][0]
		bid = pair_data['b'][0]
		spot = (float(ask) + float(bid)) / 2
		change = (prev_prices.get(symbol, {}).get('spot', spot) - spot)
		price_obj = {
			'symbol': symbol,
			'ask': ask,
			'bid': bid,
			'spot': spot,
			'change': change,
			'timestamp': timestamp
		}
		prev_prices[symbol] = price_obj

		ret.append(price_obj)
	
	return ret

async def subscribe(ws):
	clients[ws] = set()
	try:
		async for raw_msg in ws:
			msg = json.loads(raw_msg)

			if msg['event'] == 'subscribe':
				if msg['channel'] == 'rates':
					clients[ws].add('rates')
					message = {
						"channel": "rates",
						"event": "data",
						"data": get_prices()
					}
					await ws.send(json.dumps(message))
				else:
					raise ValueError('Invalid channel')
			else:
				raise ValueError('Invalid event')
	except json.JSONDecodeError:
		print('Invalid JSON')
	except Exception as e:
		print(f'Error occurred: {e}')
	finally:
		del clients[ws]


async def broadcast_updates():
    while True:
        if clients:
            prices = get_prices()
            message = {
                "channel": "rates",
                "event": "data",
                "data": prices
            }
            for ws, channels in clients.items():
                if 'rates' in channels:
                    await ws.send(json.dumps(message))
        await asyncio.sleep(REFETCH_INTERVAL)
		
async def main():
	start_server = await websockets.serve(subscribe, "localhost", 8765)
	print('WebSocket server started on ws://localhost:8765')
	await asyncio.gather(start_server.wait_closed(), broadcast_updates())

if __name__ == '__main__':
	asyncio.run(main())
	