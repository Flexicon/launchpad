import re
import yaml
import docker
from flask import Flask, render_template, request

app = Flask(__name__)


def get_docker_containers():
    try:
        client = docker.from_env()
        containers = []
        for c in client.containers.list():
            ports = []
            for container_port, bindings in (c.ports or {}).items():
                if bindings:
                    for b in bindings:
                        host_port = b.get("HostPort")
                        if host_port:
                            ports.append(host_port)
                else:
                    # exposed but not published
                    ports.append(container_port.split("/")[0])
            containers.append({
                "name": c.name,
                "image": c.image.tags[0] if c.image.tags else c.image.short_id,
                "status": c.status,
                "ports": ports,
            })
        return containers, None
    except Exception as e:
        return [], str(e)


def get_services():
    try:
        with open("services.yaml") as f:
            data = yaml.safe_load(f)
        return data.get("services", [])
    except FileNotFoundError:
        return None


_LOCAL_HOST_RE = re.compile(r'^(localhost|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+)(:\d+)?$')


def is_local_request():
    host = request.host
    return bool(_LOCAL_HOST_RE.match(host))


@app.route("/")
def index():
    containers, docker_error = get_docker_containers()
    services = get_services()
    local = is_local_request()
    return render_template("index.html",
                           containers=containers,
                           docker_error=docker_error,
                           services=services,
                           local=local)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)
