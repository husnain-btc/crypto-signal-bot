import requests

urls = [
    "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5",
    "https://api-gcp.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5",
    "https://api1.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5",
    "https://api2.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5",
    "https://api3.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5",
    "https://api4.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5",
]

for url in urls:
    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        print(r.url)
        print("STATUS:", r.status_code)
        print("LENGTH:", len(r.text))
        print("-------------------------")

    except Exception as e:
        print("ERROR:", e)
        print("-------------------------")
