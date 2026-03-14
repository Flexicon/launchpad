# Launchpad

A homeserver index page that displays your configured services and running Docker containers.

## Requirements

- Python 3.x
- Docker (running)

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example config and edit it to add your services:

```bash
cp services.example.yaml services.yaml
```

Run the app:

```bash
python app.py
```

Launchpad will be available at **http://localhost:7777**.

## Linux / systemd

To install as a persistent system service on Linux with systemd:

```bash
sudo bash setup.sh
```

This creates a `launchpad` system user, installs dependencies into a virtualenv at `/opt/launchpad`, and starts the service automatically on boot.

## Configuration

Edit `services.yaml`:

```yaml
services:
  - name: My App
    url: http://192.168.1.x:8080
    external_url: https://myapp.example.com  # optional, used when accessing remotely
    description: A short description
    tags: [web]
```

The `external_url` is used automatically when Launchpad is accessed from outside the local network.

## License

Public domain — see [UNLICENSE](UNLICENSE).
