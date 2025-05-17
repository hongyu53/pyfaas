import requests

if __name__ == "__main__":
    url = "http://localhost:5000/invoke"
    resp = requests.post(
        url,
        json={
            "id": 1,
            "reqs": [
                {
                    "id": 1,
                    "function_name": "fibonacci",
                    "SLO": 0.5,
                    "params": {"n": 10},
                },
                {
                    "id": 2,
                    "function_name": "pyaes",
                    "SLO": 0.5,
                    "params": {
                        "message_len": 100,
                    },
                },
                {
                    "id": 3,
                    "function_name": "matmul",
                    "SLO": 0.5,
                    "params": {
                        "size": 1000,
                    },
                },
                {
                    "id": 4,
                    "function_name": "linalg",
                    "SLO": 0.5,
                    "params": {
                        "size": 1000,
                    },
                },
            ],
            "SLO": 0.5,
        },
    )
    print(resp.json())
