import pygame
import sys
import math
import sqlite3
from login_page import Database


pygame.init()


#sets the dimensions of the screen
s_width = 1920
s_height = 1080
#displays the dimensions in a window
s = pygame.display.set_mode((s_width, s_height))
# sets window caption
pygame.display.set_caption("Interactive Game") 

#loads background image
bg = pygame.image.load("images/InGameScreen.png")
#scales the backgrouund to dimensions
bg = pygame.transform.scale(bg, (1920, 1080))

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

#sets the font of text
font = pygame.font.Font(None, 30)
#sets the colour of the cox
box_colour = pygame.Color('white')
#sets the separation of the boxes when they're drawn
box_margin = 20
#sets the dimensions of the box
box_width = 200
box_height = 60

#creates a list of the input boxes with their respective positions and dimensions
input = [
pygame.Rect(220, 20, 200, 60),  
pygame.Rect(220, 150, 200, 60),  
pygame.Rect(610, 20, 200, 60), 
pygame.Rect(610, 150, 200, 60),
pygame.Rect(1440, 530, 480, 250)
]

#creates a list of the text that will be displayed adjacent to the boxes
label = ["Gravity", "Distance of Target", "Initial Velocity", "Angle",""]

#creates a list of the text that will be above the output values
output = ["Acceleration (y)", "Displacement", "Time Taken", "Current Velocity"]
#creates a list of the initial output values
scientific_output = [9.81, 0, 0, 30]  

#sets the radius of the projectile
proj_radius = 7.5
#sets the colour of the projectile
projectile_color = pygame.Color('black')
#sets the starting position of the projectile
proj_initial_pos = [220, 780]
#an empty list that will store the projectile's positions during motion
projectile_movement = []

#sets the width of the target
target_width = 70
#sets the colour of the target
target_color = pygame.Color('black')
#sets the y position of the target (same level as projectile starting position)
target_y = 780  

#variable that is used to check if the box is being hovered over
active_box = None
#initial values that are in the input boxes
input_text = ["9.81", "500", "30", "45",""]  

#sets gravity equal to the first value of the list
gravity = float(input_text[0])
#sets the target distance to the second value of the list
target_distance = float(input_text[1])
#sets the initial velocity to the third value of the list
initial_velocity = float(input_text[2])
#sets the launch angle to the fourth value of the list
launch_angle = math.radians(float(input_text[3]))
#sets the text in the information box to the fifth value of the list
info_box = str(input_text[4])


#variable used to check if the target has been hit
hit = None  

#class to create buttons
class Button:
  def __init__(self, x, y, width, height, text):
    self.rect = pygame.Rect(x, y, width, height)
    self.text = text


  def draw(self, screen, font):
    #draws the button as a rectangle
    pygame.draw.rect(screen, self.color, self.rect)
    #renders the text for the button
    text_surface = font.render(self.text, True, pygame.Color('white'))
    #positions the text in the center of the button
    text_rect = text_surface.get_rect(center=self.rect.center)
    #draws the text on the button
    screen.blit(text_surface, text_rect)

  def is_clicked(self, pos):
    #checks whether the mouse is hovering over the button
    return self.rect.collidepoint(pos)

#instances of buttons that were created from the button class
start_button = Button(1000, 150, 300, 50, 'Start')
stop_button = Button(1400, 150, 300, 50, 'Stop')
exit_button = Button(1500, 825, 300, 50, 'Return to Mode Selection')
#sets the  colours of the buttons
stop_button.color = pygame.Color('red')
start_button.color = pygame.Color('green')
exit_button.color = pygame.Color('Black')

#sets a variable to track whether the projectile motion is paused
simulation_paused = False

#a function that draws the output boxes with the corresponding labels
def draw_scientific_output(screen, font, output, scientific_output, input, box_margin, box_width, box_height):
  for i, label in enumerate(output):
    label_surface = font.render(label, True, pygame.Color('white'))
    value_surface = font.render(f"{scientific_output[i]:.2f}", True, pygame.Color('black'))
    #calculates the x position based on the last input box's position and spacing
    label_x = input[-1].right + 20 + (i * (200 + 20))-900
    #draws the label and value on the screen
    screen.blit(label_surface, (label_x, 20))
    screen.blit(value_surface, (label_x, 20 + 60 + 20))

#variable that stores the initial playback speed
playback_speed = 1 

#a variable that stores whether the simulation is running
running = True
#sets the clock using inbuilt pygame function
clock = pygame.time.Clock()
#variable that stores the time since the simulation started
time_elapsed = 0
#variable that stores whether the projectile is running or not
proj_running = False
#a variable that is used when the position of the projectile is equal to its intiatial position
proj_pos = proj_initial_pos.copy()

#variables that store the new positions of the projectile as it experiences motion
x_pos = 0
y_pos = 0

#sets the colour of the output boxes
o_box_color = pygame.Color('white')
#variables that stores the dimesnions of the output box
o_width, o_height = 550, 540  
#sets the dimensions and position of the output boxes 
o_box = pygame.Rect(1400, 250, o_width, o_height)  
#creates a surface for the output box
o_surface = pygame.Surface((o_width, o_height)) 
#fills the surface with the output box color
o_surface.fill(o_box_color) 
#draws the output boxes on the screen
s.blit(o_surface, (o_box.x, o_box.y)) 

#the text that is drawn into the big output box
equations = [
"Equations:",
"Below are the 5 SUVAT equations:",
"v = u + at",
"s = ut + 0.5at^2",
"t = (v - u) / a",
"v^2 = u^2 + 2as",
"v = ut - 0.5at^2",
"",
"Below are examples of calculations you may need:",
"",
"Current Velocity: v = u + at",
"Max Height: H = (u^2 * sin^2(theta)) / (2g)",
"Displacement: s = ut + 0.5at^2",
"Final Velocity: v = sqrt(u^2 + 2gs)",
"Time: t = (v - u) / a",
"",
"Note: Change the playback speed of the projectile",
"by using the up and down arrows on the keyboard."]

#starting position of the text
start_point = []

 #creates a list of surfaces for each line of text
equation_surface = [font.render(equation, True, pygame.Color('white')) for equation in equations]

#draws the text in the output box
for i, equation_surface in enumerate(equation_surface):
  s.blit(equation_surface, (o_box.x , o_box.y  ))

#main game loop
while running:
  #a variable that records 1000 updates per 60 frames
  delta_t = clock.tick(60) / 1000  
  #draws the background image on screen
  s.blit(bg, (0, 0))

  #updates the input values to what the user enters
  try:
    gravity = float(input_text[0])
    target_distance = float(input_text[1])
    initial_velocity = float(input_text[2])
    launch_angle = math.radians(float(input_text[3]))
  #handles the case where the input text is not a valid number
  except ValueError:
    gravity = 9.81  #default value or previous valid value
    target_distance = 500  ##default value or previous valid value
    initial_velocity = 30  #default value or previous valid value
    launch_angle = math.radians(45) #default value or previous valid value
    
  #error message for gravity
  error_grav = font.render("Gravity must be between 2 and 15", True, pygame.Color('red')) 
  #error message for target distance
  error_target = font.render("Target distance must be between 200 and 1119", True, pygame.Color('red'))
  #error message for initial velocity
  error_ivel = font.render("Initial velocity must be between 30 and 150", True, pygame.Color('red'))
  #error message for launch angle
  error_angle = font.render("Launch angle must be between 0 and 89", True, pygame.Color('red'))

  #checks if the input value of gravity is between 2 and 15 or empty
  if gravity < 2 or gravity > 15 or input_text[0] == "":
    #draws the error message on the screen
    s.blit(error_grav, (135, 100))
    #sets the projectile running variable to false to stop it running
    proj_running = False

  #checks if the input value of target distance is between 200 and 1119 or empty
  elif target_distance < 200 or target_distance > 1119 or input_text[1] == "":
    #draws the error message on the screen
    s.blit(error_target, (50, 220))
    #sets the projectile running variable to false to stop it running
    proj_running = False

  #checks if the input value of initial velocity is between 30 and 150 or empty
  elif initial_velocity < 30 or initial_velocity > 150 or input_text[2] == "":
    #draws the error message on the screen
    s.blit(error_ivel, (450, 100))
    #sets the projectile running variable to false to stop it running
    proj_running = False

  #checks if the input value of launch angle is between 0 and 89 or empty
  elif launch_angle <= math.radians(0) or launch_angle > math.radians(89) or input_text[3] == "":
    #draws the error message on the screen
    s.blit(error_angle, (450, 220))
    #sets the projectile running variable to false to stop it running
    proj_running = False

  #event handling loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
          running = False
      #checks for mouse clicks 
    elif event.type == pygame.MOUSEBUTTONDOWN:
      #checks if the mouse is clicked on the start button
      if start_button.is_clicked(event.pos):
        #hit status is toggled off
        hit = None
        #sets the projectile running variable to true to start it running
        if simulation_paused:
          simulation_paused = False
          proj_running = True
        else:
          #start the projectile's motion if it's not already in motion
          if not proj_running:
            proj_running = True
            proj_pos = proj_initial_pos.copy() 
            projectile_movement.clear()

      #checks if the mouse is clicked on the stop button
      if stop_button.is_clicked(event.pos):
        #pauses the simulation
        simulation_paused = True
        #stops the projectile's motion
        proj_running = False  
        #resets the active box
        active_box = None 
      #checks for mouse clicks on input boxes
      for i, box in enumerate(input):
        #checks if the mouse is hovering over the input box
        if box.collidepoint(event.pos):
          #sets the active box to the current input box
          active_box = i
          break

      #checks if the mouse is clicked on the exit button
      if exit_button.is_clicked(event.pos):
        #runs the menu file    
        exec(open("menu.py").read())

    #checks for key presses
    elif event.type == pygame.KEYDOWN:
      #checks if the box is active
      if active_box is not None:
        #checks if backspace is pressed
        if event.key == pygame.K_BACKSPACE:
          #removes the ending character from the input text
          input_text[active_box] = input_text[active_box][:-1]
        else:
          #adds the pressed character to the input text
          input_text[active_box] += event.unicode
      #checks if the up key has been pressed
      if event.key == pygame.K_UP:
        #doubles the playback speed
        playback_speed *= 2  
        #checks if the playback speed us greater than 8
        if playback_speed > 8:
          #sets the playback speed to 8
          playback_speed = 8
      #checks if the down key has been pressed
      if event.key == pygame.K_DOWN:
        #halves the playback speed
        playback_speed /= 2  
        #checks if the playback speed is less than 0.1
        if playback_speed < 0.1: 
          #sets the playback speed to 0.1
          playback_speed = 0.1

  #draws the buttons
  start_button.draw(s, font)
  stop_button.draw(s, font)
  exit_button.draw(s, font)

  #draws the input boxes on the screen based on the previous box
  for i, box in enumerate(input):
    pygame.draw.rect(s, box_colour, box)
    label_surface = font.render(label[i], True, pygame.Color('white'))
    s.blit(label_surface, (box.x - label_surface.get_width() - 10, box.y + (60 - label_surface.get_height()) // 2))
    text_surface = font.render(input_text[i], True, pygame.Color('black'))
    s.blit(text_surface, (box.x + 5, box.y + 5))

  #draws the output box
  pygame.draw.rect(s, o_box_color, o_box)

  ##draws the sequation list onto the output box
  for i, equation in enumerate(equations):
    text_surface = font.render(equation, True, pygame.Color('black'))
    s.blit(text_surface, (o_box.x , o_box.y + 5 + (len(start_point) + i) * (font.get_height() + 5)))

  #calculates the x-coordinate based on the distance from the circle
  #draws the target line using the updated target distance
  target_x = proj_initial_pos[0] + target_distance  
  #draws the target line using the updated target distance
  pygame.draw.line(s, target_color, (target_x, target_y), (target_x + target_width, target_y), 2)

  #checks if the projectile is running
  if proj_running and not simulation_paused:
    #increments the time elapsed by delta t multiplied by playback speed
    time_elapsed += delta_t * playback_speed  

    #updates the x and y position of the projectile based on the current time elapsed
    x_pos = initial_velocity * math.cos(launch_angle) * time_elapsed
    y_pos = initial_velocity * math.sin(launch_angle) * time_elapsed - (0.5 * gravity * time_elapsed ** 2)

    #updates the projectile's position
    proj_pos[0] = proj_initial_pos[0] + x_pos
    proj_pos[1] = proj_initial_pos[1] - y_pos

    #appends the new position to the projectile path for tracing
    projectile_movement.append((int(proj_pos[0]), int(proj_pos[1])))

      
    #checks if the projectile has reached the ground
    if proj_pos[1] >= proj_initial_pos[1]:
      #checks if the projectile has hit the target
      if target_x <= proj_pos[0] <= target_x + target_width: 
        #stores a variable that will be written on the screen
        hit = "Target Hit"
        #calls a function from the database that will update total tries and successful tries
        account.increment_tries(True)
            
      else:
        #stores a variable that will be written on the screen
        hit = "Target Missed"
        #calls a function from the database that will update total tries only
        account.increment_tries(False)
      
      proj_running = False
      time_elapsed = 0
      proj_pos = proj_initial_pos.copy()
      projectile_movement.clear()
        
       
    #checks if the y position has exceeded 515 
    elif y_pos >= 515:
      #stores a variable that will be written on the screen
      hit = "Target Missed"
      proj_running = False
      time_elapsed = 0
      proj_pos = proj_initial_pos.copy()
      projectile_movement.clear()
          
          
    #checks if the x position has exceeded 1405
    elif proj_pos[0] >= 1405:
      #stores a variable that will be written on the screen
      hit = "Target Missed"
      proj_running = False
      time_elapsed = 0
      proj_pos = proj_initial_pos.copy()
      projectile_movement.clear()
      
      

  #draws the projectile on the screen
  pygame.draw.circle(s, projectile_color, (int(proj_pos[0]), int(proj_pos[1])), proj_radius)

  
  scientific_output[0] = gravity #sets the value of gravity as acceleration in the y
  scientific_output[1] = math.sqrt(x_pos**2 + y_pos**2) #calculates the displacement
  scientific_output[2] = time_elapsed  #time taken for the projectile to reach ground level
  velocity_x = initial_velocity * math.cos(launch_angle)  #calculates velocity in the x
  velocity_y = initial_velocity * math.sin(launch_angle) - (gravity * time_elapsed) #calculates velocity in the y
  scientific_output[3] = math.sqrt(velocity_x**2 + velocity_y**2)  #calculates the current velocity

  #draws the output label and updates the values every frame
  draw_scientific_output(s, font, output, scientific_output, input, 20, 200, 60)

  #checks if the hit variable was saved as "Target Missed"
  if hit == "Target Missed":
    #sets the message to be displayed on the screen
    message_surface = font.render(hit, True, pygame.Color('red')) 
    #draws the message on the screen
    s.blit(message_surface, (1920 // 2 - message_surface.get_width() // 2, 1080 // 2 - message_surface.get_height() // 2))

  #checks if the hit variable was saved as "Target Hit"
  elif hit == "Target Hit":
    #sets the message to be displayed on the screen
    message_surface1 = font.render(hit, True, pygame.Color('green'))
    #draws the message on the screen
    s.blit(message_surface1, (1920 // 2 - message_surface1.get_width() // 2, 1080 // 2 - message_surface1.get_height() // 2))

  #draws the tracer for the projectile
  if len(projectile_movement) > 1:
    pygame.draw.lines(s, projectile_color, False, projectile_movement, 3)

  #updates the screen
  pygame.display.flip()
  #limits frame rate to 60 fps
  clock.tick(60)

pygame.quit()
sys.exit()
