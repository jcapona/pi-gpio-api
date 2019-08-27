from flask import Flask, jsonify, request, abort
from pi_gpio_api.core.pi import Pi
from pi_gpio_api.core.pin_layout import IO_PINS


app = Flask(__name__)
pi = Pi()


@app.route('/api/gpio/<int:channel>', methods=['POST'])
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


@app.route('/api/gpio/<int:channel>', methods=['GET'])
@app.route('/api/gpio/', methods=['GET'])
def channel_status(channel=None):
    return jsonify(data=pi.gpio_status(channel))


@app.route('/api/gpio/info/', methods=['GET'])
def info():
    return jsonify(pi.info())


def run(host='0.0.0.0', port=5000):
    app.run(host=host, port=port)
