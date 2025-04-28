import threading

import requests


class User:
    def __init__(self, client_host="localhost", client_port=5000):
        self.client_host = client_host
        self.client_port = client_port

    def send_req(self, function_name, SLO, params={"foo": "bar"}):
        def _send_req(function_name, SLO, params):
            try:
                response = requests.post(
                    f"http://{self.client_host}:{self.client_port}/invoke",
                    json={
                        "function_name": function_name,
                        "SLO": SLO,
                        "params": params,
                    },
                )
                return response.json()
            except requests.exceptions.ConnectionError:
                raise ValueError(f"[ERROR] Server not running")

        threading.Thread(
            target=_send_req,
            args=(function_name, SLO, params),
        ).start()


if __name__ == "__main__":
    user = User(client_port=6000)
    user.send_req(
        function_name="fibonacci",
        SLO=0.5,
        params={"n": 10},
    )
