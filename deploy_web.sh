#!/bin/bash

# Web Deployment Script for Death Game Simulator
# This script builds the game for web browsers using pygame-web

echo "🌐 Death Game Simulator - Web Deployment"
echo "========================================"

# Check if pygbag is installed
if ! command -v pygbag &> /dev/null; then
    echo "📦 Installing pygame-web (pygbag)..."
    pip install --break-system-packages pygbag
fi

# Create web build
echo "🔨 Building web version..."
echo "   This creates WebAssembly files that run in browsers"

# Build the game for web
pygbag --width 800 --height 600 --name "Death Game Simulator" main_web.py

if [ $? -eq 0 ]; then
    echo "✅ Web build successful!"
    echo ""
    echo "📋 Deployment Instructions:"
    echo "   1. Files are in the 'dist' directory"
    echo "   2. Upload the entire 'dist' folder to your web server"
    echo "   3. Access via: https://yourserver.com/dist/"
    echo ""
    echo "🔗 For local testing:"
    echo "   python3 -m http.server 8000"
    echo "   Then visit: http://localhost:8000/dist/"
else
    echo "❌ Web build failed"
    echo "💡 Try installing pygame-web manually:"
    echo "   pip install pygbag"
fi