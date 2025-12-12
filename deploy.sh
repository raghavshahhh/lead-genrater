#!/bin/bash

echo "🚀 RAGSPRO Deployment Script"
echo "=============================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker found"
echo ""

# Build Docker image
echo "📦 Building Docker image..."
docker build -t ragspro-dashboard:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"
echo ""

# Test Docker image locally
echo "🧪 Testing Docker image locally..."
echo "Starting container on port 5002..."
docker run -d -p 5002:5002 --name ragspro-test ragspro-dashboard:latest

if [ $? -ne 0 ]; then
    echo "❌ Docker run failed"
    exit 1
fi

echo "✅ Container started successfully"
echo ""
echo "🌐 Dashboard should be available at: http://localhost:5002"
echo ""
echo "To view logs: docker logs ragspro-test"
echo "To stop: docker stop ragspro-test"
echo "To remove: docker rm ragspro-test"
echo ""
echo "📝 Next steps for Render deployment:"
echo "1. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Add Docker and Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to Render Dashboard: https://dashboard.render.com"
echo "3. Click 'New +' -> 'Blueprint'"
echo "4. Connect your GitHub repo: raghavshahhh/lead-genrater"
echo "5. Render will auto-detect render.yaml and deploy!"
echo ""
echo "✅ Deployment script complete!"
