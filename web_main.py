"""
Web version of Death Game Simulator using pygame-web
This version can run in web browsers
"""

import pygame
import asyncio
import sys
import os

# Import the existing game modules
from game.core_game import GameState

class WebGameEngine:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Death Game Simulator - Web Version")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_state = GameState()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        
        # UI state
        self.show_event_popup = False
        self.event_choices = []
        
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
                elif event.key == pygame.K_SPACE:
                    # Rest (advance day)
                    self.game_state.advance_day()
                elif self.show_event_popup:
                    # Handle event choices
                    if event.key == pygame.K_1 and len(self.event_choices) > 0:
                        self.game_state.handle_event_choice(self.event_choices[0]['id'])
                        self.show_event_popup = False
                    elif event.key == pygame.K_2 and len(self.event_choices) > 1:
                        self.game_state.handle_event_choice(self.event_choices[1]['id'])
                        self.show_event_popup = False
                    elif event.key == pygame.K_3 and len(self.event_choices) > 2:
                        self.game_state.handle_event_choice(self.event_choices[2]['id'])
                        self.show_event_popup = False
                        
        # Handle continuous key presses for movement
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
        # Update game state
        self.game_state.update(1/60)  # 60 FPS
        
        # Check for events
        if self.game_state.current_event and not self.show_event_popup:
            self.show_event_popup = True
            self.event_choices = self.game_state.current_event['choices']
    
    async def draw(self):
        self.screen.fill(self.BLACK)
        
        # Draw game world
        self.draw_world()
        
        # Draw player
        self.draw_player()
        
        # Draw UI
        self.draw_ui()
        
        # Draw event popup if needed
        if self.show_event_popup:
            self.draw_event_popup()
        
        # Draw game over screen
        if self.game_state.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def draw_world(self):
        # Draw simple world background
        # Grid pattern
        for x in range(0, self.width, 50):
            pygame.draw.line(self.screen, (20, 20, 20), (x, 0), (x, self.height))
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y), (self.width, y))
    
    def draw_player(self):
        if self.game_state.player_alive:
            # Scale player position to screen
            player_x = int((self.game_state.player_x / 1024) * self.width)
            player_y = int((self.game_state.player_y / 768) * self.height)
            
            # Player color based on health
            if self.game_state.player_health > 70:
                color = self.GREEN
            elif self.game_state.player_health > 40:
                color = self.YELLOW
            elif self.game_state.player_health > 20:
                color = (255, 165, 0)  # Orange
            else:
                color = self.RED
            
            # Draw player
            pygame.draw.circle(self.screen, color, (player_x, player_y), 15)
            
            # Draw health bar above player
            bar_width = 30
            bar_height = 4
            bar_x = player_x - bar_width // 2
            bar_y = player_y - 25
            
            # Background bar
            pygame.draw.rect(self.screen, self.GRAY, (bar_x, bar_y, bar_width, bar_height))
            
            # Health bar
            health_width = int((self.game_state.player_health / 100) * bar_width)
            pygame.draw.rect(self.screen, self.RED, (bar_x, bar_y, health_width, bar_height))
    
    def draw_ui(self):
        # Status display
        status = self.game_state.get_status()
        
        # Day counter
        day_text = self.font.render(f"Day: {status['day']}", True, self.WHITE)
        self.screen.blit(day_text, (10, 10))
        
        # Health
        health_text = self.small_font.render(f"Health: {status['health']:.0f}/100", True, self.WHITE)
        self.screen.blit(health_text, (10, 50))
        
        # Stamina
        stamina_text = self.small_font.render(f"Stamina: {status['stamina']:.0f}/100", True, self.WHITE)
        self.screen.blit(stamina_text, (10, 75))
        
        # Resources
        y_offset = 110
        resource_texts = [
            f"Food: {status['food']}",
            f"Water: {status['water']}",
            f"Medicine: {status['medicine']}",
            f"Fuel: {status['fuel']}",
            f"Weapons: {status['weapons']}"
        ]
        
        for text in resource_texts:
            resource_surface = self.small_font.render(text, True, self.WHITE)
            self.screen.blit(resource_surface, (10, y_offset))
            y_offset += 20
        
        # Progress bar
        progress_text = self.small_font.render(f"Progress: {status['progress']:.1f}%", True, self.WHITE)
        self.screen.blit(progress_text, (10, y_offset + 10))
        
        # Progress bar visual
        bar_width = 200
        bar_height = 10
        bar_x = 10
        bar_y = y_offset + 35
        
        pygame.draw.rect(self.screen, self.GRAY, (bar_x, bar_y, bar_width, bar_height))
        progress_width = int((status['progress'] / 100) * bar_width)
        pygame.draw.rect(self.screen, self.BLUE, (bar_x, bar_y, progress_width, bar_height))
        
        # Controls
        controls_text = [
            "Controls:",
            "WASD/Arrows: Move",
            "Space: Rest",
            "R: Restart",
            "ESC: Quit"
        ]
        
        y_offset = self.height - 130
        for text in controls_text:
            control_surface = self.small_font.render(text, True, self.WHITE)
            self.screen.blit(control_surface, (self.width - 150, y_offset))
            y_offset += 20
    
    def draw_event_popup(self):
        if not self.game_state.current_event:
            return
            
        # Draw popup background
        popup_width = 500
        popup_height = 250
        popup_x = (self.width - popup_width) // 2
        popup_y = (self.height - popup_height) // 2
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, self.WHITE, (popup_x, popup_y, popup_width, popup_height), 2)
        
        # Event title
        event = self.game_state.current_event
        title_surface = self.font.render(event['title'], True, self.WHITE)
        title_rect = title_surface.get_rect(center=(popup_x + popup_width//2, popup_y + 30))
        self.screen.blit(title_surface, title_rect)
        
        # Event description
        desc_surface = self.small_font.render(event['description'], True, self.WHITE)
        desc_rect = desc_surface.get_rect(center=(popup_x + popup_width//2, popup_y + 70))
        self.screen.blit(desc_surface, desc_rect)
        
        # Choices
        y_offset = popup_y + 110
        for i, choice in enumerate(event['choices']):
            choice_text = f"{i+1}. {choice['text']}"
            choice_surface = self.small_font.render(choice_text, True, self.WHITE)
            self.screen.blit(choice_surface, (popup_x + 20, y_offset))
            y_offset += 30
        
        # Instructions
        instruction_text = "Press 1, 2, or 3 to choose"
        instruction_surface = self.small_font.render(instruction_text, True, self.YELLOW)
        instruction_rect = instruction_surface.get_rect(center=(popup_x + popup_width//2, popup_y + popup_height - 20))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def draw_game_over(self):
        # Draw game over overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        if self.game_state.victory:
            game_over_text = "VICTORY!"
            color = self.GREEN
        else:
            game_over_text = "GAME OVER"
            color = self.RED
            
        game_over_surface = self.font.render(game_over_text, True, color)
        game_over_rect = game_over_surface.get_rect(center=(self.width//2, self.height//2 - 50))
        self.screen.blit(game_over_surface, game_over_rect)
        
        # Survival info
        survival_text = f"You survived {self.game_state.day} days"
        survival_surface = self.small_font.render(survival_text, True, self.WHITE)
        survival_rect = survival_surface.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(survival_surface, survival_rect)
        
        # Restart instruction
        restart_text = "Press R to restart"
        restart_surface = self.small_font.render(restart_text, True, self.WHITE)
        restart_rect = restart_surface.get_rect(center=(self.width//2, self.height//2 + 50))
        self.screen.blit(restart_surface, restart_rect)

async def main():
    game = WebGameEngine()
    await game.run()
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())