import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Meta credentials from your .env file
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
# Usually found in your Meta Developer Console under WhatsApp > API Setup (Phone Number ID)
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "your_phone_number_id") 

# Base Graph API URL 
GRAPH_API_URL = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"

def send_whatsapp_message(to_phone: str, text_body: str) -> bool:
    """
    Sends a text message to a user's WhatsApp number via Meta Cloud API.
    """
    if not WHATSAPP_TOKEN:
        print("❌ ERROR: WHATSAPP_TOKEN is not configured in environment variables.")
        return False

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    # Meta's payload structure for sending standard chat text messages
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": text_body
        }
    }

    try:
        response = requests.post(GRAPH_API_URL, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            print(f"✅ Message successfully sent to {to_phone}")
            return True
        else:
            print(f"❌ Meta API Error Status {response.status_code}: {response_data}")
            return False

    except Exception as e:
        print(f"❌ Network exception when sending WhatsApp message: {str(e)}")
        return False