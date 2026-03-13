import requests
import os
from datetime import datetime

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Movie event code from your URL
EVENT_CODE = "ET00484171"

API_URL = "https://in.bookmyshow.com/api/showtimes/byEvent"

PARAMS = {
    "eventCode": EVENT_CODE,
    "cityCode": "BANG"
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


def check_showtimes():

    print("Calling BookMyShow API...")

    response = requests.get(API_URL, params=PARAMS)

    data = response.json()

    venues = data.get("data", {}).get("venues", [])

    if not venues:
        print("No venues returned from API.")
        return

    for venue in venues:

        theatre = venue.get("name")

        for show in venue.get("showTimes", []):

            showtime = show.get("showTime")

            show_dt = datetime.fromisoformat(showtime)

            if show_dt.day == 15 and show_dt.hour >= 12:

                message = f"""
TEST ALERT SUCCESS 🎉

Movie detected: The Kerala Story 2: Goes Beyond
City: Bangalore
Theatre: {theatre}

Showtime: {show_dt}

Your BookMyShow bot is working correctly.
"""

                send_alert(message)

                return


def main():

    check_showtimes()


if __name__ == "__main__":
    main()
