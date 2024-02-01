import pygame
import sys
import math,time
from pygame.locals import *
from pygame import mixer

pygame.init()

#sets the dimensions of the screen
s_width, s_height = 1920, 1080 
#displays the dimensions in a window
screen = pygame.display.set_mode((s_width, s_height))
# sets window caption
pygame.display.set_caption("Simulation") 

#stores the location of the background image
bg_image_path = "images/InGameScreen.png" 
#loads background image
bg = pygame.image.load(bg_image_path) 
#scales the background to dimensions
bg = pygame.transform.scale(bg, (s_width, s_height)) 

# sets the font of loading bar
font = pygame.font.Font(None, 50) 
#sets the text shown when loading
loading_text = font.render("Loading...", True, pygame.Color('white')) 

#draws the loading text in the center of the screen
screen.blit(loading_text, (s_width/2 - loading_text.get_width()/2,
s_height/2 - loading_text.get_height()/2)) 

#sets the dimesions of the loading bar
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
  pygame.draw.rect(screen, pygame.Color('white'), outline_rect, 2) 
  #updates loading bar width and fills it
  pygame.draw.rect(screen, pygame.Color('white'), outline_rect) 
  #updates the screen
  pygame.display.flip()

#list that sets gravity values
gravity_values = [3.721, 8.87, 3.7, 24.79, 10.44] 

#sets the colour of the box white
input_box_color = pygame.Color('white')
# dimensions of the text box
box_width, box_height = 200, 60 
#spacing between each box
box_spacing = 20 
#dimensions of the information box
info_box_width, info_box_height = 480, 250

#each input box is set as a list of its x and y coordinates
input = [             
  pygame.Rect(100, 100, box_width, box_height), 
  pygame.Rect(350, 100, box_width, box_height), 
  pygame.Rect(600, 100, box_width, box_height), 
  pygame.Rect(1440, 530, box_width, box_height)
]

#sets the font of the labels
font = pygame.font.Font(None, 36) 

#labels for the input boxes boxes
label = ["Gravity", "Initial Velocity", "Angle",""] 

#labels for outputs
output = ["Acceleration (y)", "Displacement", "Time Taken", "Current Velocity"] 

#output initial values
scientific_output = [9.81, 0, 0, 30]  

#radius of the projectile
proj_radius = 7.5 
#colour of the projectile
projectile_color = pygame.Color('black') 
#initial position of the projectile
proj_initial_pos = [220, 780] 
#a list to store the positions of the projectile
projectile_movement = [] 

#used to check whether the user is hovering over a box
active_box = None 
#sets the default gravity value
grav_input = "9.81" 
#initial values of the input boxes
input_text = ["9.81", "30", "45",""]  

#stops the programming failing if no value is entered. Note: if the user wanted to type 70 for velocity, they'd have to remove both values of 3 and 0 to enter the 7 and 0. The value is set to 0 if no values are entered
for i in range(len(input_text)): 
  if input_text[i] == "":
    input_text[i] = "0.0"
#sets the gravity equal to the text input by the user
gravity = float(input_text[0]) 
#sets the velocity equal to the text input by the user
initial_velocity = float(input_text[1]) 
#sets the angle equal to the text input by the user
launch_angle = math.radians(float(input_text[2])) 
#sets the info box equal to the text input by the user
info_box = str(input_text[3]) 

#class to create buttons
class Button: 
  def __init__(self, x, y, width, height, text):
    self.rect = pygame.Rect(x, y, width, height)
    self.text = text


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
    #checks whether the mouse is hovering over the button
    return self.rect.collidepoint(pos)

class TickBox: #class used to create tickboxes
  def __init__(self, x, y, width, height):
    self.rect = pygame.Rect(x, y, width, height)
    self.width = width
    self.height = height
    self.clicked = False
  
  def draw(self,screen):
    pygame.draw.rect(screen, pygame.Color('black'), self.rect)
    #draws a rectangle as the tickbox
    if self.clicked:
      #draws a white circle in the center of the tickbox if the tickbox is clicked
      pygame.draw.circle(screen, pygame.Color('white'), self.rect.center, 5)

  def is_clicked(self,pos):
    #checks whether the mouse is hovering over the tickbox
    if self.rect.collidepoint(pos):
      #if the mouse is hovering over the tickbox, the clicked attribute is set to True
      if self.clicked:
        #the clicked attribute is set to false if the tickbox is already clicked
        self.clicked = False
        return False
        
      else:
        #the clicked tickbox is set to true if it has not already been clicked
        self.clicked = True
        return True
    return False

#class used to model air resistance
class AirResistance: 
  def __init__(self, mass, drag_coefficient, area, velocity_x, velocity_y, air_density):
    self.mass = mass
    self.drag_coefficient = drag_coefficient
    self.area = area
    self.velocity_x = velocity_x
    self.velocity_y = velocity_y
    self.air_density = air_density  

  def calculate_air_resistance(self):
    #calculates the velocity squared using the x and y components of velocity
    velocity_squared = self.velocity_x ** 2 + self.velocity_y ** 2
    #calculates the resistive force using the equation F = 0.5 * rho * A * C * V^2
    air_resistance = 0.5 * self.drag_coefficient * self.air_density * self.area * velocity_squared
    return air_resistance

  def update_velocity(self, time_elapsed):
    air_resistance = self.calculate_air_resistance()
    #updates the velocity components
    velocity_angle = math.atan2(self.velocity_y, self.velocity_x)
    
    #calculates the air resistance in the horizontal plane
    air_resistance_x = air_resistance * math.cos(velocity_angle)
    #calculates the air resistance in the vertical plane
    air_resistance_y = air_resistance * math.sin(velocity_angle)

    #calculates the acceleration in the horizonatl plane
    acceleration_x = -air_resistance_x / self.mass
    #calculates the acceleration in the vertical plane
    acceleration_y = -air_resistance_y / self.mass

    #updates the velocity components using the acceleration
    self.velocity_x += acceleration_x * time_elapsed
    self.velocity_y += acceleration_y * time_elapsed
    #prints velocity components in console (used for debugging)
    print(f"Updated velocities: {self.velocity_x}, {self.velocity_y}")
      

     

  def apply(self, velocity):
    #returns the motion of the projectile
    return -self.drag_coefficient * velocity**2

#constants used in air resistance calculation
mass = 1
drag_coefficient = 0.3
area = 1
air_density = 1
time_step = 0.001

#instances of buttons that were created from the button class
start_button = Button(1000, 150, 300, 50, 'Start')
stop_button = Button(1400, 150, 300, 50, 'Stop')
exit_button = Button(1500, 825, 300, 50, 'Return to Mode Selection')
#sets the  colours of the buttons
start_button.color = pygame.Color('green')
stop_button.color = pygame.Color('red')
exit_button.color = pygame.Color('Black')

#a list of instances of tickboxes created from the tickbox class
tickboxes = [TickBox(1500, 380, 30, 20),
             TickBox(1500, 430, 30, 20),
             TickBox(1500, 480, 30, 20),
             TickBox(1500, 530, 30, 20),
             TickBox(1500, 580, 30, 20),
             TickBox(1550, 630, 30, 20)]

#variable that stores whether the simulation is paused
simulation_paused = False

#a function that draws the output boxes with the corresponding labels
def draw_scientific_output(screen, font, output, scientific_output, input, box_spacing, box_width, box_height):
  for i, label in enumerate(output):
    label_surface = font.render(label, True, pygame.Color('white'))
    value_surface = font.render(f"{scientific_output[i]:.2f}", True, pygame.Color('black')) 
    #calculates the x position based on the last input box's position and spacing
    label_x = input[-1].right + box_spacing + (i * (box_width + box_spacing))-700
    #draws the label and value on the screen
    screen.blit(label_surface, (label_x, 20))
    screen.blit(value_surface, (label_x, 20 + box_height + box_spacing))

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
#sets the initial position of the projectile
proj_pos = proj_initial_pos.copy() 

#variables that store the new positions of the projectile as it experiences motion
x_pos = 0
y_pos = 0

#sets the colour of the output boxes
o_box_color = pygame.Color('white')
#sets the dimensions and position of the output box
o_box = pygame.Rect(1400, 250, 550, 540)  
#sets the dimensions of the text
o_surface = pygame.Surface((550, 540))
#fills the surface with the output box color
o_surface.fill(o_box_color)  
#draws the output boxes on the screen
screen.blit(o_surface, (o_box.x, o_box.y)) 

#the text that is drawn into the big output box
simulations = [
  "Projectile Motion",
  "",
  "Below are options for projectile motion on different",
  "planets:",
  "",
  "Mars",
  "",
  "Venus",
  "",
  "Mercury",
  "",
  "Jupiter",
  "",
  "Saturn",
  "",
  "Air Resistance",
  "",
  "Note: Change the playback speed of the projectile",
  "by using the up and down arrows on the keyboard."]

#starting position of the text 
start_point = [] 
#font size used for the text
font = pygame.font.Font(None, 30)

 #creates a list of surfaces for each line of text
simulation_surface = [font.render(simulation, True, pygame.Color('white')) for simulation in simulations] 

#draws the text in the output box
for i, simulation_surface in enumerate(simulation_surface):
  screen.blit(simulation_surface, (o_box.x , o_box.y  ))

#main game loop
while running:
  #converts time to seconds
  delta_t = clock.tick(60) / 1000 
  #draws the background image on screen
  screen.blit(bg, (0, 0)) 
  

  #updates the input values to what the user enters
  try:
    gravity = float(input_text[0])
    initial_velocity = float(input_text[1])
    launch_angle = math.radians(float(input_text[2]))
  except ValueError:
    #handles the case where the input text is not a valid number
    gravity = 9.81  #default value or previous valid value
    initial_velocity = 30  #default value or previous valid value
    launch_angle = math.radians(45)  #default value or previous valid value

  #event handling loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
    elif event.type == pygame.MOUSEBUTTONDOWN:
      active_box = None
      #checks for mouse clicks on input boxes
      for i, box in enumerate(input): 
        #checks if the mouse is hovering over the input box
        if box.collidepoint(event.pos): 
          #sets the active box to the current input box
          active_box = i 
          break
      #checks for mouse clicks on tickboxes
      for tickbox in tickboxes: 
        #checks if the mouse is hovering over the tickbox
        if tickbox.is_clicked(event.pos):
          #checks if the mouse is hovering over any other tickbox
          for other_tickbox in tickboxes: 
            #checks if the other tickbox is not the current tickbox
            if other_tickbox != tickbox: 
              other_tickbox.clicked = False
          #sets the gravity value to the value corresponding with that tickbox if it is clicked
        if tickboxes[0].is_clicked(event.pos):
          gravity = gravity_values[0]
          input_text[0] = str(gravity)
        elif tickboxes[1].is_clicked(event.pos):
          gravity = gravity_values[1]
          input_text[0] = str(gravity)
        elif tickboxes[2].is_clicked(event.pos):
          gravity = gravity_values[2]
          input_text[0] = str(gravity)
        elif tickboxes[3].is_clicked(event.pos):
          gravity = gravity_values[3]
          input_text[0] = str(gravity)
        elif tickboxes[4].is_clicked(event.pos):
          gravity = gravity_values[4]
          input_text[0] = str(gravity)
        elif tickboxes[5].is_clicked(event.pos):
          air_resistance = True

      #checks for clicks on start button
      if start_button.is_clicked(event.pos):
        #projectile motion will run
        proj_running = True

        #checks if the simulation is paused
        if simulation_paused: 
          #unpauses the simulation
          simulation_paused = False 
          proj_running = True
        #checks if the simulation is not paused
        else:
          proj_running = True
          time_elapsed = 0  
          proj_pos = proj_initial_pos.copy()  
          projectile_movement.clear()

      #checks if stop button is clicked
      if stop_button.is_clicked(event.pos):
        #pauses the simulation
        simulation_paused = True
        #stops projectile motion
        proj_running = False 

      #checks if exit button is clicked
      if exit_button.is_clicked(event.pos):
        #runs the menu file
        exec(open("menu.py").read())

      #checks for the event of a key being pressed
    elif event.type == pygame.KEYDOWN: 
      #checks if the box is active
      if active_box is not None: 
        #checks that no other textbox has been selected
        if not ((tickboxes[0].clicked or tickboxes[1].clicked or tickboxes[2].clicked or tickboxes[3].clicked or tickboxes[4].clicked) and active_box==0): 
          #checks if backspace is pressed
          if event.key == pygame.K_BACKSPACE: 
            #removes the ending character 
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

      #checks if the input value is a valid number
    try: 
      gravity = float(input_text[0])
    except ValueError:
        gravity = 9.81  

  #draws the buttons 
  start_button.draw(screen, font)
  stop_button.draw(screen, font)
  exit_button.draw(screen, font)
  
  #draws the input boxes on the screen based on the previous box
  for i, box in enumerate(input): 
    pygame.draw.rect(screen, input_box_color, box)
    label_surface = font.render(label[i], True, pygame.Color('white'))
    screen.blit(label_surface, (box.x, box.y - label_surface.get_height() - 5))
    text_surface = font.render(input_text[i], True, pygame.Color('black'))
    screen.blit(text_surface, (box.x + 5, box.y + 5))

  #draws the output box
  pygame.draw.rect(screen, o_box_color, o_box)

  #draws the tickboxes on the screen
  for tickbox in tickboxes: 
    tickbox.draw(screen)
    
  #draws the simulation list onto the output box
  for i, simulation in enumerate(simulations):
      text_surface = font.render(simulation, True, pygame.Color('black'))
      screen.blit(text_surface, (o_box.x , o_box.y + 5 + (len(start_point) + i) * (font.get_height() + 5)))
  
  #handles errors with inputs
  try: 
    #sets initial velocity to the users input value as afloat
    initial_velocity = float(input_text[1]) 
    #calculates the inital velocity in the horizontal and vertical directions
    initial_velocity_x = initial_velocity / math.sqrt(2)
    initial_velocity_y = initial_velocity / math.sqrt(2)

    #checks if the projectile is running
    if proj_running and not simulation_paused: 
        #increments the time elapsed by delta t multiplied by playback speed
        time_elapsed += delta_t * playback_speed  

        #checks if air resistance tickbox is clicked
        if tickboxes[5].clicked:
          #sets gravity to 9..81
          input_text[0] = "9.81"
          #creates an instance of air resistance from the air resistance class
          air_resistance = AirResistance(mass, 0.5, area, initial_velocity_x, initial_velocity_y, air_density)
          #applies air resistance
          air_resistance.update_velocity(time_elapsed)
          x_calibration = air_resistance.apply(initial_velocity * math.cos(launch_angle))
          #updates the x and y position 
          x_pos = initial_velocity * math.cos(launch_angle) * time_elapsed-((time_elapsed*10))
          y_pos = initial_velocity * math.sin(launch_angle) * time_elapsed - (0.5 * gravity * time_elapsed ** 2)
          #updates the projectiles position
          proj_pos[0] = proj_initial_pos[0] + x_pos
          proj_pos[1] = proj_initial_pos[1] - y_pos

          #checks if the projectilen has reached the ground 
          if proj_pos[1] >= proj_initial_pos[1]: 
            #projectile motion stops
            proj_running = False
            #resets the projectile to initial starting point
            proj_pos = proj_initial_pos.copy()
            #clears the list with the projectile positions stored in it
            projectile_movement.clear()
        #runs if air resistance tickbox is not clicked
        else:
          #updates the x and y position
          x_pos = initial_velocity * math.cos(launch_angle) * time_elapsed
          y_pos = initial_velocity * math.sin(launch_angle) * time_elapsed - (0.5 * gravity * time_elapsed ** 2)
          #updates the projectile's position
          proj_pos[0] = proj_initial_pos[0] + x_pos 
          proj_pos[1] = proj_initial_pos[1] - y_pos
        #appends the new position to the projectile path for tracing
        projectile_movement.append((int(proj_pos[0]), int(proj_pos[1])))
          
    #checks if the projectilen has reached the ground 
    if proj_pos[1] >= proj_initial_pos[1]: 
      proj_running = False
      proj_pos = proj_initial_pos.copy()
      projectile_movement.clear()

    #checks if the y position has exceeded 515
    elif y_pos >= 515:
        proj_running = False
          
        proj_pos = proj_initial_pos.copy()
        projectile_movement.clear()

    #checks if the x position has exceeded 1405
    elif proj_pos[0] >= 1405:
      proj_running = False

      proj_pos = proj_initial_pos.copy()
      projectile_movement.clear()
  except:pass

  #draws the projectile on the screen
  pygame.draw.circle(screen, projectile_color, (int(proj_pos[0]), int(proj_pos[1])), proj_radius)
  
  
  scientific_output[0] = gravity  #sets the value of gravity as acceleration in the y
  scientific_output[1] = math.sqrt(x_pos**2 + y_pos**2)  #calculates the displacement
  scientific_output[2] = time_elapsed  #time taken for the projectile to reach ground level
  velocity_x = initial_velocity * math.cos(launch_angle)  #calculates velocity in the x
  velocity_y = initial_velocity * math.sin(launch_angle) - (gravity * time_elapsed)  #calculates velocity in the y
  scientific_output[3] = math.sqrt(velocity_x**2 + velocity_y**2)  #calculates the current velocity

  #draws the output label and updates the values every frame
  draw_scientific_output(screen, font, output, scientific_output, input, box_spacing, box_width, box_height)


  #draws the tracer for the projectile
  if len(projectile_movement) > 1:
      pygame.draw.lines(screen, projectile_color, False, projectile_movement, 3)

  #updates the screen
  pygame.display.flip()
  #limits frame rate to 60 fps
  clock.tick(60) 

pygame.quit()
sys.exit()


