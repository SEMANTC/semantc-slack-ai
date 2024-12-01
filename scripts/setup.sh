# scripts/setup.sh
#!/bin/bash

echo "Setting up Slack AI Assistant..."

# Create necessary directories
mkdir -p credentials
mkdir -p logs

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Using Python version: $python_version"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "Setup complete! Don't forget to update your .env file with your credentials."