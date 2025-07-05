import pygame
import random
from .player import Player
from .world import World
from .resource_manager import ResourceManager
from .event_manager import EventManager
from .ui import UI

class GameEngine:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        
        # Initialize Pygame components
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Death Game Simulator")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.game_state = "menu"  # menu, playing, game_over
        self.day = 1
        self.time_passed = 0
        
        # Game components
        self.player = Player(width // 2, height // 2)
        self.world = World(width, height)
        self.resource_manager = ResourceManager()
        self.event_manager = EventManager()
        self.ui = UI(width, height)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                elif self.game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
    
    def update(self):
        if self.game_state == "playing":
            # Update time
            self.time_passed += 1
            if self.time_passed >= self.fps * 60:  # 60 seconds = 1 day
                self.day += 1
                self.time_passed = 0
                self.advance_day()
            
            # Update game components
            self.player.update()
            self.world.update()
            self.resource_manager.update()
            
            # Check for events
            if random.randint(1, 300) == 1:  # Random event chance
                self.event_manager.trigger_random_event(self.player, self.resource_manager)
            
            # Check for death conditions
            if self.player.health <= 0:
                self.game_state = "game_over"
    
    def draw(self):
        self.screen.fill(self.BLACK)
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        title_font = pygame.font.Font(None, 72)
        subtitle_font = pygame.font.Font(None, 36)
        
        title = title_font.render("DEATH GAME SIMULATOR", True, self.RED)
        subtitle = subtitle_font.render("Press SPACE to start your journey", True, self.WHITE)
        
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 100))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 2))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
    
    def draw_game(self):
        # Draw world
        self.world.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.ui.draw(self.screen, self.player, self.resource_manager, self.day)
    
    def draw_game_over(self):
        game_over_font = pygame.font.Font(None, 72)
        info_font = pygame.font.Font(None, 36)
        
        game_over_text = game_over_font.render("YOU DIED", True, self.RED)
        survival_text = info_font.render(f"You survived {self.day} days", True, self.WHITE)
        restart_text = info_font.render("Press R to restart or ESC for menu", True, self.WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        survival_rect = survival_text.get_rect(center=(self.width // 2, self.height // 2))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(survival_text, survival_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def start_game(self):
        self.game_state = "playing"
        self.day = 1
        self.time_passed = 0
        self.player.reset()
        self.resource_manager.reset()
    
    def restart_game(self):
        self.start_game()
    
    def advance_day(self):
        # Daily resource consumption
        self.resource_manager.consume_daily_resources()
        
        # Apply effects of resource shortage
        if self.resource_manager.food <= 0:
            self.player.health -= 10
        if self.resource_manager.water <= 0:
            self.player.health -= 15
        
        # Random daily events
        if random.randint(1, 3) == 1:
            self.event_manager.trigger_daily_event(self.player, self.resource_manager)