#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from gevent.monkey import patch_all

patch_all()

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from socket import socket
from logging import getLogger, shutdown
from logging.config import dictConfig
import sys

from unittest import TestCase
from websocket import create_connection
from threading import Thread


def http_handler(environ, start_response):
    start_response("400 Bad Request", [])

    return ["WebSocket connection is expected here."]


class WSTests(TestCase):
    @classmethod
    def setUpClass(cls):
        dictConfig({
            "version": 1,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "stream": sys.stdout
                }
            },
            "loggers": {
                __name__: {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": False
                }
            }
        })

    @classmethod
    def tearDownClass(cls):
        shutdown()

    def setUp(self):
        s_socket = socket()
        s_socket.bind(("localhost", 0))
        s_socket.listen(100)
        self.s_socket = s_socket
        self.err = []

    def tearDown(self):
        self.server.stop(10)
        self.s_socket.close()

    def start_server(self):
        self.server.serve_forever()

    def test_echo(self):
        data = []
        data.append("012345679")
        data.append("012345679" * 20)
        data.append("012345679" * 2000)
        data.append("012345679" * 20000)
        data.append("012345679" * 200000)

        data.append(b"012345679")
        data.append(b"012345679" * 20)
        data.append(b"012345679" * 2000)
        data.append(b"012345679" * 20000)
        data.append(b"012345679" * 200000)

        def test_echo_actual(environ, start_response):
            try:
                websocket = environ.get("wsgi.websocket")

                if websocket is None:
                    return http_handler(environ, start_response)

                while True:
                    message = websocket.receive()
                    websocket.send(message)
                websocket.close()
            except Exception as e:
                self.err.append(e)

        server = WSGIServer(self.s_socket, application=test_echo_actual, handler_class=WebSocketHandler)
        server.logger = getLogger(__name__)
        server.start()
        self.server = server
        try:
            self.server_thread = Thread(target=self.start_server)
            self.server_thread.start()

            ws = create_connection("ws://%s:%s/" % (self.server.environ["SERVER_NAME"],
                                                    self.server.environ["SERVER_PORT"]))


            try:
                for i in range(2):
                    if i == 1:
                        ws.set_mask_key(lambda _: b'1234')
                    for d in data:
                        if isinstance(d, bytes):
                            ws.send_binary(d)
                        else:
                            ws.send(d)
                        self.assertEqual(ws.recv(), d)

                    ws.ping("ping")
                    pong = ws.recv_data_frame(10)
                    self.assertEqual(pong[0], pong[1].OPCODE_PONG)
                    self.assertEqual(pong[1].data, b'ping')
                    self.assertFalse(self.err)
            finally:
                ws.close()
        finally:
            server.close()
