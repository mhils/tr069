import io
import queue
import socket
import threading
from typing import Tuple, Optional

import click

# We try to bait the requesting entity into sending credentials using basic authentication.
# The requesting entity should refuse this to prevent replay attacks.
DEFAULT_REPLY = (
    b'HTTP/1.1 401 Unauthorized\r\n'
    b'WWW-Authenticate: Basic realm="CPE"\r\n'
    b'Connection: keep-alive\r\n'
    b'Content-Length: 0\r\n'
    b'\r\n'
    b'HTTP/1.1 200 OK\r\n'
    b'Content-Length: 0\r\n'
    b'Connection: close\r\n'
    b'\r\n'
)


class ConnectionRequestServer:
    """
    A minimal TR-069 Connection Request Server.

    Main purpose of this module is to detect that providers are sending
    connection requests, it implements no authentication whatsoever.
    Connection requests are acknowledged automatically by default
    and will be printed to stdout. For non-interactive use, users may
    call instance.queue.get() to wait for a connection request.
    """
    sock: socket.socket
    thread: threading.Thread
    queue: queue.Queue
    handle_manually: bool
    address: str

    def __init__(
            self,
            address: Tuple[str, int] = ("", 7547),
            handle_manually: bool = False
    ) -> None:
        self.handle_manually = handle_manually

        self.queue = queue.Queue()
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(address)
        self.sock.listen(5)
        host, port = self.sock.getsockname()
        self.address = f"{host}:{port}"

        click.secho(
            f"=== Connection request server listening on {self.address} ===",
            fg="magenta", bold=True
        )

        self.thread = threading.Thread(
            target=self.run,
            daemon=True,
        )
        self.thread.start()

        global instance
        instance = self

    def __repr__(self):
        return f"ConnectionRequestServer({self.address})"

    def shutdown(self) -> None:
        self.sock.close()
        self.thread.join()

    def run(self):
        while True:
            try:
                sock, addr = self.sock.accept()
            except OSError:
                break
            sock.settimeout(1)
            click.secho(f"\n=== Connection request from {addr[0]} ===", fg="magenta", bold=True)
            self.queue.put((sock, addr))
            if self.handle_manually:
                self.queue.join()
            else:
                try:
                    sock.sendall(DEFAULT_REPLY)
                except OSError:  # pragma: no cover
                    pass

                # Read from the socket until timeout kicks in.
                received = io.BytesIO()
                for _ in range(1024):
                    try:
                        received.write(sock.recv(4096))
                    except OSError:  # pragma: no cover
                        break

                click.secho(
                    received.getvalue().decode("ascii", "backslashreplace").rstrip(),
                )
            sock.close()
        click.secho(
            f"=== Connection request server closed on {self.address} ===",
            fg="magenta", bold=True
        )


instance = None  # type: Optional[ConnectionRequestServer]
