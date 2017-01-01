from .gpio import Channel
from flask import Flask, request, has_request_context


app = Flask(__name__)


@app.route('/pilot')
def pilot():
    if has_request_context():
        movement = request.get('d')
        with Channel(11) as ch:
            ch.strobe(10, 0.05)
    else:
        return 200  # TODO: what to return here?


if __name__ == '__main__':
    app.run('0.0.0.0', 9999)
