# PyFaaS - A Python Simulation For Serverless

![Serverless](https://img.shields.io/badge/Serverless-FD5750.svg?style=for-the-badge&logo=Serverless&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)

PyFaaS is a lightweight Function-as-a-Service (FaaS) framework designed to manage and execute serverless functions using Docker containers. It provides a simple client-server architecture for invoking functions with specified Service Level Objectives (SLOs).

## Features

- **Dynamic Pod Management**: Automatically creates and manages Docker containers (pods) for executing functions.
- **Customizable Resource Allocation**: Allows specifying CPU and memory limits for each pod.
- **Logging**: Tracks request execution times and logs them to a YAML file.
- **Graceful Shutdown**: Ensures proper cleanup of resources during shutdown.

## Project Structure

```
pyfaas/
├── controller.py
├── pod.py
├── user.py
└── logs.yaml
template_pod/
├── app.py
├── server.py
├── dockerfile
└── requirement.txt
```

## Requirements

- Python 3.10+
- Docker installed and running
- Required Python packages (see `setup.py`)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd pyfaas
   ```
2. Setup the package:

   ```bash
   pip install .
   ```
3. Ensure Docker is installed and running:

   ```bash
   docker --version
   ```

## Example

### Build the Template Pod

Build the template pod:

```bash
cd template_pod
docker build -t fibonacci .
```

### Start the Controller

Run the `controller.py` to start the server:

```bash
cd pyfaas
python controller.py
```

The server will start on `localhost:6000` by default.

### Send Requests

Use the `user.py` script to send function invocation requests:

```bash
python user.py
```

Example request:

```python
user = User(client_port=6000)
response = user.send_req(
    function_name="fibonacci",
    SLO=0.5,
    params={"n": 10},
)
print(response)
```

### Logs

Execution logs are saved in `logs.yaml`:

```yaml
0:
  function_name: fibonacci
  SLO: 0.5
  params:
    n: 10
  e2e_time: 0.123
  real_time: 0.12
```

## Graceful Shutdown

The framework ensures proper cleanup of Docker containers during shutdown. Use `Ctrl+C` to terminate the server, and all active pods will be cleared automatically.
