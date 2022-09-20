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
COLOR_JOY_RIGHT = [150,255,150]
COLOR_JOY_STOP = [150,150,150]

ball_pos = [0,0]
p1_pos = [0,0]
p2_pos = [0,0]

STAMINA_MAX = 100

pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("HI-SP-JUDGE")

mainInfoFont= pygame.font.SysFont("ubuntu",20)
subInfoFont = pygame.font.SysFont("ubuntu",12)
status = "init"
ballPassPos = [0,0]
ballPassPosX = 0
ballPassPosY = 0
ballMoveDistance = [0,0]
passMarkerPos = [0,0]
MARKER_SPEED = 100;

clock= pygame.time.Clock()
stageCode = ""
stageName = ""

while True:
  screen.fill((0,0,0))
  if joy.get_button(7) == 1: status = 'init' #スタートで初期化
  if status == 'init':
    status = 'p1keep'
    ball_pos = [150,150]
    p1_pos = [100,500]
    p2_pos = [400,500]
    passMarkerPos[0] = 300
    passMarkerPos[1] = 500
    stageCode = '0'
    stageName = 'TUTORIAL'
    
    p1_stamina = 100
    p2_stamina = 100

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
   
  #------------
  #情報表示
  #------------
  #ステージ＆ステータス
  screen.blit(mainInfoFont.render('STAGE', True, (255, 255, 255)), [500, 80]) 
  screen.blit(mainInfoFont.render(' : ' + stageCode + "." + stageName, True, (255, 255, 255)), [580, 80]) 

  if status == 'p1pass' or status == 'p2pass' or status == 'p1keep' or status == 'p2keep':
    dispStatus = ' : ON OFFENCE'
    dispColor = [255,255,255]
  elif status == 'offCourt':
    dispStatus = ' : FAILURE(OFF COURT)'
    dispColor = [255,100,100]
  elif status == 'getPoint':
    dispStatus = ' : CLEAR!!'
    dispColor = [100,100,255]

  screen.blit(mainInfoFont.render('STATUS', True, (255, 255, 255)), [500, 120]) 
  screen.blit(mainInfoFont.render(dispStatus, True, dispColor), [580, 120]) 
  #ゲームパッド
  pygame.draw.rect(screen, (255,255,255),(500,180,250,250))
  pygame.draw.rect(screen, (0,0,0),(501,181,248,248))

  #pygame.draw.rect(screen, (255,255,255),(525,200,200,200)) #base
  pygame.draw.rect(screen, (255,255,255),(525,250,40,150))
  pygame.draw.rect(screen, (0,0,0),(526,251,38,148))
  pygame.draw.rect(screen, (255,255,255),(685,250,40,150))
  pygame.draw.rect(screen, (0,0,0),(686,251,38,148))
  
  pygame.draw.rect(screen, (255,255,255),(525,250,200,80))
  pygame.draw.rect(screen, (0,0,0),(526,251,198,78))

  #十字キー
  pygame.draw.line(screen, (255,255,255), (565, 270), (565, 310))
  pygame.draw.line(screen, (255,255,255), (545, 290), (585, 290))

  #ボタン(ABXY)
  BTN_DIS = 18
  pygame.draw.circle(screen, (255,255,255), (685-BTN_DIS,290),10)
  pygame.draw.circle(screen, (0,0,0), (685-BTN_DIS,290),9)
  pygame.draw.circle(screen, (255,255,255), (685,290-BTN_DIS),10)
  pygame.draw.circle(screen, (0,0,0), (685,290-BTN_DIS),9)
  pygame.draw.circle(screen, (255,255,255), (685+BTN_DIS,290),10)
  pygame.draw.circle(screen, (0,0,0), (685+BTN_DIS,290),9)
  pygame.draw.circle(screen, (255,255,255), (685,290+BTN_DIS),10)
  pygame.draw.circle(screen, (0,0,0), (685,290+BTN_DIS),9)

  #スタートボタン
  pygame.draw.rect(screen, (255,200,200), (595,280,60,15))
  pygame.draw.rect(screen, (0,0,0), (596,281,58,13))
  screen.blit(subInfoFont.render('RESTART', True, (255, 200, 200)), [600, 280]) 

  #ボタン（RL)
  screen.blit(mainInfoFont.render('INFO : INPUT', True, (255, 255, 255)), [565, 190]) 
  pygame.draw.rect(screen, (255,255,255),(545,230,50,20))
  pygame.draw.rect(screen, (0,0,0),(546,231,48,18))
  pygame.draw.rect(screen, (0,255,255),(655,230,50,20))
  pygame.draw.rect(screen, (0,0,0),(656,231,48,18))
  screen.blit(subInfoFont.render('PASS', True, (0, 255, 255)), [665, 232]) 

  #TIPS
  screen.blit(subInfoFont.render('TIPS : ', True, (255, 255, 255)), [480, 450]) 
  screen.blit(subInfoFont.render('Stage selection is a numerical input on the keyboard.', True, (255, 255, 255)), [480, 470]) 

  screen.blit(subInfoFont.render('p1_stamina : ' + str(p1_stamina), True, (255, 255, 255)), [480, 490]) 
  screen.blit(subInfoFont.render('p2_stamina : ' + str(p2_stamina), True, (255, 255, 255)), [480, 510]) 
  pygame.draw.rect(screen, COLOR_JOY_LEFT,(526,330,38, 69))
  pygame.draw.rect(screen, (0,0,0),(526,330,38, 69 * (STAMINA_MAX-p1_stamina)/100))
  pygame.draw.rect(screen, COLOR_JOY_RIGHT,(686,330,38, 69))
  pygame.draw.rect(screen, (0,0,0),(686,330,38, 69 * (STAMINA_MAX-p2_stamina)/100))


  #----------------------------
  #ゲームパッドによる移動処理
  #---------------------------
  x0 = joy.get_axis(0)
  y0 = joy.get_axis(1)

  x1 = joy.get_axis(3)
  y1 = joy.get_axis(4)

  pygame.draw.circle(screen, (0,0,255), (595,365),30)
  pygame.draw.circle(screen, (0,0,0), (595,365),29)
  pygame.draw.circle(screen, COLOR_JOY_LEFT, (595 + x0*30 ,365 + y0*30),5)
  
  pygame.draw.circle(screen, (0,255,0),(655,365),30)
  pygame.draw.circle(screen, (0,0,0),(655,365),29)
  pygame.draw.circle(screen, COLOR_JOY_RIGHT,(655 + x1*30 ,365 + y1*30),5)

  if joy.get_button(9) == 0:
    sp0 = 3
    if p1_stamina < STAMINA_MAX: p1_stamina = p1_stamina + 2
  elif status != 'p1keep':
    if p1_stamina > 0:
      sp0 = 5
      p1_stamina = p1_stamina - 3 
    else:
      sp0 = 3
  else:
    if p1_stamina < STAMINA_MAX: p1_stamina = p1_stamina + 2

  
  if joy.get_button(10) == 0:
    sp1 = 3
    if p2_stamina < STAMINA_MAX: p2_stamina = p2_stamina + 2
  elif status != 'p2keep': 
    if p2_stamina > 0:
      sp1 = 5
      p2_stamina = p2_stamina - 3 
    else:
      sp1 = 3
  else:
    if p2_stamina < STAMINA_MAX: p2_stamina = p2_stamina + 2
 

  if status != 'p1keep' and status != 'getPoint':
    p1_pos[0] = p1_pos[0] + x0*sp0
    p1_pos[1] = p1_pos[1] + y0*sp0
 
  if status != 'p2keep' and status != 'getPoint':
    p2_pos[0] = p2_pos[0] + x1*sp1
    p2_pos[1] = p2_pos[1] + y1*sp1

  #---------------------------
  #パスのベクトルマーカー制御
  #---------------------------
  if status == 'p1keep':
    passMarkerPos[0] = p1_pos[0] + x0 * MARKER_SPEED
    passMarkerPos[1] = p1_pos[1] + y0 * MARKER_SPEED
    markColor = COLOR_JOY_LEFT

  if status == 'p2keep':
    passMarkerPos[0] = p2_pos[0] + x1 * MARKER_SPEED
    passMarkerPos[1] = p2_pos[1] + y1 * MARKER_SPEED
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
    ballMoveDistance = [(passMarkerPos[0] - ball_pos[0]) /20,(passMarkerPos[1] - ball_pos[1])/20]

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
  elif status == 'getPoint':
    pygame.draw.circle(screen, (0, 0, 255), [ballPassPosX,ballPassPosY] , BALL_RADIUS)


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
  if status == 'p1keep' or status == 'getPoint': 
    pygame.draw.circle(screen, COLOR_JOY_STOP, p1_pos , P_RADIUS)
  else:
    pygame.draw.circle(screen, COLOR_JOY_LEFT, p1_pos , P_RADIUS)

  if status == 'p2keep' or status == 'getPoint': 
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

  pygame.display.update()
  clock.tick(60)
  
  for event in pygame.event.get():
    if event.type == pygame.locals.KEYDOWN: 
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()
