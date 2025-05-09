#!/bin/bash
# Unified uninstallation script for Licensing System

# Detect environment
if [ -d "/usr/local/cpanel" ]; then
    ENV="cpanel"
    INSTALL_DIR="/home/$(whoami)/public_html/lic"
else
    ENV="standard"
    INSTALL_DIR="/opt/lic"
fi

echo "Detected environment: $ENV"
echo "Uninstalling from: $INSTALL_DIR"

# Check if running as root (required for standard installation)
if [ "$ENV" = "standard" ] && [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root for standard installation. Please use sudo."
    exit 1
fi

# Check if installation directory exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Installation directory not found: $INSTALL_DIR"
    exit 1
fi

# Stop the application
echo "Stopping the application..."
if [ "$ENV" = "standard" ]; then
    systemctl stop licensing.service
    systemctl disable licensing.service
    rm -f /etc/systemd/system/licensing.service
    systemctl daemon-reload
else
    if [ -f "$INSTALL_DIR/app.pid" ]; then
        pid=$(cat "$INSTALL_DIR/app.pid")
        if ps -p $pid > /dev/null; then
            kill $pid
            rm -f "$INSTALL_DIR/app.pid"
        fi
    fi
fi

# Remove virtual environment
echo "Removing virtual environment..."
rm -rf "$INSTALL_DIR/venv"

# Remove application files
echo "Removing application files..."
rm -rf "$INSTALL_DIR/app"
rm -rf "$INSTALL_DIR/alembic"
rm -f "$INSTALL_DIR/.env"
rm -f "$INSTALL_DIR/requirements.txt"
rm -f "$INSTALL_DIR/app.log"
rm -f "$INSTALL_DIR/start.sh"
rm -f "$INSTALL_DIR/stop.sh"
rm -f "$INSTALL_DIR/status.sh"
rm -f "$INSTALL_DIR/restart.sh"
rm -f "$INSTALL_DIR/logs.sh"
rm -f "$INSTALL_DIR/create_admin.py"
rm -f "$INSTALL_DIR/alembic.ini"
rm -f "$INSTALL_DIR/__pycache__"
rm -rf "$INSTALL_DIR/app/__pycache__"
rm -rf "$INSTALL_DIR/app/api/__pycache__"
rm -rf "$INSTALL_DIR/app/core/__pycache__"
rm -rf "$INSTALL_DIR/app/db/__pycache__"
rm -rf "$INSTALL_DIR/app/models/__pycache__"
rm -rf "$INSTALL_DIR/app/schemas/__pycache__"
rm -rf "$INSTALL_DIR/app/services/__pycache__"

# Remove installation directory if empty
if [ -z "$(ls -A $INSTALL_DIR)" ]; then
    echo "Removing empty installation directory..."
    rmdir "$INSTALL_DIR"
fi

echo "Uninstallation complete!"
