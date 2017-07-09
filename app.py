from flask import Flask, jsonify, request, abort
from functools import wraps


app = Flask(__name__)


def check_header(func):
    @wraps(func)
    def _check_header(*args, **kwargs):
        if not request.json:
            abort(400)
        return func(**kwargs)
    return _check_header


@app.route("/api/gpio", methods=["POST"])
@check_header
def setGPIO(act={}):
    act = "post"
    return jsonify(act)


@app.route("/api/gpio/channel/<int:channel>", methods=["GET"])
def getGPIO(channel):
    return jsonify(channel)


@app.route("/api/gpio/channel/<int:channel>", methods=["PUT"])
@check_header
def updateGPIO(channel={}):
    act = "put"
    return jsonify(act)


@app.route("/api/gpio/channel/<int:channel>", methods=["DELETE"])
def deleteGPIO(channel):
    act = "del"
    return jsonify(act)


if __name__ == "__main__":
    app.run(debug=True)
