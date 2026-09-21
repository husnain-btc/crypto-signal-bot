import requests
import time

# NTFY settings
NTFY_TOPIC = "YOUR_NTFY_TOPIC"

def send_signal(message):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    requests.post(url, data=message.encode("utf-8"))

send_signal("🤖 Crypto Bot TEST — Bot is running!")

print("Bot started successfully.")

while True:
    time.sleep(300)
