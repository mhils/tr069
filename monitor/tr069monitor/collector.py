"""
A minimal log collector for TR-069 monitors.

This should ultimately be replaced with something more sophisticated,
but our favored technology isn't there yet: https://github.com/trivago/gollum/issues/70
"""
import ssl
from typing import IO

import tornado.ioloop
import tornado.web
import tornado.httpserver


class FlowCollector(tornado.web.RequestHandler):
    def post(self):
        self.settings["flow_file"].write(self.request.body)
        self.settings["flow_file"].flush()
        print(".", end="", flush=True)


def make_app(flow_file: IO[bytes]):
    return tornado.web.Application(
        [(r"/", FlowCollector)],
        flow_file=flow_file
    )


if __name__ == "__main__":
    with open("data/tr069.log", "ab") as f:
        app = make_app(f)
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile="cert.crt", keyfile="cert.key")
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_context)
        http_server.listen(443)
        tornado.ioloop.IOLoop.current().start()
