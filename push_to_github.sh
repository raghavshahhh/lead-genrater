#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     GitHub Push Script - Lead Generation Bot            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo "Install from: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check if already initialized
if [ -d ".git" ]; then
    echo "📦 Git repository already initialized"
else
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
fi

echo ""
echo "📝 Adding files to git..."
git add .
echo "✅ Files added"

echo ""
echo "💾 Creating commit..."
git commit -m "Initial commit - Premium Lead Generation System"
echo "✅ Commit created"

echo ""
echo "🔗 Setting up GitHub remote..."
echo ""
echo "⚠️  IMPORTANT: First create a repository on GitHub!"
echo "   1. Go to: https://github.com/new"
echo "   2. Name: lead-generation-bot"
echo "   3. Keep it PRIVATE"
echo "   4. Don't initialize with README"
echo "   5. Click 'Create Repository'"
echo ""

read -p "Have you created the repository? (yes/no): " created

if [ "$created" != "yes" ]; then
    echo ""
    echo "❌ Please create the repository first, then run this script again"
    exit 1
fi

echo ""
read -p "Enter your GitHub username: " username

if [ -z "$username" ]; then
    echo "❌ Username cannot be empty!"
    exit 1
fi

echo ""
echo "🔗 Adding remote..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$username/lead-generation-bot.git"
echo "✅ Remote added"

echo ""
echo "🌿 Setting branch to main..."
git branch -M main
echo "✅ Branch set"

echo ""
echo "⬆️  Pushing to GitHub..."
echo ""
echo "⚠️  You'll need to enter your GitHub credentials:"
echo "   Username: $username"
echo "   Password: Use Personal Access Token (not regular password)"
echo ""
echo "   Get token from: https://github.com/settings/tokens"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                  ✅ SUCCESS!                             ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Code pushed to GitHub successfully!"
    echo ""
    echo "📍 Your repository:"
    echo "   https://github.com/$username/lead-generation-bot"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Go to: https://render.com"
    echo "   2. Sign up with GitHub"
    echo "   3. Create new Web Service"
    echo "   4. Connect your repository"
    echo "   5. Add environment variables"
    echo "   6. Deploy!"
    echo ""
    echo "📖 See DEPLOY_ONLINE.md for detailed instructions"
else
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "Common issues:"
    echo "   1. Wrong username/password"
    echo "   2. Use Personal Access Token instead of password"
    echo "   3. Repository not created on GitHub"
    echo "   4. Internet connection issue"
    echo ""
    echo "Get Personal Access Token:"
    echo "   https://github.com/settings/tokens"
fi
