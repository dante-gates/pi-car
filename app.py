# http://html5doctor.com/server-sent-events/
# https://mike.depalatis.net/flask-and-server-sent-events.html

import time

from flask import Flask, request, has_request_context, render_template, Response

from car import Car
import constants as cn
from utils.log import Logging


app = Flask(__name__)
car = Car()

_logger = Logging.get_logger(__name__)


@app.route('/')
def root():
    return render_template('client.html', movements=cn.Movements)


@app.route('/drive')
def pilot():
    if has_request_context():
        movement = request.args.get('direction', None)
        _logger.debug('request to drive: %s' % movement)
        car.drive(movement)
        return 'received', 200
    else:
        return 'foo', 200  # TODO: what to return here?


if __name__ == '__main__':
    app.run('0.0.0.0', 9999)
