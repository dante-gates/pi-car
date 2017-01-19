# http://html5doctor.com/server-sent-events/
# https://mike.depalatis.net/flask-and-server-sent-events.html

import time

from flask import Flask, request, has_request_context, render_template, Response

from car import Car
from utils import MovementObserver


app = Flask(__name__)

observer = MovementObserver()
car = Car(observers=[observer])


@app.route('/')
def root():
    return render_template('client.html')


@app.route('/_drive')
def pilot():
    if has_request_context():
        movement = request.args.get('direction', None)  # None for testing
        car.drive(movement)
        return 'received', 200
    else:
        return 'foo', 200  # TODO: what to return here?


def _movement_stream(observer):
    while True:
        time.sleep(.1)
        if observer.movements:
            yield 'data: {"movement": "%s"}\n\n' % observer.movements.pop()


@app.route('/_movement')
def _movement():
    global observer
    resp = Response(_movement_stream(observer), mimetype='text/event-stream')
    return resp


if __name__ == '__main__':
    import logging
    logging.basicConfig(level='DEBUG')
    app.run('0.0.0.0', 9999)
    app.run(threaded=True)
