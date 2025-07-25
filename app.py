from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from google.oauth2.service_account import Credentials
import os
import json

app = Flask(__name__)

# Google Sheets setup using environment variable (Render-compatible)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
google_creds = json.loads(os.environ["GOOGLE_CREDS_JSON"])  # Load from Render env
credentials = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(credentials)
sheet = client.open("RetailBotData").worksheet("Sheet1")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg:
        sheet.append_row([sender, incoming_msg])
        msg.body(f"Received: {incoming_msg}")
    else:
        msg.body("Please send a valid message.")

    return str(resp)

# ✅ Required to start Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
 