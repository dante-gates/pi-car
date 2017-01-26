import logging
import time

from constants import Movements as mv
from utils.gpio import Channel
from utils.log import Logging


class _Machinery:
    def __init__(self, channel, *args, **kwargs):
        self._channel = channel

    def move(self):
        with Channel(self._channel) as ch:
            ch.output(1)
            time.sleep(.005)


class Car:
    _forward = _Machinery(11)
    _logger = Logging.get_logger(__name__)

    def __init__(self, observers=[]):
        self._observers = observers
        self.movement = mv.stop

    def drive(self, direction):
        self.movement = direction
        self._logger.debug(self.movement)
        if direction == mv.forward:
            self._drive_forward()
        self.movement = mv.stop

    def add_observer(self, observer):
        self._observers.append(observer)

    def _drive_forward(self):
        self._forward.move()

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, val):
        self._movement = val
        for obs in self._observers:
            obs.receive(self._movement)
