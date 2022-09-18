import pygame
import pygame.locals
import sys
import math
import keyboard
import numpy as np
import copy
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
status = "init"
ballPassPos = [0,0]
ballPassPosX = 0
ballPassPosY = 0
ballMoveDistance = [0,0]

while True:

  if status == 'init':
    status = 'p1keep'
    ball_pos = [150,150]
    p1_pos = [200,200]
    p2_pos = [400,200]

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

  pygame.draw.line(screen, (0,0,255),
                   (INIT_X + FIELD_WIDTH - GOAL_ARIA_WIDTH + 3, INIT_Y + 3),
                   (INIT_X + FIELD_WIDTH - 3, INIT_Y + 3),width=3)

  pygame.draw.line(screen, (0,0,255),
                   (INIT_X + FIELD_WIDTH - 3, INIT_Y + 3),
                   (INIT_X + FIELD_WIDTH - 3, INIT_Y + FIELD_HEIGHT - 3),width=3)
  pygame.draw.line(screen, (0,0,255),
                   (INIT_X + FIELD_WIDTH - 3, INIT_Y + FIELD_HEIGHT - 3),
                   (INIT_X + FIELD_WIDTH - GOAL_ARIA_WIDTH + 3,
                   INIT_Y + FIELD_HEIGHT - 3),width=3)
  pygame.draw.line(screen, (0,0,255),
                   (INIT_X + FIELD_WIDTH  - GOAL_ARIA_WIDTH + 3,
                    INIT_Y + FIELD_HEIGHT - 3),
                   (INIT_X + FIELD_WIDTH - GOAL_ARIA_WIDTH + 3, INIT_Y + 3)
                  ,width=3)
##  pygame.draw.rect(screen, (0,0,255), (100,100,200,200))

  #---------------------
  #ボールコート外判定
  #---------------------
  #screen.blit(font.render('ballPassPosX : ' + str(ballPassPosX) , True, (255, 255, 255)), [10, 50]) 
  #screen.blit(font.render('INIT_X : ' + str(INIT_X) , True, (255, 255, 255)), [10, 70]) 
  if status == 'p1pass' or status == 'p2pass':
    if ballPassPosX + BALL_RADIUS < INIT_X or \
       ballPassPosY + BALL_RADIUS < INIT_Y or \
       ballPassPosX - BALL_RADIUS > INIT_X + FIELD_WIDTH or \
       ballPassPosY - BALL_RADIUS > INIT_Y + FIELD_HEIGHT:
      status = 'offCourt'
  if status == 'offCourt':
    pygame.draw.circle(screen, (255, 0,0), [ballPassPosX,ballPassPosY] , BALL_RADIUS)

  #---------------------------------
  #ボールの描画(保持時)
  #---------------------------------
  #マウス座標の取得
  if status == 'p1keep' or status == 'p2keep':
    mouseX, mouseY = pygame.mouse.get_pos()
   
    if status == 'p1keep': pPos = p1_pos
    elif status == 'p2keep': pPos = p2_pos

    if mouseX - pPos[0] != 0:
      cos = math.cos(math.atan((pPos[1] - mouseY)/(mouseX - pPos[0])))
      ballX = cos * (P_RADIUS + BALL_RADIUS)
    else: ballX = 0
       
    if  mouseX - pPos[0] != 0:
      sin = math.sin(math.atan((pPos[1] - mouseY)/(mouseX - pPos[0])))
      ballY = sin * (P_RADIUS + BALL_RADIUS)
    else: ballY = 0
        
    if mouseX - pPos[0] < 0: 
      ballX = -ballX
      ballY = -ballY

    ball_pos[0] = pPos[0] + ballX
    ball_pos[1] = pPos[1] - ballY
  
    pygame.draw.circle(screen, (0,200,255), ball_pos , BALL_RADIUS)

  screen.blit(font.render('status : ' + str(status) , True, (255, 255, 255)), [10, 10]) 
  
  #自キャラの描画1
  pygame.draw.circle(screen, (255,255,255), p1_pos , P_RADIUS)
  pygame.draw.circle(screen, (255,255,255), p2_pos , P_RADIUS)

  #---------------------
  #ボールの描画
  #---------------------
  if status == "p1pass" or status == "p2pass" :
    ballPassPosX = ballPassPosX + ballMoveDistance[0] 
    ballPassPosY = ballPassPosY + ballMoveDistance[1] 
    pygame.draw.circle(screen, (0,200,255), [ballPassPosX,ballPassPosY] , BALL_RADIUS)

  #---------------------
  #ボールのキャッチ判定
  #---------------------
  if status == 'p1pass' or status == 'p2pass':
    
    playerPos = [9999,9999]
    if status == 'p1pass': playerPos = np.array(p2_pos)
    elif status == 'p2pass': playerPos = np.array(p1_pos)

    ballPos = np.array([ballPassPosX, ballPassPosY])
    norm = np.linalg.norm(playerPos - ballPos) 
    #screen.blit(font.render('norm : ' + str(norm), True, (255, 255, 255)), [10, 30]) 
    if norm <= BALL_RADIUS + P_RADIUS:
      if status == 'p1pass':status = 'p2keep'
      elif status == 'p2pass':status = 'p1keep'
 
      # 得点判定
      if ballPassPosX >= INIT_X + FIELD_WIDTH - GOAL_ARIA_WIDTH \
         and ballPassPosX <= INIT_X + FIELD_WIDTH \
         and ballPassPosY >= INIT_Y \
         and ballPassPosY <= INIT_Y + FIELD_HEIGHT:
        status = 'getPoint'

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
      if status == 'p1keep': status = "p1pass"
      if status == 'p2keep': status = "p2pass"
      
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
      if (pygame.key.name(event.key) == 's' or pygame.key.name(event.key) == 'a') and status != 'p1keep':
        pressKeyMode = "left" 
        pressKeyPlayer = 1
      elif pygame.key.name(event.key) == 'f' and status != 'p1keep':
        pressKeyMode = "right" 
        pressKeyPlayer = 1
      elif pygame.key.name(event.key) == 'e' and status != 'p1keep':
        pressKeyMode = "up" 
        pressKeyPlayer = 1
      elif pygame.key.name(event.key) == 'd' and status != 'p1keep':
        pressKeyMode = "down" 
        pressKeyPlayer = 1
     #player2の操作
      elif pygame.key.name(event.key) == 'j' and status != 'p2keep':
        pressKeyMode = "left" 
        pressKeyPlayer = 2 
      elif (pygame.key.name(event.key) == ';' or pygame.key.name(event.key) == 'l') and status != 'p2keep':
        pressKeyMode = "right" 
        pressKeyPlayer = 2
      elif pygame.key.name(event.key) == 'i' and status != 'p2keep':
        pressKeyMode = "up" 
        pressKeyPlayer = 2
      elif pygame.key.name(event.key) == 'k' and status != 'p2keep':
        pressKeyMode = "down" 
        pressKeyPlayer = 2
      
      elif pygame.key.name(event.key) == '1':
        #リスタート
        status = 'init'

      else:
        pressKeyMode = ""
        #print("押されたキー = " + pygame.key.name(event.key))

    # キーを話した時
    if event.type == pygame.locals.KEYUP:  
      pressKeyMode = ""
      #print('key up!!!')
