import docker
import docker.errors
import requests

client = docker.from_env()


class Pod:
    def __init__(
        self,
        image: str,
        cpu: float,
        memory: int,
        host_port: int,
        container_port: int,
        name: str = None,
    ):
        self.image = image
        self.cpu = cpu
        self.memory = memory
        self.host_port = host_port
        self.ports = {container_port: host_port}
        self.name = name
        self._init_container()

    def _init_container(self):
        global client
        try:
            container = client.containers.run(
                self.image,
                detach=True,
                mem_limit=f"{self.memory}m",
                memswap_limit=f"{self.memory}m",
                cpu_shares=int(self.cpu * 1024),
                ports=self.ports,
                name=self.name,
            )
            self.id = container.short_id
        except docker.errors.ImageNotFound:
            raise ValueError(f"[ERROR] Image {self.image} not found")

    def start(self):
        try:
            container = client.containers.get(self.id)
            container.start()
        except docker.errors.APIError:
            self.clear()
            raise ValueError(f"[ERROR] Port {self.host_port} already in use")
        while not container.logs().decode("utf-8"):
            container.reload()

    def send_request(self, req):
        try:
            response = requests.post(
                f"http://localhost:{self.host_port}/invoke", json=req
            )
            if response.status_code != 200:
                raise ValueError(
                    f"[ERROR] Received non-200 response: {response.status_code}, Content: {response.text}"
                )
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                raise ValueError(
                    f"[ERROR] Failed to decode JSON response: {response.text}"
                )
        except requests.exceptions.ConnectionError:
            raise ValueError(f"[ERROR] Container {self.image}-{self.id} not running")

    def update_alloc(self, cpu=None, memory=None):
        if cpu:
            self.cpu = cpu
        if memory:
            self.memory = memory
        container = client.containers.get(self.id)
        container.update(
            cpu_shares=int(self.cpu * 1024),
            mem_limit=f"{self.memory}m",
            memswap_limit=f"{self.memory}m",
        )

    def clear(self):
        try:
            container = client.containers.get(self.id)
            container.remove(force=True)
        except docker.errors.NotFound:
            # already removed
            pass
