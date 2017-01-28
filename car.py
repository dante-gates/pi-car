import logging
import time
from threading import Thread
from queue import Queue

from constants import Movements as mv
from utils.concurrency import Sentinel
from utils.gpio import Channel
from utils.log import Logging


class _Machinery:
    def __init__(self, channel, *args, **kwargs):
        self._channel = channel

    def move(self):
        with Channel(self._channel) as ch:
            ch.output(1)
            time.sleep(.005)


Shutdown = Sentinel('Shutdown')


# TODO: make car singleton
class Car:
    _forward = _Machinery(11)
    _logger = Logging.get_logger(__name__)

    def __init__(self, observers=[]):
        self._observers = observers
        self.movement = mv.stop
        self._commands = Queue()

    def start(self):
        def run(instance):
            while True:
                command = instance._commands.get()
                instance._logger.debug('Got command %s' % command)
                if command is Shutdown:
                    instance._logger.info('Shutting down')
                    break
                else:
                    instance._drive(command)
        t = Thread(target=run, args=(self,))
        t.start()

    def add_command(self, command):
        if command == 'shutdown':
            command = Shutdown
        self._commands.put(command)

    def _drive(self, direction):
        self.movement = direction
        self._logger.debug('Moving ' + self.movement)
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
