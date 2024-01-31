import pygame
import sqlite3
import login_page

pygame.init()
#sets the dimensions of the screen
s_width = 1920
s_height = 1080
#creates a window with the dimensions of the screen
s = pygame.display.set_mode((s_width, s_height))

#sets an image as the background
bg = pygame.image.load("images/optionsBg.png")
#scales the image to the dimensions of the screen
bg = pygame.transform.scale(bg, (1920, 1080))

#sets the font of the loading text
font = pygame.font.Font(None, 50)
#states the text to be displayed
loading_text = font.render("Loading...", True, pygame.Color('white'))

#draws the loading text in the centre of the screen
s.blit(loading_text, (s_width/2 - loading_text.get_width()/2,
s_height/2 - loading_text.get_height()/2))

#sets the dimensions of the loading bar
b_width, b_height = 500, 50
#sets the top of the loading bar
rect_top = s_height/2 + loading_text.get_height()
#sets the outline of the loading bar
outline_rect = filled_rect = pygame.Rect(s_width/2 - b_width/2, rect_top, b_width, b_height)
#sets the width of the loading bar
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
  
#sets the colour of the box
box_color = (255, 255, 255)  
#sets the width of the box
box_width = 400  
#sets the height of the box
box_height = 600  

#sets the font for the title
font = pygame.font.Font(None, 50)
#sets the colour of the title
title_colour = (255, 255, 255)  
#sets the colour of the text
text_colour = (0,0,0) 

#sets the title for each box
box1_title = "Total Attempts"
box2_title = "Successful Attempts"
box3_title = "Success Rate"

#sets the main heading when screen is loaded
main_heading = "Your Statistics!"
#sets the font for the main heading
main_font = pygame.font.Font("fonts/Dungeon Depths.otf", 50)  
#renders the main heading
main_surface = main_font.render(main_heading, True, title_colour) 
#sets the x coordinate of the main heading to the middle of the screen
main_x = 1920 // 2 - main_surface.get_width() // 2  
#sets the y coordinate of the main heading to the top of the screen
main_y = 50  

#class to create buttons
class Button:
  def __init__(self, x, y, width, height, text):
    self.rect = pygame.Rect(x, y, width, height)
    self.text = text

  def draw(self, s, font):
    #draws the button as a rectangle
    pygame.draw.rect(s, self.color, self.rect)
    #renders the text
    text_surface = font.render(self.text, True, pygame.Color('white'))
    #positions the text in the center of the button
    text_rect = text_surface.get_rect(center=self.rect.center)
    #draws the text on the button
    s.blit(text_surface, text_rect)

  def is_clicked(self, pos):
    #checks if the button is clicked
    if self.rect.collidepoint(pos):
      #checks whether the mouse is hovering over the button
      return self.rect.collidepoint(pos)


#creates an instance of the button class
exit = Button(1500, 100, 300, 50, 'Return to Mode Selection')
#sets the colour of the button
exit.color = pygame.Color('Black')
#sets the fon size of the text on the button
exit.font = pygame.font.Font(None, 30)

#sets the running variable to true
running = True 

#connects to the database
conn = sqlite3.connect('user_accounts.db') 
#a cursor is created
curs = conn.cursor() 
#prints texts[0]
print(texts[0]) 
#selects all the data from the table with the corresponding username
curs.execute('''SELECT * FROM accounts WHERE username=?''',(texts[0],)) 
record = curs.fetchall() 
#obtains the first record
record = record[0]
#the change is committed 
conn.commit() 
#the connection is closed
conn.close()

#main game loop
while running:

  #draws the background image on screen
  s.blit(bg, (0, 0))

  #draws three boxes at differing x coordinates and equal y coordinates
  pygame.draw.rect(s, box_color, (100, 200, box_width, box_height)) 
  pygame.draw.rect(s, box_color, (760, 200, box_width, box_height))
  pygame.draw.rect(s, box_color, (1420, 200, box_width, box_height))
  #draws the title onto the corresponding boxes
  text_surface = font.render(box1_title, True, text_colour)
  s.blit(text_surface, (175, 225))
  text_surface = font.render(box2_title, True, text_colour)
  s.blit(text_surface, (790, 225))
  text_surface = font.render(box3_title, True, text_colour)
  s.blit(text_surface, (1510, 225))
  #draws the title at the top of the screen
  s.blit(main_surface, (main_x, main_y))

  #draws the selected records from the database onto the screen in the designated box
  s.blit(font.render(str(record[2]),0,(0,0,0)),(270,350))
  s.blit(font.render(str(record[3]),0,(0,0,0)),(950,350))
  s.blit(font.render(str(record[4])+"%",0,(0,0,0)),(1575,350))

  #draws the exit button
  exit.draw(s, exit.font)
 
  #event handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    #checks if the mouse is clicked
    elif event.type == pygame.MOUSEBUTTONDOWN:
      #checks if the exit button is clicked
      if exit.is_clicked(event.pos):
        #runs the menu file
        exec(open("menu.py").read())

  #updates the screen
  pygame.display.flip()

pygame.quit()
