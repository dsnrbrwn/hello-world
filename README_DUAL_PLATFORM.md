# Death Game Simulator - Dual Platform

A 2D survival simulation game inspired by Oregon Trail, but with a darker twist. Now available on both **Desktop** and **Mobile** platforms!

## 🎮 Game Overview

Navigate a hostile environment where death lurks around every corner. Manage scarce resources, make difficult moral choices, and survive long enough to reach safety. Features permadeath - when you die, you're truly dead.

## 📱 Platform Support

### Desktop Version (Pygame)
- **Controls**: Keyboard (WASD/Arrow keys) + Mouse
- **Platforms**: Windows, macOS, Linux
- **Graphics**: High-resolution 1024x768

### Mobile Version (Kivy) 
- **Controls**: Touch screen (drag to move)
- **Platforms**: Android (iOS buildable)
- **Graphics**: Responsive UI, optimized for mobile

## 🚀 Quick Start

### Desktop Version
```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Mobile Version (Testing on Desktop)
```bash
# Install mobile dependencies
pip install -r requirements_mobile.txt

# Run mobile version on desktop (for testing)
python mobile_main.py
```

## 📦 Building for Mobile

### Android APK
```bash
# Make build script executable
chmod +x build_mobile.sh

# Build Android APK
./build_mobile.sh
```

The APK will be created in `bin/deathgamesimulator-0.1-armeabi-v7a-debug.apk`

### Manual Build
```bash
# Install buildozer
pip install buildozer

# Initialize buildozer (first time only)
buildozer init

# Build debug APK
buildozer android debug

# Build release APK (for distribution)
buildozer android release
```

## 🎯 How to Play

### Desktop Controls
- **WASD** or **Arrow Keys**: Move player
- **Mouse**: Navigate menus and make choices
- **ESC**: Return to menu
- **R**: Restart when dead

### Mobile Controls
- **Drag**: Move player around the screen
- **Tap**: Select menu options and event choices
- **Menu Button**: Access game options
- **Rest Button**: Restore stamina (advances day)

## 🎲 Game Features

### Core Mechanics
- **Resource Management**: Food, Water, Medicine, Fuel, Weapons
- **Health System**: Health, Stamina, Morale tracking
- **Environmental Hazards**: Weather, terrain, wildlife
- **Random Events**: Moral choices that affect survival
- **Permadeath**: No respawning when you die

### Victory Conditions
- Reach the target distance (1000 units)
- Survive the journey while managing resources
- Make smart decisions during random encounters

## 🛠️ Development

### Project Structure
```
├── game/
│   ├── core_game.py        # Shared game logic
│   ├── game_engine.py      # Desktop-specific engine
│   ├── player.py           # Desktop player class
│   ├── ui.py              # Desktop UI components
│   └── ...                # Other desktop modules
├── main.py                 # Desktop entry point
├── mobile_main.py          # Mobile entry point
├── requirements.txt        # Desktop dependencies
├── requirements_mobile.txt # Mobile dependencies
└── buildozer.spec         # Android build configuration
```

### Shared Logic
Both versions use the same core game logic (`game/core_game.py`) but different UI frameworks:
- **Desktop**: Pygame for graphics and input
- **Mobile**: Kivy for touch interface and responsive design

## 📋 Requirements

### Desktop
- Python 3.7+
- Pygame 2.5.2+
- NumPy 1.24.3+

### Mobile Development
- Python 3.7+
- Kivy 2.2.0+
- Buildozer 1.5.0+
- Android SDK (auto-downloaded by buildozer)
- Java 8 or 11

### Android Device
- Android 5.0+ (API level 21+)
- 50MB storage space
- ARM or x86 processor

## 🐛 Troubleshooting

### Desktop Issues
- **Pygame not found**: Run `pip install pygame`
- **Display issues**: Update your graphics drivers
- **Performance problems**: Lower FPS in game_engine.py

### Mobile Build Issues
- **Buildozer fails**: Install Java 8 or 11
- **SDK issues**: Set ANDROID_SDK_ROOT environment variable
- **Build timeout**: Increase timeout in buildozer.spec
- **APK won't install**: Enable "Unknown Sources" in Android settings

### Common Solutions
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools

# Clean buildozer cache
buildozer android clean

# Reinstall dependencies
pip install -r requirements_mobile.txt --force-reinstall
```

## 🎨 Customization

### Graphics
- Desktop: Edit drawing functions in `game/ui.py`
- Mobile: Modify widget graphics in `mobile_main.py`

### Game Balance
- Edit resource consumption in `game/core_game.py`
- Adjust event probabilities and outcomes
- Modify victory conditions and difficulty

### Controls
- Desktop: Change key bindings in `game/player.py`
- Mobile: Adjust touch sensitivity in `mobile_main.py`

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on both platforms
5. Submit a pull request

## 🎯 Roadmap

- [ ] iOS support
- [ ] Web version (Pygame Web)
- [ ] Multiplayer mode
- [ ] Enhanced graphics
- [ ] Sound effects
- [ ] Save/load system
- [ ] Achievement system

---

**Ready to test your survival skills?** 

- **Desktop**: `python main.py`
- **Mobile**: `python mobile_main.py` (or build APK)

Good luck, survivor! 🏃‍♂️💀