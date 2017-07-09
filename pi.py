from os import environ

ENV = environ["PI_ENV"]
if ENV == "DEBUG":
    import rpi_debug as GPIO
else:
    import RPi.GPIO as GPIO


class Pi(object):

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.status = {}

    def __del__(self):
        self.clean()

    def clean(self):
        GPIO.cleanup()

    def setInput(self, channel):
        GPIO.setup(channel, GPIO.IN)
        self.status[channel] = 'input'

    def setOutput(self, channel):
        GPIO.setup(channel, GPIO.OUT)
        self.status[channel] = 'output'

    def read(self, channel):
        return GPIO.input(channel)

    def write(self, channel, state):
        GPIO.output(channel, state)

    def status(self, channel = None):
        if channel in self.status:
            return self.status[channel]
        return self.status

    def version(self):
        print(GPIO.RPI_INFO)
        print(GPIO.VERSION)
