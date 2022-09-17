import pygame
import pygame.locals
import sys
import math
from pynput import keyboard

SCREEN_SIZE = (800, 600)
FIELD_WIDTH = 600
FIELD_HEIGHT = 400

INIT_X = 100
INIT_Y = 100
P_MOVE_SPEED = 8 
P_RADIUS = 10
GOAL_ARIA_WIDTH = 150

BALL_RADIUS = 5 
ball_pos = [150,150]

p1_pos = [200,200]
p2_pos = [400,200]

pressKeyMode = "" 
pressKeyPlayer = ""

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("HI-SP-JUDGE")


font = pygame.font.Font(None,15)
status = "none"
ballPassPos = [0,0]
ballPassPosX = 0
ballPassPosY = 0
ballMoveDistance = [0,0]

while True:
  screen.fill((0,0,0))
  #------------
  #コートの描画
  #------------
  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y), (INIT_X + FIELD_WIDTH, INIT_Y))
  pygame.draw.line(screen, (255,255,255), (INIT_X + FIELD_WIDTH, INIT_Y), (INIT_X + FIELD_WIDTH, INIT_Y + FIELD_HEIGHT))
  pygame.draw.line(screen, (255,255,255), (INIT_X + FIELD_WIDTH, INIT_Y + FIELD_HEIGHT), (INIT_X, INIT_Y + FIELD_HEIGHT))
  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y + FIELD_HEIGHT), (INIT_X, INIT_Y))

  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y + FIELD_HEIGHT), (INIT_X, INIT_Y))
  pygame.draw.line(screen, (255,255,255), (INIT_X + FIELD_WIDTH - GOAL_ARIA_WIDTH, INIT_Y), (INIT_X + FIELD_WIDTH - GOAL_ARIA_WIDTH, INIT_Y + FIELD_HEIGHT))

  #---------------------------------
  #ボールの描画(保持時)
  #---------------------------------

  #マウス座標
  mouseX, mouseY = pygame.mouse.get_pos()
 
  if mouseX - p1_pos[0] != 0:
    cos = math.cos(math.atan((p1_pos[1] - mouseY)/(mouseX - p1_pos[0])))
    ballX = cos * (P_RADIUS + BALL_RADIUS)
  else: ballX = 0
     
  if  mouseX - p1_pos[0] != 0:
    sin = math.sin(math.atan((p1_pos[1] - mouseY)/(mouseX - p1_pos[0])))
    ballY = sin * (P_RADIUS + BALL_RADIUS)
  else: ballY = 0
    
  
  if mouseX - p1_pos[0] < 0: ballX = -ballX
  if mouseX - p1_pos[0] < 0: ballY = -ballY
  ball_pos[0] = p1_pos[0] + ballX
  ball_pos[1] = p1_pos[1] - ballY
  pygame.draw.circle(screen, (0,200,255), ball_pos , BALL_RADIUS)
  
  #---------------------
  #ボールの描画（パス時)
  #---------------------
  

  #補助線の描画
  #pygame.draw.line(screen, (255,255,255), (p1_pos), (mouseX, mouseY))

  #角度を算出
  #textMousePos = font.render('mouse_pos : ' + f'{mouseX}, {mouseY}', True, (255, 255, 255))
  #screen.blit(textMousePos, [10, 10]) 

  #ballAngle = math.atan((p1_pos[1] - mouseY)/(mouseX - p1_pos[0])) * 180/ math.pi
  #screen.blit(font.render('angle: ' + str(ballAngle) , True, (255, 255, 255)), [10, 70]) 
  #screen.blit(font.render('mouseY : ' + str(mouseY) , True, (255, 255, 255)), [10, 30]) 
  #screen.blit(font.render('p1_pos[1] : ' + str(p1_pos[1]) , True, (255, 255, 255)), [10, 50]) 
  #screen.blit(font.render('x : ' + str(mouseX - p1_pos[0]) , True, (255, 255, 255)), [10, 30]) 
  #screen.blit(font.render('y : ' + str(p1_pos[1] - mouseY) , True, (255, 255, 255)), [10, 50]) 
  #screen.blit(font.render('sin : ' + str(sin) , True, (255, 255, 255)), [10, 90]) 
  #screen.blit(font.render('ballY : ' + str(ballY) , True, (255, 255, 255)), [10, 110]) 
   
  #自キャラの描画1
  pygame.draw.circle(screen, (255,255,255), p1_pos , P_RADIUS)
  pygame.draw.circle(screen, (255,255,255), p2_pos , P_RADIUS)

  #ボールバスの描画
  if status == "pass":
    pygame.draw.line(screen, (255,255,255), p1_pos, clickPos)
    ballPassPosX = ballPassPosX + ballMoveDistance[0] 
    ballPassPosY = ballPassPosY + ballMoveDistance[1] 
    pygame.draw.circle(screen, (255,0,0), [ballPassPosX,ballPassPosY] , BALL_RADIUS)
    screen.blit(font.render('ballPassPos: ' + str(ballPassPosX) + "," + str(ballPassPosY) , True, (255, 255, 255)), [10, 70]) 
    screen.blit(font.render('ballMoveDistance: ' + str(ballMoveDistance[0]) + "," + str(ballMoveDistance[1]) , True, (255, 255, 255)), [10, 90]) 
    
  pygame.display.update()
  
  for event in pygame.event.get():
    #移動処理(前フレーム）
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

    
    if event.type == pygame.locals.MOUSEBUTTONDOWN:
      status = "pass"
      clickPos = pygame.mouse.get_pos()
      ballPassPosX = ball_pos[0]
      ballPassPosY = ball_pos[1]
      ballMoveDistance = [(clickPos[0] - ball_pos[0]) /1000,(clickPos[1] - ball_pos[1])/1000]

    #キー入力処理
    if event.type == pygame.locals.KEYDOWN: 
      #終了処理
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()
      
      #player1の操作
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
     #player2の操作
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
        #print("押されたキー = " + pygame.key.name(event.key))

    # キーを話した時
    if event.type == pygame.locals.KEYUP:  
      pressKeyMode = ""
      #print('key up!!!')
