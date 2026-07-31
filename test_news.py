import requests

url = "https://feeds.bbci.co.uk/news/rss.xml"

try:
    response = requests.get(url, timeout=10)

    print("Status Code:", response.status_code)
    print(response.text[:500])

except Exception as e:
    print("ERROR:", e)