"""
Web-deployable version of Death Game Simulator
Compatible with pygame-web/pygbag for browser deployment
"""

import asyncio
import pygame
import random
from typing import Dict

# Pygame-web compatible imports
import pygame.freetype

class WebGameState:
    """Simplified game state for web version"""
    
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        self.day = 1
        self.time_passed = 0
        self.game_over = False
        self.victory = False
        
        # Player stats
        self.player_health = 100
        self.player_stamina = 100
        self.player_x = 400
        self.player_y = 300
        self.player_alive = True
        
        # Resources
        self.food = 50
        self.water = 30
        self.medicine = 10
        self.fuel = 20
        self.weapons = 5
        
        # Progress
        self.distance_traveled = 0
        self.target_distance = 1000
        self.current_event = None
    
    def update(self, dt: float):
        if self.game_over or not self.player_alive:
            return
        
        self.time_passed += dt
        
        if self.time_passed >= 60:  # 60 seconds = 1 day
            self.advance_day()
            self.time_passed = 0
        
        # Random events
        if random.randint(1, 2000) == 1:
            self.trigger_random_event()
        
        # Check death conditions
        if self.player_health <= 0:
            self.player_alive = False
            self.game_over = True
        
        # Check victory
        if self.distance_traveled >= self.target_distance:
            self.victory = True
            self.game_over = True
    
    def move_player(self, dx: float, dy: float):
        if not self.player_alive:
            return
        
        self.player_x += dx
        self.player_y += dy
        
        # Keep player on screen
        self.player_x = max(20, min(780, self.player_x))
        self.player_y = max(20, min(580, self.player_y))
        
        # Update distance
        distance = (dx**2 + dy**2)**0.5
        self.distance_traveled += distance * 0.1
        
        # Use stamina
        self.player_stamina -= distance * 0.01
        if self.player_stamina < 0:
            self.player_stamina = 0
            self.player_health -= 0.5
    
    def advance_day(self):
        self.day += 1
        
        # Resource consumption
        self.food -= random.randint(3, 7)
        self.water -= random.randint(5, 10)
        self.fuel -= random.randint(1, 3)
        
        # Effects of shortage
        if self.food <= 0:
            self.player_health -= 15
            self.food = 0
        if self.water <= 0:
            self.player_health -= 20
            self.water = 0
        if self.fuel <= 0:
            self.player_health -= 5
            self.fuel = 0
        
        # Restore stamina
        self.player_stamina = min(100, self.player_stamina + 20)
        
        # Daily events
        if random.randint(1, 3) == 1:
            self.trigger_daily_event()
    
    def trigger_random_event(self):
        events = [
            {
                "title": "Wild Animal Attack",
                "description": "A hostile animal blocks your path!",
                "choices": [
                    {"text": "Fight it", "id": "fight_animal"},
                    {"text": "Run away", "id": "flee_animal"},
                    {"text": "Use weapon", "id": "weapon_animal"}
                ]
            },
            {
                "title": "Sick Traveler",
                "description": "You encounter a sick traveler.",
                "choices": [
                    {"text": "Help them", "id": "help_sick"},
                    {"text": "Ignore them", "id": "ignore_sick"},
                    {"text": "Rob them", "id": "rob_sick"}
                ]
            },
            {
                "title": "Resource Cache",
                "description": "You found supplies!",
                "choices": [
                    {"text": "Take everything", "id": "take_all"},
                    {"text": "Take some", "id": "take_some"},
                    {"text": "Leave it", "id": "leave_cache"}
                ]
            }
        ]
        
        self.current_event = random.choice(events)
    
    def trigger_daily_event(self):
        events = [
            "harsh_weather",
            "found_berries", 
            "storm_damage",
            "met_travelers"
        ]
        
        event = random.choice(events)
        if event in ["harsh_weather", "storm_damage"]:
            self.player_health -= random.randint(5, 15)
            self.fuel -= random.randint(1, 5)
        elif event in ["found_berries", "met_travelers"]:
            self.food += random.randint(2, 8)
    
    def handle_event_choice(self, choice_id: str):
        if not self.current_event:
            return
        
        if choice_id == "fight_animal":
            if random.randint(1, 2) == 1:
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
                self.player_health -= random.randint(15, 35)
        
        elif choice_id == "help_sick":
            if self.medicine > 0:
                self.medicine -= 1
            else:
                self.player_health -= 5
        
        elif choice_id == "rob_sick":
            self.food += random.randint(1, 5)
            self.water += random.randint(1, 3)
        
        elif choice_id == "take_all":
            self.food += random.randint(10, 20)
            self.water += random.randint(5, 15)
            self.medicine += random.randint(1, 5)
            self.fuel += random.randint(3, 10)
        
        elif choice_id == "take_some":
            self.food += random.randint(3, 8)
            self.water += random.randint(2, 6)
        
        self.current_event = None

class WebGame:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Death Game Simulator")
        
        self.clock = pygame.time.Clock()
        self.game_state = WebGameState()
        self.running = True
        
        # Try to load font
        try:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            # Fallback if no font available
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 100, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        
        # UI state
        self.show_event_popup = False
    
    async def run(self):
        while self.running:
            await self.handle_events()
            await self.update()
            await self.draw()
            await asyncio.sleep(0)
    
    async def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.game_state.reset_game()
                    self.show_event_popup = False
                elif event.key == pygame.K_SPACE:
                    self.game_state.advance_day()
                elif self.show_event_popup and self.game_state.current_event:
                    choices = self.game_state.current_event['choices']
                    if event.key == pygame.K_1 and len(choices) > 0:
                        self.game_state.handle_event_choice(choices[0]['id'])
                        self.show_event_popup = False
                    elif event.key == pygame.K_2 and len(choices) > 1:
                        self.game_state.handle_event_choice(choices[1]['id'])
                        self.show_event_popup = False
                    elif event.key == pygame.K_3 and len(choices) > 2:
                        self.game_state.handle_event_choice(choices[2]['id'])
                        self.show_event_popup = False
        
        # Movement
        keys = pygame.key.get_pressed()
        dx = dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -3
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 3
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -3
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 3
        
        if dx != 0 or dy != 0:
            self.game_state.move_player(dx, dy)
    
    async def update(self):
        self.game_state.update(1/60)
        
        # Show event popup
        if self.game_state.current_event and not self.show_event_popup:
            self.show_event_popup = True
    
    async def draw(self):
        self.screen.fill(self.BLACK)
        
        # Draw world grid
        for x in range(0, self.width, 50):
            pygame.draw.line(self.screen, (20, 20, 20), (x, 0), (x, self.height))
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y), (self.width, y))
        
        # Draw player
        if self.game_state.player_alive:
            # Player color based on health
            if self.game_state.player_health > 70:
                color = self.GREEN
            elif self.game_state.player_health > 40:
                color = self.YELLOW
            else:
                color = self.RED
            
            pygame.draw.circle(self.screen, color, 
                             (int(self.game_state.player_x), int(self.game_state.player_y)), 15)
            
            # Health bar
            bar_x = int(self.game_state.player_x) - 15
            bar_y = int(self.game_state.player_y) - 25
            pygame.draw.rect(self.screen, self.GRAY, (bar_x, bar_y, 30, 4))
            health_width = int((self.game_state.player_health / 100) * 30)
            pygame.draw.rect(self.screen, self.RED, (bar_x, bar_y, health_width, 4))
        
        # Draw UI
        self.draw_ui()
        
        # Draw event popup
        if self.show_event_popup:
            self.draw_event_popup()
        
        # Draw game over
        if self.game_state.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def draw_ui(self):
        # Status
        day_text = self.font.render(f"Day: {self.game_state.day}", True, self.WHITE)
        self.screen.blit(day_text, (10, 10))
        
        health_text = self.small_font.render(f"Health: {self.game_state.player_health:.0f}", True, self.WHITE)
        self.screen.blit(health_text, (10, 50))
        
        stamina_text = self.small_font.render(f"Stamina: {self.game_state.player_stamina:.0f}", True, self.WHITE)
        self.screen.blit(stamina_text, (10, 70))
        
        # Resources
        resources = [
            f"Food: {self.game_state.food}",
            f"Water: {self.game_state.water}",
            f"Medicine: {self.game_state.medicine}",
            f"Fuel: {self.game_state.fuel}",
            f"Weapons: {self.game_state.weapons}"
        ]
        
        y_offset = 100
        for resource in resources:
            text = self.small_font.render(resource, True, self.WHITE)
            self.screen.blit(text, (10, y_offset))
            y_offset += 20
        
        # Progress
        progress = (self.game_state.distance_traveled / self.game_state.target_distance) * 100
        progress_text = self.small_font.render(f"Progress: {progress:.1f}%", True, self.WHITE)
        self.screen.blit(progress_text, (10, y_offset + 10))
        
        # Progress bar
        pygame.draw.rect(self.screen, self.GRAY, (10, y_offset + 35, 200, 10))
        progress_width = int((progress / 100) * 200)
        pygame.draw.rect(self.screen, self.BLUE, (10, y_offset + 35, progress_width, 10))
        
        # Controls
        controls = [
            "WASD: Move",
            "Space: Rest", 
            "R: Restart",
            "ESC: Quit"
        ]
        
        y_offset = self.height - 100
        for control in controls:
            text = self.small_font.render(control, True, self.WHITE)
            self.screen.blit(text, (self.width - 120, y_offset))
            y_offset += 20
    
    def draw_event_popup(self):
        if not self.game_state.current_event:
            return
        
        # Popup background
        popup_width = 500
        popup_height = 200
        popup_x = (self.width - popup_width) // 2
        popup_y = (self.height - popup_height) // 2
        
        pygame.draw.rect(self.screen, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, self.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
        
        # Event text
        event = self.game_state.current_event
        title = self.font.render(event['title'], True, self.WHITE)
        title_rect = title.get_rect(center=(popup_x + popup_width//2, popup_y + 30))
        self.screen.blit(title, title_rect)
        
        desc = self.small_font.render(event['description'], True, self.WHITE)
        desc_rect = desc.get_rect(center=(popup_x + popup_width//2, popup_y + 60))
        self.screen.blit(desc, desc_rect)
        
        # Choices
        y_offset = popup_y + 90
        for i, choice in enumerate(event['choices']):
            choice_text = f"{i+1}. {choice['text']}"
            choice_surface = self.small_font.render(choice_text, True, self.WHITE)
            self.screen.blit(choice_surface, (popup_x + 20, y_offset))
            y_offset += 25
        
        # Instructions
        instruction = self.small_font.render("Press 1, 2, or 3", True, self.YELLOW)
        instruction_rect = instruction.get_rect(center=(popup_x + popup_width//2, popup_y + popup_height - 15))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game_over(self):
        # Overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        if self.game_state.victory:
            text = "VICTORY!"
            color = self.GREEN
        else:
            text = "GAME OVER"
            color = self.RED
        
        game_over = self.font.render(text, True, color)
        game_over_rect = game_over.get_rect(center=(self.width//2, self.height//2 - 50))
        self.screen.blit(game_over, game_over_rect)
        
        # Stats
        survival = self.small_font.render(f"Survived {self.game_state.day} days", True, self.WHITE)
        survival_rect = survival.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(survival, survival_rect)
        
        # Restart
        restart = self.small_font.render("Press R to restart", True, self.WHITE)
        restart_rect = restart.get_rect(center=(self.width//2, self.height//2 + 50))
        self.screen.blit(restart, restart_rect)

async def main():
    game = WebGame()
    await game.run()
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())