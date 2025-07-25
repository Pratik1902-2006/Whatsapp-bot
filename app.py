from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ================================
# 🔐 Google Sheets Setup
# ================================
# Define scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from service_key.json
creds = ServiceAccountCredentials.from_json_keyfile_name("service_key.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet and tab
sheet = client.open("RetailBotData").worksheet("Sheet1")  # Change names as needed

# ================================
# 🌐 Flask Routes
# ================================

@app.route('/')
def home():
    return "✅ Flask + Twilio WhatsApp bot is running!"

@app.route('/whatsapp', methods=["POST"])
def whatsapp_bot():
    # Receive incoming message
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")  # Format: whatsapp:+91xxxxxxxxxx

    # Create Twilio response
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg:
        # Save to Google Sheet
        sheet.append_row([sender, incoming_msg])

        # Reply to user
        msg.body(f"📝 Message received: {incoming_msg}")
    else:
        msg.body("❗ Please send a valid message.")

    return str(resp)

# ================================
# 🚀 Start the Flask Server
# ================================

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True)
