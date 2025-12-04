#!/bin/bash

echo "🚀 Deploying Lead Generation Bot to GitHub"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files..."
git add .

# Commit
echo "💾 Committing changes..."
read -p "Enter commit message (default: 'Update system'): " commit_msg
commit_msg=${commit_msg:-"Update system"}
git commit -m "$commit_msg"

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo "🔗 Adding GitHub remote..."
    read -p "Enter your GitHub repository URL: " repo_url
    git remote add origin "$repo_url"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://render.com"
echo "2. Sign up / Login with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your repository"
echo "5. Add environment variables:"
echo "   - GEMINI_API_KEY"
echo "   - GMAIL_ADDRESS"
echo "   - GMAIL_APP_PASSWORD"
echo "6. Click 'Create Web Service'"
echo ""
echo "🎉 Your app will be live in 5-10 minutes!"
