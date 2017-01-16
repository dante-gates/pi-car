from flask import Flask, request, has_request_context, render_template

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


@app.route('/_movement')
def _movement():
    return car.movement, 203


if __name__ == '__main__':
    import sys
    try:
        debug = sys.argv[1]
    except IndexError:
        debug = False
    if debug:
        app.debug=True
        app.run()
    else:
        app.run('0.0.0.0', 9999)
        app.run()

