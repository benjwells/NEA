import pygame
from login_page import Button

pygame.init()

s_width, s_height = 1920, 1080 

screen = pygame.display.set_mode((s_width, s_height))

bg_image = "images/modeSelection.png"
bg = pygame.image.load(bg_image)
bg = pygame.transform.scale(bg, (s_width, s_height))

interactive_game_image = pygame.image.load("images/InteractiveGameButton.png")
simulation_image = pygame.image.load("images/SimulationButton.png")
statistics_image = pygame.image.load("images/StatisticsButton.png")
options_image = pygame.image.load("images/options.png")

button_width, button_height = 400, 100  
spacing = 30  
game_button = Button(s_width/2 - button_width/2, s_height/2 - 2*button_height - 1.5*spacing, interactive_game_image, button_width, button_height)
simulation_button = Button(s_width/2 - button_width/2, s_height/2 - button_height - 0.5*spacing, simulation_image, button_width, button_height)
statistics_button = Button(s_width/2 - button_width/2, s_height/2 + 0.5*spacing, statistics_image, button_width, button_height)
options_button = Button(s_width/2 - button_width/2, s_height/2 + button_height + 1.5*spacing, options_image, button_width, button_height)

font = pygame.font.Font(None, 50)

loading_text = font.render("Loading...", True, pygame.Color('white'))

screen.blit(loading_text, (s_width/2 - loading_text.get_width()/2, s_height/2 - loading_text.get_height()/2))

b_width, b_height = 500, 50
bord = pygame.Rect(s_width/2 - b_width/2, s_height/2 + loading_text.get_height(), b_width, b_height)
filled_rect = pygame.Rect(s_width/2 - b_width/2, s_height/2 + loading_text.get_height(), 0, b_height)

loading = True
ticks = pygame.time.get_ticks()
while loading:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  if (pygame.time.get_ticks() - ticks) < 3000:
    
    filled_rect.width = ((pygame.time.get_ticks() - ticks) / 3000) * b_width
  else:
    loading = False

  pygame.draw.rect(screen, pygame.Color('white'), bord, 2)
  pygame.draw.rect(screen, pygame.Color('white'), filled_rect)

  pygame.display.flip()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if game_button.isOver(pygame.mouse.get_pos()):
        
        bg_image = "images/InGameScreen.png"
        bg = pygame.image.load(bg_image)
        bg = pygame.transform.scale(bg, (s_width, s_height))

        screen.blit(bg, (0, 0))
        pygame.display.flip()
  
        exec(open("interactive_game.py").read())
      elif simulation_button.isOver(pygame.mouse.get_pos()):
        exec(open("simulation.py").read())
        
      elif statistics_button.isOver(pygame.mouse.get_pos()):
        exec(open("statistics.py").read())
        
      elif options_button.isOver(pygame.mouse.get_pos()):
        exec(open("options.py").read())
        
  screen.blit(bg, (0, 0))
  game_button.draw(screen)
  simulation_button.draw(screen)
  statistics_button.draw(screen)
  options_button.draw(screen)
  
  pygame.display.flip()
  
pygame.quit()
