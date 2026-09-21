import requests
from datetime import datetime, timezone

# =========================
# SETTINGS
# =========================

NTFY_TOPIC = "YOUR_NTFY_TOPIC"

COINS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT"
]

BINANCE_ENDPOINTS = [
    "https://api.binance.com/api/v3/klines",
    "https://api1.binance.com/api/v3/klines",
    "https://api2.binance.com/api/v3/klines",
    "https://api3.binance.com/api/v3/klines",
    "https://api4.binance.com/api/v3/klines"
]

# =========================
# GET BINANCE 1H CANDLES
# =========================

def get_klines(symbol, interval="1h", limit=100):

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    for endpoint in BINANCE_ENDPOINTS:

        try:
            response = requests.get(
                endpoint,
                params=params,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()

                if len(data) >= 50:
                    print(
                        f"{symbol}: Binance data received from "
                        f"{endpoint}"
                    )
                    return data

            print(
                f"{symbol}: {endpoint} -> "
                f"HTTP {response.status_code}"
            )

        except Exception as e:
            print(f"{symbol}: endpoint error -> {e}")

    return None


# =========================
# RSI
# =========================

def calculate_rsi(closes, period=14):

    gains = []
    losses = []

    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    if len(gains) < period:
        return None

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


# =========================
# ANALYZE COIN
# =========================

def analyze_coin(symbol):

    candles = get_klines(symbol, "1h", 100)

    if not candles:
        return None

    # Last candle can still be forming.
    # We use the latest CLOSED candle.
    closed = candles[:-1]

    opens = [float(x[1]) for x in closed]
    highs = [float(x[2]) for x in closed]
    lows = [float(x[3]) for x in closed]
    closes = [float(x[4]) for x in closed]

    if len(closes) < 60:
        return None

    # Current closed candle
    current_open = opens[-1]
    current_close = closes[-1]

    # Previous 2 candles
    c1_open = opens[-2]
    c1_close = closes[-2]

    c2_open = opens[-3]
    c2_close = closes[-3]

    # Red current candle
    current_red = current_close < current_open

    # Two previous green candles
    previous_green_1 = c1_close > c1_open
    previous_green_2 = c2_close > c2_open

    # Pump percentage of previous green candles
    pump_1 = ((c1_close - c1_open) / c1_open) * 100
    pump_2 = ((c2_close - c2_open) / c2_open) * 100

    # RSI
    rsi = calculate_rsi(closes, 14)

    # Simple 1H uptrend:
    # recent price above older price
    price_20 = closes[-20]
    price_50 = closes[-50]

    uptrend_1h = (
        closes[-1] > price_20
        and closes[-1] > price_50
    )

    # Signal conditions
    signal = (
        current_red
        and previous_green_1
        and previous_green_2
        and pump_1 >= 1.0
        and pump_2 >= 1.0
        and rsi is not None
        and 30 <= rsi <= 40
        and uptrend_1h
    )

    return {
        "symbol": symbol,
        "price": current_close,
        "rsi": rsi,
        "current_red": current_red,
        "green1": previous_green_1,
        "green2": previous_green_2,
        "pump1": pump_1,
        "pump2": pump_2,
        "uptrend_1h": uptrend_1h,
        "signal": signal
    }


# =========================
# NTFY
# =========================

def send_notification(message):

    url = f"https://ntfy.sh/{NTFY_TOPIC}"

    response = requests.post(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": "🚨 Crypto BUY Setup",
            "Priority": "high"
        },
        timeout=15
    )

    print(
        "ntfy notification:",
        response.status_code
    )


# =========================
# MAIN
# =========================

print("================================")
print("🚀 CRYPTO SIGNAL BOT STARTED")
print("================================")

signals = []

for coin in COINS:

    result = analyze_coin(coin)

    if result is None:
        print(f"{coin}: No data")
        continue

    print(
        f"{coin} | "
        f"Price={result['price']:.6f} | "
        f"RSI={result['rsi']:.2f} | "
        f"Red={result['current_red']} | "
        f"Green1={result['green1']} | "
        f"Green2={result['green2']} | "
        f"Pump1={result['pump1']:.2f}% | "
        f"Pump2={result['pump2']:.2f}% | "
        f"Uptrend={result['uptrend_1h']}"
    )

    if result["signal"]:
        signals.append(result)


# =========================
# SEND ONLY IF SIGNAL EXISTS
# =========================

if signals:

    message = "🚨 CRYPTO BUY SETUP FOUND\n\n"

    for s in signals:

        message += (
            f"🪙 {s['symbol']}\n"
            f"Price: {s['price']}\n"
            f"RSI: {s['rsi']:.2f}\n"
            f"Previous Green 1: +{s['pump1']:.2f}%\n"
            f"Previous Green 2: +{s['pump2']:.2f}%\n"
            f"Current Candle: RED 🔴\n"
            f"1H Trend: UP 📈\n"
            f"--------------------\n"
        )

    send_notification(message)

else:

    print("No complete BUY setup found.")

print("================================")
print("BOT FINISHED")
print("================================")
