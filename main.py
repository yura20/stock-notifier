import os
import requests
from pyquery import PyQuery

TOPIC = os.getenv("TOPIC", "stock_alerts")
STOCK_CODE = os.getenv("STOCK_CODE", "1rTPUST")
VARIATION_STARTWITH = os.getenv("VARIATION_STARTWITH")  # Optional

alerts_url = f"https://ntfy.sh/{TOPIC}"
stock_url = f"https://www.boursorama.com/bourse/trackers/cours/{STOCK_CODE}/"

response = requests.get(stock_url)

if response.status_code == 200:
    pq = PyQuery(response.text)
    tag = pq('div.c-faceplate__fluctuation span.c-instrument.c-instrument--variation')
    value = tag.text()

    send_alert = True
    if VARIATION_STARTWITH:
        send_alert = value.startswith(VARIATION_STARTWITH)

    if send_alert:
        requests.post(alerts_url, data=f"Index update: {value}")
        print(f"Alert sent: Index update: {value}")
    else:
        print(f"No alert needed: {value}")
else:
    print(f"Failed to fetch stock data, status code: {response.status_code}")