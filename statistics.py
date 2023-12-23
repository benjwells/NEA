import pygame

pygame.init()

s = pygame.display.set_mode((1920,1080))

bg = pygame.image.load("images/optionsBg.png")
bg = pygame.transform.scale(bg, (1920, 1080))

box_color = (255, 255, 255)  
box_width = 400  
box_height = 600  
box_y = 1080 // 2 - box_height // 2  # Y position (center of the screen)


font = pygame.font.Font(None, 50)
title_colour = (255, 255, 255)  
text_colour = (0,0,0) 

titles = ["Total Attempts", "Successful Attempts", "Success Rate"]


first_heading = "Your Statistics!"
first_font = pygame.font.Font("fonts/Dungeon Depths.otf", 50)  
first_surface = first_font.render(first_heading, True, title_colour)
first_x = 1920 // 2 - first_surface.get_width() // 2   
first_y = box_y // 2 - first_surface.get_height() // 2  

 
running = True
while running:
    # Fill the screen with the background image
    s.blit(bg, (0, 0))

   
    s.blit(first_surface, (first_x, first_y))

    for i, title in enumerate(titles):
        box_x = 1920 // 3 * i + 1920 // 6 - box_width // 2
        pygame.draw.rect(s, box_color, pygame.Rect(box_x, box_y, box_width, box_height))
        title_surface = font.render(title, True , text_colour)
        title_x = box_x + (box_width - title_surface.get_width()) // 2
        title_y = box_y  # The title is at the top of the box
        s.blit(title_surface, (title_x, title_y))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

