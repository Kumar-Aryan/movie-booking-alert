import requests
import os
import re

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MOVIE_URL = "https://in.bookmyshow.com/bengaluru/movies/dhurandhar-the-revenge"


def send_alert(message):

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def user_replied():

    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    response = requests.get(url).json()

    if response["result"]:

        for update in response["result"]:

            if "message" in update:

                if str(update["message"]["chat"]["id"]) == CHAT_ID:

                    return True

    return False


print("Checking BookMyShow page...")


# Stop alerts if user responded
if user_replied():

    print("User replied. Stopping alerts.")

else:

    response = requests.get(MOVIE_URL)

    if response.status_code == 200:

        page = response.text.lower()

        if "dhurandhar" in page:

            date_patterns = [
                "19 mar",
                "mar 19",
                "19 march",
                "march 19"
            ]

            date_found = any(pattern in page for pattern in date_patterns)

            if date_found:

                pm_times = re.findall(r"\b([1-9]|1[0-2]):[0-5][0-9]\s?pm\b", page)

                if pm_times:

                    message = """
🚨 BOOKINGS OPEN 🚨

Movie: Dhurandhar The Revenge
City: Bangalore
Date: 19 March
Showtimes after 12 PM detected

Book now:
https://in.bookmyshow.com/bengaluru/movies/dhurandhar-the-revenge

Reply STOP to this bot to stop alerts.
"""

                    send_alert(message)

                else:

                    print("No PM showtimes yet.")

            else:

                print("19 March shows not detected yet.")

    else:

        print("Failed to load page.")
