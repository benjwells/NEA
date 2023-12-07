import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Load and set the background image
background_image_path = "images/InGameScreen.png"
background = pygame.image.load(background_image_path)
background = pygame.transform.scale(background, (screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Interactive Game")

# Define the input box properties
input_box_color = pygame.Color('white')
input_box_width, input_box_height = 200, 60
input_box_margin = 20

# Define the positions of the input boxes
input_boxes = [
    pygame.Rect(220, 20, input_box_width, input_box_height),  # Gravity
    pygame.Rect(220, 20 + input_box_height + 3 * input_box_margin, input_box_width, input_box_height),  # Distance of Target
    pygame.Rect(220 + input_box_width + 2 * input_box_margin + 150, 20, input_box_width, input_box_height),  # Initial Velocity
    pygame.Rect(220 + input_box_width + 2 * input_box_margin + 150, 20 + input_box_height + 3 * input_box_margin, input_box_width, input_box_height)  # Angle
]

# Create a font object for the labels and input text
font = pygame.font.Font(None, 36)

# Define the labels
labels = ["Gravity", "Distance of Target", "Initial Velocity", "Angle"]

# Define the output labels and their initial values
output_labels = ["Acceleration", "Displacement", "Time Taken", "Current Velocity"]
output_values = [0, 0, 0, 0]  # Initial values for acceleration, displacement, time, and velocity

# Define the projectile's properties
projectile_radius = 5
projectile_color = pygame.Color('black')
# Align the projectile with the left side of the left input box and set y to 780
projectile_start_pos = [input_boxes[0].left, 780]

# List to store the positions of the projectile for the tracer
projectile_path = []

# Define the target line properties
target_length = 60
target_color = pygame.Color('red')
target_y = projectile_start_pos[1]  # Same y-coordinate as the circle's starting position

# Input box state
active_box = None
input_texts = ["9.81", "500", "30", "45"]  # Default values for gravity, distance, velocity, and angle

# Convert input texts to their respective values
gravity = float(input_texts[0])
target_distance = float(input_texts[1])
initial_velocity = float(input_texts[2])
launch_angle = math.radians(float(input_texts[3]))

# Define a variable to track the hit status
hit_status = None  # Possible values: None, "Target Hit"

# Game loop
running = True
clock = pygame.time.Clock()
time_elapsed = 0
projectile_in_motion = False
projectile_pos = projectile_start_pos.copy()

while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            active_box = None
            for i, box in enumerate(input_boxes):
                if box.collidepoint(event.pos):
                    active_box = i
                    break
        elif event.type == pygame.KEYDOWN:
            if active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_texts[active_box] = input_texts[active_box][:-1]
                else:
                    input_texts[active_box] += event.unicode
            if event.key == pygame.K_RETURN:
                gravity = float(input_texts[0])
                target_distance = float(input_texts[1])  # Directly use the input value as the distance
                initial_velocity = float(input_texts[2])
                launch_angle = math.radians(float(input_texts[3]))
                # Start the projectile's motion
                projectile_in_motion = True
                time_elapsed = 0  # Reset the time elapsed for the new launch
                projectile_pos = projectile_start_pos.copy()  # Reset the position
                projectile_path.clear()

    # Draw the input boxes, labels, and text
    for i, box in enumerate(input_boxes):
        pygame.draw.rect(screen, input_box_color, box)
        label_surface = font.render(labels[i], True, pygame.Color('white'))
        screen.blit(label_surface, (box.x - label_surface.get_width() - 10, box.y + (input_box_height - label_surface.get_height()) // 2))
        text_surface = font.render(input_texts[i], True, pygame.Color('black'))
        screen.blit(text_surface, (box.x + 5, box.y + 5))

    # Draw the target line using the updated target distance
    target_x = projectile_start_pos[0] + target_distance  # Calculate the x-coordinate based on the distance from the circle
    pygame.draw.line(screen, target_color, (target_x, target_y), (target_x + target_length, target_y), 2)

    # Draw the projectile at the starting position before motion
    pygame.draw.circle(screen, projectile_color, (int(projectile_start_pos[0]), int(projectile_start_pos[1])), projectile_radius)

    # Calculate and draw the projectile if it's in motion
    if projectile_in_motion:
        time_elapsed += dt  # Increment the time elapsed only when the projectile is in motion

        # Calculate the horizontal (x) and vertical (y) position of the projectile
        x_pos = initial_velocity * math.cos(launch_angle) * time_elapsed
        y_pos = initial_velocity * math.sin(launch_angle) * time_elapsed - (0.5 * gravity * time_elapsed ** 2)

        # Update the projectile's position
        projectile_pos[0] = projectile_start_pos[0] + x_pos
        projectile_pos[1] = projectile_start_pos[1] - y_pos

        # Add the current position to the projectile path for the tracer
        projectile_path.append((int(projectile_pos[0]), int(projectile_pos[1])))

        # Check if the projectile's y-coordinate is equal to the target's y-coordinate
        if int(projectile_pos[1]) == target_y:
            # Check if the projectile's x-coordinate is within the target's length range
            if target_x <= projectile_pos[0] <= target_x + target_length:
                hit_status = "Target Hit"
            else:
                hit_status = None  # Reset hit status if not within target range
        else:
            hit_status = None  # Reset hit status if not at the same y-coordinate

        # Stop the projectile motion if it has fallen below the starting y-coordinate or crossed past the target area
        if projectile_pos[1] >= projectile_start_pos[1] or projectile_pos[0] > target_x + target_length:
            projectile_in_motion = False
            time_elapsed = 0
            projectile_pos = projectile_start_pos.copy()
            projectile_path.clear()

        # Draw the projectile on the screen
        pygame.draw.circle(screen, projectile_color, (int(projectile_pos[0]), int(projectile_pos[1])), projectile_radius)

        # Update the output values
        output_values[0] = gravity  # Acceleration is constant and equal to gravity
        output_values[1] = math.sqrt(x_pos**2 + y_pos**2)  # Displacement from the start
        output_values[2] = time_elapsed  # Time taken since the launch
        velocity_x = initial_velocity * math.cos(launch_angle)  # Horizontal velocity component
        velocity_y = initial_velocity * math.sin(launch_angle) - (gravity * time_elapsed)  # Vertical velocity component
        output_values[3] = math.sqrt(velocity_x**2 + velocity_y**2)  # Current velocity

    # Draw the output labels and values
    for i, label in enumerate(output_labels):
        label_surface = font.render(label, True, pygame.Color('white'))
        value_surface = font.render(f"{output_values[i]:.2f}", True, pygame.Color('black'))
        # Calculate the x position based on the last input box's position and spacing
        label_x = input_boxes[-1].right + input_box_margin + (i * (input_box_width + input_box_margin))
        # Draw the label and value on the screen
        screen.blit(label_surface, (label_x, 20))
        screen.blit(value_surface, (label_x, 20 + input_box_height + input_box_margin))

    # Draw the hit status message if available
    if hit_status:
        message_surface = font.render(hit_status, True, pygame.Color('green'))
        screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height // 2 - message_surface.get_height() // 2))

    # Draw the tracer for the projectile
    if len(projectile_path) > 1:
        pygame.draw.lines(screen, projectile_color, False, projectile_path, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
