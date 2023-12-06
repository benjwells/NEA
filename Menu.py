import pygame
from login_page import Button
import time

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen_width, screen_height = 1920, 1080

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the background image
background_image_path = "images/modeSelection.png"
background = pygame.image.load(background_image_path)
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load the button images
interactive_game_image = pygame.image.load("images/InteractiveGameButton.png")
simulation_image = pygame.image.load("images/SimulationButton.png")
statistics_image = pygame.image.load("images/StatisticsButton.png")
options_image = pygame.image.load("images/options.png")

# Create the buttons
button_width, button_height = 400, 100  # Adjust these values as needed
spacing = 30  # Adjust this value as needed to change the spacing between the buttons
interactive_game_button = Button(screen_width/2 - button_width/2, screen_height/2 - 2*button_height - 1.5*spacing, interactive_game_image, button_width, button_height)
simulation_button = Button(screen_width/2 - button_width/2, screen_height/2 - button_height - 0.5*spacing, simulation_image, button_width, button_height)
statistics_button = Button(screen_width/2 - button_width/2, screen_height/2 + 0.5*spacing, statistics_image, button_width, button_height)
options_button = Button(screen_width/2 - button_width/2, screen_height/2 + button_height + 1.5*spacing, options_image, button_width, button_height)

# Create a font object
font = pygame.font.Font(None, 50)

# Render the loading message
loading_surface = font.render("Loading...", True, pygame.Color('white'))

# Display the loading message
screen.blit(loading_surface, (screen_width/2 - loading_surface.get_width()/2, screen_height/2 - loading_surface.get_height()/2))

# Create the loading bar
bar_width, bar_height = 500, 50
outline_rect = pygame.Rect(screen_width/2 - bar_width/2, screen_height/2 + loading_surface.get_height(), bar_width, bar_height)
filled_rect = pygame.Rect(screen_width/2 - bar_width/2, screen_height/2 + loading_surface.get_height(), 0, bar_height)

loading = True
start_ticks = pygame.time.get_ticks()
while loading:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	if (pygame.time.get_ticks() - start_ticks) < 3000:
		# Update the width of the filled part of the loading bar
		filled_rect.width = ((pygame.time.get_ticks() - start_ticks) / 3000) * bar_width
	else:
		loading = False

	# Draw the loading bar
	pygame.draw.rect(screen, pygame.Color('white'), outline_rect, 2)
	pygame.draw.rect(screen, pygame.Color('white'), filled_rect)

	pygame.display.flip()

# After the loading screen
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if interactive_game_button.isOver(pygame.mouse.get_pos()):
				exec(open("interactive_game.py").read())
			elif simulation_button.isOver(pygame.mouse.get_pos()):
				exec(open("simulation.py").read())
			elif statistics_button.isOver(pygame.mouse.get_pos()):
				exec(open("statistics.py").read())
			elif options_button.isOver(pygame.mouse.get_pos()):
				exec(open("options.py").read())

	# Blit the background and buttons
	screen.blit(background, (0, 0))
	interactive_game_button.draw(screen)
	simulation_button.draw(screen)
	statistics_button.draw(screen)
	options_button.draw(screen)

	pygame.display.flip()

pygame.quit()
