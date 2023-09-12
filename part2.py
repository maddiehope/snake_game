# SNAKE GAME
# March 2023
# Maddie Hope 

# * 2D movement of the snake across the x-y plane controlled by M5-Stick movement using the accelerometer.
# * The snake must move around and collect all the food to get as long as possible.
# * Running into the food allows the snake to collect it- each food adds one length and causes snake to 'sparkle'.
# * If the snake runs into its own tail or the window boundaries, it dies & the game ends.
# * You can customize and change the color of your snake if you press the M5 stick button.
# * Each time the snake eats food & grows longer, 10 points is added to the final score. 

# Snake Game inspired by: https://www.edureka.co/blog/snake-game-with-pygame/ 
# -------------------------------------------------------------------------------------------------------

import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import time
import struct
import random
import pygame 
import math


# PYGAME CONFIG PARAMS --------------------------

pygame.init()
running = True

sysfont = pygame.font.get_default_font()

clock = pygame.time.Clock()

surface_width = 600 # window width
surface_height = 600 # window height

snake_x, snake_y = surface_width//2  , (surface_height//2)-30 # initial snake pos (center)
snake_body = [(snake_x, snake_y)]
snake_block = 10 # size of each length of the snake square
snake_length = 1 # initial length of snake (one block)
snake_list = []
snake_speed = 15

food_x, food_y = 0, 0 # initial food pos

score = 0 # initial score
high_score = 0 # resets every time the game is closed

# window config
main_surface= pygame.display.set_mode([surface_width,surface_height]) # size of window 
pygame.display.set_caption('Snake Game') # window title

# text config
font = pygame.font.SysFont(None, 16)

# noise config
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat_sound.wav")

# apple image
apple_image = pygame.image.load('apple.png')
apple_surface = pygame.transform.scale(apple_image, (snake_block, snake_block)) # scaling 

# color config 
RED = (255,69,0)
ORANGE = (255,140,0)
YELLOW = (255,215,0)
BLUE = (32,255,170)
PURPLE = (147,112,219)
BLACK = (0,0,0)
WHITE = (255,255,255)
colors = [BLACK, RED, ORANGE, YELLOW, BLUE, PURPLE, WHITE]
snake_color = BLACK # initial snake color is black

# FUNCTIONS -------------------------------------

# generating random food position
def generate_food():
  global food_x 
  global food_y
  global snake_block

  food_x = round(random.randrange(0, surface_width - snake_block) / 10.0) * 10.0
  food_y = round(random.randrange(0, surface_height - snake_block) / 10.0) * 10.0

  global apple_surface
  apple_surface = pygame.transform.scale(apple_image, (snake_block*3, snake_block*3))

# update snake position
def update_snake(accel_x, accel_y, grow):
    global snake_x, snake_y

    # move the head of the snake
    snake_x += int(accel_x * snake_block)
    snake_y += int(accel_y * snake_block)

    if grow:
      snake_body.append((snake_x, snake_y))

def draw_snake(snake_block, snake_list, sparkle=False):
    global colors
    global snake_color

    if sparkle:
        offset = 3 # offset between each rectangle in the sparkle effect
        for x in snake_list:
            for i, color in enumerate(colors):
                rect = pygame.Rect(x[0]+i*offset, x[1]+i*offset, snake_block, snake_block)
                pygame.draw.rect(main_surface, color, rect)
    else:
        for x in snake_list:
            pygame.draw.rect(main_surface, snake_color, [x[0], x[1], snake_block, snake_block])

def change_color():
  global colors
  global snake_color

  index_of_curr = colors.index(snake_color)
  new = index_of_curr+1

  if new > (len(colors)-1): # once we get to the last element in the list
    new = 0

  snake_color = colors[new]

# checking if the snake ate the food
def food_collision(snake_x, snake_y):
    global snake_length
    global food_x, food_y
    global score

    distance = math.sqrt((snake_x - food_x)**2 + (snake_y - food_y)**2)

    if distance < 20:
        snake_length += 1
        score += 10

        generate_food()
        update_snake(0, 0, True)
        draw_snake(snake_block, snake_list, True) # draw the snake with sparkle effect
        eat_sound.play() # sound effect

        main_surface.blit(apple_surface, (food_x, food_y)) # draw apple image
    else:
        draw_snake(snake_block, snake_list) # draw the snake normally        
        main_surface.blit(apple_surface, (food_x, food_y)) # draw apple image

def message(msg, color):
  global score
  global high_score
  global snake_length
  global snake_x, snake_y
  global snake_list
  global food_x, food_y
  global img

  if score > high_score:
    high_score = score

  main_surface.fill((255,255,255))
  mesg = font.render(f"{msg} Press Q-Quit or C-Play Again", True, color)
  score_mesg = font.render(f"High score: {high_score}", True, color)

  main_surface.blit(mesg, [surface_width/4, surface_height/2])
  main_surface.blit(score_mesg, [(surface_width/2)-35, (surface_height/2)+20])

  # resetting snake params
  snake_length = 1
  snake_x, snake_y = surface_width//2 , (surface_height//2) - 30
  snake_list = []
  
def reset_score():
  global score
  score = 0

  pygame.display.update()
  # -----------------------------------------------

# CONNECTING TO DEVICE THROUGH BLE ----------------------------------------------------------------------

async def run():
  print("Searching devices...")
  devices = await BleakScanner.discover()

  def notification_callback(sender,payload):
    print(sender, payload)

  # Bleak connection aided by https://github.com/naoki-sawada/m5stack-ble/blob/master/client/main.py 
  device = list(filter(lambda d: d.name == "M5StickCPlus-Maddie", devices))
  if len(device) == 0:
    print("Device 'M5StickCPlus-Maddie' NOT found.")
  else:
    print("Device 'M5StickCPlus-Maddie' found.")

    address = device[0].address
    async with BleakClient(address) as client:
      print("Connecting to device...")

      # PYGAME ------------------------------------------------------------------------------------ 

      running = True
      game_over = False
      game_over_message = ""
      generate_food()

      pygame.key.set_repeat(50, 50) # enabling key repeat events

      while running:

        while game_over == True:

          for event in pygame.event.get():

            if event.type == pygame.QUIT: # this happens when the window is closed
              running = False 
              game_over = False

            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_q):
              running = False
              game_over = False

            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_c):
              reset_score()
              running = True
              game_over = False

        # getting accelerometer data 
        accelerometer_data_bytes = await client.read_gatt_char("5e8be540-13b8-49bf-af35-63b725c5c066")
        accel_x, accel_y, accel_z = struct.unpack('<fff', accelerometer_data_bytes[:12]) # note accel_z is unused

        # getting button data
        button_data_bytes = await client.read_gatt_char("e672f43d-ee01-4e48-bf96-4e772413c930")
        button_press = struct.unpack('<b', button_data_bytes[:1])
        if button_press == (1,):
          print("button press recieved")
          change_color()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: # this happens when the window is closed
                running = False 

        update_snake(accel_x, accel_y, False)
        main_surface.fill((143,188,139))

        if snake_x >= surface_width or snake_x < 0 or snake_y >= surface_height or snake_y < 0:
          game_over_message = "You ran into the wall!"
          message(game_over_message, (255,0,0))
          game_over = True # ending game if snake runs into wall

        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
 
        for x in snake_list[:-1]: 
            if x == snake_head:
              game_over_message = "You ran into your tail!"
              message(game_over_message, (255,0,0))
              game_over = True # ending game if snake runs into itself 
 
        draw_snake(snake_block, snake_list)
        food_collision(snake_x, snake_y)

        # score update
        img = font.render(f'Score: {score} points', True, (255,0,0)) # text
        main_surface.blit(img, (10, 10))

        pygame.display.update()
        clock.tick(snake_speed)

      pygame.quit()

      # -------------------------------------------------------------------------------------------

asyncio.run(run())