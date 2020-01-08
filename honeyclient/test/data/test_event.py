import textwrap

from tr069 import event


def test_from_xml():
    assert event.from_xml("") == []

    e, = event.from_xml("""
    <Event soap-enc:arrayType="cwmp:EventStruct[1]">
        <EventStruct>
            <EventCode>4 VALUE CHANGE</EventCode>
            <CommandKey>foo</CommandKey>
        </EventStruct>
    </Event>""")
    assert e.code == "4 VALUE CHANGE"
    assert e.command_key == "foo"


def test_event_to_xml():
    e = event.Event(
        "foo",
        "bar",
    )
    assert repr(e)
    assert e.to_xml() == textwrap.dedent('''
    <EventStruct>
        <EventCode>foo</EventCode>
        <CommandKey>bar</CommandKey>
    </EventStruct>
    ''').strip()
