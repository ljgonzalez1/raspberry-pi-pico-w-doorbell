"""
Simple GET request notification provider implementation.
"""
import urequests
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class SimpleGetProvider(BaseProvider):
    """Provider for sending notifications via simple GET requests."""

    def __init__(self):
        """Initialize the Simple GET provider."""
        if not settings.PROVIDER_SIMPLE_GET_ENABLED:
            return

        self.config = settings.SIMPLE_GET_CONFIG

    async def send(self, message):
        """Send a GET request to configured endpoint."""
        if not settings.PROVIDER_SIMPLE_GET_ENABLED:
            return

        response = None
        try:
            url = f"http://{self.config['host']}:{self.config['port']}"
            print(f"Sending GET request to {url}")

            response = urequests.get(url)

            if response.status_code == 200:
                print("GET request successful")

            else:
                print(f"GET request failed: {response.text}")

        except Exception as e:
            print(f"GET request error: {str(e)}")
            raise

        finally:
            if response:
                response.close()
