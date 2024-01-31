import pygame


pygame.init()
s_width = 1920
s_height = 1080
s = pygame.display.set_mode((s_width, s_height))

bg = pygame.image.load("images/modeSelection.png")
bg = pygame.transform.scale(bg, (1920, 1080))

game_b = pygame.image.load("images/InteractiveGameButton.png")
simulation_b = pygame.image.load("images/SimulationButton.png")
statistics_b = pygame.image.load("images/StatisticsButton.png")
options_b = pygame.image.load("images/options.png")

class Button:
  def __init__(self, x, y, image, width, height):
    self.image = image
    self.width = width
    self.height = height
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
    self.rect = self.image.get_rect() 
    self.rect.topleft = (x, y) 

  def draw(self, surface):
    surface.blit(self.image, self.rect)

  def Over(self, pos):
    if self.rect.collidepoint(pos):
      return True

  def resize(self, width, height):
    self.image = pygame.transform.scale(self.image, (width, height))
    self.rect.size = self.image.get_size()
    return False
    
game = Button(760, 300, game_b, 400, 100)
simulation = Button(760, 425, simulation_b, 400, 100)
stats = Button(760, 550, statistics_b, 400, 100)
optn = Button(760, 675, options_b, 400, 100)


font = pygame.font.Font(None, 50)
loading_text = font.render("Loading...", True, pygame.Color('white'))

s.blit(loading_text, (s_width/2 - loading_text.get_width()/2,
s_height/2 - loading_text.get_height()/2))


b_width, b_height = 500, 50
rect_top = s_height/2 + loading_text.get_height()
outline_rect = filled_rect = pygame.Rect(s_width/2 - b_width/2, rect_top, b_width, b_height)
filled_rect.width = 0
pygame.draw.rect(s, pygame.Color('white'), outline_rect)

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

  pygame.draw.rect(s, pygame.Color('white'), outline_rect, 2)
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
