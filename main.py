import pygame
import sys
from game.game_engine import GameEngine

def main():
    # Initialize Pygame
    pygame.init()
    
    # Game settings
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60
    
    # Create the game engine
    game = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)
    
    # Run the game
    game.run()
    
    # Quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()