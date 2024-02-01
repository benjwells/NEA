import pygame

pygame.init()

#defines the dimensions of the screen
s_width = 1920
s_height = 1080

#creates a window with the dimensions of the screen
s = pygame.display.set_mode((s_width, s_height))

#defines an image as the background
bg = pygame.image.load("images/optionsBg.png")
#scales the image to the dimensions of the screen
bg = pygame.transform.scale(bg, (1920, 1080))

#defines the font of the loading text
font = pygame.font.Font(None, 50)
#states the text to be displayed
loading_text = font.render("Loading...", True, pygame.Color('white'))

#draws the loading text in the centre of the screen
s.blit(loading_text, (s_width/2 - loading_text.get_width()/2,
s_height/2 - loading_text.get_height()/2))

#defines the dimensions of the loading bar
b_width, b_height = 500, 50
#defines the top of the loading bar
rect_top = s_height/2 + loading_text.get_height() 
#defines the outline of the loading bar
outline_rect = filled_rect = pygame.Rect(s_width/2 - b_width/2, rect_top, b_width, b_height)
#defines the width of the loading bar
filled_rect.width = 0

#defines loading to be true
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
  

#class to create sliders
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.min = min_val
        self.max = max_val
        self.val = min_val
        self.dragging = False
        self.color = color

    #event handling
    def handle_event(self, event):
      #checks if the mouse is clicked
      if event.type == pygame.MOUSEBUTTONDOWN:
        #checks if the mouse is clicked within the slider
        if self.rect.collidepoint(event.pos): 
          #defines the dragging variable to true
          self.dragging = True 
      #checks if the mouse is released
      elif event.type == pygame.MOUSEBUTTONUP:
        #defines the dragging variable to false
        self.dragging = False
      #checks if the mouse is being moved while the mouse is being clicked
      elif event.type == pygame.MOUSEMOTION:
        if self.dragging: 
          #the x coordinate of the mouse is retrieved
          x, _ = event.pos 
          #calculates the position of the slider
          self.val = self.min + (x - self.rect.x) / self.rect.w * (self.max - self.min) 
          #checks if the sliders value is less than the minimum value
          if self.val < self.min: 
            #if it is, the slider value is set to the minimum value
            self.val = self.min
          #checks if the sliders value is greater than the maximum value
          elif self.val > self.max:
            #if it is, the slider value is set to the maximum value
            self.val = self.max
            
    def draw(self, screen):
      #draws the slider as a rectangle
      pygame.draw.rect(screen, self.color, self.rect, 1) 
      #calculates the x coordinate of the slider
      x = self.rect.x + (self.val - self.min) / (self.max - self.min) * self.rect.w 
      #draws the slider value as a circle
      pygame.draw.circle(screen, self.color, (int(x), self.rect.centery), 10)

#creates two instances of sliders from the slider class
slider1 = Slider(700, 600, 500, 20, 0, 100, (0, 0, 0))
slider2 = Slider(700, 220, 500, 20, 0, 100, (0, 0, 0))

##class to create buttons
class Button:
  def __init__(self, x, y, width, height, text):
    self.rect = pygame.Rect(x, y, width, height)
    self.text = text
    self.clicked = False


  def draw(self, screen, font):
    #draws the button as a rectangle
    pygame.draw.rect(screen, self.color, self.rect)
    #renders the text
    text_surface = font.render(self.text, True, pygame.Color('white'))
    #positions the text in the center of the button
    text_rect = text_surface.get_rect(center=self.rect.center)
    #draws the text on the button
    screen.blit(text_surface, text_rect)

  def is_clicked(self, pos):
    #checks if the button is clicked
    if self.rect.collidepoint(pos):
      #checks whether the mouse is hovering over the button
      self.clicked = not self.clicked 
      return True
    return False

#creates an instance of the button class
exit_button = Button(1500, 825, 300, 50, 'Return to Mode Selection')
#defines the colour of the button
exit_button.color = pygame.Color('Black')
#defines the font size of the text on the button
exit_button.font = pygame.font.Font(None, 30)

#class to create tickbox
class TickBox:
  def __init__(self, x, y, width, height):
    self.rect = pygame.Rect(x, y, width, height)
    self.width = width
    self.height = height
    self.clicked = False

  def draw(self,screen):
    #draws the tickbox as a rectangle
    pygame.draw.rect(screen, pygame.Color('black'), self.rect)
    #checks if the tickbox is clicked
    if self.clicked:
      #if it is, a circle is drawn in the centre of the tickbox to indicate that it's active
      pygame.draw.circle(screen, pygame.Color('white'), self.rect.center, 20)
      
  def handle_event(self, event):
    #checks if the mouse is clicked when the mouse is over the tickbox
    if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
      #toggles the click variable
      self.clicked = not self.clicked 

#creates two instances of tickboxes from the tickbox class
mute_m = TickBox(900, 410, 100, 50)
mute_sfx = TickBox(900, 850, 100, 50)

#draws the background image on screen
s.blit(bg, (0, 0))
#defines the music volume to 100
music_vol = 100
#defines the sound effects volume to 100
sfx_vol = 100

#defines the colour of the box
box_color = (255, 255, 255)  
#defines the position of the box in the centre of the screen at the top
box_x = 1920 // 2 - 400 
box_y = 0  

#defines the dimensions of the box
box_width = 800  
box_height = 1080  

#defines the font and colour of the text on screen
font = pygame.font.Font(None, 50)
text_color = (0, 0, 0)  

#defines the title
title = "Options"

#the title is rendered
title_surface = font.render(title, True , text_color)

#the position of the title on the screen at the top and in the centre is defined
title_x = box_x + (box_width - title_surface.get_width()) // 2
title_y = 10  

#the text for the box is defined
main_text = ["",
   "",
   "Music Volume"
   "",
   "", 
   "",
   "",
   "Mute Music", 
   "",
   "",
   "",
   "",
   "SFX Volume",
   "",
   "",
   "",
   "",
   "Mute SFX"]



#main game loop
running = True
while running:

  #draws the background image on screen
  s.blit(bg, (0, 0))

  #the box is drawn
  pygame.draw.rect(s, box_color, pygame.Rect(box_x, box_y, box_width, box_height))

  #four rectangles are drawn with height of 5 to represent lines to split up the options
  pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 100 , box_width, 5))
  pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 300 , box_width, 5))
  pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 500 , box_width, 5))
  pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 700 , box_width, 5))
  
  #the title is drawn on the screen
  s.blit(title_surface, (title_x, title_y))

  #the button is drawn on the screen
  exit_button.draw(s, exit_button.font)

  #the text is drawn into the text box bassed on the main_text list
  for i, line in enumerate(main_text):
    text_surface = font.render(line, True, text_color)
    text_x = box_x + (box_width - text_surface.get_width()) // 2
    text_y = title_y + title_surface.get_height() + 10 + i * (font.get_height() + 10) 
    s.blit(text_surface, (text_x, text_y))

  #the tickboxes are drawn on screen
  mute_m.draw(s)
  mute_sfx.draw(s)

  #the sliders are drawn on screen
  slider1.draw(s)
  slider2.draw(s)

  #event handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    #checks if the mouse is clicked
    elif event.type == pygame.MOUSEBUTTONDOWN:
      #if it is clicked whilst the mouse is over the exit button, the menu file is run
      if exit_button.is_clicked(event.pos):
        exec(open("menu.py").read())
    #checks if the mouse button has been released
    elif event.type == pygame.MOUSEBUTTONUP:  
      #calls the function from the tickbox class to check if the tickbox has been clicked
      if mute_m.handle_event(event):
        #if it has been clicked, the music volume is set to 0
        if mute_m.clicked:
           music_vol = 0
        #if it has not been clicked, music volume stays at 100
        else:
          music_vol = 100
        #calls the function from the tickbox class to check if the tickbox has been clicked
      if mute_sfx.handle_event(event):
        #if it has been clicked, the music volume is set to 0
        if mute_sfx.clicked:
          sfx_vol = 0
        #if it has not been clicked, music volume stays at 100
        else:
          sfx_vol = 100
      #checks if the tickbox for music is clicked
    if mute_m.clicked:
      #if it has, the slider value is set to the minimum slider value.
      slider2.val = slider2.min
    #if not, the slider value functions as normal
    else:
      slider2.handle_event(event)
    #checks if the tickbox for sound effects is clicked
    if mute_sfx.clicked:
      #if it is, the slider value is set to the minimum slider value.
      slider1.val = slider1.min
    #if not, the slider value functions as normal
    else:
      slider1.handle_event(event)

  #updates the screen
  pygame.display.flip()

pygame.quit()
