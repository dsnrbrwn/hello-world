"""
Core game logic independent of UI framework
This module contains the game state and logic that can be shared
between desktop (Pygame) and mobile (Kivy) versions
"""

import random
import time
from typing import Dict, List, Tuple, Optional

class GameState:
    """Core game state that's independent of the UI framework"""
    
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """Reset game to initial state"""
        self.day = 1
        self.time_passed = 0
        self.game_over = False
        self.victory = False
        
        # Player stats
        self.player_health = 100
        self.player_stamina = 100
        self.player_morale = 100
        self.player_x = 512  # Center position
        self.player_y = 384
        self.player_alive = True
        
        # Resources
        self.food = 50
        self.water = 30
        self.medicine = 10
        self.fuel = 20
        self.weapons = 5
        
        # Game progress
        self.distance_traveled = 0
        self.target_distance = 1000
        self.current_event = None
        
        # Statistics
        self.deaths_from_starvation = 0
        self.deaths_from_disease = 0
        self.deaths_from_violence = 0
        self.total_events_faced = 0
    
    def update(self, dt: float):
        """Update game state - call this every frame"""
        if self.game_over or not self.player_alive:
            return
        
        # Update time
        self.time_passed += dt
        
        # Advance day every 60 seconds of real time
        if self.time_passed >= 60:
            self.advance_day()
            self.time_passed = 0
        
        # Check for random events
        if random.randint(1, 1000) == 1:
            self.trigger_random_event()
        
        # Check death conditions
        if self.player_health <= 0:
            self.player_alive = False
            self.game_over = True
        
        # Check victory conditions
        if self.distance_traveled >= self.target_distance:
            self.victory = True
    
    def move_player(self, dx: float, dy: float):
        """Move player and update distance traveled"""
        if not self.player_alive:
            return
            
        # Update position
        self.player_x += dx
        self.player_y += dy
        
        # Update distance traveled
        distance_this_move = (dx**2 + dy**2)**0.5
        self.distance_traveled += distance_this_move * 0.1  # Scale factor
        
        # Moving costs stamina
        self.player_stamina -= distance_this_move * 0.01
        if self.player_stamina < 0:
            self.player_stamina = 0
            # Exhaustion damages health
            self.player_health -= 0.5
    
    def advance_day(self):
        """Advance to next day with resource consumption"""
        self.day += 1
        
        # Daily resource consumption
        self.food -= random.randint(3, 7)
        self.water -= random.randint(5, 10)
        self.fuel -= random.randint(1, 3)
        
        # Apply effects of resource shortage
        if self.food <= 0:
            self.player_health -= 15
            self.food = 0
        if self.water <= 0:
            self.player_health -= 20
            self.water = 0
        if self.fuel <= 0:
            self.player_health -= 5  # Cold/exposure
            self.fuel = 0
        
        # Restore some stamina each day
        self.player_stamina = min(100, self.player_stamina + 20)
        
        # Random daily events
        if random.randint(1, 3) == 1:
            self.trigger_daily_event()
    
    def trigger_random_event(self):
        """Trigger a random encounter"""
        events = [
            {
                "title": "Wild Animal Attack",
                "description": "A hostile animal blocks your path!",
                "choices": [
                    {"text": "Fight it (-health, +food if win)", "id": "fight_animal"},
                    {"text": "Run away (-stamina)", "id": "flee_animal"},
                    {"text": "Use weapon (-weapon)", "id": "weapon_animal"}
                ]
            },
            {
                "title": "Sick Traveler",
                "description": "You encounter a sick traveler asking for help.",
                "choices": [
                    {"text": "Help them (-medicine, +morale)", "id": "help_sick"},
                    {"text": "Ignore them (-morale)", "id": "ignore_sick"},
                    {"text": "Rob them (+resources, -morale)", "id": "rob_sick"}
                ]
            },
            {
                "title": "Resource Cache",
                "description": "You found an abandoned supply cache!",
                "choices": [
                    {"text": "Take everything (+resources)", "id": "take_all"},
                    {"text": "Take only what you need (+some resources)", "id": "take_some"},
                    {"text": "Leave it for others (+morale)", "id": "leave_cache"}
                ]
            }
        ]
        
        self.current_event = random.choice(events)
        self.total_events_faced += 1
    
    def trigger_daily_event(self):
        """Trigger a daily event"""
        daily_events = [
            "Harsh weather slows your progress",
            "You found some berries along the way",
            "A storm damages your supplies",
            "You met friendly travelers who shared food"
        ]
        
        event = random.choice(daily_events)
        if "weather" in event or "storm" in event:
            self.player_health -= random.randint(5, 15)
            self.fuel -= random.randint(1, 5)
        elif "berries" in event or "food" in event:
            self.food += random.randint(2, 8)
    
    def handle_event_choice(self, choice_id: str):
        """Handle player's choice for current event"""
        if not self.current_event:
            return
        
        if choice_id == "fight_animal":
            if random.randint(1, 2) == 1:  # 50% chance to win
                self.player_health -= random.randint(10, 25)
                self.food += random.randint(5, 15)
            else:
                self.player_health -= random.randint(20, 40)
        
        elif choice_id == "flee_animal":
            self.player_stamina -= 30
        
        elif choice_id == "weapon_animal":
            if self.weapons > 0:
                self.weapons -= 1
                self.food += random.randint(8, 20)
            else:
                # No weapon available, fight with bare hands
                self.player_health -= random.randint(15, 35)
        
        elif choice_id == "help_sick":
            if self.medicine > 0:
                self.medicine -= 1
                self.player_morale += 10
            else:
                self.player_morale -= 5
        
        elif choice_id == "ignore_sick":
            self.player_morale -= 15
        
        elif choice_id == "rob_sick":
            self.food += random.randint(1, 5)
            self.water += random.randint(1, 3)
            self.player_morale -= 25
        
        elif choice_id == "take_all":
            self.food += random.randint(10, 20)
            self.water += random.randint(5, 15)
            self.medicine += random.randint(1, 5)
            self.fuel += random.randint(3, 10)
        
        elif choice_id == "take_some":
            self.food += random.randint(3, 8)
            self.water += random.randint(2, 6)
            self.medicine += random.randint(0, 2)
        
        elif choice_id == "leave_cache":
            self.player_morale += 20
        
        # Clear current event
        self.current_event = None
    
    def get_status(self) -> Dict:
        """Get current game status for UI"""
        return {
            "day": self.day,
            "health": self.player_health,
            "stamina": self.player_stamina,
            "morale": self.player_morale,
            "food": self.food,
            "water": self.water,
            "medicine": self.medicine,
            "fuel": self.fuel,
            "weapons": self.weapons,
            "distance_traveled": int(self.distance_traveled),
            "target_distance": self.target_distance,
            "progress": (self.distance_traveled / self.target_distance) * 100,
            "alive": self.player_alive,
            "game_over": self.game_over,
            "victory": self.victory,
            "current_event": self.current_event
        }