#!/bin/bash

# Install necessary Python libraries
pip3 install aiohttp arduinobootloader intelhex

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
