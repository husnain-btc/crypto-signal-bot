import requests
from datetime import datetime, timezone

url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc"

params = {
    "vs_currency": "usd",
    "days": "1"
}

response = requests.get(
    url,
    params=params,
    timeout=20
)

print("Status:", response.status_code)

response.raise_for_status()

data = response.json()

print("Number of OHLC candles:", len(data))

print("\nLast 5 candles:")

for candle in data[-5:]:
    timestamp, open_price, high, low, close = candle

    dt = datetime.fromtimestamp(
        timestamp / 1000,
        tz=timezone.utc
    )

    print(
        dt.strftime("%Y-%m-%d %H:%M UTC"),
        "| Open:", open_price,
        "| High:", high,
