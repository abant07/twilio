# type: ignore
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import time
from time import sleep
from datetime import datetime, timedelta
from threading import Thread


def background_message():
    app = Flask(__name__)

    @app.route("/sms", methods=["POST"])
    def send_reply():
        global replied
        tomorrow_datetime = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow_datetime.strftime("%m-%d-%Y")
        resp = MessagingResponse()
        body = request.values.get("Body").upper()
        if body == "OK":
            resp.message("Your next dose is at 8:30 AM on " + tomorrow)
            replied = True
        else:
            resp.message("Please reply OK to confirm vitmamins")

        sleep(0.1)
        return str(resp)

    app.run(debug=False)


def send_first_message():
    account_sid = "TWILIO_ACCOUNT_SID"
    auth_token = "TWILIO_AUTH_TOKEN"
    client = Client(account_sid, auth_token)

    client.messages.create(from_="TWILIO_NUMBER", body="Hello", to="CLIENT_NUMBER")
    print("Message has been sent")


daemon = Thread(target=background_message, daemon=True, name="Monitor")
daemon.start()
replied = False
while True:
    current_time = time.strftime("%H:%M:%S %p")
    if current_time == "08:30:00 AM":
        send_first_message()
        replied = False
    sleep(0.4)
