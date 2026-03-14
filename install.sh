#!/bin/bash
set -e

INSTALL_DIR="/opt/launchpad"
REPO="https://github.com/Flexicon/launchpad"

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root: curl -fsSL $REPO/raw/main/install.sh | sudo bash"
    exit 1
fi

if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Updating existing installation..."
    git -C "$INSTALL_DIR" pull
else
    echo "Cloning Launchpad..."
    git clone "$REPO" "$INSTALL_DIR"
fi

bash "$INSTALL_DIR/setup.sh"
