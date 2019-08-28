from flask import Flask, jsonify, request, abort
from pi_gpio_api.core.pi import Pi
from pi_gpio_api.core.pin_layout import IO_PINS, POWER_PINS


app = Flask('pi_gpio_api')
pi = Pi()


@app.route('/api/gpio/io/<int:channel>', methods=['POST'])
def set_channel_status(channel):
    if not request.json:
        abort(400)
    if channel not in IO_PINS:
        abort(400., 'Invalid pin')

    content = request.json

    if content.get('type'):
        pi.set_channel_function(channel, content.get('type'))
    if content.get('value'):
        pi.write(channel, content.get('value'))

    status = {'status': pi.gpio_status(channel)}
    return jsonify(status)


@app.route('/api/gpio/io/<int:channel>', methods=['GET'])
@app.route('/api/gpio/io/', methods=['GET'])
def channel_status(channel=None):
    if not channel:
        channel = IO_PINS
    elif channel not in IO_PINS:
        abort(400, "Not an IO pin")
    return jsonify(io=pi.gpio_status(channel))


@app.route('/api/gpio/power/<int:channel>', methods=['GET'])
@app.route('/api/gpio/power/', methods=['GET'])
def power_channels(channel=None):
    if not channel:
        channel = POWER_PINS
    elif channel not in POWER_PINS:
        abort(400, "Not a power pin")
    return jsonify(power_pins=pi.gpio_status(channel))


@app.route('/api/gpio/', methods=['GET'])
def all_channels():
    return jsonify(io=pi.gpio_status(IO_PINS),
                   power_pins=pi.gpio_status(POWER_PINS))


@app.route('/api/gpio/info/', methods=['GET'])
def info():
    return jsonify(revision=pi.info())


def run(host='0.0.0.0', port=5000):
    app.run(host=host, port=port)
