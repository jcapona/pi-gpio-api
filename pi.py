import RPi.GPIO as GPIO


class Pi(object):

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.status = {}

    def __del__(self):
        self.clean()

    def clean(self, channel=None):
        if channel:
            GPIO.cleanup(channel)
        else:
            GPIO.cleanup()

    def setInput(self, channel):
        if channel in self.status and self.status[channel] is 'input':
            pass
        GPIO.setup(channel, GPIO.IN)
        self.status[channel] = {'type': 'input'}

    def setOutput(self, channel):
        if channel in self.status and self.status[channel] is 'output':
            pass
        GPIO.setup(channel, GPIO.OUT)
        self.status[channel] = {'type': 'output'}

    def read(self, channel):
        try:
            self.setInput(channel)
            ret = GPIO.input(channel)
        except Exception as e:
            ret = 'ERROR: ' + str(e)
        return ret

    def write(self, channel, state):
        try:
            self.setOutput(channel)
            GPIO.output(channel, state)
            self.status[channel].update({'status': state})
        except Exception as e:
            return 'ERROR: ' + str(e)
        return 'Ok'

    def getStatus(self, channel = None):
        if channel in self.status:
            return {channel: self.status[channel]}
        return self.status

    def version(self):
        return {
            'info': GPIO.RPI_INFO,
            'version': GPIO.VERSION
        }
