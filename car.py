from .gpio import Channel


class _Machinery:
    def __init__(self, channel, *args, **kwargs):
        self._channel = channel

    def move(self):
        with Channel(self._channel) as ch:
            ch.output(1)

class Car:
    _forward = _Machinery(11)

    def drive(self, direction):
        if direction == 'forward':
            self._drive_forward()

    def _drive_forward(self):
        self._forward.move()
