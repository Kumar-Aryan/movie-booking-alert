import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://in.bookmyshow.com/bengaluru/movies/dhurandhar-the-revenge"

def send_alert(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

print("Checking Dhurandar booking page...")

response = requests.get(URL)

if response.status_code == 200:

    page = response.text.lower()

    if "book tickets" in page or "showtimes" in page:

        message = """
🎬 DHURANDAR BOOKINGS MAY BE OPEN

City: Bangalore  
Date: 19 March (2nd half)

Check immediately:
https://in.bookmyshow.com/bengaluru/movies/dhurandhar-the-revenge
"""

        send_alert(message)
