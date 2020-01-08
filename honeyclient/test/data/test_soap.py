from tr069.data import soap


def test_soapify():
    assert soap.CWMP_VERSION in soap.soapify("")


def test_fix_cwmp_id():
    assert soap.fix_cwmp_id("", "") == ""

    assert soap.fix_cwmp_id("""
    <cwmp:ID SOAP-ENV:mustUnderstand="1">foo</cwmp:ID>
    """, """
    <cwmp:ID SOAP-ENV:mustUnderstand="1">2</cwmp:ID>
    """) == """
    <cwmp:ID SOAP-ENV:mustUnderstand="1">2</cwmp:ID>
    """

    assert soap.fix_cwmp_id(
        "<cwmp:ID>foo</cwmp:ID>",
        "<cwmp:ID SOAP-ENV:mustUnderstand=\"1\">2</cwmp:ID>"
    ) == "<cwmp:ID>2</cwmp:ID>"

    assert soap.fix_cwmp_id("<cwmp:ID>foo</cwmp:ID>", "") == "<cwmp:ID>foo</cwmp:ID>"
    assert soap.fix_cwmp_id("", "<cwmp:ID>foo</cwmp:ID>") == ""


def test_extract_rpc_name():
    assert soap.extract_rpc_name("<soap:Body><cwmp:Foo>") == "cwmp:Foo"
    assert soap.extract_rpc_name("<soap:Body><cwmp:Foo />") == "cwmp:Foo"
    assert soap.extract_rpc_name("<SOAP-ENV:Body><cwmp:Foo>") == "cwmp:Foo"
    assert soap.extract_rpc_name("<cwmp:Foo>") is None
    assert soap.extract_rpc_name("") is None
