import logging
import gevent
from gevent.queue import Queue


class Observer:
	_logger = logging.getLogger(__name__)

	def __init__(self):
		self._q = Queue()

	def receive(self, movement):
		self._logger.debug('received movement %s' % movement)
		def pub():
			self._q.put(movement)
		gevent.spawn(pub)

	def get(self):
		return self._q.get()
