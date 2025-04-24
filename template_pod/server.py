import time

from app import fibonacci
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/invoke", methods=["POST"])
def invoke():
    start = time.perf_counter()
    req = request.get_json()
    # ----------------------------------
    id = req["id"]
    function_name = req["function_name"]
    slo = req["SLO"]
    params = req["params"]
    # ----------------------------------
    fibonacci(params["n"])
    end = time.perf_counter()
    res = {
        "id": id,
        "real_time": end - start,
    }
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
