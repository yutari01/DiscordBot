#!/bin/bash
set -e

echo "Starting the installation script..."
echo "Updating APT package lists..."
sudo apt update

echo "Installing system dependencies: ffmpeg, libopus0..."
sudo apt install -y ffmpeg libopus0

echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo "Installing Python packages: discord.py, yt-dlp, PyNaCl, google-api-python-client, spotipy, accelerate..."
python3 -m pip install -U discord.py yt-dlp PyNaCl google-api-python-client spotipy accelerate
python3 -m pip install git+https://github.com/shumingma/transformers.git

echo "All installations completed successfully!"
exit 0