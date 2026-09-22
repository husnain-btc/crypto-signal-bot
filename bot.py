import requests
import time
import traceback

print("================================")
print("🚀 CRYPTO SIGNAL BOT STARTED")
print("================================")

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT",
    "LTCUSDT", "BCHUSDT", "ATOMUSDT", "NEARUSDT", "APTUSDT",
    "ARBUSDT", "OPUSDT", "SUIUSDT", "SEIUSDT", "INJUSDT",
    "TIAUSDT", "FILUSDT", "ETCUSDT", "AAVEUSDT", "UNIUSDT",
    "MKRUSDT", "CRVUSDT", "ALGOUSDT", "VETUSDT", "HBARUSDT",
    "ICPUSDT", "GRTUSDT", "FTMUSDT", "EOSUSDT", "THETAUSDT",
    "RUNEUSDT", "EGLDUSDT", "SANDUSDT", "MANAUSDT", "AXSUSDT",
    "GALAUSDT", "CHZUSDT", "ENJUSDT", "ONEUSDT", "ZILUSDT",
    "IOTAUSDT", "KAVAUSDT", "LDOUSDT", "IMXUSDT", "WLDUSDT"
]

URL = "https://api.binance.com/api/v3/klines"

def get_klines(symbol):
    try:
        r = requests.get(
            URL,
            params={
                "symbol": symbol,
                "interval": "1h",
                "limit": 60
            },
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        print(symbol, "HTTP", r.status_code)

        if r.status_code != 200:
            return None

        return r.json()

    except Exception as e:
        print(symbol, "ERROR:", e)
        return None


def rsi(closes, period=14):
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


def check_signal(symbol):
    data = get_klines(symbol)

    if not data or len(data) < 55:
        return None

    # Last candle = currently forming candle
    # Previous candle = latest completed candle
    candles = data[:-1]

    c = candles[-1]
    c1 = candles[-2]
    c2 = candles[-3]

    closes = [float(x[4]) for x in candles]

    current_close = closes[-1]
    sma20 = sum(closes[-20:]) / 20
    sma50 = sum(closes[-50:]) / 50

    current_rsi = rsi(closes)

    # 1H uptrend
    uptrend = current_close > sma20 and sma20 > sma50

    # Latest completed candle RED
    latest_red = float(c[4]) < float(c[1])

    # Two candles before it GREEN
    green1 = float(c1[4]) > float(c1[1])
    green2 = float(c2[4]) > float(c2[1])

    # Their pump %
    pump1 = ((float(c1[4]) - float(c1[1])) / float(c1[1])) * 100
    pump2 = ((float(c2[4]) - float(c2[1])) / float(c2[1])) * 100

    two_green_1pct = pump1 >= 1 and pump2 >= 1

    # RSI 30-40
    rsi_ok = current_rsi is not None and 30 <= current_rsi <= 40

    if uptrend and latest_red and two_green_1pct and rsi_ok:

        return {
            "symbol": symbol,
            "rsi": round(current_rsi, 2),
            "pump1": round(pump1, 2),
            "pump2": round(pump2, 2),
            "price": current_close
        }

    return None


try:

    signals = []

    for symbol in SYMBOLS:

        result = check_signal(symbol)

        if result:
            signals.append(result)

            print()
            print("🔥🔥 SIGNAL FOUND 🔥🔥")
            print("COIN:", result["symbol"])
            print("RSI:", result["rsi"])
            print("GREEN 1:", result["pump1"], "%")
            print("GREEN 2:", result["pump2"], "%")
            print("PRICE:", result["price"])
            print("==========================")

    print()
    print("================================")
    print("SCAN FINISHED")
    print("SIGNALS FOUND:", len(signals))
    print("================================")

    if not signals:
        print("No matching setup right now.")

except Exception:
    print("❌ BOT ERROR")
    traceback.print_exc()
    raise
