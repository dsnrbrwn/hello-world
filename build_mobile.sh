#!/bin/bash

# Death Game Simulator - Mobile Build Script
# This script helps you build the Android APK from the Kivy mobile version

echo "🎮 Death Game Simulator - Mobile Build Script"
echo "=============================================="

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer not found. Installing mobile requirements..."
    pip install -r requirements_mobile.txt
else
    echo "✅ Buildozer found"
fi

# Check if Android SDK is setup
if [ -z "$ANDROID_SDK_ROOT" ] && [ -z "$ANDROID_HOME" ]; then
    echo "⚠️  Android SDK not detected. Buildozer will download it automatically."
    echo "   This may take a while on first run..."
fi

# Create debug APK
echo "🔨 Building Android APK..."
echo "   This may take 30-60 minutes on first build..."

buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📱 APK file is located in: bin/deathgamesimulator-0.1-armeabi-v7a-debug.apk"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Copy APK to your Android device"
    echo "   2. Enable 'Unknown Sources' in Android settings"
    echo "   3. Install and run the APK"
else
    echo "❌ Build failed. Check the output above for errors."
    echo "💡 Common solutions:"
    echo "   - Install Java 8 or 11"
    echo "   - Install Android SDK"
    echo "   - Check buildozer.spec configuration"
fi