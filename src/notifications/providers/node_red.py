"""
Node-RED notification provider implementation.
"""
import urequests
from ..base_provider import BaseProvider
from config import settings
from utils.logging import dprint as print


class NodeRedProvider(BaseProvider):
    """Provider for sending notifications via Node-RED."""

    def __init__(self):
        """Initialize the Node-RED provider."""
        if not settings.PROVIDER_NODE_RED_ENABLED:
            return

        self.config = settings.NODE_RED_CONFIG

    async def send(self, message):
        """Send a message to Node-RED endpoint."""
        if not settings.PROVIDER_NODE_RED_ENABLED:
            return

        response = None
        try:
            url = (f"{self.config['protocol']}://{self.config['host']}:"
                  f"{self.config['port']}/{self.config['path']}"
                  f"?payload={self.config['payload']}"
                  f"&title={self.config['title']}"
                  f"&tema={self.config['subject']}")

            print(f"Sending to Node-RED: {url}")

            response = urequests.get(url)

            if response.status_code == 200:
                print("Node-RED request successful")
            else:
                print(f"Node-RED request failed: {response.text}")

        except Exception as e:
            print(f"Node-RED error: {str(e)}")
            raise

        finally:
            if response:
                response.close()