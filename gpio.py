import time
import RPi.GPIO as GPIO


class Channel:
    def __init__(self, channel, *args, **kwargs):
        # args, kwargs passed to setup
        self._channel = channel
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.OUT, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, ex_val, ex_ty, ex_tb):
        self.output(0)
        GPIO.cleanup(self._channel)

    def output(self, state):
        GPIO.output(self._channel, state)

    def strobe(self, howlong, pause=0.5):
        t_lapse = 0
        state = 0
        while 1:
            state = (state + 1) % 2
            self.output(state)
            time.sleep(pause)
            t_lapse += pause
            if t_lapse > howlong:
                break
