#!/usr/bin/env python3
"""
Death Game Simulator - Text Version
A console-based survival game that works anywhere!
"""

import random
import time
import os

class TextDeathGameSimulator:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.day = 1
        self.player_health = 100
        self.player_stamina = 100
        self.distance_traveled = 0
        self.target_distance = 1000
        
        # Resources
        self.food = 50
        self.water = 30
        self.medicine = 10
        self.fuel = 20
        self.weapons = 5
        
        # Game state
        self.game_over = False
        self.victory = False
        self.current_event = None
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_status(self):
        """Display current game status"""
        print("=" * 60)
        print(f"💀 DEATH GAME SIMULATOR - Day {self.day} 💀")
        print("=" * 60)
        print(f"Health: {self.player_health:3.0f}/100 {'💚' if self.player_health > 70 else '💛' if self.player_health > 40 else '❤️'}")
        print(f"Stamina: {self.player_stamina:3.0f}/100 {'⚡' if self.player_stamina > 50 else '🔋'}")
        print()
        print("📦 Resources:")
        print(f"  🍖 Food: {self.food}")
        print(f"  💧 Water: {self.water}")
        print(f"  💊 Medicine: {self.medicine}")
        print(f"  ⛽ Fuel: {self.fuel}")
        print(f"  🔫 Weapons: {self.weapons}")
        print()
        progress = (self.distance_traveled / self.target_distance) * 100
        print(f"🗺️  Journey Progress: {progress:.1f}% ({self.distance_traveled:.0f}/{self.target_distance})")
        
        # Progress bar
        bar_length = 20
        filled = int((progress / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}]")
        print()
    
    def get_player_input(self, prompt, valid_choices):
        """Get valid input from player"""
        while True:
            try:
                choice = input(prompt).strip().lower()
                if choice in valid_choices:
                    return choice
                print(f"❌ Invalid choice. Please enter: {', '.join(valid_choices)}")
            except KeyboardInterrupt:
                print("\n👋 Thanks for playing!")
                exit(0)
    
    def move_forward(self):
        """Move forward on the journey"""
        if self.player_stamina <= 0:
            print("😴 You're too exhausted to move! Rest first.")
            return
        
        # Move distance based on stamina
        move_distance = random.randint(10, 30)
        if self.player_stamina < 30:
            move_distance //= 2
        
        self.distance_traveled += move_distance
        self.player_stamina -= random.randint(5, 15)
        
        if self.player_stamina < 0:
            self.player_stamina = 0
            self.player_health -= 5
        
        print(f"🚶 You travel {move_distance} units forward.")
        
        # Random encounter chance
        if random.randint(1, 3) == 1:
            self.trigger_random_event()
    
    def rest(self):
        """Rest to restore stamina"""
        print("😴 You rest for the day...")
        self.advance_day()
        self.player_stamina = min(100, self.player_stamina + 30)
        print(f"⚡ Stamina restored! Current: {self.player_stamina:.0f}/100")
    
    def advance_day(self):
        """Advance to the next day"""
        self.day += 1
        
        # Daily resource consumption
        food_consumed = random.randint(3, 7)
        water_consumed = random.randint(5, 10)
        fuel_consumed = random.randint(1, 3)
        
        self.food -= food_consumed
        self.water -= water_consumed
        self.fuel -= fuel_consumed
        
        print(f"🌅 Day {self.day} begins!")
        print(f"   📉 Consumed: {food_consumed} food, {water_consumed} water, {fuel_consumed} fuel")
        
        # Effects of resource shortage
        if self.food <= 0:
            self.player_health -= 15
            self.food = 0
            print("🍖 💀 You're starving! Health decreases.")
        
        if self.water <= 0:
            self.player_health -= 20
            self.water = 0
            print("💧 💀 You're dehydrated! Health decreases.")
        
        if self.fuel <= 0:
            self.player_health -= 5
            self.fuel = 0
            print("⛽ 🥶 No fuel for warmth! Health decreases.")
        
        # Random daily events
        if random.randint(1, 3) == 1:
            self.trigger_daily_event()
    
    def trigger_daily_event(self):
        """Trigger a daily environmental event"""
        events = [
            ("🌧️ Harsh weather slows your progress", "weather"),
            ("🍓 You found some berries!", "berries"),
            ("⛈️ A storm damages your supplies", "storm"),
            ("👥 You met friendly travelers who shared food", "travelers")
        ]
        
        event_text, event_type = random.choice(events)
        print(f"📰 Event: {event_text}")
        
        if event_type in ["weather", "storm"]:
            damage = random.randint(5, 15)
            fuel_loss = random.randint(1, 5)
            self.player_health -= damage
            self.fuel -= fuel_loss
            print(f"   💔 Lost {damage} health and {fuel_loss} fuel")
        
        elif event_type in ["berries", "travelers"]:
            food_gain = random.randint(2, 8)
            self.food += food_gain
            print(f"   🍖 Gained {food_gain} food!")
    
    def trigger_random_event(self):
        """Trigger a random encounter requiring player choice"""
        events = [
            {
                "title": "🐺 Wild Animal Attack",
                "description": "A hostile wolf blocks your path, growling menacingly!",
                "choices": [
                    {"text": "Fight it with bare hands", "id": "fight_bare"},
                    {"text": "Use a weapon", "id": "use_weapon"},
                    {"text": "Try to scare it away", "id": "scare"},
                    {"text": "Run away", "id": "flee"}
                ]
            },
            {
                "title": "🤒 Sick Traveler", 
                "description": "You encounter a sick traveler asking for help.",
                "choices": [
                    {"text": "Give them medicine", "id": "help_medicine"},
                    {"text": "Share food and water", "id": "help_food"},
                    {"text": "Ignore them", "id": "ignore"},
                    {"text": "Rob them", "id": "rob"}
                ]
            },
            {
                "title": "📦 Abandoned Cache",
                "description": "You discover an abandoned supply cache!",
                "choices": [
                    {"text": "Take everything", "id": "take_all"},
                    {"text": "Take only what you need", "id": "take_some"},
                    {"text": "Leave it for others", "id": "leave"},
                    {"text": "Set a trap for other survivors", "id": "trap"}
                ]
            }
        ]
        
        self.current_event = random.choice(events)
        self.display_event()
    
    def display_event(self):
        """Display current event and handle player choice"""
        event = self.current_event
        print("\n" + "=" * 60)
        print(f"⚠️  {event['title']} ⚠️")
        print("=" * 60)
        print(event['description'])
        print("\nWhat do you do?")
        
        choices = event['choices']
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice['text']}")
        
        valid_choices = [str(i) for i in range(1, len(choices) + 1)]
        choice_num = self.get_player_input("\nEnter your choice (1-4): ", valid_choices)
        
        choice_id = choices[int(choice_num) - 1]['id']
        self.handle_event_choice(choice_id)
        self.current_event = None
    
    def handle_event_choice(self, choice_id):
        """Handle the consequences of player's choice"""
        print("\n" + "-" * 40)
        
        if choice_id == "fight_bare":
            if random.randint(1, 2) == 1:
                damage = random.randint(15, 30)
                food_gain = random.randint(8, 20)
                self.player_health -= damage
                self.food += food_gain
                print(f"💪 You defeated the wolf! But took {damage} damage.")
                print(f"🍖 Gained {food_gain} food from the hunt.")
            else:
                damage = random.randint(25, 45)
                self.player_health -= damage
                print(f"😵 The wolf overwhelmed you! Lost {damage} health.")
        
        elif choice_id == "use_weapon":
            if self.weapons > 0:
                self.weapons -= 1
                food_gain = random.randint(12, 25)
                self.food += food_gain
                print(f"🔫 You killed the wolf with your weapon!")
                print(f"🍖 Gained {food_gain} food. Weapons remaining: {self.weapons}")
            else:
                damage = random.randint(20, 40)
                self.player_health -= damage
                print(f"😱 You have no weapons! The wolf attacked. Lost {damage} health.")
        
        elif choice_id == "scare":
            if random.randint(1, 3) == 1:
                print("😤 You scared the wolf away successfully!")
            else:
                damage = random.randint(10, 20)
                stamina_loss = random.randint(15, 25)
                self.player_health -= damage
                self.player_stamina -= stamina_loss
                print(f"😰 The wolf wasn't intimidated! Lost {damage} health and {stamina_loss} stamina.")
        
        elif choice_id == "flee":
            stamina_loss = random.randint(20, 35)
            self.player_stamina -= stamina_loss
            print(f"🏃 You ran away safely but lost {stamina_loss} stamina.")
        
        elif choice_id == "help_medicine":
            if self.medicine > 0:
                self.medicine -= 1
                print("😇 You helped the traveler. They blessed your journey.")
                # Small chance of reward
                if random.randint(1, 3) == 1:
                    reward = random.randint(5, 15)
                    self.food += reward
                    print(f"🎁 They gave you {reward} food in return!")
            else:
                print("😔 You have no medicine to spare.")
        
        elif choice_id == "help_food":
            if self.food >= 5 and self.water >= 3:
                self.food -= 5
                self.water -= 3
                print("😇 You shared your supplies. Good karma follows you.")
                # Restore some health from good deed
                self.player_health = min(100, self.player_health + 5)
            else:
                print("😔 You don't have enough supplies to share.")
        
        elif choice_id == "ignore":
            print("😐 You ignored the traveler and continued on.")
        
        elif choice_id == "rob":
            loot_food = random.randint(3, 10)
            loot_water = random.randint(2, 6)
            self.food += loot_food
            self.water += loot_water
            self.player_health -= 5  # Guilt/bad karma
            print(f"😈 You robbed them. Gained {loot_food} food and {loot_water} water.")
            print("💔 But your conscience weighs heavy... (-5 health)")
        
        elif choice_id == "take_all":
            loot = {
                "food": random.randint(15, 30),
                "water": random.randint(10, 20),
                "medicine": random.randint(2, 6),
                "fuel": random.randint(5, 15),
                "weapons": random.randint(1, 3)
            }
            for resource, amount in loot.items():
                setattr(self, resource, getattr(self, resource) + amount)
            print("🎁 You took everything from the cache!")
            for resource, amount in loot.items():
                print(f"   {resource.title()}: +{amount}")
        
        elif choice_id == "take_some":
            loot = {
                "food": random.randint(5, 12),
                "water": random.randint(3, 8),
                "medicine": random.randint(1, 3)
            }
            for resource, amount in loot.items():
                setattr(self, resource, getattr(self, resource) + amount)
            print("😇 You took only what you needed.")
            for resource, amount in loot.items():
                print(f"   {resource.title()}: +{amount}")
        
        elif choice_id == "leave":
            print("😇 You left the supplies for someone more desperate.")
            # Good karma
            self.player_health = min(100, self.player_health + 3)
            print("💚 Your good deed restores 3 health.")
        
        elif choice_id == "trap":
            weapons_gain = random.randint(1, 2)
            self.weapons += weapons_gain
            print(f"😈 You set a trap. When it triggers, you'll gain {weapons_gain} weapons.")
            print("💔 But at what cost to your humanity...")
        
        print("-" * 40)
        input("\nPress Enter to continue...")
    
    def check_game_over(self):
        """Check if the game is over"""
        if self.player_health <= 0:
            self.game_over = True
            print("\n💀💀💀 YOU DIED 💀💀💀")
            print(f"You survived {self.day} days in the wasteland.")
            
            # Death message based on resources
            if self.food <= 0:
                print("🍖 Cause of death: Starvation")
            elif self.water <= 0:
                print("💧 Cause of death: Dehydration")
            else:
                print("💔 Cause of death: Fatal injuries")
            
            return True
        
        if self.distance_traveled >= self.target_distance:
            self.victory = True
            self.game_over = True
            print("\n🎉🎉🎉 VICTORY! 🎉🎉🎉")
            print(f"You reached safety after {self.day} days!")
            print("You are one of the few survivors of the death game.")
            return True
        
        return False
    
    def main_menu(self):
        """Display main menu and get player choice"""
        print("\n🎮 What would you like to do?")
        print("1. Move forward")
        print("2. Rest (advance day)")
        print("3. Check status")
        print("4. Quit game")
        
        choice = self.get_player_input("Enter your choice (1-4): ", ["1", "2", "3", "4"])
        
        if choice == "1":
            self.move_forward()
        elif choice == "2":
            self.rest()
        elif choice == "3":
            input("\nPress Enter to continue...")
        elif choice == "4":
            print("👋 Thanks for playing Death Game Simulator!")
            return False
        
        return True
    
    def play(self):
        """Main game loop"""
        print("=" * 60)
        print("💀 WELCOME TO DEATH GAME SIMULATOR 💀")
        print("=" * 60)
        print("🎯 Goal: Travel 1000 units to reach safety")
        print("⚠️  Warning: Resources are scarce, death is permanent")
        print("💡 Tip: Balance risk and reward to survive")
        print("=" * 60)
        input("Press Enter to begin your journey...")
        
        while not self.game_over:
            self.clear_screen()
            self.display_status()
            
            if self.check_game_over():
                break
            
            if not self.main_menu():
                break
        
        # Game over
        print("\n" + "=" * 60)
        if self.victory:
            print("🏆 Congratulations on your survival!")
        else:
            print("💀 Better luck next time, survivor.")
        print("=" * 60)
        
        restart = self.get_player_input("Play again? (y/n): ", ["y", "yes", "n", "no"])
        if restart in ["y", "yes"]:
            self.reset_game()
            self.play()

if __name__ == "__main__":
    game = TextDeathGameSimulator()
    game.play()