import requests
import os
import json

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MOVIE_URL = "https://in.bookmyshow.com/bengaluru/movies/dhurandhar-the-revenge"

STATE_FILE = "state.json"


def send_alert(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def already_notified():

    try:
        with open(STATE_FILE) as f:
            data = json.load(f)
            return data.get("notified", False)

    except:
        return False


def mark_notified():

    with open(STATE_FILE, "w") as f:
        json.dump({"notified": True}, f)


def check_booking():

    response = requests.get(MOVIE_URL)

    page = response.text.lower()
    if True:

    # if "mar 19" in page or "19 mar" in page:

        if "pm" in page:

            if not already_notified():

                message = """
🎬 DHURANDAR BOOKINGS OPEN

City: Bangalore
Date: 19 March
Time: After 12 PM

Book immediately:
https://in.bookmyshow.com/bengaluru/movies/dhurandhar-the-revenge
"""

                send_alert(message)

                mark_notified()


check_booking()
