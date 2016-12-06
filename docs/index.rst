.. karellen-geventws documentation master file, created by
   sphinx-quickstart on Tue Dec  6 14:28:21 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to karellen-geventws's documentation!
=============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


karellen-geventws
================

karellen-geventws is a `WebSocket`_ library for the gevent_ networking library
It is a fork of gevent-websocket originally written by `Jeffrey Gelens`_

karellen-geventws It is licensed under the Apache 2.0 license.

::

    from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

    class EchoApplication(WebSocketApplication):
        def on_message(self, message):
            self.ws.send(message)

    WebSocketServer(
        ('', 8000),
        Resource({'/': EchoApplication})
    )


Add WebSockets to your WSGI application
=======================================

It isn't necessary to use the build-in `WebSocketServer` to start using
WebSockets. WebSockers can be added to existing applications very easy by
making the non-standard `wsgi.websocket` variable available in the WSGI
environment. An example using `Flask <http://flask.pocoo.org>`_ follows::

    from geventwebsocket import WebSocketServer, WebSocketError
    from flask import Flask, request, render_template

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api')
    def api():
        ws = request.environ.get('wsgi.websocket')

        if not ws:
            abort(400, "Expected WebSocket request")

        while True:
            try:
                message = ws.receive()
                ws.send("Your message was: {}".format(message))
            except WebSocketError:
                # Possibility to execute code when connection is closed
                break

    if __name__ == '__main__':
        server = WebSocketServer(("", 8000), app)
        server.serve_forever()

Also the browser Javascript application can be very simple::

    <!DOCTYPE html>
    <html>
    <head>
      <script>
        var ws = new WebSocket("ws://localhost:8000/api");

        ws.onopen = function() {
            ws.send("Hello, world");
        };
        ws.onmessage = function (event) {
            alert(event.data);
        };
      </script>
    </head>
    </html>

Features
========

- Framework for WebSocket servers and WebSocket subprotocols
- Implementation of RFC6455_ and Hybi-10+
- gevent_ based: high performance, asynchronous
- standards conformance (100% passes the `Autobahn Websocket Testsuite`_)

Installation
============

Distribute & Pip
----------------

Installing karellen-geventws is simple with `pip <http://www.pip-installer.org>`_::

    $ pip install karellen-geventws

Get the Code
------------

Requests is being developed on BitBucket.

You can clone the repsistory::

    git clone https://github.com/karellen/karellen-geventws

Once you have a copy, you can either embed it in your application, or installed
it on your system with::

    $ python setup.py install

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Autobahn Websocket Testsuite: http://autobahn.ws/testsuite
.. _RFC6455: http://datatracker.ietf.org/doc/rfc6455/?include_text=1
.. _WebSocket: http://www.websocket.org/aboutwebsocket.html
.. _repository: https://github.com/karellen/karellen-geventws
.. _PyPi: http://pypi.python.org/pypi/karellen-geventws/
.. _karellen-geventws: https://github.com/karellen/karellen-geventws
.. _gevent: http://www.gevent.org
.. _Jeffrey Gelens: http://www.noppo.pro
