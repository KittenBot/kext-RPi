#!/bin/bash

# Check if Python is installed
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 is required but it's not installed. Aborting."; exit 1; }

# Install necessary Python libraries
pip3 install aiohttp arduinobootloader intelhex

# Clone
git clone https://github.com/kittenbot/kext-rpi.git

# Change directory
cd kext-rpi

# Create a systemd service
echo "[Unit]
Description=Kblock Rpi Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 $(pwd)/server.py
WorkingDirectory=$(pwd)
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$(whoami)

[Install]
WantedBy=multi-user.target" > kblock-rpi.service

# Copy the service to systemd
sudo cp kblock-rpi.service /etc/systemd/system/

# Enable the service
sudo systemctl enable kblock-rpi.service
sudo systemctl start kblock-rpi.service
