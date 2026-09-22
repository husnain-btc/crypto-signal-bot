import requests
import time
from datetime import datetime

# ==============================
# SETTINGS
# ==============================

INTERVAL = "1h"
RSI_MIN = 30
RSI_MAX = 40
PUMP_MIN = 1.0
TP_PERCENT = 1.0

COINS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "TRXUSDT", "AVAXUSDT", "LINKUSDT",
    "DOTUSDT", "LTCUSDT", "BCHUSDT", "ATOMUSDT", "ETCUSDT",
    "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "NEARUSDT",
    "INJUSDT", "SUIUSDT", "SEIUSDT", "TIAUSDT", "AAVEUSDT",
    "UNIUSDT", "LDOUSDT", "MKRUSDT", "SNXUSDT", "RUNEUSDT",
    "GRTUSDT", "FETUSDT", "RENDERUSDT", "WIFUSDT", "PEPEUSDT",
    "SHIBUSDT", "FLOKIUSDT", "BONKUSDT", "VTHOUSDT", "IOTAUSDT",
    "ALGOUSDT", "XLMUSDT", "HBARUSDT", "SANDUSDT", "MANAUSDT",
    "AXSUSDT", "GALAUSDT", "CHZUSDT", "EGLDUSDT", "IMXUSDT",
    "STXUSDT", "CRVUSDT", "ENSUSDT", "COMPUSDT", "DYDXUSDT",
    "APEUSDT", "JASMYUSDT", "CFXUSDT"
]

BASE_URLS = [
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com"
]


# ==============================
# GET BINANCE DATA
# ==============================

def get_klines(symbol, limit=100):

    for base in BASE_URLS:

        url = base + "/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": INTERVAL,
            "limit": limit
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if response.status_code == 200:
                return response.json()

            print(
                symbol,
                "HTTP",
                response.status_code
            )

        except Exception as e:

            print(symbol, "ERROR:", e)

    return None


# ==============================
# RSI
# ==============================

def calculate_rsi(closes, period=14):

    if len(closes) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, len(closes)):

        change = closes[i] - closes[i - 1]

        if change >= 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):

        avg_gain = (
            avg_gain * (period - 1) + gains[i]
        ) / period

        avg_loss = (
            avg_loss * (period - 1) + losses[i]
        ) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


# ==============================
# UP TREND
# ==============================

def is_uptrend(closes):

    if len(closes) < 50:
        return False

    sma20 = sum(closes[-20:]) / 20
    sma50 = sum(closes[-50:]) / 50

    return (
        closes[-1] > sma20
        and sma20 > sma50
    )


# ==============================
# CANDLE %
# ==============================

def candle_change(candle):

    open_price = float(candle[1])
    close_price = float(candle[4])

    if open_price == 0:
        return 0

    return (
        (close_price - open_price)
        / open_price
        * 100
    )


# ==============================
# CHECK SIGNAL
# ==============================

def check_signal(symbol):

    data = get_klines(symbol)

    if not data:
        return None

    try:

        # Last candle is normally still forming.
        # We use the last CLOSED candle.
        current = data[-2]

        green1 = data[-3]
        green2 = data[-4]

        closes = [
            float(x[4])
            for x in data[:-1]
        ]

        rsi = calculate_rsi(closes)

        if rsi is None:
            return None

        # 1H uptrend
        if not is_uptrend(closes):
            return None

        # Current candle must be RED
        current_open = float(current[1])
        current_close = float(current[4])

        if current_close >= current_open:
            return None

        # RSI filter
        if rsi < RSI_MIN or rsi > RSI_MAX:
            return None

        # Two previous green candles
        green1_change = candle_change(green1)
        green2_change = candle_change(green2)

        if green1_change < PUMP_MIN:
            return None

        if green2_change < PUMP_MIN:
            return None

        return {
            "symbol": symbol,
            "rsi": rsi,
            "green1": green1_change,
            "green2": green2_change,
            "red": candle_change(current),
            "price": current_close
        }

    except Exception as e:

        print(symbol, "ANALYSIS ERROR:", e)

        return None


# ==============================
# SCAN
# ==============================

def scan():

    print("")
    print("=" * 55)
    print("CRYPTO SIGNAL BOT")
    print("=" * 55)
    print(
        "Time:",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    print("Coins:", len(COINS))
    print("Timeframe:", INTERVAL)
    print("RSI:", RSI_MIN, "-", RSI_MAX)
    print("=" * 55)

    signals = []

    for number, symbol in enumerate(COINS, 1):

        print(
            "[" + str(number) + "/" +
            str(len(COINS)) + "]",
            symbol
        )

        result = check_signal(symbol)

        if result:

            signals.append(result)

            print(
                ">>> SIGNAL:",
                symbol
            )

        time.sleep(0.15)

    print("")
    print("=" * 55)
    print("RESULT")
    print("=" * 55)

    if not signals:

        print("NO SIGNAL FOUND")
        print("WAIT")

    else:

        print(
            "SIGNALS FOUND:",
            len(signals)
        )

        for s in signals:

            print("")
            print("================================")
            print("BUY SETUP:", s["symbol"])
            print("RSI:", round(s["rsi"], 2))
            print(
                "GREEN 1:",
                round(s["green1"], 2),
                "%"
            )
            print(
                "GREEN 2:",
                round(s["green2"], 2),
                "%"
            )
            print(
                "CURRENT RED:",
                round(s["red"], 2),
                "%"
            )
            print(
                "PRICE:",
                s["price"]
            )
            print(
                "TARGET:",
                TP_PERCENT,
                "%"
            )
            print("================================")

    print("")
    print("Next scan in 5 minutes...")


# ==============================
# START BOT
# ==============================

print("")
print("================================")
print("CRYPTO SIGNAL BOT STARTED")
print("================================")
print("Binance Spot")
print("1H Strategy")
print("50+ Coins")
print("================================")

while True:

    try:

        scan()

    except KeyboardInterrupt:

        print("BOT STOPPED")
        break

    except Exception as e:

        print("BOT ERROR:", e)

    time.sleep(300)
