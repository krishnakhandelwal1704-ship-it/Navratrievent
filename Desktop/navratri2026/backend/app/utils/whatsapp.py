import os

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

def send_whatsapp_ticket(phone_number: str, message_body: str):
    if not TWILIO_AVAILABLE:
        print("Twilio package not installed. Skipping WhatsApp notification.")
        return None
    
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_number = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    
    if not account_sid or not auth_token:
        print("Twilio credentials not configured. Skipping WhatsApp notification.")
        return None
        
    try:
        client = Client(account_sid, auth_token)
        formatted_number = phone_number if phone_number.startswith("whatsapp:") else f"whatsapp:{phone_number}"
        
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=formatted_number
        )
        return message.sid
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return None