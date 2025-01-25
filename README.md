# newton-takehome

Language of implementation: **Python**

## Setup

Install dependencies
```bash
pip3 install -r requirements.txt
```

Launch the WebSocket server:
```bash
python3 server.py [--interval <refetch interval in seconds>]
```

(Optional) Run the client:
```bash
python3 client.py
```

## Specification
The WebSocket server provides an interface for a client to subscribe to real-time crypto asset prices.

To subscribe, connect to the websocket running at `"ws://localhost:8765"` and send the following serialized JSON message:
```json
{
	"event": "subscribe",
	"channel": "rates"
}
```

After subscribing, you will receive price updates (in USD) for the following assets **every 10 seconds**:
- BTC
- ETH
- LTC
- XRP
- BCH
- USDC
- XMR
- XLM
- USDT
- DOGE
- LINK
- MATIC
- UNI
- COMP
- AAVE
- DAI
- SUSHI
- SNX
- CRV
- DOT
- YFI
- MKR
- PAXG
- ADA
- BAT
- ENJ
- AXS
- DASH
- EOS
- BAL
- KNC
- ZRX
- SAND
- GRT
- QNT
- ETC
- ETHW
- 1INCH
- CHZ
- CHR
- SUPER
- OMG
- FTM
- MANA
- SOL
- ALGO
- LUNC
- UST
- ZEC
- XTZ
- REN
- UMA
- SHIB
- LRC
- ANKR
- EGLD
- AVAX
- GALA
- ALICE
- ATOM
- DYDX
- STORJ
- CTSI
- BAND
- ENS
- RNDR
- MASK
- APE

The following assets are missing from the original requested list:
- CELO
- SKL
- AMP
- QCAD
- ONE
- ELF
- HBAR

Prices are sourced from [Kraken's API](https://docs.kraken.com/api/).