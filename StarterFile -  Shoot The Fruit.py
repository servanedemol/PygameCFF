import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Target properties
#class Target:
#    def __init__(self):
        

# Game loop
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw target
    
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()