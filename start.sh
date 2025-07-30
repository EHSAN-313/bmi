#!/bin/bash

echo "========================================"
echo "  Instagram DM Automation Tool"
echo "========================================"
echo ""
echo "Starting the application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(sys.version_info.major, sys.version_info.minor)" | tr ' ' '.')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Python $required_version or higher is required"
    echo "Current version: Python $python_version"
    exit 1
fi

# Install dependencies
echo "Installing/updating dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo ""
echo "Dependencies installed successfully!"
echo ""
echo "Starting Instagram DM Automation Tool..."
echo ""
echo "The web interface will be available at:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Make the script executable
chmod +x start.sh

# Start the Flask server
python3 server.py