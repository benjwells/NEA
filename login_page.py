import pygame
import sqlite3
from sqlite3 import Error
import hashlib


try:
  #imports the mixer module from pygame
  from pygame import mixer 
  #initializes the mixer module
  mixer.init() 
  #loads the sound file (bg.mp3 is a placeholder)
  mixer.music.load("bg.mp3") 
  #sets the volume
  mixer.music.set_volume(0.7) 
  #plays the sound
  mixer.music.play()
except Exception as e:
  print(e)

pygame.init()

#sets the width and height of the screen
screen = pygame.display.set_mode((1920, 1080))

#loads background image
bg = pygame.image.load("images/background.png")
#scales the background to dimensions
bg = pygame.transform.scale(bg, (1920, 1080))

#creates a list of input boxes
input_boxes = [pygame.Rect(230, 500 + i*120 - 120, 500, 80) for i in range(3)] 
#creates a list of colours
colors = [pygame.Color('white') for _ in range(3)]
#variable used to determine which input box the mouse is over
active_box = None

#sets the font of the text
font = pygame.font.Font(r"fonts/Dungeon Depths.otf", 25) 
global texts
#creates a list of texts that will be displayed in the input boxes intially
texts = ['Username', 'Password', 'Confirm Password']
#creates a list of text that will be displayed in the password boxes
passwords = ['', '']

#loads images for the buttons
signup_image = pygame.image.load("images/create_account_button.png")
login_image = pygame.image.load("images/login.png")

#class to create buttons
class Button:
  def __init__(self, x, y, image, width, height):
    self.image = image
    self.width = width
    self.height = height
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
    self.rect = self.image.get_rect() 
    self.rect.topleft = (x, y) 

  #function to draw the button on the screen
  def draw(self, surface):
    surface.blit(self.image, self.rect)

  #function to check if the mouse is over the button
  def Over(self, pos):
    if self.rect.collidepoint(pos):
      return True

  #function to scale the button image to the desired dimensions
  def resize(self, width, height):
    self.image = pygame.transform.scale(self.image, (width, height))
    self.rect.size = self.image.get_size()
    return False

#creates two instances of buttons with the desired coordinates and images
create_account_button = Button(1150, 375, signup_image, 500, 120)
login_button = Button(1150, 600, login_image, 500, 120)

#class to create the database
class Database:
  def __init__(self, db_name):
      self.conn = self.create_connection(db_name)
      if self.conn is not None:
          self.create_table()

  #function that creates a connection to the database
  def create_connection(self, db_name): 
      conn = None
      try:
        conn = sqlite3.connect(db_name)  
        return conn
      except Error as e:
        print(e)
      return conn

  #creates a table of values listed below in the database
  def create_table(self): 
    try:
        sql = '''CREATE TABLE accounts (
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            total_tries INTEGER DEFAULT 0,
            successful_tries INTEGER DEFAULT 0,
            success_rate REAL DEFAULT 0.0
        );'''
        self.conn.execute(sql)
    except Error as e:
      print(e)

  #
  def increment_tries(self, success): 
    #selects all fields from the accounts table where the username is equal to the input
    sql = '''SELECT * FROM accounts WHERE username = ?;'''
    cur = self.conn.cursor()
    cur.execute(sql, (texts[0],))
    
    #fetches all the records returned
    record = cur.fetchall()
    
    #stores record[0] in a temporary variable
    temp = record[0]
    
    #an empty list to store the fields
    record = []
   
    #appends each field to the record list
    for i in temp:
      record.append(i)

    #increments the total_tries field by 1
    record[2] +=1
    #checks if the user was successful in their attempt
    if success:
      #increments the successful_tries field by 1
      record[3] +=1
    #calculates the success rate as a percentage
    record[4] = round((record[3]/record[2])*100)

    #the new values are updated
    sql = '''UPDATE accounts SET total_tries = ?,successful_tries = ?, success_rate = ? WHERE username = ?;'''
    #executes the sql statement with the new values as parameters
    self.conn.execute(sql, (record[2],record[3],record[4],texts[0]))
    self.conn.commit()

  #function to control logins
  def login(self, username, password): 
    #checks whether the account already exists in the database
    if self.check_account_exists((username, password)):
      print(f"Welcome {username}!")
    #error message if the account does exist
    else:
      print("Invalid username or password!")

  #function to control sign ups
  def create_account(self, account):
    #unpacks the account tuple
    username, password = account 
    print(password)
    #hashes the password using the hash password function
    hashed_password = hash_password(password)
    #inserts the account details into the database setting the total_tries, successful_tries and success_rate to 0
    sql = '''INSERT INTO accounts(username, password,total_tries,successful_tries,success_rate)
          VALUES(?, ?,0,0,0);'''
    #executes the sql statement with the new values as parameters
    self.conn.execute(sql, (username, hashed_password))
    self.conn.commit()

  #function to check if the account already exists
  def check_username_exists(self, username):
    #selects all fields from the accounts table where the username is equal to the input
    sql = '''SELECT * FROM accounts WHERE username = ?'''
    cur = self.conn.cursor()
    cur.execute(sql, (username,))
    rows = cur.fetchall()
    return len(rows) > 0

  #function to check if the account already exists
  def check_account_exists(self, account):
    #unpacks the account tuple
    username, password = account
    #hashes the password using the hash password function
    hashed_password = Database.hash_password(password) 
    #selects all fields from the accounts table where the username and password are equal to the input
    sql = '''SELECT * FROM accounts WHERE username = ? AND password = ?;'''
    cur = self.conn.cursor()
    cur.execute(sql, (username, hashed_password))
    rows = cur.fetchall()
    return len(rows) > 0

  #functions for hashing passwords
  def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#creates an instance of the database
account = Database('user_accounts.db')


#sets the error message
error_message = ''
#sets the colour of the error message
error_color = pygame.Color('red')

#main game loop
while True: 
  #event handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    #checks if the mouse is clicked
    if event.type == pygame.MOUSEBUTTONDOWN:
      #checks if the mouse is over any of the input boxes
      for i, box in enumerate(input_boxes): 
        #sets the text to be displayed in the input box
        display_text = texts[i] 
        #checks that the selected input box is not the password boxes and the password boxes are empty
        if i > 0 and active_box != i and passwords[i - 1] == '': 
          #if that is true, the texts below are shown in the password and confirm password boxes
          display_text = ['Password', 'Confirm Password'][i - 1] 
        #renders the text on surface
        txt_surface = font.render(display_text, True, pygame.Color('white'))
        #draws the text onto the screen
        screen.blit(txt_surface, (box.x+5, box.y+5))
        #draws the boxes on the screen as rectangles
        pygame.draw.rect(screen, colors[i], box, 2)
        #checks if the mouse is over the input boxes
        if box.collidepoint(event.pos):
          #sets the active box to the current input box
          active_box = i
          #changes the colour to dark green
          colors[i] = pygame.Color('darkgreen')
          if texts[i] in ['Username', 'Password', 'Confirm Password']:
            texts[i] = ''
        #checks if the mouse is not over the input boxes
        else:
          #the colour of the input box is set to white
          colors[i] = pygame.Color('white')
          #checks if the text for the active box is empty
          if texts[i] == '':
            #the boxes are labelled with the text below
            texts[i] = ['Username', 'Password', 'Confirm Password'][i]
      #checks if the mouse is over the create account button
      if create_account_button.Over(pygame.mouse.get_pos()):
        #checks if the username and password boxes are not empty
        if texts[0] == 'Username' or passwords[0] == '':
          #an error message is displayed in red
          error_message = "Please enter a valid username or password!"
          error_color = pygame.Color('red')
        #checks if the passwords match
        elif passwords[0] != passwords[1]:
          #error message is displayed in red
          error_message = "Passwords do not match!"
          error_color = pygame.Color('red')
        #checks if the username already exists
        elif not account.check_username_exists(texts[0]):
          #if it doesn't it is added to the database
          account.create_account([texts[0], passwords[0]])
          #error message is shown on screen in green
          error_message = "Account created successfully!"
          error_color = pygame.Color('green')
        #checks if the username already exists
        else:
          #displays an error mmessage in red
          error_message = "Username already exists!"
          error_color = pygame.Color('red')

      #checks if the mouse is over the login button
      if login_button.Over(pygame.mouse.get_pos()):
        #waits 300ms
        pygame.time.wait(300)
        #checks if the username and password boxes are not empty
        if texts[0] == 'Username' or passwords[0] == '':
          #error message is displayed in red
          error_message = "Please enter a valid username or password!"
          error_color = pygame.Color('red')
        #checks if the account exists
        elif not account.check_account_exists((texts[0], passwords[0])):
          #if not error message is displayed in red
          error_message = "Sign up first!"
          error_color = pygame.Color('red')
        #checks if the passwords match
        elif passwords[0] != passwords[1]:
          #if not error message is displayed in red
          error_message = "Passwords do not match!"
          error_color = pygame.Color('red')
        #if they match, the menu file is run
        else:
          exec(open("menu.py").read())
                  
    #checks if keys are pressed              
    if event.type == pygame.KEYDOWN:
      if active_box is not None:
        #checks if the key is backspace
        if event.key == pygame.K_BACKSPACE:
          texts[active_box] = texts[active_box][:-1] 
          #checks if the characters in the active box are more than 0
          if active_box > 0
            #if they are, it removes the last character from the active box
            passwords[active_box - 1] = passwords[active_box - 1][:-1] 
        #if any other key is pressed, it will be added to the active box
        else:
          if active_box > 0:
            passwords[active_box - 1] += event.unicode 
            texts[active_box] += '*'
          else:
            texts[active_box] += event.unicode


  #sets the background colour to grey
  screen.fill((30, 30, 30)) 
  #draws the background image on screen
  screen.blit(bg, (0, 0))

  #draws the input boxes on the screen
  for i, box in enumerate(input_boxes):
    txt_surface = font.render(texts[i], True, pygame.Color('white'))  
    screen.blit(txt_surface, (box.x+5, box.y+5))
    pygame.draw.rect(screen, colors[i], box, 2)

  #draws the buttons on screen using the function from the class
  create_account_button.draw(screen)
  login_button.draw(screen)
  
  #renders the error message
  error_surface = font.render(error_message, True, error_color) 
  #draws the error message on the screen
  screen.blit(error_surface, (960 - error_surface.get_width()/2, 1080 - error_surface.get_height() - 200))  
  #updates the screen
  pygame.display.flip()

