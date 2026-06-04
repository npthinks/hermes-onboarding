from twilio.rest import Client
import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

def send_welcome_sms(to_number: str, user_name: str):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Hi {user_name}! Your Hermes AI agent is ready. Reply to this message to start chatting with your personal assistant.",
        from_=TWILIO_NUMBER,
        to=to_number
    )
    
    return message.sid