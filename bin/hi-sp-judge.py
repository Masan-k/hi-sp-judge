import pygame,pygame.locals,sys,math,copy
import numpy as np
SCREEN_SIZE = (800, 600)
FIELD_WIDTH = 400
FIELD_HEIGHT = 500

INIT_X = 50
INIT_Y = 50
P_MOVE_SPEED = 8 
P_RADIUS = 10
BALL_RADIUS = 5 
GOAL_ARIA = 150

COLOR_JOY_LEFT = [150,150,255]
COLOR_JOY_RIGHT = [100,255,100]
COLOR_JOY_STOP = [150,150,150]

ball_pos = [0,0]
p1_pos = [0,0]
p2_pos = [0,0]

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

clock= pygame.time.Clock()

while True:
  screen.fill((0,0,0))

  #---------------
  #スタートで初期化
  #---------------
  if joy.get_button(7) == 1: status = 'init'

  if status == 'init':
    status = 'p1keep'
    ball_pos = [150,150]
    p1_pos = [100,500]
    p2_pos = [400,500]
    passMarkerPos[0] = 300
    passMarkerPos[1] = 500

  #------------
  #コートの描画
  #------------
  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y), (INIT_X + FIELD_WIDTH, INIT_Y))
  pygame.draw.line(screen, (255,255,255), (INIT_X + FIELD_WIDTH, INIT_Y), (INIT_X + FIELD_WIDTH, INIT_Y + FIELD_HEIGHT))
  pygame.draw.line(screen, (255,255,255), (INIT_X + FIELD_WIDTH, INIT_Y + FIELD_HEIGHT), (INIT_X, INIT_Y + FIELD_HEIGHT))
  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y + FIELD_HEIGHT), (INIT_X, INIT_Y))

  pygame.draw.line(screen, (255,255,255), (INIT_X, INIT_Y + GOAL_ARIA), (INIT_X + FIELD_WIDTH , INIT_Y + GOAL_ARIA))
  pygame.draw.rect(screen, (0,0,255), (INIT_X + 2 , INIT_Y + 2, FIELD_WIDTH - 3 , GOAL_ARIA - 3))
  pygame.draw.rect(screen, (0,0,0), (INIT_X + 4 , INIT_Y + 4, FIELD_WIDTH - 7 , GOAL_ARIA - 7))
 
  #----------------------------
  #ゲームパッドによる移動処理
  #---------------------------
  x0 = joy.get_axis(0)
  y0 = joy.get_axis(1)

  x1 = joy.get_axis(3)
  y1 = joy.get_axis(4)

  pygame.draw.rect(screen,(0,0,255),(500,310,80,80))
  pygame.draw.rect(screen,(0,0,0),(501,311,78,78))
  pygame.draw.circle(screen, COLOR_JOY_LEFT, (540 + x0*40 ,350 + y0*40),5)
  
  pygame.draw.rect(screen,(0,255,0),(600,310,80,80))
  pygame.draw.rect(screen,(0,0,0),(601,311,78,78))
  pygame.draw.circle(screen, COLOR_JOY_RIGHT,(640 + x1*40 ,350 + y1*40),5)

  if joy.get_button(9) == 0: sp0 = 3
  else: sp0 = 5

  if joy.get_button(10) == 0: sp1 = 3
  else: sp1 = 5

  if status != 'p1keep':
    p1_pos[0] = p1_pos[0] + x0*sp0
    p1_pos[1] = p1_pos[1] + y0*sp0
  else:
    #パスのベクトルを示すマーカー
    passMarkerPos[0] = passMarkerPos[0] + x0*7
    passMarkerPos[1] = passMarkerPos[1] + y0*7
     
  if status != 'p2keep':
    p2_pos[0] = p2_pos[0] + x1*sp1
    p2_pos[1] = p2_pos[1] + y1*sp1
    markColor = COLOR_JOY_LEFT
  else:
    passMarkerPos[0] = passMarkerPos[0] + x1*7
    passMarkerPos[1] = passMarkerPos[1] + y1*7
    markColor = COLOR_JOY_RIGHT

  if status == 'p1pass' or status == 'p2pass':
    markColor = COLOR_JOY_STOP

  pygame.draw.line(screen,markColor,(passMarkerPos[0]-10,passMarkerPos[1]-10),(passMarkerPos[0]+10,passMarkerPos[1]+10))
  pygame.draw.line(screen,markColor,(passMarkerPos[0]+10,passMarkerPos[1]-10),(passMarkerPos[0]-10,passMarkerPos[1]+10))

  #--------
  #パス処理
  #--------
  if (status == 'p1keep' or status =='p2keep') and (joy.get_button(4) == 1 or joy.get_button(5)) == 1:
    if status == 'p1keep': status = "p1pass"
    if status == 'p2keep': status = "p2pass"
      
    ballPassPosX = ball_pos[0]
    ballPassPosY = ball_pos[1]
    ballMoveDistance = [(passMarkerPos[0] - ball_pos[0]) /100,(passMarkerPos[1] - ball_pos[1])/100]

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
  
  #自キャラの描画1
  if status == 'p1keep': 
    pygame.draw.circle(screen, COLOR_JOY_STOP, p1_pos , P_RADIUS)
  else:
    pygame.draw.circle(screen, COLOR_JOY_LEFT, p1_pos , P_RADIUS)

  if status == 'p2keep': 
    pygame.draw.circle(screen, COLOR_JOY_STOP, p2_pos , P_RADIUS)
  else:
    pygame.draw.circle(screen, COLOR_JOY_RIGHT, p2_pos , P_RADIUS)

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
      passMarkerPos[0] = ballPassPosX
      passMarkerPos[1] = ballPassPosY

      if status == 'p1pass': status = 'p2keep'
      elif status == 'p2pass': status = 'p1keep'
 
      # 得点判定
      if ballPassPosX >= INIT_X \
         and ballPassPosX <= INIT_X + FIELD_WIDTH \
         and ballPassPosY >= INIT_Y \
         and ballPassPosY <= INIT_Y + GOAL_ARIA:
        status = 'getPoint'

  screen.blit(font.render('status : ' + str(status) , True, (255, 255, 255)), [10, 10]) 
  screen.blit(font.render('fps : ' + str(round(clock.get_fps()*10)/10) , True, (255, 255, 255)), [10, 30]) 
  pygame.display.update()
  clock.tick(60)
  
  for event in pygame.event.get():
    if event.type == pygame.locals.KEYDOWN: 
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()
