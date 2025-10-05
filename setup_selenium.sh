#!/bin/bash
# Setup script for Selenium and ChromeDriver

echo "Setting up Selenium and ChromeDriver..."

# Check if Chrome is installed
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    echo "Chrome/Chromium not found. Installing Chromium..."
    sudo apt-get update
    sudo apt-get install -y chromium-browser chromium-chromedriver
else
    echo "Chrome/Chromium found"
fi

# Install ChromeDriver if not present
if ! command -v chromedriver &> /dev/null; then
    echo "Installing ChromeDriver..."
    
    # Get Chrome version
    CHROME_VERSION=$(google-chrome --version 2>/dev/null || chromium-browser --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+')
    echo "Chrome version: $CHROME_VERSION"
    
    # Download matching ChromeDriver
    wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O /tmp/chromedriver_version
    CHROMEDRIVER_VERSION=$(cat /tmp/chromedriver_version)
    
    echo "Downloading ChromeDriver version: $CHROMEDRIVER_VERSION"
    wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -O /tmp/chromedriver.zip
    
    unzip -q /tmp/chromedriver.zip -d /tmp/
    sudo mv /tmp/chromedriver /usr/local/bin/
    sudo chmod +x /usr/local/bin/chromedriver
    
    rm /tmp/chromedriver.zip /tmp/chromedriver_version
    
    echo "ChromeDriver installed successfully"
else
    echo "ChromeDriver already installed"
fi

# Verify installation
echo ""
echo "Verification:"
chromedriver --version
google-chrome --version 2>/dev/null || chromium-browser --version 2>/dev/null

echo ""
echo "✓ Selenium setup complete!"
echo "You can now run the scraper with Selenium support."
