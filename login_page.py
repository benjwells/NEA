import pygame
import sqlite3
from sqlite3 import Error
import hashlib

try:
  from pygame import mixer
  mixer.init() 
  mixer.music.load("bg.mp3") 
  mixer.music.set_volume(0.7) 
  mixer.music.play()
except Exception as e:
  print(e)

pygame.init()

screen = pygame.display.set_mode((1920, 1080))

bg = pygame.image.load("images/background.png")
bg = pygame.transform.scale(bg, (1920, 1080))

input_boxes = [pygame.Rect(230, 500 + i*120 - 120, 500, 80) for i in range(3)]
colors = [pygame.Color('white') for _ in range(3)]
active_box = None

font = pygame.font.Font(r"fonts/Dungeon Depths.otf", 25) 
global texts
texts = ['Username', 'Password', 'Confirm Password']
passwords = ['', '']

signup_image = pygame.image.load("images/create_account_button.png")
login_image = pygame.image.load("images/login.png")


def hash_password(password):
  return hashlib.sha256(password.encode()).hexdigest()



class Button:
  def __init__(self, x, y, image, width, height):
    self.image = image
    self.width = width
    self.height = height
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
    self.rect = self.image.get_rect()  # Create a rect style object using the get_rect method of the image
    self.rect.topleft = (x, y) 

  def draw(self, surface):
    surface.blit(self.image, self.rect)

  def Over(self, pos):
    if self.rect.collidepoint(pos):
      return True

  def resize(self, width, height):
    self.image = pygame.transform.scale(self.image, (width, height))
    self.rect.size = self.image.get_size()
    return False

create_account_button = Button(1150, 375, signup_image, 500, 120)
login_button = Button(1150, 600, login_image, 500, 120)


class Database:
  def __init__(self, db_name):
      self.conn = self.create_connection(db_name)
      if self.conn is not None:
          self.create_table()


  def create_connection(self, db_name):
      conn = None
      try:
        conn = sqlite3.connect(db_name)  
        return conn
      except Error as e:
        print(e)
      return conn

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

  def increment_tries(self, success):
    sql = '''SELECT * FROM accounts WHERE username = ?;'''
    cur = self.conn.cursor()
    cur.execute(sql, (texts[0],))
    record = cur.fetchall()
    temp = record[0]
    record = []
    for i in temp:
      record.append(i)
  
    record[2] +=1
    if success:
      record[3] +=1
    record[4] = round((record[3]/record[2])*100)
    sql = '''UPDATE accounts SET total_tries = ?,successful_tries = ?, success_rate = ? WHERE username = ?;'''
    self.conn.execute(sql, (record[2],record[3],record[4],texts[0]))
    self.conn.commit()

  def login(self, username, password):
    if self.check_account_exists((username, password)):
      print(f"Welcome {username}!")
    else:
      print("Invalid username or password!")

  def create_account(self, account):
    username, password = account
    print(password)
    hashed_password = hash_password(password)
    sql = '''INSERT INTO accounts(username, password,total_tries,successful_tries,success_rate)
          VALUES(?, ?,0,0,0);'''
    self.conn.execute(sql, (username, hashed_password))
    self.conn.commit()

  def check_username_exists(self, username):
    sql = '''SELECT * FROM accounts WHERE username = ?'''
    cur = self.conn.cursor()
    cur.execute(sql, (username,))
    rows = cur.fetchall()
    return len(rows) > 0

  def check_account_exists(self, account):
    username, password = account
    hashed_password = Database.hash_password(password)
    sql = '''SELECT * FROM accounts WHERE username = ? AND password = ?;'''
    cur = self.conn.cursor()
    cur.execute(sql, (username, hashed_password))
    rows = cur.fetchall()
    return len(rows) > 0

  def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


account = Database('user_accounts.db')



error_message = ''
error_color = pygame.Color('red')


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        for i, box in enumerate(input_boxes):
            display_text = texts[i]
            if i > 0 and active_box != i and passwords[i - 1] == '':
              display_text = ['Password', 'Confirm Password'][i - 1]
            txt_surface = font.render(display_text, True, pygame.Color('white'))
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
        if create_account_button.Over(pygame.mouse.get_pos()):
            if texts[0] == 'Username' or passwords[0] == '':
              error_message = "Please enter a valid username or password!"
              error_color = pygame.Color('red')
            elif passwords[0] != passwords[1]:
              error_message = "Passwords do not match!"
              error_color = pygame.Color('red')
            elif not account.check_username_exists(texts[0]):
              account.create_account([texts[0], passwords[0]])
              error_message = "Account created successfully!"
              error_color = pygame.Color('green')
            else:
              error_message = "Username already exists!"
              error_color = pygame.Color('red')

        if login_button.Over(pygame.mouse.get_pos()):
          pygame.time.wait(300)
          if texts[0] == 'Username' or passwords[0] == '':
            error_message = "Please enter a valid username or password!"
            error_color = pygame.Color('red')
          elif not account.check_account_exists((texts[0], passwords[0])):
            error_message = "Sign up first!"
            error_color = pygame.Color('red')
          elif passwords[0] != passwords[1]:
            error_message = "Passwords do not match!"
            error_color = pygame.Color('red')
          else:
            exec(open("menu.py").read())
                  
                  
    if event.type == pygame.KEYDOWN:
      if active_box is not None:
        if event.key == pygame.K_BACKSPACE:
          texts[active_box] = texts[active_box][:-1]
          if active_box > 0:
            passwords[active_box - 1] = passwords[active_box - 1][:-1]
        else:
          if active_box > 0:
            passwords[active_box - 1] += event.unicode
            texts[active_box] += '*'
          else:
            texts[active_box] += event.unicode

  
  screen.fill((30, 30, 30))
  screen.blit(bg, (0, 0))
  for i, box in enumerate(input_boxes):
    txt_surface = font.render(texts[i], True, pygame.Color('white'))  
    screen.blit(txt_surface, (box.x+5, box.y+5))
    pygame.draw.rect(screen, colors[i], box, 2)
  create_account_button.draw(screen)
  login_button.draw(screen)
  
  
  error_surface = font.render(error_message, True, error_color)  
  screen.blit(error_surface, (960 - error_surface.get_width()/2, 1080 - error_surface.get_height() - 200))  
  pygame.display.flip()

