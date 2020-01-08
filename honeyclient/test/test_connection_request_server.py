import socket

from tr069 import connection_request_server


def test_server_automated(capsys):
    serv = connection_request_server.ConnectionRequestServer(("127.0.0.1", 0))
    assert connection_request_server.instance == serv
    assert repr(serv)

    assert "server listening" in capsys.readouterr()[0]

    sock = socket.socket()
    sock.connect(serv.sock.getsockname())
    sock.send(b"foo")
    assert sock.recv(4096) == connection_request_server.DEFAULT_REPLY

    assert serv.queue.get()
    assert serv.queue.empty()
    assert "Connection request" in capsys.readouterr()[0]

    sock.close()
    serv.shutdown()
    assert "server closed" in capsys.readouterr()[0]


def test_server_manual():
    serv = connection_request_server.ConnectionRequestServer(("127.0.0.1", 0), handle_manually=True)

    sock = socket.socket()
    sock.connect(serv.sock.getsockname())

    csock, addr = serv.queue.get()
    csock.send(b"foo")
    serv.queue.task_done()

    assert sock.recv(4096) == b'foo'
    assert serv.queue.empty()

    sock.close()
    serv.shutdown()
