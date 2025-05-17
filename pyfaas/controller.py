import atexit
import threading
import time
from multiprocessing import Manager, Process, Value

from flask import Flask, jsonify, request
from pyfaas.pod import Pod


class Controller:
    def __init__(self, host="localhost", port=5000):
        # controller is composed of: client, and scheduler.
        self.manager = Manager()
        atexit.register(self._atexit)

        ###################
        ## client config ##
        ###################
        self.host = host
        self.port = port
        self.client = Flask(__name__)
        self._init_routes()

        self.req_pool = self.manager.Queue()
        self.res_pool = self.manager.dict()
        self.id_counter = Value("i", 0)

        ######################
        ## scheduler config ##
        ######################
        self.pods = self.manager.Queue()

    ############
    ## Client ##
    ############
    def _next_id(self):
        with self.id_counter.get_lock():
            id = self.id_counter.value
            self.id_counter.value += 1
        return id

    def _init_routes(self):
        @self.client.route("/invoke", methods=["POST"])
        def invoke():
            req = request.get_json()
            id = self._next_id()
            req["id"] = id
            arrival_time = time.perf_counter()
            print(f"Receiving request-{id}")
            self.req_pool.put(req)

            while not id in self.res_pool:
                time.sleep(0.5)

            res = self.res_pool[id]
            completion_time = time.perf_counter()
            req["e2e_time"] = completion_time - arrival_time
            req["real_time"] = res["real_time"]
            del self.res_pool[id]
            return jsonify(res)

    def run(self):
        Process(target=self.schedule, daemon=True).start()
        self.client.run(host=self.host, port=self.port)

    # <------------------------------------------------> #

    ###############
    ## Scheduler ##
    ###############
    def create_pod(self, image, cpu, memory, host_port, container_port, name=None):
        pod = Pod(image, cpu, memory, host_port, container_port, name)
        self.pods.put(pod)
        pod.start()
        return pod

    def _get_reqs(self):
        reqs = []
        while not self.req_pool.empty():
            req = self.req_pool.get()
            reqs.append(req)
        return reqs

    def _send_req(self, req):
        if not self.pods.empty():
            pod = self.pods.get()
        else:
            pod = self.create_pod(
                image="ditto",
                cpu=0.25,
                memory=256,
                host_port=10000 + req["id"],
                container_port=5000,
            )
        res = pod.send_request(req)
        self.pods.put(pod)
        id = req["id"]
        self.res_pool[id] = res

    def schedule(self):
        #####################################
        ## Template FCFS scheduling policy ##
        #####################################
        while True:
            try:
                reqs = self._get_reqs()
                if reqs:
                    for req in reqs:
                        threading.Thread(target=self._send_req, args=(req,)).start()
                time.sleep(0.5)
            except KeyboardInterrupt:
                break

    def _atexit(self):
        print("[INFO] Waiting...")
        # clear all pods
        while not self.pods.empty():
            pod = self.pods.get()
            pod.clear()


if __name__ == "__main__":
    demo = Controller(port=6000)
    demo.run()
