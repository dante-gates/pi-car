# http://html5doctor.com/server-sent-events/
# https://mike.depalatis.net/flask-and-server-sent-events.html


from flask import Flask, request, has_request_context, render_template, Response

from .car import Car


app = Flask(__name__)
car = Car()


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


def _movement_stream():
    prev = car.movement
    while True:
        cur = car.movement
        if not cur == prev:
            yield 'data: {"movement": "%s"}\n\n' % cur


@app.route('/_movement')
def _movement():
    resp = Response(_movement_stream(), mimetype='text/event-stream')
    return resp


if __name__ == '__main__':
    import logging
    import sys
    logging.getLogger().setLevel('DEBUG')
    logging.basicConfig()
    try:
        debug = sys.argv[1]
    except IndexError:
        debug = False
    if debug:
        app.debug=True
        app.run()
    else:
        app.run('0.0.0.0', 9999)
        app.run(threaded=True)

