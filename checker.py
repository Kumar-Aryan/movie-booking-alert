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

    if response.get("result"):

        for update in response["result"]:

            if "message" in update:

                if str(update["message"]["chat"]["id"]) == CHAT_ID:
                    return True

    return False


def booking_detected(page):

    if "dhurandhar" not in page:
        return False

    date_patterns = [
        "19 mar",
        "mar 19",
        "19 march",
        "march 19"
    ]

    if not any(pattern in page for pattern in date_patterns):
        return False

    pm_times = re.findall(r"\b([1-9]|1[0-2]):[0-5][0-9]\s?pm\b", page)

    if pm_times:
        return True

    return False


def check_booking():

    print("Checking BookMyShow page...")

    response = requests.get(MOVIE_URL)

    if response.status_code != 200:
        print("Failed to load page")
        return

    page = response.text.lower()

    if booking_detected(page):

        message = """
🚨 BOOKINGS OPEN 🚨

Movie: Dhurandhar The Revenge
City: Bangalore
Date: 19 March
Showtimes after 12 PM detected

Book now:
https://in.bookmyshow.com/bengaluru/movies/dhurandhar-the-revenge

Reply STOP to stop alerts.
"""

        send_alert(message)

    else:

        print("Bookings not detected yet.")


def main():

    if user_replied():

        print("User responded. Stopping alerts.")

        return

    check_booking()


if __name__ == "__main__":
    main()
