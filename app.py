#from .gpio import Channel
from flask import Flask, request, has_request_context, render_template


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('client.html')


@app.route('/_drive')
def pilot():
    if has_request_context():
        movement = request.args.get('direction', None)  # None for testing
        print(movement)
#        with Channel(11) as ch:
#            ch.strobe(10, 0.05)
        return 200
    else:
        return 'foo', 200  # TODO: what to return here?



if __name__ == '__main__':
    app.run()
