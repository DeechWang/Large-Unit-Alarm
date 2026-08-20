import os
import json
from twilio.rest import Client

def call():
    try:
        with open("config.json") as f:
            config = json.load(f)
            account_sid = config.get('TWILIO_SID')
            auth_token = config.get('TWILIO_AUTH')
    except FileNotFoundError:
        raise FileNotFoundError("config.json not found")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in config.json")
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="your-phone",
        from_="twilio-number",
        timeout="15"
    )
    print(call.sid)