"""
Twilio WhatsApp notification provider implementation.
"""
import urequests
import ubinascii
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class TwilioWhatsAppProvider(BaseProvider):
    """Provider for sending notifications via Twilio WhatsApp."""

    def __init__(self):
        """Initialize the Twilio WhatsApp provider."""
        if not settings.PROVIDER_TWILIO_WHATSAPP_ENABLED:
            return

        self.config = settings.TWILIO_WHATSAPP_CONFIG
        self.auth = ubinascii.b2a_base64(
            f"{self.config['account_sid']}:{self.config['auth_token']}"
        ).decode().strip()

    async def send(self, message):
        """Send a WhatsApp message to all configured numbers."""
        if not settings.PROVIDER_TWILIO_WHATSAPP_ENABLED:
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

                print(f"Sending WhatsApp to {to_number}")
                response = urequests.post(url, headers=headers, data=data)

                if response.status_code == 201:
                    print(f"WhatsApp sent to {to_number}")
                else:
                    print(f"Failed to send WhatsApp: {response.text}")

            except Exception as e:
                print(f"WhatsApp error: {str(e)}")
                raise

            finally:
                if response:
                    response.close()
