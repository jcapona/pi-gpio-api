import RPi.GPIO as GPIO
from pi_gpio_api.core import pin_layout


class Pi(object):
    channel_functions = {
        GPIO.IN: 'Input',
        GPIO.OUT: 'Output',
        GPIO.I2C: 'I2C',
        GPIO.SPI: 'SPI',
        GPIO.HARD_PWM: 'HARD_PWM',
        GPIO.SERIAL: 'Serial',
        GPIO.UNKNOWN: 'Unknown'
    }

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.status = {}

    def __del__(self):
        self.clean()

    def clean(self, channel=None):
        if channel:
            return GPIO.cleanup(channel)
        GPIO.cleanup()

    def __get_function_by_string(self, fcn_string):
        for k, v in self.channel_functions.items():
            if v.lower() == fcn_string:
                return k

    def set_channel_function(self, channel, fnc):
        if channel not in pin_layout.IO_PINS:
            raise AttributeError('Can\'t change function to non IO pins')

        self.clean(channel)
        GPIO.setup(channel, self.__get_function_by_string(fnc))

    def read(self, channel):
        if channel in pin_layout.POWER_PINS:
            return

        try:
            ret = GPIO.input(channel)
        except Exception as e:
            ret = 'ERROR: ' + str(e)
        return ret

    def write(self, channel, state):
        if channel not in pin_layout.IO_PINS:
            raise AttributeError('Can\'t write to non IO pins')

        state = GPIO.HIGH if state else GPIO.LOW
        try:
            GPIO.output(channel, state)
        except Exception as e:
            print('ERROR: ' + str(e))

    def info(self):
        return {
            'revision': GPIO.RPI_INFO,
        }

    def gpio_status(self, channel=None):
        pins = pin_layout.ALL_PINS if not channel else [channel]

        data = []
        for p in pins:
            status = {}
            status['pin'] = p
            status['pin_function'] = self.pin_function_name(p)
            if p in pin_layout.IO_PINS:
                status['pin_state'] = self.read(p)
            data.append(status)

        return data

    def pin_function_name(self , pin):
        try:
            descr = self.set_channel_functions[GPIO.gpio_function(pin)]
        except:
            descr = pin_layout.pin_description(pin)
        return descr