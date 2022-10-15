import pygame
import pygame.locals
import sys
import math
import numpy as np
import menu
import info
import field
import player
import ball
import CommonConst as common
debugStatus = "init"
SCREEN_SIZE = (800, 600)

pygame.init()
joyCount = pygame.joystick.get_count()

if joyCount == 0:
  print("Please connect GamePad! (count:" + str(joyCount) + ")")
  exit()
elif joyCount == 1:
  joy = pygame.joystick.Joystick(0)
  joy.init()

else:
  joy = pygame.joystick.Joystick(0)
  joy.init()
  
  joy2 = pygame.joystick.Joystick(1)
  joy2.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("HI-SP-JUDGE")

menu = menu.menu(pygame,screen)
while True:
  screen.fill((0,0,0))
  menu.update()
  pygame.display.update()
  if menu.status == "decision":break

stageCode = ""
stageName = ""

clock= pygame.time.Clock()
  
field = field.field(pygame,screen)
info = info.info(pygame,screen)
player = player.player(pygame,screen)
player.init()
ball = ball.ball(pygame,screen)
ball.init()

status = 'init'

while True:
  screen.fill((0,0,0))
  if joy.get_button(7) == 1: status = 'init' #スタートで初期化
  if status == 'init':
    status = 'p1keep'
    stageCode = '0'
    stageName = 'TUTORIAL'
    player.init()
    ball.init()
    
  field.draw() #コートの描画
  info.draw(status,stageCode,stageName) #情報表示 

  player.update(status) #プレイヤーの更新
  ball.updatePassMarker(status,player) #パス用マーカーの更新

  #---------------------
  #ボールのパス処理
  #---------------------
  if(joy.get_button(4) == 1 or joy.get_button(5)) == 1 and ball.isExistMark:
    ball.initPass()

    if (status == 'p1keep'): status = "p1pass"
    elif (status =='p2keep'): status = "p2pass"

  if status == 'p1keep' or status == 'p2keep':
    ball.updateKeep(status,player)
  if status == "p1pass" or status == "p2pass" :
    ball.updatePass()

  #---------------------
  #ボールコート外判定
  #---------------------
  if status == 'p1pass' or status == 'p2pass':
   if ball.ball_pos[0] + common.BALL_RADIUS < field.START_X or \
       ball.ball_pos[1] + common.BALL_RADIUS < field.START_Y or \
       ball.ball_pos[0] - common.BALL_RADIUS > field.START_X + field.WIDTH or \
       ball.ball_pos[1] - common.BALL_RADIUS > field.START_Y + field.HEIGHT:
       status = 'offCourt'
 
  #---------------------
  #ボールのカット判定
  #---------------------
  if status == "p1pass" or status == "p2pass" :
    ballArray = np.array([ball.ball_pos[0], ball.ball_pos[1]])

    p3Array = np.array(player.p3_pos)
    p3norm = np.linalg.norm(p3Array - ballArray) 
    if p3norm <= common.BALL_RADIUS + common.P_RADIUS:
      status = "interception"
      
    p4Array = np.array(player.p4_pos)
    p4norm = np.linalg.norm(p4Array - ballArray) 
    if p4norm <= common.BALL_RADIUS + common.P_RADIUS:
      status = "interception"

  #---------------------
  #ボールのキャッチ判定
  #---------------------
  if status == 'p1pass' or status == 'p2pass':
    
    playerPos = [9999,9999]
    if status == 'p1pass': playerPos = np.array(player.p2_pos)
    elif status == 'p2pass': playerPos = np.array(player.p1_pos)

    ballPos = np.array([ball.ball_pos[0], ball.ball_pos[1]])
    norm = np.linalg.norm(playerPos - ballPos) 
    if norm <= common.BALL_RADIUS + common.P_RADIUS:
      ball.passMarkerPos[0] = ball.ball_pos[0]
      ball.passMarkerPos[1] = ball.ball_pos[1]

      if status == 'p1pass': status = 'p2keep'
      elif status == 'p2pass': status = 'p1keep'
 
      # 得点判定
      if ball.ball_pos[0] >= field.START_X \
         and ball.ball_pos[0] <= field.START_X + field.WIDTH \
         and ball.ball_pos[1] >= field.START_Y \
         and ball.ball_pos[1] <= field.START_Y + field.GOAL_ARIA:
        status = 'getPoint'

  #ゲーム終了時のボール描画
  if status == 'offCourt' or status == "interception":
    pygame.draw.circle(screen, (255, 0,0), [ball.ball_pos[0],ball.ball_pos[1]] , common.BALL_RADIUS)
  elif status == 'getPoint':
    pygame.draw.circle(screen, (0, 0, 255), [ball.ball_pos[0],ball.ball_pos[1]] , common.BALL_RADIUS)

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
