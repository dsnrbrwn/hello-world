import pygame

class UI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        
        # UI Layout
        self.panel_height = 120
        self.panel_width = 300
        self.margin = 10
        
    def draw(self, screen, player, resource_manager, day):
        # Draw main UI panel
        self.draw_main_panel(screen, player, resource_manager, day)
        
        # Draw resource bars
        self.draw_resource_bars(screen, resource_manager)
        
        # Draw player status
        self.draw_player_status(screen, player)
        
        # Draw controls help
        self.draw_controls(screen)
    
    def draw_main_panel(self, screen, player, resource_manager, day):
        # Background panel
        panel_rect = pygame.Rect(self.margin, self.margin, 
                                self.panel_width, self.panel_height)
        pygame.draw.rect(screen, self.DARK_GRAY, panel_rect)
        pygame.draw.rect(screen, self.WHITE, panel_rect, 2)
        
        # Day counter
        day_text = self.font_large.render(f"Day {day}", True, self.WHITE)
        screen.blit(day_text, (self.margin + 10, self.margin + 10))
        
        # Health display
        health_text = self.font_medium.render(f"Health: {player.health}/100", True, self.WHITE)
        screen.blit(health_text, (self.margin + 10, self.margin + 50))
        
        # Status indicators
        status_y = self.margin + 75
        if player.sick:
            sick_text = self.font_small.render("SICK", True, self.RED)
            screen.blit(sick_text, (self.margin + 10, status_y))
        
        if player.injured:
            injured_text = self.font_small.render("INJURED", True, self.YELLOW)
            screen.blit(injured_text, (self.margin + 60, status_y))
        
        if player.exhausted:
            exhausted_text = self.font_small.render("EXHAUSTED", True, self.BLUE)
            screen.blit(exhausted_text, (self.margin + 130, status_y))
    
    def draw_resource_bars(self, screen, resource_manager):
        # Resource panel
        resource_panel_x = self.margin
        resource_panel_y = self.margin + self.panel_height + 10
        resource_panel_width = self.panel_width
        resource_panel_height = 150
        
        panel_rect = pygame.Rect(resource_panel_x, resource_panel_y, 
                                resource_panel_width, resource_panel_height)
        pygame.draw.rect(screen, self.DARK_GRAY, panel_rect)
        pygame.draw.rect(screen, self.WHITE, panel_rect, 2)
        
        # Title
        title_text = self.font_medium.render("Resources", True, self.WHITE)
        screen.blit(title_text, (resource_panel_x + 10, resource_panel_y + 10))
        
        # Resource bars
        resources = resource_manager.get_resource_status()
        bar_width = 200
        bar_height = 15
        start_y = resource_panel_y + 40
        
        for i, (resource_name, data) in enumerate(resources.items()):
            y = start_y + i * 25
            
            # Resource name
            name_text = self.font_small.render(f"{resource_name.capitalize()}:", True, self.WHITE)
            screen.blit(name_text, (resource_panel_x + 10, y))
            
            # Background bar
            bar_rect = pygame.Rect(resource_panel_x + 80, y, bar_width, bar_height)
            pygame.draw.rect(screen, self.GRAY, bar_rect)
            
            # Resource bar
            if data["max"] > 0:
                fill_width = int((data["current"] / data["max"]) * bar_width)
                fill_rect = pygame.Rect(resource_panel_x + 80, y, fill_width, bar_height)
                
                # Color based on status
                if data["status"] == "Good":
                    color = self.GREEN
                elif data["status"] == "Moderate":
                    color = self.YELLOW
                elif data["status"] == "Low":
                    color = (255, 165, 0)  # Orange
                else:
                    color = self.RED
                
                pygame.draw.rect(screen, color, fill_rect)
            
            # Resource text
            resource_text = self.font_small.render(f"{data['current']}/{data['max']}", True, self.WHITE)
            screen.blit(resource_text, (resource_panel_x + 290, y))
    
    def draw_player_status(self, screen, player):
        # Player status panel (right side)
        status_panel_x = self.screen_width - 250
        status_panel_y = self.margin
        status_panel_width = 240
        status_panel_height = 200
        
        panel_rect = pygame.Rect(status_panel_x, status_panel_y, 
                                status_panel_width, status_panel_height)
        pygame.draw.rect(screen, self.DARK_GRAY, panel_rect)
        pygame.draw.rect(screen, self.WHITE, panel_rect, 2)
        
        # Title
        title_text = self.font_medium.render("Player Status", True, self.WHITE)
        screen.blit(title_text, (status_panel_x + 10, status_panel_y + 10))
        
        # Health bar
        health_label = self.font_small.render("Health:", True, self.WHITE)
        screen.blit(health_label, (status_panel_x + 10, status_panel_y + 40))
        
        health_bar_rect = pygame.Rect(status_panel_x + 70, status_panel_y + 40, 150, 15)
        pygame.draw.rect(screen, self.GRAY, health_bar_rect)
        
        health_fill = int((player.health / player.max_health) * 150)
        health_fill_rect = pygame.Rect(status_panel_x + 70, status_panel_y + 40, health_fill, 15)
        
        if player.health > 70:
            health_color = self.GREEN
        elif player.health > 40:
            health_color = self.YELLOW
        else:
            health_color = self.RED
        
        pygame.draw.rect(screen, health_color, health_fill_rect)
        
        # Other stats
        stats_y = status_panel_y + 70
        
        stamina_text = self.font_small.render(f"Stamina: {player.stamina}/100", True, self.WHITE)
        screen.blit(stamina_text, (status_panel_x + 10, stats_y))
        
        morale_text = self.font_small.render(f"Morale: {player.morale}/100", True, self.WHITE)
        screen.blit(morale_text, (status_panel_x + 10, stats_y + 20))
        
        # Survival info
        survival_y = stats_y + 50
        survival_title = self.font_small.render("Survival Status:", True, self.WHITE)
        screen.blit(survival_title, (status_panel_x + 10, survival_y))
        
        if player.alive:
            alive_text = self.font_small.render("ALIVE", True, self.GREEN)
            screen.blit(alive_text, (status_panel_x + 10, survival_y + 20))
        else:
            dead_text = self.font_small.render("DEAD", True, self.RED)
            screen.blit(dead_text, (status_panel_x + 10, survival_y + 20))
    
    def draw_controls(self, screen):
        # Controls panel (bottom)
        controls_panel_y = self.screen_height - 80
        controls_panel_height = 70
        
        panel_rect = pygame.Rect(self.margin, controls_panel_y, 
                                self.screen_width - 2 * self.margin, controls_panel_height)
        pygame.draw.rect(screen, self.DARK_GRAY, panel_rect)
        pygame.draw.rect(screen, self.WHITE, panel_rect, 2)
        
        # Controls text
        controls_text = [
            "Controls: WASD or Arrow Keys to move",
            "ESC: Return to menu | R: Restart (when dead)",
            "Survive as long as possible in this hostile world!"
        ]
        
        for i, text in enumerate(controls_text):
            text_surface = self.font_small.render(text, True, self.WHITE)
            screen.blit(text_surface, (self.margin + 10, controls_panel_y + 10 + i * 18))
    
    def draw_event_notification(self, screen, event_text):
        # Event notification (center of screen)
        notification_width = 400
        notification_height = 100
        notification_x = (self.screen_width - notification_width) // 2
        notification_y = (self.screen_height - notification_height) // 2
        
        # Background
        notification_rect = pygame.Rect(notification_x, notification_y, 
                                       notification_width, notification_height)
        pygame.draw.rect(screen, self.BLACK, notification_rect)
        pygame.draw.rect(screen, self.RED, notification_rect, 3)
        
        # Text
        text_surface = self.font_medium.render(event_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(notification_x + notification_width // 2, 
                                                 notification_y + notification_height // 2))
        screen.blit(text_surface, text_rect)