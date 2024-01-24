import pygame
from login_page import Button

pygame.init()

s = pygame.display.set_mode((1920,1080))

bg = pygame.image.load("images/modeSelection.png")
bg = pygame.transform.scale(bg, (1920, 1080))

game_b = pygame.image.load("images/InteractiveGameButton.png")
simulation_b = pygame.image.load("images/SimulationButton.png")
statistics_b = pygame.image.load("images/StatisticsButton.png")
options_b = pygame.image.load("images/options.png")

game = Button(760, 300, game_b, 400, 100)
simulation = Button(760, 425, simulation_b, 400, 100)
stats = Button(760, 550, statistics_b, 400, 100)
optn = Button(760, 675, options_b, 400, 100)


font = pygame.font.Font(None, 50)
loading_text = font.render("Loading...", True, pygame.Color('white'))

s.blit(loading_text, (960 - loading_text.get_width()/2, 540 - loading_text.get_height()/2))


bord = pygame.Rect(710, 540 + loading_text.get_height(), 500, 50)
filled_rect = pygame.Rect(710, 540 + loading_text.get_height(), 0, 50)
loading = True

ticks = pygame.time.get_ticks()
while loading:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  if (pygame.time.get_ticks() - ticks) < 3000:
    
    filled_rect.width = ((pygame.time.get_ticks() - ticks) / 3000) * 500
  else:
    loading = False

  pygame.draw.rect(s, pygame.Color('white'), bord, 2)
  pygame.draw.rect(s, pygame.Color('white'), filled_rect)

  pygame.display.flip()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if game.Over(pygame.mouse.get_pos()):
        exec(open("interactive_game.py").read())
      elif simulation.Over(pygame.mouse.get_pos()):
        exec(open("simulation.py").read())
        
      elif stats.Over(pygame.mouse.get_pos()):
        exec(open("statistics.py").read())
        
      elif optn.Over(pygame.mouse.get_pos()):
        exec(open("options.py").read())
        
  s.blit(bg, (0, 0))
  game.draw(s)
  simulation.draw(s)
  stats.draw(s)
  optn.draw(s)
  
  pygame.display.flip()
  
pygame.quit()
