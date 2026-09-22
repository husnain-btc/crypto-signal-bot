import requests
import time
from datetime import datetime

# ============================================================
# 🚀 CRYPTO SIGNAL BOT
# Binance Spot | 1H Strategy
# ============================================================

INTERVAL = "1h"

# Tumhari strategy
RSI_MIN = 30
RSI_MAX = 40

PUMP_MIN = 1.0          # Previous 2 green candles minimum +1%
TP_PERCENT = 1.0

# 50+ Binance USDT pairs
COINS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "TRXUSDT", "AVAXUSDT", "LINKUSDT",
    "DOTUSDT", "MATICUSDT", "LTCUSDT", "BCHUSDT", "ATOMUSDT",
    "ETCUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT",
    "NEARUSDT", "INJUSDT", "SUIUSDT", "SEIUSDT", "TIAUSDT",
    "AAVEUSDT", "UNIUSDT", "LDOUSDT", "MKRUSDT", "SNXUSDT",
    "RUNEUSDT", "GRTUSDT", "FETUSDT", "RENDERUSDT", "WIFUSDT",
    "PEPEUSDT", "SHIBUSDT", "FLOKIUSDT", "BONKUSDT",
    "VTHOUSDT", "IOTAUSDT", "ALGOUSDT", "XLMUSDT", "HBARUSDT",
    "SANDUSDT", "MANAUSDT", "AXSUSDT", "GALAUSDT", "CHZUSDT",
    "EGLDUSDT", "IMXUSDT", "STXUSDT", "CRVUSDT", "ENSUSDT",
    "COMPUSDT", "DYDXUSDT", "APEUSDT", "JASMYUSDT", "CFXUSDT"
]

# Binance API endpoints
BASE_URLS = [
    "https://api.binance.com",
    "
