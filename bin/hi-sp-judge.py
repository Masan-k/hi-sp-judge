import pygame
import pygame.locals
import sys
import math
import keyboard
import numpy as np
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
joy = pygame.joystick.Joystick(0)
joy.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("HI-SP-JUDGE")


font = pygame.font.Font(None,15)
status = "init"
ballPassPos = [0,0]
ballPassPosX = 0
ballPassPosY = 0
ballMoveDistance = [0,0]
passMarkerPos = [0,0]

while True:
  screen.fill((0,0,0))

  if status == 'init':
    status = 'p1keep'
    ball_pos = [150,150]
    p1_pos = [200,200]
    p2_pos = [400,200]
    passMarkerPos = [300,200]

  #----------------------------
  #ゲームパッドによる移動処理
  #---------------------------
  x0 = joy.get_axis(0)
  y0 = joy.get_axis(1)

  x1 = joy.get_axis(3)
  y1 = joy.get_axis(4)

  pygame.draw.rect(screen,(255,255,255),(400,10,80,80))
  pygame.draw.rect(screen,(0,0,0),(401,11,78,78))
  pygame.draw.circle(screen,(200,255,200),(440 + x0*40 ,50 + y0*40),5)
  
  pygame.draw.rect(screen,(255,255,255),(500,10,80,80))
  pygame.draw.rect(screen,(0,0,0),(501,11,78,78))
  pygame.draw.circle(screen,(200,200,255),(540 + x1*40 ,50 + y1*40),5)

  if status != 'p1keep':
    p1_pos[0] = p1_pos[0] + x0
    p1_pos[1] = p1_pos[1] + y0
  else:
    #パスのベクトルを示すマーカー
    passMarkerPos[0] = passMarkerPos[0] + x0*3
    passMarkerPos[1] = passMarkerPos[1] + y0*3
     
  if status != 'p2keep':
    p2_pos[0] = p2_pos[0] + x1
    p2_pos[1] = p2_pos[1] + y1
  else:
    passMarkerPos[0] = passMarkerPos[0] + x1*3
    passMarkerPos[1] = passMarkerPos[1] + y1*3

  pygame.draw.line(screen,(255,255,255),(passMarkerPos[0]-10,passMarkerPos[1]-10),(passMarkerPos[0]+10,passMarkerPos[1]+10))
  pygame.draw.line(screen,(255,255,255),(passMarkerPos[0]+10,passMarkerPos[1]-10),(passMarkerPos[0]-10,passMarkerPos[1]+10))

  #--------
  #パス処理
  #--------
  if joy.get_button(4) == 1 or joy.get_button(5) == 1:
    screen.blit(font.render('pass!!', True, (255, 255, 255)), [10, 50])

    if status == 'p1keep': status = "p1pass"
    if status == 'p2keep': status = "p2pass"
      
    ballPassPosX = ball_pos[0]
    ballPassPosY = ball_pos[1]
    ballMoveDistance = [(passMarkerPos[0] - ball_pos[0]) /1000,(passMarkerPos[1] - ball_pos[1])/1000]

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

  #---------------------
  #ボールコート外判定
  #---------------------
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
   
    if status == 'p1keep': pPos = p1_pos
    elif status == 'p2keep': pPos = p2_pos

    if passMarkerPos[0] - pPos[0] != 0:
      cos = math.cos(math.atan((pPos[1] - passMarkerPos[1])/(passMarkerPos[0]  - pPos[0])))
      ballX = cos * (P_RADIUS + BALL_RADIUS)
    else: ballX = 0
       
    if passMarkerPos[0] - pPos[0] != 0:
      sin = math.sin(math.atan((pPos[1] - passMarkerPos[1])/(passMarkerPos[0] - pPos[0])))
      ballY = sin * (P_RADIUS + BALL_RADIUS)
    else: ballY = 0
        
    if passMarkerPos[0] - pPos[0] < 0: 
      ballX = -ballX
      ballY = -ballY

    ball_pos[0] = pPos[0] + ballX
    ball_pos[1] = pPos[1] - ballY
  
    pygame.draw.circle(screen, (255,255,255), ball_pos , BALL_RADIUS)

  screen.blit(font.render('status : ' + str(status) , True, (255, 255, 255)), [10, 10]) 
  
  #自キャラの描画1
  pygame.draw.circle(screen, (200,255,200), p1_pos , P_RADIUS)
  pygame.draw.circle(screen, (200,200,255), p2_pos , P_RADIUS)

  #---------------------
  #ボールの描画
  #---------------------
  if status == "p1pass" or status == "p2pass" :
    ballPassPosX = ballPassPosX + ballMoveDistance[0] 
    ballPassPosY = ballPassPosY + ballMoveDistance[1] 
    pygame.draw.circle(screen, (255,255,255), [ballPassPosX,ballPassPosY] , BALL_RADIUS)

  #---------------------
  #ボールのキャッチ判定
  #---------------------
  if status == 'p1pass' or status == 'p2pass':
    
    playerPos = [9999,9999]
    if status == 'p1pass': playerPos = np.array(p2_pos)
    elif status == 'p2pass': playerPos = np.array(p1_pos)

    ballPos = np.array([ballPassPosX, ballPassPosY])
    norm = np.linalg.norm(playerPos - ballPos) 
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

    
    #キー入力処理
    if event.type == pygame.locals.KEYDOWN: 
      #終了処理
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()
      
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
