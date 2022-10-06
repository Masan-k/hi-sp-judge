import pygame,pygame.locals,sys,math,copy
import numpy as np
from enum import Enum

class InputMode(Enum):
  PAD = 1
  KEY = 2

def drawMarkPass():
  pygame.draw.line(screen,markColor,(passMarkerPos[0]-10,passMarkerPos[1]-10),(passMarkerPos[0]+10,passMarkerPos[1]+10))
  pygame.draw.line(screen,markColor,(passMarkerPos[0]+10,passMarkerPos[1]-10),(passMarkerPos[0]-10,passMarkerPos[1]+10))

debugStatus = "init"
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

COLOR_DIFENSE = [255,150,150]

STAMINA_MAX = 100
MARKER_SPEED = 100;
NO_PASS_DIS = 0.1
NO_MOVE_DIS = 0.05

ball_pos = [0,0]
p1_pos = [0,0]
p2_pos = [0,0]
p3_pos = [0,0]
p4_pos = [0,0]

pygame.init()
joyCount = pygame.joystick.get_count()

user2InputMode = 0
if joyCount == 0:
  print("Please connect GamePad! (count:" + str(joyCount) + ")")
  exit()
elif joyCount == 1:
  user2InputMode = InputMode.KEY 
  print("Please connect GamePad! (count:" + str(joyCount) + ")")
  print("userInputMode  >> " + str(user2InputMode))

  joy = pygame.joystick.Joystick(0)
  joy.init()

else:
  user2InputMode = InputMode.PAD
  print("userInputMode  >> " + str(user2InputMode))

  joy = pygame.joystick.Joystick(0)
  joy.init()
  
  joy2 = pygame.joystick.Joystick(1)
  joy2.init()


screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("HI-SP-JUDGE")

mainInfoFont= pygame.font.SysFont("ubuntu",15)
subInfoFont = pygame.font.SysFont("ubuntu",12)
status = "init"
ballPassPos = [0,0]
ballPassPosX = 0
ballPassPosY = 0
ballMoveDistance = [0,0]
passMarkerPos = [0,0]
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
    p3_pos = [100,400]

    p2_pos = [400,500]
    p4_pos = [400,400]
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
  screen.blit(mainInfoFont.render('STAGE', True, (255, 255, 255)), [470, 80]) 
  screen.blit(mainInfoFont.render(' : ' + stageCode + "." + stageName, True, (255, 255, 255)), [550, 80]) 

  if status == 'p1pass' or status == 'p2pass' or status == 'p1keep' or status == 'p2keep':
    dispStatus = ' : ON OFFENCE'
    dispColor = [255,255,255]
  elif status == 'offCourt':
    dispStatus = ' : FAILURE(OUT OF BOUNDS)'
    dispColor = [255,100,100]
  elif status == 'getPoint':
    dispStatus = ' : CLEAR!!'
    dispColor = [100,100,255]
  elif status == 'interception':
    dispStatus = ' : FAILURE(INTERCEPTION)'
    dispColor = [255,100,100]


  screen.blit(mainInfoFont.render('STATUS', True, (255, 255, 255)), [470, 120]) 
  screen.blit(mainInfoFont.render(dispStatus, True, dispColor), [550, 120]) 
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

  pygame.draw.rect(screen, COLOR_JOY_LEFT,(526,330,38, 69))
  pygame.draw.rect(screen, (0,0,0),(526,330,38, 69 * (STAMINA_MAX-p1_stamina)/100))
  pygame.draw.rect(screen, COLOR_JOY_RIGHT,(686,330,38, 69))
  pygame.draw.rect(screen, (0,0,0),(686,330,38, 69 * (STAMINA_MAX-p2_stamina)/100))

  #--------------------------------
  #ゲームパッドによる移動処理(P1P2)
  #--------------------------------
  x0 = joy.get_axis(0)
  y0 = joy.get_axis(1)
  #screen.blit(subInfoFont.render('x0 : ' + str(x0), True, (255, 255, 255)), [480, 490]) 
  #screen.blit(subInfoFont.render('y0 : ' + str(y0), True, (255, 255, 255)), [480, 510]) 

  x1 = joy.get_axis(3)
  y1 = joy.get_axis(4)

  pygame.draw.circle(screen, (0,0,255), (595,365),30)
  pygame.draw.circle(screen, (0,0,0), (595,365),29)
  pygame.draw.circle(screen, COLOR_JOY_LEFT, (595 + x0*30 ,365 + y0*30),5)
  
  pygame.draw.circle(screen, (0,255,0),(655,365),30)
  pygame.draw.circle(screen, (0,0,0),(655,365),29)
  pygame.draw.circle(screen, COLOR_JOY_RIGHT,(655 + x1*30 ,365 + y1*30),5)

    #screen.blit(subInfoFont.render('x0(j2) : ' + str(joy2x0), True, (255, 255, 255)), [480, 550]) 
    #screen.blit(subInfoFont.render('y0(j2) : ' + str(joy2y0), True, (255, 255, 255)), [480, 570])

  #P1加速設定
  if joy.get_button(9) == 0:
    sp0 = 3
    if p1_stamina < STAMINA_MAX: p1_stamina = p1_stamina + 2
  elif status != 'p1keep':
    if p1_stamina > 0:
      sp0 = 5
      p1_stamina = p1_stamina - 4 
      if p1_stamina < 0: p1_stamina = 0
    else:
      sp0 = 3
  else:
    if p1_stamina < STAMINA_MAX: p1_stamina = p1_stamina + 2

  #P2加速設定
  if joy.get_button(10) == 0:
    sp1 = 3
    if p2_stamina < STAMINA_MAX: p2_stamina = p2_stamina + 2
  elif status != 'p2keep': 
    if p2_stamina > 0:
      sp1 = 5
      p2_stamina = p2_stamina - 4 
      if p2_stamina < 0: p2_stamina = 0
    else:
      sp1 = 3
  else:
    if p2_stamina < STAMINA_MAX: p2_stamina = p2_stamina + 2
 
  p1Array = np.array(p1_pos)
  p2Array = np.array(p2_pos)
  p3Array = np.array(p3_pos)
  p4Array = np.array(p4_pos)

  #P1移動
  if status != 'p1keep' and status != 'getPoint':
    next_p1_pos = [0,0]
    next_p1_pos[0] = p1_pos[0] + x0*sp0
    next_p1_pos[1] = p1_pos[1] + y0*sp0

    if status == 'p2keep':
      p12norm = np.linalg.norm(np.array(next_p1_pos) - p2Array) - BALL_RADIUS * 2
    else:
      p12norm = np.linalg.norm(np.array(next_p1_pos) - p2Array) 

    p13norm = np.linalg.norm(np.array(next_p1_pos) - p3Array) 
    p14norm = np.linalg.norm(np.array(next_p1_pos) - p4Array) 

    if p12norm > P_RADIUS * 2 and p13norm  > P_RADIUS * 2 and p14norm  > P_RADIUS * 2:
      p1_pos[0] = p1_pos[0] + x0*sp0
      p1_pos[1] = p1_pos[1] + y0*sp0
 
  #P2移動
  if status != 'p2keep' and status != 'getPoint':
    next_p2_pos = [0,0]
    next_p2_pos[0] = p2_pos[0] + x1*sp1
    next_p2_pos[1] = p2_pos[1] + y1*sp1

    if status == 'p1keep':
      p21norm = np.linalg.norm(np.array(next_p2_pos) - p1Array) - BALL_RADIUS * 2
    else:
      p21norm = np.linalg.norm(np.array(next_p2_pos) - p1Array) 

    p23norm = np.linalg.norm(np.array(next_p2_pos) - p3Array) 
    p24norm = np.linalg.norm(np.array(next_p2_pos) - p4Array) 

    if p21norm > P_RADIUS * 2 and p23norm > P_RADIUS * 2 and p24norm > P_RADIUS * 2:
      p2_pos[0] = p2_pos[0] + x1*sp1
      p2_pos[1] = p2_pos[1] + y1*sp1

  #P3移動
  if user2InputMode == InputMode.PAD:
    joy2x0 = joy2.get_axis(0)
    joy2y0 = joy2.get_axis(1)
    joy2x1 = joy2.get_axis(3)
    joy2y1 = joy2.get_axis(4)

  sp3 = 3
  next_p3_pos = [0,0]
  next_p3_pos[0] = p3_pos[0] + joy2x0 * sp3
  next_p3_pos[1] = p3_pos[1] + joy2y0 * sp3

  if status == 'p1keep':
    p31norm = np.linalg.norm(np.array(next_p3_pos) - p1Array) - BALL_RADIUS * 2
  else:
    p31norm = np.linalg.norm(np.array(next_p3_pos) - p1Array)

  if status == 'p2keep':
    p32norm = np.linalg.norm(np.array(next_p3_pos) - p2Array) - BALL_RADIUS * 2
  else:
    p32norm = np.linalg.norm(np.array(next_p3_pos) - p2Array) 

  p34norm = np.linalg.norm(np.array(next_p3_pos) - p4Array) 

  #プレイヤー通しの重複回避処理
  if p31norm > P_RADIUS * 2 and p32norm > P_RADIUS * 2 and p34norm > P_RADIUS * 2:
    p3_pos[0] = p3_pos[0] + joy2x0*sp3
    p3_pos[1] = p3_pos[1] + joy2y0*sp3

    #ディスクをキャッチプレイヤーに他プレイやーが接していた場合、
    #レシーバーから離れるのはOKだが近づくのはNG
  else:
    if status == "p1keep":
      now_p31norm = np.linalg.norm(np.array(p3_pos) - p1Array)
      if P_RADIUS*2 <= now_p31norm and now_p31norm <= P_RADIUS*2 + BALL_RADIUS*2 :
        next_p31norm = np.linalg.norm(np.array(next_p3_pos) - p1Array)
        if next_p31norm > P_RADIUS*2:
          p3_pos[0] = p3_pos[0] + joy2x0*sp3
          p3_pos[1] = p3_pos[1] + joy2y0*sp3

    elif status == "p2keep":
      now_p32norm = np.linalg.norm(np.array(p3_pos) - p2Array)
      if P_RADIUS*2 <= now_p32norm and now_p32norm <= P_RADIUS*2 + BALL_RADIUS*2 :
        next_p32norm = np.linalg.norm(np.array(next_p3_pos) - p2Array)
        if next_p32norm > P_RADIUS*2:
          p3_pos[0] = p3_pos[0] + joy2x0*sp3
          p3_pos[1] = p3_pos[1] + joy2y0*sp3



  #P4移動
  sp4 = 3
  next_p4_pos = [0,0]
  next_p4_pos[0] = p4_pos[0] + joy2x1 * sp4
  next_p4_pos[1] = p4_pos[1] + joy2y1 * sp4

  if status == 'p1keep':
    p41norm = np.linalg.norm(np.array(next_p4_pos) - p1Array) - BALL_RADIUS * 2
  else:
    p41norm = np.linalg.norm(np.array(next_p4_pos) - p1Array)

  if status == 'p2keep':
    p42norm = np.linalg.norm(np.array(next_p4_pos) - p2Array) - BALL_RADIUS * 2
  else:
    p42norm = np.linalg.norm(np.array(next_p4_pos) - p2Array) 

  p43norm = np.linalg.norm(np.array(next_p4_pos) - p3Array) 

  if p41norm > P_RADIUS * 2 and p42norm > P_RADIUS * 2 and p43norm > P_RADIUS * 2:
    p4_pos[0] = p4_pos[0] + joy2x1*sp4
    p4_pos[1] = p4_pos[1] + joy2y1*sp4

    #ディスクをキャッチプレイヤーに他プレイやーが接していた場合、
    #レシーバーから離れるのはOKだが近づくのはNG
  else:
    if status == "p1keep":
      now_p41norm = np.linalg.norm(np.array(p4_pos) - p1Array)
      if P_RADIUS*2 <= now_p41norm and now_p41norm <= P_RADIUS*2 + BALL_RADIUS*2 :
        next_p41norm = np.linalg.norm(np.array(next_p4_pos) - p1Array)
        if next_p41norm > P_RADIUS*2:
          p4_pos[0] = p4_pos[0] + joy2x1*sp4
          p4_pos[1] = p4_pos[1] + joy2y1*sp4

    elif status == "p2keep":
      now_p42norm = np.linalg.norm(np.array(p4_pos) - p2Array)
      if P_RADIUS*2 <= now_p42norm and now_p42norm <= P_RADIUS*2 + BALL_RADIUS*2 :
        next_p42norm = np.linalg.norm(np.array(next_p4_pos) - p2Array)
        if next_p42norm > P_RADIUS*2:
          p4_pos[0] = p4_pos[0] + joy2x1*sp4
          p4_pos[1] = p4_pos[1] + joy2y1*sp4

 
  screen.blit(subInfoFont.render('debagStatus : ' + debugStatus, True, (255, 255, 255)), [480, 530]) 

  #---------------------------
  #パスのベクトルマーカー制御
  #---------------------------
  isExistMark = False
  if status == 'p1keep' and (NO_PASS_DIS <= abs(x0) or NO_PASS_DIS <= abs(y0)):
    passMarkerPos[0] = p1_pos[0] + x0 * MARKER_SPEED
    passMarkerPos[1] = p1_pos[1] + y0 * MARKER_SPEED
    markColor = COLOR_JOY_LEFT

    drawMarkPass()
    isExistMark = True
  if status == 'p2keep' and (NO_PASS_DIS <= abs(x1) or NO_PASS_DIS <= abs(y1)):
    passMarkerPos[0] = p2_pos[0] + x1 * MARKER_SPEED
    passMarkerPos[1] = p2_pos[1] + y1 * MARKER_SPEED
    markColor = COLOR_JOY_RIGHT
    drawMarkPass()
    isExistMark = True
 
  if status == 'p1pass' or status == 'p2pass':
    markColor = COLOR_JOY_STOP
    drawMarkPass()

  #--------
  #パス処理
  #--------
  if(joy.get_button(4) == 1 or joy.get_button(5)) == 1 and isExistMark:
    ballPassPosX = ball_pos[0]
    ballPassPosY = ball_pos[1]
    ballMoveDistance = [(passMarkerPos[0] - ball_pos[0]) /20,(passMarkerPos[1] - ball_pos[1])/20]
    if (status == 'p1keep'): status = "p1pass"
    elif (status =='p2keep'): status = "p2pass"
      
  #---------------------
  #ボールコート外判定
  #---------------------
  if status == 'p1pass' or status == 'p2pass':
    if ballPassPosX + BALL_RADIUS < INIT_X or \
       ballPassPosY + BALL_RADIUS < INIT_Y or \
       ballPassPosX - BALL_RADIUS > INIT_X + FIELD_WIDTH or \
       ballPassPosY - BALL_RADIUS > INIT_Y + FIELD_HEIGHT:
      status = 'offCourt'

  #---------------------------
  #ボールの描画(ゲーム終了時)
  #---------------------------
  if status == 'offCourt' or status == "interception":
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
  
  #自キャラの描画
  if status == 'p1keep' or status == 'getPoint': 
    pygame.draw.circle(screen, COLOR_JOY_STOP, p1_pos , P_RADIUS)
  else:
    pygame.draw.circle(screen, COLOR_JOY_LEFT, p1_pos , P_RADIUS)

  if status == 'p2keep' or status == 'getPoint': 
    pygame.draw.circle(screen, COLOR_JOY_STOP, p2_pos , P_RADIUS)
  else:
    pygame.draw.circle(screen, COLOR_JOY_RIGHT, p2_pos , P_RADIUS)

  #P3の描画
  pygame.draw.circle(screen, COLOR_DIFENSE, p3_pos , P_RADIUS)
  pygame.draw.circle(screen, COLOR_DIFENSE, p4_pos , P_RADIUS)

  #---------------------
  #ボールの描画(パス中)
  #---------------------
  if status == "p1pass" or status == "p2pass" :
    ballPassPosX = ballPassPosX + ballMoveDistance[0] 
    ballPassPosY = ballPassPosY + ballMoveDistance[1] 
    pygame.draw.circle(screen, (255,255,255), [ballPassPosX,ballPassPosY] , BALL_RADIUS)

  #---------------------
  #ボールのカット判定
  #---------------------
  if status == "p1pass" or status == "p2pass" :
    ballArray = np.array([ballPassPosX, ballPassPosY])

    p3Array = np.array(p3_pos)
    p3norm = np.linalg.norm(p3Array - ballArray) 
    if p3norm <= BALL_RADIUS + P_RADIUS: status = "interception"
      
    p4Array = np.array(p4_pos)
    p4norm = np.linalg.norm(p4Array - ballArray) 
    if p4norm <= BALL_RADIUS + P_RADIUS: status = "interception"

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

      #--------------------------------
      #キーボードによる移動処理(P3,4)
      #--------------------------------
      if pygame.key.name(event.key) == 's' or pygame.key.name(event.key) == 'a':
        p3_pos[0] = p3_pos[0] - 10 
      elif pygame.key.name(event.key) == 'f':
        p3_pos[0] = p3_pos[0] + 10 
      elif pygame.key.name(event.key) == 'e':
        p3_pos[1] = p3_pos[1] - 10 
      elif pygame.key.name(event.key) == 'd':
        p3_pos[1] = p3_pos[1] + 10 

      elif pygame.key.name(event.key) == 'j':
        p4_pos[0] = p4_pos[0] - 10 
      elif pygame.key.name(event.key) == ';' or pygame.key.name(event.key) == 'l':
        p4_pos[0] = p4_pos[0] + 10 
      elif pygame.key.name(event.key) == 'i':
        p4_pos[1] = p4_pos[1] - 10 
      elif pygame.key.name(event.key) == 'k':
        p4_pos[1] = p4_pos[1] + 10 
