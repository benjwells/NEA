import pygame

pygame.init()

#sets the dimensions of the screen
s_width = 1920
s_height = 1080
#displays the dimensions in a window
s = pygame.display.set_mode((s_width, s_height))
# sets window caption
pygame.display.set_caption("Menu")

#loads background image
bg = pygame.image.load("images/modeSelection.png")
#scales the background to dimensions
bg = pygame.transform.scale(bg, (1920, 1080))

#loads the image for the game button
game_b = pygame.image.load("images/InteractiveGameButton.png") 
#loads the image for the simulation button
simulation_b = pygame.image.load("images/SimulationButton.png")
#loads the image for the statistics button
statistics_b = pygame.image.load("images/StatisticsButton.png")
#loads the image for the options button
options_b = pygame.image.load("images/options.png")

#class to create buttons
class Button:
  def __init__(self, x, y, image, width, height):
    self.image = image
    self.width = width
    self.height = height
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
    self.rect = self.image.get_rect() 
    self.rect.topleft = (x, y) 

  #function to draw the button on the screen
  def draw(self, surface): 
    surface.blit(self.image, self.rect)

  #function to check if the mouse is over the button
  def Over(self, pos): 
    if self.rect.collidepoint(pos):
      return True

  #function to scale the button image to the desired dimensions
  def resize(self, width, height): 
    self.image = pygame.transform.scale(self.image, (width, height))
    self.rect.size = self.image.get_size()
    return False

#creates four instances of buttons with the desired coordinates and images
game = Button(760, 300, game_b, 400, 100)
simulation = Button(760, 425, simulation_b, 400, 100)
stats = Button(760, 550, statistics_b, 400, 100)
optn = Button(760, 675, options_b, 400, 100)

# sets the font of loading bar
font = pygame.font.Font(None, 50)
#sets the text shown when loading
loading_text = font.render("Loading...", True, pygame.Color('white'))

#draws the loading text in the center of the screen
s.blit(loading_text, (s_width/2 - loading_text.get_width()/2,
s_height/2 - loading_text.get_height()/2))

#sets the dimesions of the loading bar
b_width, b_height = 500, 50
#sets the top of the loading bar
rect_top = s_height/2 + loading_text.get_height()
#sets the outline of the loading bar
outline_rect = filled_rect = pygame.Rect(s_width/2 - b_width/2, rect_top, b_width, b_height)
#sets the width of the loading ba
filled_rect.width = 0

#sets the loading to true
loading = True
#gets the ticks until 3000 ticks is reached
ticks = pygame.time.get_ticks()
while loading:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  #if the ticks is less than 3000, the width of the loading bar increases
  if (pygame.time.get_ticks() - ticks) < 3000:
    filled_rect.width = ((pygame.time.get_ticks() - ticks) / 3000) * b_width
  else:
    #stops loading process
    loading = False

  #draws the outline of the loading bar
  pygame.draw.rect(s, pygame.Color('white'), outline_rect, 2)
  #updates loading bar width and fills it
  pygame.draw.rect(s, pygame.Color('white'), filled_rect)
  #updates the screen
  pygame.display.flip()

#a variable that stores whether the simulation is running
running = True

#main game loop
while running:

  #event handling loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
    #checks if the mouse is clicked
    if event.type == pygame.MOUSEBUTTONDOWN:
      #checks if the game button is clicked
      if game.Over(pygame.mouse.get_pos()):
        #runs the interactive game file
        exec(open("interactive_game.py").read())
      #checks if the simulation button is clicked  
      elif simulation.Over(pygame.mouse.get_pos()):
        #runs the simulation file
        exec(open("simulation.py").read())
      #checks if the statistics button is clicked
      elif stats.Over(pygame.mouse.get_pos()):
        #runs the statistics file
        exec(open("statistics.py").read())
      #checks if the options button is clicked  
      elif optn.Over(pygame.mouse.get_pos()):
        #runs the options file
        exec(open("options.py").read())
        
  #draws the background image on screen
  s.blit(bg, (0, 0))
  #draws the buttons on the screen using a function from the button class
  game.draw(s)
  simulation.draw(s)
  stats.draw(s)
  optn.draw(s)

  #updates the screen
  pygame.display.flip()
  
pygame.quit()
