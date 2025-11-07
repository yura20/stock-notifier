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

    tag_var = pq('div.c-faceplate__fluctuation span.c-instrument.c-instrument--variation')
    variation = tag_var.text()

    tag_price = pq('div.c-faceplate__company span.c-instrument.c-instrument--last')
    price = tag_price.text()

    tag_name = pq('div.c-faceplate__company a.c-faceplate__company-link')
    name = tag_name.text()

    value = f"{price} EUR ({variation})"

    send_alert = True

    if variation.startswith("+"):
        tags = "chart_with_upwards_trend"
    elif variation.startswith("-"):
        tags = "chart_with_downwards_trend"
    else:
        tags = "grey_question"

    if VARIATION_STARTWITH:
        send_alert = variation.startswith(VARIATION_STARTWITH)

    if send_alert:
        response = requests.post(alerts_url,
            data=value.encode("utf-8"),
            headers={
                "Title": name,
                "Priority": "low",
                "Tags": tags,
            }
        )
        if response.status_code == 200:
            print(f"Alert sent:\n{name}\n{value}")
        else:
            print(f"Failed to send alert, status code: {response.status_code}")
    else:
        print(f"No alert needed:\n{name}\n{value}")
else:
    print(f"Failed to fetch stock data, status code: {response.status_code}")