import time
from multiprocessing import Manager, Process

from app import *
from flask import Flask, jsonify, request


class Server:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.client = Flask(__name__)
        self._init_routes()
        # <-----------------------------> #
        self.manager = Manager()
        self.res_pool = self.manager.Queue()
        self.function_mapper = {
            "fibonacci": fibonacci,
            "pyaes": aes,
            "matmul": matmul,
            "linalg": linalg,
        }

    def _wrapper(self, id, func, params):
        start = time.perf_counter()
        func(params)
        end = time.perf_counter()
        self.res_pool.put({"id": id, "real_time": end - start})

    def _get_resps(self):
        resps = []
        while not self.res_pool.empty():
            res = self.res_pool.get()
            resps.append(res)
        return resps

    def _init_routes(self):
        @self.client.route("/invoke", methods=["POST"])
        def invoke():
            start = time.perf_counter()
            b_req = request.get_json()
            ###### decompose batched request ######
            b_id = b_req["id"]
            reqs = b_req["reqs"]
            slo = b_req["SLO"]
            #######################################
            processes = []
            for req in reqs:
                id = req["id"]
                function_name = req["function_name"]
                slo = req["SLO"]
                params = req["params"]
                # ----------------------------------
                if function_name not in self.function_mapper:
                    return jsonify({"error": "function not found"})
                # ----------------------------------
                p = Process(
                    target=self._wrapper,
                    kwargs={
                        "id": id,
                        "func": self.function_mapper[function_name],
                        "params": params,
                    },
                )
                processes.append(p)
            for p in processes:
                p.start()
            for p in processes:
                p.join()
            resps = self._get_resps()
            end = time.perf_counter()
            b_res = {
                "id": b_id,
                "real_time": end - start,
                "resps": resps,
            }
            return jsonify(b_res)

    def run(self):
        self.client.run(host=self.host, port=self.port)


if __name__ == "__main__":
    demo = Server()
    demo.run()
