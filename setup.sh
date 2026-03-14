#!/bin/bash
set -e

cd /opt/launchpad

# Create dedicated system user if it doesn't exist
if ! id launchpad &>/dev/null; then
    useradd --system --no-create-home --shell /usr/sbin/nologin --groups docker launchpad
    echo "Created user: launchpad"
else
    # Make sure launchpad is in the docker group
    usermod -aG docker launchpad
    echo "User launchpad already exists, ensured docker group membership"
fi

# Files owned by invoking user, group-readable by launchpad
OWNER=$(stat -c '%U' /opt/launchpad)
chown -R "$OWNER":launchpad /opt/launchpad
chmod -R g+rX /opt/launchpad

python3 -m venv venv
venv/bin/pip install -r requirements.txt

cp launchpad.service /etc/systemd/system/launchpad.service
systemctl daemon-reload
systemctl enable launchpad
systemctl restart launchpad

echo "Launchpad is running at http://localhost:7777"
