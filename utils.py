from collections import deque
import logging


class MovementObserver:
	movements = deque()
	_logger = logging.getLogger(__name__)

	def recieve_signal(self, movement):
		self._logger.debug('received movement %s' % movement)
		self.movements.append(movement)
