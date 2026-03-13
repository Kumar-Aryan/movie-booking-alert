import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://in.bookmyshow.com/bengaluru/movies"

def send_alert(message):

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

def check_movie():

    response = requests.get(URL)

    page_text = response.text.lower()

    if "dhurandar" in page_text:

        message = """
🎬 BOOKINGS MAY BE OPEN

Movie: Dhurandar The Revenge
City: Bangalore
Date: 19 March (2nd half)

Check BookMyShow quickly:
https://in.bookmyshow.com
"""

        send_alert(message)

check_movie()
