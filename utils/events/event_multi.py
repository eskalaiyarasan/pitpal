import pickle
import socket
import ssl
import threading


class BaseRemoteEvent(BaseEventClass):
    def __init__(self, start_offset, step):
        self._subscribers = {}
        self._counter = start_offset
        self._step = step
        self._lock = threading.Lock()
        self.logger = PitPalLogger.get_logger()

    def inc(self):
        with self._lock:
            val = self._counter
            if val <= 100000:
                self._counter += self._step
                return hex(val)
            return None

    def register(self, event_type, callback):
        self._subscribers.setdefault(event_type, []).append(callback)

    def _trigger_local(self, event_num, event_type, *args, **kwargs):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(event_num, *args, **kwargs)


class RemoteEventServer(BaseRemoteEvent):
    def __init__(self, max_clients=4, port=8443, cert="server.crt", key="server.key"):
        # Server always starts at 1, step is max_clients + 1
        super().__init__(start_offset=1, step=max_clients + 1)
        self.port = port
        self.max_clients = max_clients
        self.current_client_count = 0

        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=cert, keyfile=key)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("0.0.0.0", self.port))
            sock.listen(self.max_clients)
            while True:
                client_sock, addr = sock.accept()
                conn = self.context.wrap_socket(client_sock, server_side=True)
                self.current_client_count += 1
                # Handshake: Tell client their ID (offset) and the global Step
                handshake = {"offset": self.current_client_count + 1, "step": self.step}
                conn.sendall(pickle.dumps(handshake))

                threading.Thread(
                    target=self._handle_client, args=(conn,), daemon=True
                ).start()

    def _handle_client(self, conn):
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                packet = pickle.loads(data)
                # Server receives event from client, triggers local subscribers
                self._trigger_local(
                    packet["num"], packet["type"], *packet["args"], **packet["kwargs"]
                )

    def notify(self, event_type, *args, **kwargs):
        """Server notifies all clients + local"""
        event_num = self.inc()
        # 1. Trigger local
        self._trigger_local(event_num, event_type, *args, **kwargs)
        # 2. Logic to loop through active 'conn' objects and sendall(packet) would go here


class RemoteEventClient(BaseRemoteEvent):
    def __init__(self, host="127.0.0.1", port=8443, cert_path="server.crt"):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations(cert_path)
        self.conn = None

    def connect(self):
        sock = socket.create_connection((self.host, self.port))
        self.conn = self.context.wrap_socket(sock, server_hostname=self.host)

        # Handshake: Get offset and step from server
        setup = pickle.loads(self.conn.recv(1024))
        super().__init__(start_offset=setup["offset"], step=setup["step"])

        threading.Thread(target=self._listen_to_server, daemon=True).start()

    def _listen_to_server(self):
        with self.conn:
            while True:
                data = self.conn.recv(4096)
                if not data:
                    break
                packet = pickle.loads(data)
                self._trigger_local(
                    packet["num"], packet["type"], *packet["args"], **packet["kwargs"]
                )

    def notify(self, event_type, *args, **kwargs):
        event_num = self.inc()
        packet = {"num": event_num, "type": event_type, "args": args, "kwargs": kwargs}
        # 1. Trigger local
        self._trigger_local(event_num, event_type, *args, **kwargs)
        # 2. Send to server
        if self.conn:
            self.conn.sendall(pickle.dumps(packet))
