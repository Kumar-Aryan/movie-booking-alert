import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

EVENT_CODE = "ET00484171"

API_URL = "https://in.bookmyshow.com/api/showtimes/byEvent"

PARAMS = {
    "eventCode": EVENT_CODE,
    "cityCode": "BANG"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def send_alert(message):

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def main():

    print("Calling BookMyShow API...")

    response = requests.get(API_URL, params=PARAMS, headers=HEADERS)

    print("Status:", response.status_code)

    print("First 1000 characters of response:")
    print(response.text[:1000])

    send_alert("Debug test: script executed successfully")


if __name__ == "__main__":
    main()
