import requests

NTFY_TOPIC = "YOUR_NTFY_TOPIC"

BINANCE_URL = "https://api.binance.com/api/v3/klines"


def get_klines(symbol, interval="1h", limit=5):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(
        BINANCE_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()
    return response.json()


def send_ntfy(message):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"

    response = requests.post(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": "Crypto Signal Bot",
            "Priority": "high"
        },
        timeout=15
    )

    response.raise_for_status()


def check_red_candle(symbol):
    candles = get_klines(symbol, "1h", 5)

    # Last completed 1H candle
    candle = candles[-2]

    open_price = float(candle[1])
    close_price = float(candle[4])

    return close_price < open_price


symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT"
]


signals = []

for symbol in symbols:

    try:
        if check_red_candle(symbol):
            signals.append(symbol)

    except Exception as error:
        print(symbol, "ERROR:", error)


if signals:

    message = "🔴 1H RED CANDLE\n\n"

    for symbol in signals:
        message += f"• {symbol}\n"

    send_ntfy(message)

    print(message)

else:

    print("No red-candle setup found.")
