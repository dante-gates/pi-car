import logging
import gevent
from gevent.queue import Queue


class Logging:
	_format = '[%(asctime)s][%(levelname)-8s][%(module)-9s][%(msg)s]'

	@classmethod
	def get_logger(cls, name):
		logger = logging.getLogger(__name__)
		Logging.format_logger(logger)
		logger.setLevel('DEBUG')
		return logger

	@classmethod
	def format_logger(cls, logger):
		if not logger.handlers:
			hdl = logging.StreamHandler()
			fmt = logging.Formatter(cls._format)
			hdl.setFormatter(fmt)
			logger.addHandler(hdl)


class Observer:
	_logger = Logging.get_logger(__name__)

	def __init__(self):
		self._q = Queue()

    def receive(self, movement):
        self._logger.debug('received movement %s' % movement)
        def pub():
                self._q.put(movement)
        gevent.spawn(pub)


	def get(self):
		return self._q.get()

	def empty(self):
		return self._q.empty()
