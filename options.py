import pygame

pygame.init()

s = pygame.display.set_mode((1920,1080))

bg = pygame.image.load("images/optionsBg.png")
bg = pygame.transform.scale(bg, (1920, 1080))

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.min = min_val
        self.max = max_val
        self.val = min_val
        self.dragging = False
        self.color = color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True 
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
              x, _ = event.pos
              self.val = self.min + (x - self.rect.x) / self.rect.w * (self.max - self.min)
              if self.val < self.min:
                self.val = self.min
              elif self.val > self.max:
                self.val = self.max
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 1)
        x = self.rect.x + (self.val - self.min) / (self.max - self.min) * self.rect.w
        pygame.draw.circle(screen, self.color, (int(x), self.rect.centery), 10)

slider1 = Slider(700, 600, 500, 20, 0, 100, (0, 0, 0))
slider2 = Slider(700, 220, 500, 20, 0, 100, (0, 0, 0))

class Button:
 def __init__(self, x, y, width, height, text):
     self.rect = pygame.Rect(x, y, width, height)
     self.text = text
     self.clicked = False


 def draw(self, screen, font):
   pygame.draw.rect(screen, self.color, self.rect)
   text_surface = font.render(self.text, True, pygame.Color('white'))
   text_rect = text_surface.get_rect(center=self.rect.center)
   screen.blit(text_surface, text_rect)

 def is_clicked(self, pos):
   if self.rect.collidepoint(pos):
    self.clicked = not self.clicked
    return True
   return False

exit_button = Button(1500, 825, 300, 50, 'Return to Mode Selection')
exit_button.color = pygame.Color('Black')
exit_button.font = pygame.font.Font(None, 30)

class TickBox:
  def __init__(self, x, y, width, height):
    self.rect = pygame.Rect(x, y, width, height)
    self.width = width
    self.height = height
    self.clicked = False

  def draw(self,screen):
    pygame.draw.rect(screen, pygame.Color('black'), self.rect)
    if self.clicked:
      pygame.draw.circle(screen, pygame.Color('white'), self.rect.center, 20)
      

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
      self.clicked = not self.clicked

    
mute_m = TickBox(900, 410, 100, 50)
mute_sfx = TickBox(900, 850, 100, 50)

s.blit(bg, (0, 0))
music_vol = 100
sfx_vol = 100
# Define the box properties
box_color = (255, 255, 255)  
box_x = 1920 // 2 - 400  # X position (center of the screen minus half the box width)
box_y = 0  # Y position (top of the screen)
box_width = 800  # Width
box_height = 1080  # Height (same as screen height)


# Define the text properties
font = pygame.font.Font(None, 50)
text_color = (0, 0, 0)  

title = "Options"
titlefont = pygame.font.Font(None, 100)
# Render the title
title_surface = font.render(title, True , text_color)


title_x = box_x + (box_width - title_surface.get_width()) // 2
title_y = 10  # A small margin from the top of the box

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



  # Game loop
running = True
while running:
    # Fill the screen with the background image
    s.blit(bg, (0, 0))

    # Draw the box
    pygame.draw.rect(s, box_color, pygame.Rect(box_x, box_y, box_width, box_height))
    pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 100 , box_width, 5))
    pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 300 , box_width, 5))
    pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 500 , box_width, 5))
    pygame.draw.rect(s, (0,0,0) , pygame.Rect(box_x, 700 , box_width, 5))
    # Draw the title on the screen
    s.blit(title_surface, (title_x, title_y))

    exit_button.draw(s, exit_button.font)

    # Draw the text
    for i, line in enumerate(main_text):
        text_surface = font.render(line, True, text_color)
        text_x = box_x + (box_width - text_surface.get_width()) // 2
        text_y = title_y + title_surface.get_height() + 10 + i * (font.get_height() + 10)  # Below the previous line with a small margin
        s.blit(text_surface, (text_x, text_y))

    mute_m.draw(s)
    mute_sfx.draw(s)
    slider1.draw(s)
    slider2.draw(s)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event.pos):
              exec(open("menu.py").read())
        elif event.type == pygame.MOUSEBUTTONUP:  
          if mute_m.handle_event(event):
             if mute_m.clicked:
               music_vol = 0
             else:
               music_vol = 100
          if mute_sfx.handle_event(event):
             if mute_sfx.clicked:
               sfx_vol = 0
             else:
               sfx_vol = 100
        if mute_m.clicked:
          slider2.val = slider2.min
        else:
          slider2.handle_event(event)
        if mute_sfx.clicked:
          slider1.val = slider1.min
        else:
          slider1.handle_event(event)
      
    pygame.display.flip()

pygame.quit()
