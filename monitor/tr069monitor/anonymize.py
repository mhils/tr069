import re
from typing import Optional

from mitmproxy.net.http import Message


# From the tr069 package.
# We probably want to declare that as a dependency at some point.
def extract_rpc_name(xml: str) -> Optional[str]:
    message_type = re.search(r"<[-\w]+:Body>\s*<(.+?)[ /]*>", xml, re.IGNORECASE)
    if message_type:
        return message_type.group(1)
    return None


def fully_anonymize(message: Message) -> None:
    """
    Anonymize TR-069 RPC in place.

    Message contents are redacted almost entirely, only the RPC method name is retained.
    """
    message.headers.clear()
    rpc = extract_rpc_name(message.text)
    message.text = f"<!-- redacted -->\n<soap:Body><{rpc}/></soap:Body>"


def redact(message: Message) -> None:
    """
    Redact the most sensitive information -- passwords and authentication credentials -- of a
    TR-069 RPC in place.
    """
    for x in ["cookie", "set-cookie", "authorization"]:
        message.headers.pop(x, None)
    message.text = re.sub(
        r"<[^<>]*Password[^<>]*>.+?</[^<>]*Password[^<>]*>",
        "<!-- redacted pass -->",
        message.text,
        flags=re.IGNORECASE
    )
    if "password" in message.text.lower():
        # This should not happen anymore... let's be safe and redact entirely.
        fully_anonymize(message)
