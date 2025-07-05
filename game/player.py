import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.size = 20
        
        # Player stats
        self.max_health = 100
        self.health = self.max_health
        self.stamina = 100
        self.morale = 100
        
        # Player state
        self.alive = True
        self.sick = False
        self.injured = False
        self.exhausted = False
        
        # Colors
        self.color = (0, 255, 0)  # Green when healthy
        self.health_color = (255, 0, 0)  # Red for health bar
        
        # Movement
        self.dx = 0
        self.dy = 0
        
    def update(self):
        if not self.alive:
            return
            
        # Handle input
        keys = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dy = self.speed
        
        # Normalize diagonal movement
        if self.dx != 0 and self.dy != 0:
            self.dx *= 0.707  # 1/sqrt(2)
            self.dy *= 0.707
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Update color based on health
        if self.health > 70:
            self.color = (0, 255, 0)  # Green - healthy
        elif self.health > 40:
            self.color = (255, 255, 0)  # Yellow - injured
        elif self.health > 20:
            self.color = (255, 165, 0)  # Orange - badly injured
        else:
            self.color = (255, 0, 0)  # Red - near death
        
        # Check if alive
        if self.health <= 0:
            self.alive = False
    
    def draw(self, screen):
        if not self.alive:
            # Draw as a skull or X
            pygame.draw.line(screen, (255, 0, 0), 
                           (self.x - self.size//2, self.y - self.size//2),
                           (self.x + self.size//2, self.y + self.size//2), 3)
            pygame.draw.line(screen, (255, 0, 0), 
                           (self.x + self.size//2, self.y - self.size//2),
                           (self.x - self.size//2, self.y + self.size//2), 3)
        else:
            # Draw player as a circle
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            
            # Draw health bar above player
            bar_width = 30
            bar_height = 5
            bar_x = self.x - bar_width // 2
            bar_y = self.y - self.size - 10
            
            # Background bar
            pygame.draw.rect(screen, (100, 100, 100), 
                           (bar_x, bar_y, bar_width, bar_height))
            
            # Health bar
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, self.health_color, 
                           (bar_x, bar_y, health_width, bar_height))
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    def reset(self):
        self.health = self.max_health
        self.stamina = 100
        self.morale = 100
        self.alive = True
        self.sick = False
        self.injured = False
        self.exhausted = False
    
    def get_bounds(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)