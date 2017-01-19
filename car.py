import logging

from gpio import Channel


class _Machinery:
    def __init__(self, channel, *args, **kwargs):
        self._channel = channel

    def move(self):
        with Channel(self._channel) as ch:
            ch.output(1)

class Car:
    _forward = _Machinery(11)
    _logger = logging.getLogger(__name__)

    def __init__(self, observers=[]):
        self._observers = observers
        self.movement = 'stopped'

    def drive(self, direction):
        self.movement = direction
        self._logger.debug(self.movement)
        if direction == 'forward':
            self._drive_forward()
        self.movement = 'stopped'

    def _drive_forward(self):
        self._forward.move()

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, val):
        self._movement = val
        for obs in self._observers:
            obs.recieve_signal(self._movement)
