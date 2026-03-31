import os
import pickle
import socket
import tempfile
import uuid

from utils.events.event_base import BaseEventClass

from utils.logging.pitpal_logger import PitPalLogger


import os
import pickle
import socket
import ssl  # Required for TLS
from utils.events.event_base import BaseEventClass
from utils.logging.pitpal_logger import PitPalLogger

class RemoteEventClass(BaseEventClass):
    def __init__(self, host="127.0.0.1", port=8443, cert_path=None, auth_token=None):
        """
        Modified to use TCP + TLS.
        :param host: Server IP (default localhost)
        :param port: Server Port
        :param cert_path: Path to the CA certificate to verify the server
        :param auth_token: Optional string for application-level handshake
        """
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.auth_token = auth_token
        self.logger = PitPalLogger.get_logger()

        # Initialize SSL Context
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        if self.cert_path and os.path.exists(self.cert_path):
            self.context.load_verify_locations(self.cert_path)
        else:
            # For local testing with self-signed certs, you might disable verification
            # (Not recommended for production)
            self.context.check_hostname = False
            self.context.verify_mode = ssl.CERT_NONE

    def __str__(self):
        return f"tls://{self.host}:{self.port}"

    def notify(self, event_type, *args, **kwargs):
        packet = {
            "type": event_type,
            "args": args,
            "kwargs": kwargs,
            "auth": self.auth_token  # Including auth inside the encrypted payload
        }
        payload = pickle.dumps(packet)

        try:
            # 1. Create standard TCP socket
            with socket.create_connection((self.host, self.port)) as sock:
                # 2. Wrap the socket with TLS
                with self.context.wrap_socket(sock, server_hostname=self.host) as ssock:
                    self.logger.debug(f"Event: LocalEvent(TLS): notify {event_type}")
                    ssock.sendall(payload)

        except (ConnectionRefusedError, ssl.SSLError) as e:
            self.logger.error(f"Event: LocalEvent(TLS) notify failed: {e}")

class LocalEventClass(RemoteEventClass):
    def __init__(self,  port=8443, cert_path=None, auth_token=None):
        super().__init("127.0.0.1",,port, cert_path, auth_token)
