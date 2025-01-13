"""
Twilio SMS notification provider implementation.
"""
import urequests
import ubinascii
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class TwilioSMSProvider(BaseProvider):
    """Provider for sending notifications via Twilio SMS."""

    def __init__(self):
        """Initialize the Twilio SMS provider."""
        if not settings.PROVIDER_TWILIO_SMS_ENABLED:
            return

        self.config = settings.TWILIO_SMS_CONFIG
        self.auth = ubinascii.b2a_base64(
            f"{self.config['account_sid']}:{self.config['auth_token']}"
        ).decode().strip()

    async def send(self, message):
        """Send an SMS to all configured numbers."""
        if not settings.PROVIDER_TWILIO_SMS_ENABLED:
            return

        for to_number in self.config['to_numbers']:
            response = None
            try:
                url = (f"https://api.twilio.com/2010-04-01/Accounts/"
                      f"{self.config['account_sid']}/Messages.json")

                headers = {
                    'Authorization': f'Basic {self.auth}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                data = (f"From={self.config['from_number']}&"
                       f"To={to_number}&"
                       f"Body={message}")

                print(f"Sending SMS to {to_number}")
                response = urequests.post(url, headers=headers, data=data)

                if response.status_code == 201:
                    print(f"SMS sent to {to_number}")

                else:
                    print(f"Failed to send SMS: {response.text}")

            except Exception as e:
                print(f"SMS error: {str(e)}")
                raise

            finally:
                if response:
                    response.close()
