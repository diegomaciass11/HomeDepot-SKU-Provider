#!/bin/bash

# Instalar Chrome
mkdir -p /opt/chrome
curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
apt update && apt install -y ./chrome.deb
cp "$(which google-chrome)" /opt/chrome/chrome

# Instalar Chromedriver
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
curl -sSL "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -o chromedriver.zip
unzip chromedriver.zip
mv chromedriver /opt/chromedriver
chmod +x /opt/chromedriver
