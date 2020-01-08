from tr069.data import rpcs


def test_get_rpc_methods():
    assert rpcs.make_get_rpc_methods()
