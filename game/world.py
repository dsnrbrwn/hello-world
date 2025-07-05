import pygame
import random
import math

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # World properties
        self.terrain_size = 40
        self.terrain_grid = []
        self.generate_terrain()
        
        # Environmental hazards
        self.hazards = []
        self.generate_hazards()
        
        # Colors
        self.GRASS = (34, 139, 34)
        self.DIRT = (139, 69, 19)
        self.WATER = (0, 191, 255)
        self.MOUNTAIN = (105, 105, 105)
        self.DESERT = (238, 203, 173)
        self.DANGER = (255, 0, 0)
        
    def generate_terrain(self):
        # Generate a simple terrain grid
        cols = self.width // self.terrain_size + 1
        rows = self.height // self.terrain_size + 1
        
        for row in range(rows):
            terrain_row = []
            for col in range(cols):
                # Generate terrain type based on position and random factor
                terrain_type = self.get_terrain_type(col, row)
                terrain_row.append(terrain_type)
            self.terrain_grid.append(terrain_row)
    
    def get_terrain_type(self, col, row):
        # Use noise-like generation for more realistic terrain
        base_noise = random.random()
        
        # Create some patterns
        if base_noise < 0.1:
            return "water"
        elif base_noise < 0.2:
            return "mountain"
        elif base_noise < 0.3:
            return "desert"
        elif base_noise < 0.4:
            return "dirt"
        else:
            return "grass"
    
    def generate_hazards(self):
        # Generate random environmental hazards
        num_hazards = random.randint(5, 15)
        for _ in range(num_hazards):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            hazard_type = random.choice(["storm", "predator", "bandit_camp"])
            self.hazards.append({
                "x": x,
                "y": y,
                "type": hazard_type,
                "active": True,
                "radius": random.randint(30, 80)
            })
    
    def update(self):
        # Update dynamic world elements
        for hazard in self.hazards:
            if hazard["type"] == "storm":
                # Storms move randomly
                hazard["x"] += random.randint(-2, 2)
                hazard["y"] += random.randint(-2, 2)
                
                # Keep storms within bounds
                hazard["x"] = max(0, min(self.width, hazard["x"]))
                hazard["y"] = max(0, min(self.height, hazard["y"]))
    
    def draw(self, screen):
        # Draw terrain
        for row in range(len(self.terrain_grid)):
            for col in range(len(self.terrain_grid[row])):
                x = col * self.terrain_size
                y = row * self.terrain_size
                
                terrain_type = self.terrain_grid[row][col]
                color = self.get_terrain_color(terrain_type)
                
                pygame.draw.rect(screen, color, 
                               (x, y, self.terrain_size, self.terrain_size))
        
        # Draw hazards
        for hazard in self.hazards:
            if hazard["active"]:
                color = self.get_hazard_color(hazard["type"])
                pygame.draw.circle(screen, color, 
                                 (int(hazard["x"]), int(hazard["y"])), 
                                 hazard["radius"], 2)
                
                # Draw hazard icon/symbol
                self.draw_hazard_symbol(screen, hazard)
    
    def get_terrain_color(self, terrain_type):
        colors = {
            "grass": self.GRASS,
            "dirt": self.DIRT,
            "water": self.WATER,
            "mountain": self.MOUNTAIN,
            "desert": self.DESERT
        }
        return colors.get(terrain_type, self.GRASS)
    
    def get_hazard_color(self, hazard_type):
        if hazard_type == "storm":
            return (128, 128, 128)  # Gray
        elif hazard_type == "predator":
            return (255, 0, 0)  # Red
        elif hazard_type == "bandit_camp":
            return (255, 165, 0)  # Orange
        return (255, 255, 255)  # White default
    
    def draw_hazard_symbol(self, screen, hazard):
        x, y = int(hazard["x"]), int(hazard["y"])
        
        if hazard["type"] == "storm":
            # Draw lightning bolt
            points = [(x-5, y-10), (x+5, y-5), (x-2, y-5), (x+5, y+10), (x-5, y+5), (x+2, y+5)]
            if len(points) >= 3:
                pygame.draw.polygon(screen, (255, 255, 0), points)
        
        elif hazard["type"] == "predator":
            # Draw triangle (predator teeth)
            points = [(x, y-8), (x-6, y+8), (x+6, y+8)]
            pygame.draw.polygon(screen, (255, 0, 0), points)
        
        elif hazard["type"] == "bandit_camp":
            # Draw crossed swords
            pygame.draw.line(screen, (255, 165, 0), (x-6, y-6), (x+6, y+6), 3)
            pygame.draw.line(screen, (255, 165, 0), (x+6, y-6), (x-6, y+6), 3)
    
    def check_hazard_collision(self, player_x, player_y):
        for hazard in self.hazards:
            if hazard["active"]:
                distance = math.sqrt((player_x - hazard["x"])**2 + (player_y - hazard["y"])**2)
                if distance < hazard["radius"]:
                    return hazard
        return None
    
    def get_terrain_at(self, x, y):
        col = int(x // self.terrain_size)
        row = int(y // self.terrain_size)
        
        if 0 <= row < len(self.terrain_grid) and 0 <= col < len(self.terrain_grid[row]):
            return self.terrain_grid[row][col]
        return "grass"