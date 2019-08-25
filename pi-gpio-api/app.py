from flask import Flask, jsonify, request, abort
from functools import wraps
from pi import Pi


app = Flask(__name__)
pi = Pi()


def check_header(func):
    @wraps(func)
    def _check_header(*args, **kwargs):
        if not request.json:
            abort(400)
        return func(**kwargs)
    return _check_header


@app.route("/api/gpio/output/<int:channel>", methods=["POST"])
@check_header
def setOutput(channel):
    content = request.json
    if 'value' in content:
        status = {channel: pi.write(channel, int(content['value']))}
        return jsonify(status)
    abort(422)


@app.route("/api/gpio/input/<int:channel>", methods=["GET"])
def setInput(channel):
    status = {channel: pi.read(int(channel))}
    return jsonify(status)


@app.route("/api/gpio", methods=["GET"])
@app.route("/api/gpio/<int:channel>", methods=["GET"])
def getGPIO(channel=None):
    return jsonify(pi.getStatus(channel))


@app.route("/api/gpio/version", methods=["GET"])
@app.route("/api/gpio/info", methods=["GET"])
def info():
    return jsonify(pi.version())


if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)
