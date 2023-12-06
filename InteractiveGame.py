import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Interactive Game")

# Create a font object
font = pygame.font.Font(None, 50)

# Render the text
text_surface = font.render("Interactive Game menu", True, (255, 255, 255))

# Get the rectangle of the text surface
text_rect = text_surface.get_rect()

# Center the rectangle
text_rect.center = (screen_width / 2, screen_height / 2)

# Game loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Fill the screen with black
	screen.fill((0, 0, 0))

	# Blit the text onto the screen
	screen.blit(text_surface, text_rect)

	# Update the display
	pygame.display.flip()

pygame.quit()
sys.exit()
