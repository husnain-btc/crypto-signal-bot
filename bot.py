import requests

NTFY_TOPIC = "YOUR_NTFY_TOPIC"

url = f"https://ntfy.sh/{NTFY_TOPIC}"

response = requests.post(
    url,
    data="🤖 Crypto Bot TEST — GitHub Actions is working!".encode("utf-8"),
    headers={
        "Title": "Crypto Bot Test",
        "Priority": "high"
    }
)

print("Notification sent:", response.status_code)
