# http://html5doctor.com/server-sent-events/
# https://mike.depalatis.net/flask-and-server-sent-events.html

import time

from flask import Flask, request, has_request_context, render_template, Response
import gevent
from gevent.queue import Queue
from gevent.wsgi import WSGIServer

from car import Car
from utils import Observer


app = Flask(__name__)
car = Car()

import logging

_logger = logging.getLogger(__name__)


@app.route('/')
def root():
    return render_template('client.html')


@app.route('/drive')
def pilot():
    if has_request_context():
        movement = request.args.get('direction', None)
        _logger.debug('request to drive: %s' % movement)
        car.drive(movement)
        return 'received', 200
    else:
        return 'foo', 200  # TODO: what to return here?


@app.route('/subscribe/movement')
def subscribe_movement():
    _logger.debug('subscribing to movements')
    def stream():
        obs = Observer()
        car.add_observer(obs)
        try:
            while True:
                _logger.debug('waiting to get movement...')
                res = obs.get()
                _logger.debug('got movement: %s' % res)
                yield 'data: %s\n\n' % res
                _logger.debug('sent movement to client: %s' % res)
        except GeneratorExit:
            pass

    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    import logging
    logging.basicConfig(level='DEBUG')
    server = WSGIServer(('localhost', 9999), app)
    server.serve_forever()
