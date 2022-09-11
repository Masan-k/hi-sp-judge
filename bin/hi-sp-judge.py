import pygame
import pygame.locals
import sys
from pynput import keyboard

SCREEN_SIZE = (800, 600)

FIELD_WIDTH = 600
FIELD_HEIGHT = 400

INIT_X = 100
INIT_Y = 100

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("HI-SP-JUDGE")

p_radius = 10
p1_pos = [200,200]
p2_pos = [400,200]
pressKeyMode = "" 
P_MOVE_SPEED = 8 
pressKeyPlayer = ""

while True:
  screen.fill((0,0,0))
  #コートの描画
  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y), (INIT_X + FIELD_WIDTH, INIT_Y))
  pygame.draw.line(screen, (255,255,255), (INIT_X + FIELD_WIDTH, INIT_Y), (INIT_X + FIELD_WIDTH, INIT_Y + FIELD_HEIGHT))
  pygame.draw.line(screen, (255,255,255), (INIT_X + FIELD_WIDTH, INIT_Y + FIELD_HEIGHT), (INIT_X, INIT_Y + FIELD_HEIGHT))
  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y + FIELD_HEIGHT), (INIT_X, INIT_Y))

  #自キャラの描画1
  pygame.draw.circle(screen, (255,255,255), p1_pos , p_radius)
  pygame.draw.circle(screen, (255,255,255), p2_pos , p_radius)
  
  pygame.display.update()
  for event in pygame.event.get():
    if pressKeyMode == "left": 
      
      if pressKeyPlayer == 1: p1_pos[0] = p1_pos[0] - P_MOVE_SPEED
      else: p2_pos[0] = p2_pos[0] - P_MOVE_SPEED

    if pressKeyMode == "right":
      if pressKeyPlayer == 1: p1_pos[0] = p1_pos[0] + P_MOVE_SPEED 
      else: p2_pos[0] = p2_pos[0] + P_MOVE_SPEED 

    if pressKeyMode == "up":
      if pressKeyPlayer == 1: p1_pos[1] = p1_pos[1] - P_MOVE_SPEED 
      else: p2_pos[1] = p2_pos[1] - P_MOVE_SPEED 

    if pressKeyMode == "down":
      if pressKeyPlayer == 1: p1_pos[1] = p1_pos[1] + P_MOVE_SPEED 
      else: p2_pos[1] = p2_pos[1] + P_MOVE_SPEED 

    if event.type == pygame.locals.KEYDOWN:  # キーを押したとき
      print('key down!!!')
      if event.key == pygame.locals.K_ESCAPE: # 終了
        pygame.quit()
        sys.exit()
      
      #player1
      if pygame.key.name(event.key) == 's' or pygame.key.name(event.key) == 'a':
        pressKeyMode = "left" 
        pressKeyPlayer = 1
      elif pygame.key.name(event.key) == 'f':
        pressKeyMode = "right" 
        pressKeyPlayer = 1
      elif pygame.key.name(event.key) == 'e':
        pressKeyMode = "up" 
        pressKeyPlayer = 1
      elif pygame.key.name(event.key) == 'd':
        pressKeyMode = "down" 
        pressKeyPlayer = 1
     #player2
      elif pygame.key.name(event.key) == 'j':
        pressKeyMode = "left" 
        pressKeyPlayer = 2 
      elif pygame.key.name(event.key) == ';' or pygame.key.name(event.key) == 'l':
        pressKeyMode = "right" 
        pressKeyPlayer = 2
      elif pygame.key.name(event.key) == 'i':
        pressKeyMode = "up" 
        pressKeyPlayer = 2
      elif pygame.key.name(event.key) == 'k':
        pressKeyMode = "down" 
        pressKeyPlayer = 2

      else:
        pressKeyMode = ""
        print("押されたキー = " + pygame.key.name(event.key))

    if event.type == pygame.locals.KEYUP:  # キーを話した時
      pressKeyMode = ""
      print('key up!!!')
