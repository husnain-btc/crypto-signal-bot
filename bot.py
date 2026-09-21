import requests
import time

NTFY_TOPIC = "YOUR_NTFY_TOPIC"

# ==========================================
# GET TOP 50 COINS
# ==========================================

def get_top_50():

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    print("Top 50 HTTP:", response.status_code)

    response.raise_for_status()

    return response.json()


# ==========================================
# GET HOURLY DATA
# ==========================================

def get_hourly_prices(coin_id):

    url = (
        f"https://api.coingecko.com/api/v3/"
        f"coins/{coin_id}/market_chart"
    )

    params = {
        "vs_currency": "usd",
        "days": "2",
        "interval": "hourly"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    if response.status_code != 200:
        print(
            coin_id,
            "HTTP",
            response.status_code
        )
        return None

    return response.json().get("prices", [])


# ==========================================
# RSI
# ==========================================

def calculate_rsi(values, period=14):

    if len(values) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, len(values)):

        change = values[i] - values[i - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


# ==========================================
# ANALYZE
# ==========================================

def analyze(coin):

    coin_id = coin["id"]
    symbol = coin["symbol"].upper()

    prices = get_hourly_prices(coin_id)

    if not prices:
        return None

    values = [float(x[1]) for x in prices]

    if len(values) < 50:
        return None

    current = values[-1]
    previous = values[-2]
    previous2 = values[-3]

    move_current = (
        (current - previous) / previous
    ) * 100

    move_previous = (
        (previous - previous2) / previous2
    ) * 100

    rsi = calculate_rsi(values)

    if rsi is None:
        return None

    # Current movement RED
    red = move_current < 0

    # Previous movement GREEN
    green1 = move_previous > 0

    # Basic trend filter
    trend_20h = current > values[-21]
    trend_50h = current > values[-50]

    uptrend = trend_20h and trend_50h

    signal = (
        red
        and green1
        and 30 <= rsi <= 40
        and uptrend
    )

    print(
        f"{symbol} | "
        f"RSI {rsi:.2f} | "
        f"Current {move_current:.2f}% | "
        f"Previous {move_previous:.2f}% | "
        f"Uptrend {uptrend} | "
        f"Signal {signal}"
    )

    if signal:

        return {
            "symbol": symbol,
            "price": current,
            "rsi": rsi,
            "current": move_current,
            "previous": move_previous
        }

    return None


# ==========================================
# NTFY
# ==========================================

def send_ntfy(signals):

    message = "🚨 CRYPTO SIGNAL FOUND\n\n"

    for s in signals:

        message += (
            f"🪙 {s['symbol']}USDT\n"
            f"Price: {s['price']}\n"
            f"RSI: {s['rsi']:.2f}\n"
            f"Current: {s['current']:.2f}% 🔴\n"
            f"Previous: +{s['previous']:.2f}% 🟢\n"
            f"Trend: UP 📈\n"
            f"----------------\n"
        )

    url = f"https://ntfy.sh/{NTFY_TOPIC}"

    response = requests.post(
        url,
        data=message
