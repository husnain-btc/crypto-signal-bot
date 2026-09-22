import requests

url = "https://api-gcp.binance.com/api/v3/klines"

params = {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 5
}

r = requests.get(
    url,
    params=params,
    timeout=10,
    headers={"User-Agent": "Mozilla/5.0"}
)

print("URL:", r.url)
print("STATUS:", r.status_code)
print("RESPONSE:", r.text[:500])
