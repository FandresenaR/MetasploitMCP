#!/bin/bash
# Quick deployment script for Fly.io

set -e

echo "🚀 MetasploitMCP Fly.io Deployment Script"
echo "=========================================="

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed."
    echo "Install it with: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

echo "✅ flyctl found"

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "❌ Not logged in to Fly.io"
    echo "Run: flyctl auth login"
    exit 1
fi

echo "✅ Logged in to Fly.io"

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found in current directory"
    exit 1
fi

echo "✅ Dockerfile found"

# Check if fly.toml exists
if [ ! -f "fly.toml" ]; then
    echo "⚠️  fly.toml not found. Running flyctl launch..."
    flyctl launch --no-deploy
else
    echo "✅ fly.toml found"
fi

# Ask user if they want to set secrets
echo ""
read -p "Do you want to set environment secrets? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Setting secrets..."
    read -p "Enter MSFRPCD_PASSWORD (or press Enter to skip): " msf_pass
    if [ ! -z "$msf_pass" ]; then
        flyctl secrets set MSFRPCD_PASSWORD="$msf_pass"
    fi
    
    read -p "Enter OPENROUTER_API_KEY (or press Enter to skip): " openrouter_key
    if [ ! -z "$openrouter_key" ]; then
        flyctl secrets set OPENROUTER_API_KEY="$openrouter_key"
    fi
fi

# Deploy
echo ""
echo "🚢 Deploying to Fly.io..."
flyctl deploy

echo ""
echo "✅ Deployment complete!"
echo "📊 Check status: flyctl status"
echo "📜 View logs: flyctl logs"
echo "🌐 Open app: flyctl open"
