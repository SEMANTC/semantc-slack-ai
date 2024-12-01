# scripts/deploy.sh
#!/bin/bash

echo "Deploying Slack AI Assistant..."

# Build Docker image
docker build -t slack-ai-assistant:latest .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Docker image built successfully"
else
    echo "Error building Docker image"
    exit 1
fi

# Run container
docker run -d \
    --name slack-ai-assistant \
    -p 8080:8080 \
    --env-file .env \
    -v $(pwd)/credentials:/app/credentials \
    slack-ai-assistant:latest

echo "Deployment complete! Application is running on port 8080"