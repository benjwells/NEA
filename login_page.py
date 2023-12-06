import pygame
import sqlite3
from sqlite3 import Error
import hashlib

# Function to hash a password
def hash_password(password):
	return hashlib.sha256(password.encode()).hexdigest()

class Button:
	def __init__(self, x, y, image, width, height):
		self.image = image
		self.width = width
		self.height = height
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self, surface):
		surface.blit(self.image, self.rect)

	def isOver(self, pos):
		if self.rect.collidepoint(pos):
		  return True

	def resize(self, width, height):
		self.image = pygame.transform.scale(self.image, (width, height))
		self.rect.size = self.image.get_size()
		return False

def main():
	# Initialize Pygame
	pygame.init()

	# Set the dimensions of the window
	screen_width, screen_height = 1920, 1080
	screen = pygame.display.set_mode((screen_width, screen_height))

	# Load the background image
	background_image_path = "images/background.png"
	background = pygame.image.load(background_image_path)
	background = pygame.transform.scale(background, (screen_width, screen_height))

	# Create the input boxes
	box_width, box_height = 500, 80  # Increased box size
	margin = 40  # Increased margin
	input_boxes = [pygame.Rect(screen_width/4 - box_width/2, screen_height/2 + i*box_height + i*margin - 1.5*box_height - margin, box_width, box_height) for i in range(3)]
	colors = [pygame.Color('white') for _ in range(3)]
	active_box = None

	# Create a font object
	font = pygame.font.Font(r"fonts/Dungeon Depths.otf", 25)  # Increased font size

	# Create a list to hold the text in each box
	texts = ['Username', 'Password', 'Confirm Password']
	passwords = ['', '']

	# Load the button images
	create_account_image = pygame.image.load("images/create_account_button.png")
	login_image = pygame.image.load("images/login.png")

	# Create the buttons
	button_width, button_height = 500, 120  # Increased button width
	create_account_button = Button(screen_width*3/4 - button_width/2, screen_height/2 - 1.5*button_height, create_account_image, button_width, button_height)
	login_button = Button(screen_width*3/4 - button_width/2, screen_height/2 + 0.5*button_height, login_image, button_width, button_height)

	# Function to create a connection to the SQLite database
	def create_connection():
		conn = None
		try:
			conn = sqlite3.connect('user_accounts.db')  # Creates a database in memory
			return conn
		except Error as e:
			print(e)
		return conn

	# Function to create a table in the database to store user accounts
	def create_table(conn):
		try:
			sql = '''CREATE TABLE accounts (
						username TEXT NOT NULL,
						password TEXT NOT NULL
					);'''
			conn.execute(sql)
		except Error as e:
			print(e)

	# Function to insert a new account into the accounts table
	def create_account(conn, account):
		username, password = account
		hashed_password = hash_password(password)
		sql = '''INSERT INTO accounts(username, password)
				  VALUES(?, ?);'''
		conn.execute(sql, (username, hashed_password))
		conn.commit()

	# Function to check if a username already exists in the database
	def check_username_exists(conn, username):
		sql = '''SELECT * FROM accounts WHERE username = ?;'''
		cur = conn.cursor()
		cur.execute(sql, (username,))
		rows = cur.fetchall()
		return len(rows) > 0

	# Function to check if an account exists in the database
	def check_account_exists(conn, account):
		username, password = account
		hashed_password = hash_password(password)
		sql = '''SELECT * FROM accounts WHERE username = ? AND password = ?;'''
		cur = conn.cursor()
		cur.execute(sql, (username, hashed_password))
		rows = cur.fetchall()
		return len(rows) > 0

	# Create a connection to the database and create the table
	conn = create_connection()
	if conn is not None:
		create_table(conn)
	else:
		print("Error! Cannot create the database connection.")

	# Variable to hold the error message
	error_message = ''
	error_color = pygame.Color('red')

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				for i, box in enumerate(input_boxes):
					display_text = texts[i]
					if i > 0 and active_box != i and passwords[i - 1] == '':  # If it's a password or confirm password box and it's not active and it's empty
						display_text = ['Password', 'Confirm Password'][i - 1]
					txt_surface = font.render(display_text, True, pygame.Color('white'))  # Text color is white
					screen.blit(txt_surface, (box.x+5, box.y+5))
					pygame.draw.rect(screen, colors[i], box, 2)
					if box.collidepoint(event.pos):
						active_box = i
						colors[i] = pygame.Color('darkgreen')
						if texts[i] in ['Username', 'Password', 'Confirm Password']:
							texts[i] = ''
					else:
						colors[i] = pygame.Color('white')
						if texts[i] == '':
							texts[i] = ['Username', 'Password', 'Confirm Password'][i]
				if create_account_button.isOver(pygame.mouse.get_pos()):
					if texts[0] == 'Username' or passwords[0] == '':  # Check if the username field is empty
						error_message = "Please enter a valid username or password!"
						error_color = pygame.Color('red')
					elif passwords[0] == passwords[1]:  # If the password and confirm password fields match
						if not check_username_exists(conn, texts[0]):  # If the username does not already exist
							create_account(conn, (texts[0], passwords[0]))  # Create the account
							error_message = "Account created successfully!"
							error_color = pygame.Color('green')
						else:
							error_message = "Username already exists!"
							error_color = pygame.Color('red')
					else:
						error_message = "Passwords do not match!"
						error_color = pygame.Color('red')

				if login_button.isOver(pygame.mouse.get_pos()):
					pygame.time.wait(300)  # Wait for 300 milliseconds
					if texts[0] == 'Username' or passwords[0] == '':  # Check if the username or password field is empty
						error_message = "Please enter a valid username or password!"
						error_color = pygame.Color('red')
					elif check_account_exists(conn, (texts[0], passwords[0])):  # If the account exists
						# Open a new window with 'menu.py'
						exec(open("menu.py").read())
					else:
						error_message = "Sign up first!"
						error_color = pygame.Color('red')
			if event.type == pygame.KEYDOWN:
				if active_box is not None:
					if event.key == pygame.K_BACKSPACE:
						texts[active_box] = texts[active_box][:-1]
						if active_box > 0:  # If it's a password or confirm password box
							passwords[active_box - 1] = passwords[active_box - 1][:-1]
					else:
						if active_box > 0:  # If it's a password or confirm password box
							passwords[active_box - 1] += event.unicode
							texts[active_box] += '*'
						else:  # If it's the username box
							texts[active_box] += event.unicode

		screen.fill((30, 30, 30))
		screen.blit(background, (0, 0))
		for i, box in enumerate(input_boxes):
			txt_surface = font.render(texts[i], True, pygame.Color('white'))  # Text color is white
			screen.blit(txt_surface, (box.x+5, box.y+5))
			pygame.draw.rect(screen, colors[i], box, 2)
		create_account_button.draw(screen)
		login_button.draw(screen)

		# Render the error message
		error_surface = font.render(error_message, True, error_color)  # Error color is red
		screen.blit(error_surface, (screen_width/2 - error_surface.get_width()/2, screen_height - error_surface.get_height() - 200))  # Moved the text a little higher

		pygame.display.flip()

if __name__ == "__main__":
	main()
