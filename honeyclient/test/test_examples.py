import os
import runpy
from pathlib import Path

import mock

root_dir = Path(__file__).parent / '..'
example_dir = root_dir / 'examples'

@mock.patch('requests.Session')
def test_01_introduction(Session):
    Session().post().text = ""
    Session().post().status_code = 204
    runpy.run_path(str(example_dir / "01_introduction.py"))


def test_02_devices():
    os.chdir(root_dir)
    runpy.run_path(str(example_dir / "02_devices.py"))


@mock.patch('requests.Session')
def test_03_rpcs(Session):
    Session().post().text = ""
    Session().send = Session().post
    runpy.run_path(str(example_dir / "03_rpcs.py"))


@mock.patch('time.sleep')
@mock.patch('tr069.ConnectionRequestServer')
def test_04_connection_request(ConnectionRequestServer, _):
    ConnectionRequestServer().queue.get.return_value = "sock", "addr"
    runpy.run_path(str(example_dir / "04_connection_requests.py"))


def test_05_proxy():
    runpy.run_path(str(example_dir / "05_proxy.py"))


def test_06_authentication():
    runpy.run_path(str(example_dir / "06_authentication.py"))
