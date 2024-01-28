import pygame
import sys
import math
import sqlite3
from login_page import Database


# Initialize Pygame
pygame.init()
font = pygame.font.Font(None, 30)
font_loading = pygame.font.Font(None, 50)

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Interactive Game")

bg = pygame.image.load("images/InGameScreen.png")
bg = pygame.transform.scale(bg, (1920, 1080))

def hash_password(password):
  return hashlib.sha256(password.encode()).hexdigest()

loading_text = font_loading.render("Loading...", True, pygame.Color('white'))

screen.blit(loading_text, (1920/2 - loading_text.get_width()/2,
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

  pygame.draw.rect(screen, pygame.Color('white'), outline_rect, 2)
  pygame.draw.rect(screen, pygame.Color('white'), filled_rect)

  pygame.display.flip()


box_colour = pygame.Color('white')
box_margin = 20
box_width = 200
box_height = 60
input = [
    pygame.Rect(220, 20, 200, 60),  
    pygame.Rect(220, 150, 200, 60),  
    pygame.Rect(610, 20, 200, 60), 
    pygame.Rect(610, 150, 200, 60),
    pygame.Rect(1440, 530, 480, 250)
]

label = ["Gravity", "Distance of Target", "Initial Velocity", "Angle",""]


output = ["Acceleration (y)", "Displacement", "Time Taken", "Current Velocity"]
scientific_output = [9.81, 0, 0, 30] 

proj_radius = 7.5
projectile_color = pygame.Color('black')

proj_initial_pos = [220, 780]

projectile_movement = []

target_width = 70
target_color = pygame.Color('black')
target_y = 780  

# Input box state
active_box = None
input_text = ["9.81", "500", "30", "45",""]  

# Convert input texts to their respective values
gravity = float(input_text[0])
target_distance = float(input_text[1])
initial_velocity = float(input_text[2])
launch_angle = math.radians(float(input_text[3]))
info_box = str(input_text[4])


# Define a variable to track the hit status
hit = None  # Possible values: None, "Target Hit"

# Define a Button class
class Button:
  def __init__(self, x, y, width, height, text):
      self.rect = pygame.Rect(x, y, width, height)
      self.text = text


  def draw(self, screen, font):
      # Draw the button rectangle
      pygame.draw.rect(screen, self.color, self.rect)
      # Render the text
      text_surface = font.render(self.text, True, pygame.Color('white'))
      # Get the text rectangle
      text_rect = text_surface.get_rect(center=self.rect.center)
      # Blit the text onto the screen
      screen.blit(text_surface, text_rect)

  def is_clicked(self, pos):
      # Return True if the button is clicked
      return self.rect.collidepoint(pos)

# Create buttons
start_button = Button(1000, 150, 300, 50, 'Start')
stop_button = Button(1400, 150, 300, 50, 'Stop')
exit_button = Button(1500, 825, 300, 50, 'Return to Mode Selection')
stop_button.color = pygame.Color('red')
start_button.color = pygame.Color('green')
exit_button.color = pygame.Color('Black')
# Add a variable to track the paused state
simulation_paused = False

# Define a function to draw the output label and values
def draw_scientific_output(screen, font, output, scientific_output, input, box_margin, box_width, box_height):
    for i, label in enumerate(output):
        label_surface = font.render(label, True, pygame.Color('white'))
        value_surface = font.render(f"{scientific_output[i]:.2f}", True, pygame.Color('black'))
        # Calculate the x position based on the last input box's position and spacing
        label_x = input[-1].right + 20 + (i * (200 + 20))-900
        # Draw the label and value on the screen
        screen.blit(label_surface, (label_x, 20))
        screen.blit(value_surface, (label_x, 20 + 60 + 20))

playback_speed = 1 

running = True
clock = pygame.time.Clock()
time_elapsed = 0
proj_running = False
proj_pos = proj_initial_pos.copy()

# Initialize x_pos and y_pos with default values
x_pos = 0
y_pos = 0

# Define the properties of the output box
o_box_color = pygame.Color('white')
o_200, o_60 = 550, 540  # You can adjust these values as needed
o_box = pygame.Rect(1400, 250, o_200, o_60)  
o_surface = pygame.Surface((o_200, o_60))  # Create a surface for the output box
o_surface.fill(o_box_color)  # Fill the surface with the output box color
screen.blit(o_surface, (o_box.x, o_box.y)) 


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
    "Time: t = (v - u) / a",]

start_point = []
count = 0
suc_count = 0

equation_surface = [font.render(equation, True, pygame.Color('white')) for equation in equations]
for i, equation_surface in enumerate(equation_surface):
    screen.blit(equation_surface, (o_box.x , o_box.y  ))

while running:
  delta_t = clock.tick(60) / 1000  
  screen.blit(bg, (0, 0))

  # Update the values based on the input texts
  try:
      gravity = float(input_text[0])
      target_distance = float(input_text[1])
      initial_velocity = float(input_text[2])
      launch_angle = math.radians(float(input_text[3]))
  except ValueError:
      # Handle the case where the input text is not a valid number
      gravity = 9.81  # Default value or previous valid value
      target_distance = 500  # Default value or previous valid value
      initial_velocity = 30  
      launch_angle = math.radians(45)  

  error_grav = font.render("Gravity must be between 2 and 15", True, pygame.Color('red'))

  error_target = font.render("Target distance must be between 200 and 1119", True, pygame.Color('red'))

  error_ivel = font.render("Initial velocity must be between 30 and 150", True, pygame.Color('red'))

  error_angle = font.render("Launch angle must be between 0 and 89", True, pygame.Color('red'))

  if gravity < 2 or gravity > 15 or input_text[0] == "":
    screen.blit(error_grav, (135, 100))
    proj_running = False

  elif target_distance < 200 or target_distance > 1119 or input_text[1] == "":
    screen.blit(error_target, (50, 220))
    proj_running = False

  elif initial_velocity < 30 or initial_velocity > 150 or input_text[2] == "":
    screen.blit(error_ivel, (450, 100))
    proj_running = False

  elif launch_angle <= math.radians(0) or launch_angle > math.radians(89) or input_text[3] == "":
    screen.blit(error_angle, (450, 220))
    proj_running = False



  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
          if start_button.is_clicked(event.pos):
            hit = None
              # Toggle the paused state and resume motion if paused
            if simulation_paused:
                simulation_paused = False
                proj_running = True
            else:
                  # Start the projectile's motion only if it's not already in motion
                if not proj_running:
                    proj_running = True

                    proj_pos = proj_initial_pos.copy()  # Reset the position
                    projectile_movement.clear()
          if stop_button.is_clicked(event.pos):
              # Pause the simulation
              simulation_paused = True
              proj_running = False  # Stop the projectile's motion
          active_box = None
          for i, box in enumerate(input):
              if box.collidepoint(event.pos):
                  active_box = i
                  break
          if exit_button.is_clicked(event.pos):
            #Exit program
            
            exec(open("menu.py").read())
      elif event.type == pygame.KEYDOWN:
          if active_box is not None:
              if event.key == pygame.K_BACKSPACE:
                  input_text[active_box] = input_text[active_box][:-1]
              else:
                  input_text[active_box] += event.unicode
          # Add these lines to handle the up and down arrow keys
          if event.key == pygame.K_UP:
              playback_speed *= 2  # Double the playback speed
              if playback_speed > 8:
                playback_speed = 8
          if event.key == pygame.K_DOWN:
              playback_speed /= 2  # Halve the playback speed
              if playback_speed < 0.1:  # prevent playback_speed from going too low
                  playback_speed = 0.1

  start_button.draw(screen, font)
  stop_button.draw(screen, font)
  exit_button.draw(screen, font)
  for i, box in enumerate(input):
      pygame.draw.rect(screen, box_colour, box)
      label_surface = font.render(label[i], True, pygame.Color('white'))
      screen.blit(label_surface, (box.x - label_surface.get_width() - 10, box.y + (60 - label_surface.get_height()) // 2))
      text_surface = font.render(input_text[i], True, pygame.Color('black'))
      screen.blit(text_surface, (box.x + 5, box.y + 5))

  # Draw the output box
  pygame.draw.rect(screen, o_box_color, o_box)

  # Draw the equations in the output box below the calculations
  for i, equation in enumerate(equations):
      text_surface = font.render(equation, True, pygame.Color('black'))
      screen.blit(text_surface, (o_box.x , o_box.y + 5 + (len(start_point) + i) * (font.get_height() + 5)))


  # Draw the target line using the updated target distance
  target_x = proj_initial_pos[0] + target_distance  # Calculate the x-coordinate based on the distance from the circle
  pygame.draw.line(screen, target_color, (target_x, target_y), (target_x + target_width, target_y), 2)


  if proj_running and not simulation_paused:
    time_elapsed += delta_t * playback_speed  # Increment the time elapsed by dt * playback_speed

    # Calculate the horizontal (x) and vertical (y) position of the projectile
    x_pos = initial_velocity * math.cos(launch_angle) * time_elapsed
    y_pos = initial_velocity * math.sin(launch_angle) * time_elapsed - (0.5 * gravity * time_elapsed ** 2)

    # Update the projectile's position
    proj_pos[0] = proj_initial_pos[0] + x_pos
    proj_pos[1] = proj_initial_pos[1] - y_pos

    # Add the new position to the projectile path for tracing
    projectile_movement.append((int(proj_pos[0]), int(proj_pos[1])))

      
    
    if proj_pos[1] >= proj_initial_pos[1]:
        if target_x <= proj_pos[0] <= target_x + target_width:
            hit = "Target Hit"
            suc_count += 1
            account.increment_tries(True)
            
        else:
            hit = "Target Missed"
            account.increment_tries(False)
        proj_running = False
        time_elapsed = 0
        proj_pos = proj_initial_pos.copy()
        projectile_movement.clear()
        count += 1
       
    
    elif y_pos >= 515:
        hit = "Target Missed"
        proj_running = False
        time_elapsed = 0
        proj_pos = proj_initial_pos.copy()
        projectile_movement.clear()
        count += 1
        
    
    elif proj_pos[0] >= 1405:
      hit = "Target Missed"
      proj_running = False
      time_elapsed = 0
      proj_pos = proj_initial_pos.copy()
      projectile_movement.clear()
      count += 1
      

  # Draw the projectile on the screen
  pygame.draw.circle(screen, projectile_color, (int(proj_pos[0]), int(proj_pos[1])), proj_radius)

  scientific_output[0] = gravity  # Acceleration is constant and equal to gravity
  scientific_output[1] = math.sqrt(x_pos**2 + y_pos**2)  # Displacement from the start
  scientific_output[2] = time_elapsed  # Time taken since the launch
  velocity_x = initial_velocity * math.cos(launch_angle)  # Horizontal velocity component
  velocity_y = initial_velocity * math.sin(launch_angle) - (gravity * time_elapsed)  # Vertical velocity component
  scientific_output[3] = math.sqrt(velocity_x**2 + velocity_y**2)  # Current velocity

  # Draw the output label and values every frame
  draw_scientific_output(screen, font, output, scientific_output, input, 20, 200, 60)

  # Draw the hit status message if available
  if hit == "Target Missed":
    message_surface = font.render(hit, True, pygame.Color('red'))
    screen.blit(message_surface, (1920 // 2 - message_surface.get_width() // 2, 1080 // 2 - message_surface.get_height() // 2))
  elif hit == "Target Hit":
    message_surface1 = font.render(hit, True, pygame.Color('green'))
    screen.blit(message_surface1, (1920 // 2 - message_surface1.get_width() // 2, 1080 // 2 - message_surface1.get_height() // 2))

  # Draw the tracer for the projectile
  if len(projectile_movement) > 1:
      pygame.draw.lines(screen, projectile_color, False, projectile_movement, 3)


  pygame.display.flip()
  clock.tick(60)

pygame.quit()
sys.exit()
