import requests

url = "https://api.coingecko.com/api/v3/ping"

response = requests.get(url, timeout=15)

print("Status:", response.status_code)
print("Response:", response.text)
