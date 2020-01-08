from tr069.data import device
from tr069.data import rpcs


def test_inform():
    assert rpcs.make_inform(device=device.DEFAULT)


def test_warn_missing_param(capsys):
    d = device.Device("a", "b", "c", "d")
    assert rpcs.make_inform(device=d)
    assert "Missing required inform parameter" in capsys.readouterr()[1]
