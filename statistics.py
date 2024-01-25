import pygame
import sqlite3
import login_page


pygame.init()

s = pygame.display.set_mode((1920,1080))

bg = pygame.image.load("images/optionsBg.png")
bg = pygame.transform.scale(bg, (1920, 1080))

font_loading = pygame.font.Font(None, 50)
loading_text = font_loading.render("Loading...", True, pygame.Color('white'))

s.blit(loading_text, (1920/2 - loading_text.get_width()/2,
1080/2 - loading_text.get_height()/2))

outline_rect = pygame.Rect(710, 540 + loading_text.get_height(), 500, 50)
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

  pygame.draw.rect(s, pygame.Color('white'), outline_rect, 2)
  pygame.draw.rect(s, pygame.Color('white'), filled_rect)

  pygame.display.flip()

box_color = (255, 255, 255)  
box_width = 400  
box_height = 600  


font = pygame.font.Font(None, 50)
title_colour = (255, 255, 255)  
text_colour = (0,0,0) 

box1_title = "Total Attempts"
box2_title = "Successful Attempts"
box3_title = "Success Rate"

main_heading = "Your Statistics!"
main_font = pygame.font.Font("fonts/Dungeon Depths.otf", 50)  
main_surface = main_font.render(main_heading, True, title_colour)
main_x = 1920 // 2 - main_surface.get_width() // 2  
main_y = 50  

class Button:
 def __init__(self, x, y, width, height, text):
     self.rect = pygame.Rect(x, y, width, height)
     self.text = text


 def draw(self, s, font):
   pygame.draw.rect(s, self.color, self.rect)
   text_surface = font.render(self.text, True, pygame.Color('white'))
   text_rect = text_surface.get_rect(center=self.rect.center)
   s.blit(text_surface, text_rect)

 def is_clicked(self, pos):
   if self.rect.collidepoint(pos):
    return self.rect.collidepoint(pos)



exit = Button(1500, 100, 300, 50, 'Return to Mode Selection')
exit.color = pygame.Color('Black')
exit.font = pygame.font.Font(None, 30)

running = True


conn = sqlite3.connect('user_accounts.db')
curs = conn.cursor()

curs.execute('''SELECT * FROM accounts WHERE username=?''', texts[0])
record = curs.fetchall()
record = record[0]
conn.commit()
conn.close()



while running:

  s.blit(bg, (0, 0))

  pygame.draw.rect(s, box_color, (100, 200, box_width, box_height))
  pygame.draw.rect(s, box_color, (760, 200, box_width, box_height))
  pygame.draw.rect(s, box_color, (1420, 200, box_width, box_height))
  text_surface = font.render(box1_title, True, text_colour)
  s.blit(text_surface, (175, 225))
  text_surface = font.render(box2_title, True, text_colour)
  s.blit(text_surface, (790, 225))
  text_surface = font.render(box3_title, True, text_colour)
  s.blit(text_surface, (1510, 225))
  s.blit(main_surface, (main_x, main_y))

  s.blit(font.render(str(record[2]),0,(0,0,0)),(270,350))
  s.blit(font.render(str(record[3]),0,(0,0,0)),(950,350))
  s.blit(font.render(str(record[4])+"%",0,(0,0,0)),(1575,350))
	
  exit.draw(s, exit.font)
 
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
      if exit.is_clicked(event.pos):
        exec(open("menu.py").read())
  
  pygame.display.flip()

pygame.quit()

