import logging

from .gpio import Channel


class _Machinery:
    def __init__(self, channel, *args, **kwargs):
        self._channel = channel

    def move(self):
        with Channel(self._channel) as ch:
            ch.output(1)

class Car:
    movement = 'stopped'
    _forward = _Machinery(11)
    _logger = logging.getLogger(__name__)

    def drive(self, direction):
        self.movement = direction
        self._logger.debug(self.movement)
        if direction == 'forward':
            self._drive_forward()
        # self.movement = 'stopped'

    def _drive_forward(self):
        self._forward.move()
