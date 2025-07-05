# 2D Death Game Simulator

A brutal 2D survival simulation inspired by Oregon Trail, but with a deadly twist. Navigate a hostile environment where death lurks around every corner and resources are scarce.

## 🎮 Game Overview

You are a lone survivor in a harsh, unforgiving world. Your goal is simple: **survive as long as possible**. But in this death game, every decision matters, resources are scarce, and death is permanent.

### Key Features

- **Permadeath**: When you die, you're truly dead - no respawning
- **Resource Management**: Carefully manage food, water, medicine, weapons, and fuel
- **Random Events**: Face unexpected challenges and moral dilemmas
- **Environmental Hazards**: Avoid storms, predators, and bandit camps
- **Dynamic World**: Terrain affects resource availability and survival chances
- **Day/Night Cycle**: Each day brings new challenges and resource consumption

## 🚀 Quick Start

### Installation

1. **Install Python 3.7+** if you haven't already
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

```bash
python main.py
```

## 🎯 How to Play

### Controls
- **WASD or Arrow Keys**: Move your character
- **SPACE**: Start game (from menu)
- **ESC**: Return to menu
- **R**: Restart (when dead)

### Game Mechanics

#### Resources
- **Food**: Prevents starvation (consumed daily)
- **Water**: Prevents dehydration (consumed daily)  
- **Medicine**: Heals injuries and prevents illness
- **Weapons**: Used for hunting and defense
- **Fuel**: Used for warmth and transportation

#### Survival
- Resources are consumed daily
- Running out of food or water damages your health
- Random events can help or harm you
- Environmental hazards pose constant threats
- Your health decreases to zero = permanent death

#### Terrain Types
- **Grass**: Can find food (berries, small game)
- **Water**: Refill your water supplies
- **Mountains**: Find medicine (herbs) or weapon materials
- **Desert**: Harsh conditions, limited resources
- **Dirt**: Neutral terrain

#### Environmental Hazards
- **Storms**: Moving weather systems that deal damage
- **Predators**: Dangerous animals that attack
- **Bandit Camps**: Hostile survivors

### Death Game Elements

Unlike Oregon Trail, this game is designed to be lethal:
- **Frequent deadly events**: Illness, injury, equipment loss
- **Severe resource scarcity**: Resources run out quickly
- **Environmental hostility**: Weather and terrain are dangerous
- **No mercy**: Bad decisions lead to permanent consequences
- **Moral choices**: Help others vs. self-preservation

## 🎲 Random Events

The game features numerous random events that test your survival skills:

- **Medical emergencies**: Illness, injuries that require medicine
- **Equipment problems**: Lost or damaged supplies
- **Social encounters**: Other survivors, merchants, moral dilemmas
- **Environmental challenges**: Severe weather, dangerous terrain
- **Resource discoveries**: Finding supplies or losing them

## 🏆 Victory Conditions

- **Survive as long as possible**: Track your personal best
- **Day counter**: See how many days you can survive
- **Death statistics**: Learn from your failures

## 🔧 Technical Details

- **Language**: Python 3.7+
- **Graphics**: Pygame
- **Architecture**: Modular design with separate systems
- **Performance**: 60 FPS target, optimized for smooth gameplay

## 📁 Project Structure

```
death-game-simulator/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── game/                   # Game package
│   ├── __init__.py
│   ├── game_engine.py      # Core game loop
│   ├── player.py           # Player character
│   ├── world.py            # Game world and terrain
│   ├── resource_manager.py # Resource management
│   ├── event_manager.py    # Random events
│   └── ui.py               # User interface
├── GAME_CONCEPT.md         # Detailed game design
└── README.md               # This file
```

## 🎮 Strategy Tips

1. **Conserve resources**: Don't waste food/water early on
2. **Avoid hazards**: Storms and predators are deadly
3. **Explore terrain**: Different areas offer different resources
4. **Manage health**: Use medicine before it's too late
5. **Make hard choices**: Sometimes helping others isn't worth it

## 🔮 Future Enhancements

- **Interactive events**: Player choice in encounters
- **Multiplayer**: Compete with other survivors
- **Larger world**: More terrain types and locations
- **Skill system**: Character progression and specialization
- **Story mode**: Narrative-driven survival scenarios
- **Graphics upgrade**: Better sprites and animations

## 🐛 Known Issues

- Events are currently auto-resolved (future: player choice)
- Limited terrain variety
- No save/load system (by design - permadeath)

## 🤝 Contributing

This is a consultative project for learning game development. Feel free to:
- Suggest new features
- Report bugs
- Propose gameplay improvements
- Add new event types

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Remember: In this death game, survival isn't guaranteed. Every decision matters. Good luck!**
