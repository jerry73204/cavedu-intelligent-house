#!/bin/bash
# Fail script if any command fails.
set -e

# Check that script is run as root with sudo.
# Install dependencies.
apt-get -y install python-pip python-opencv python-dev
echo "Installation complete!"
echo
echo "Make sure to run sudo raspi-config and enable the camera."
