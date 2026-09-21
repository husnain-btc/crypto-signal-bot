import requests

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

params = {
    "vs_currency": "usd",
    "days": "2",
    "interval": "hourly"
}

response = requests.get(url, params=params, timeout=20)

print("Status:", response.status_code)

response.raise_for_status()

data = response.json()

prices = data["prices"]

print("Number of hourly price points:", len(prices))

print("\nLast 5 hourly prices:")

for timestamp, price in prices[-5:]:
    print(timestamp, price)
