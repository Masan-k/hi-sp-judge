import CommonConst as common
import math
MARKER_SPEED = 100;
NO_PASS_DIS = 0.1
NO_MOVE_DIS = 0.05

class ball:
  def __init__(self,py, sc):
    self.pygame = py
    self.screen = sc
    self.joyCount = py.joystick.get_count()

    if self.joyCount == 1:
      self.joy1 = py.joystick.Joystick(0)
      self.joy1.init()
 
  def init(self):
    self.passMarkerPos = [300,500]
    self.ball_pos = [150,150]
    self.isExistMark = False
 
  def drawMarkPass(self):
    self.pygame.draw.line(self.screen,self.markColor,(self.passMarkerPos[0]-10,self.passMarkerPos[1]-10),(self.passMarkerPos[0]+10,self.passMarkerPos[1]+10))
    self.pygame.draw.line(self.screen,self.markColor,(self.passMarkerPos[0]+10,self.passMarkerPos[1]-10),(self.passMarkerPos[0]-10,self.passMarkerPos[1]+10))

  def initPass(self):
    #self.ballPassPosX = self.ball_pos[0]
    #self.ballPassPosY = self.ball_pos[1]
    self.ballMoveDistance = [(self.passMarkerPos[0] - self.ball_pos[0]) /20,(self.passMarkerPos[1] - self.ball_pos[1])/20]

  def updatePass(self):
    #self.ballPassPosX = self.ballPassPosX + self.ballMoveDistance[0] 
    #self.ballPassPosY = self.ballPassPosY + self.ballMoveDistance[1] 
    #self.pygame.draw.circle(self.screen, (255,255,255), [self.ballPassPosX,self.ballPassPosY] , common.BALL_RADIUS)
    self.ball_pos[0] = self.ball_pos[0] + self.ballMoveDistance[0] 
    self.ball_pos[1] = self.ball_pos[1] + self.ballMoveDistance[1] 
    self.pygame.draw.circle(self.screen, (255,255,255), [self.ball_pos[0],self.ball_pos[1]] , common.BALL_RADIUS)

  #---------------------------------
  #ボールの描画(保持時)
  #---------------------------------
  def updateKeep(self,status,player):
    #マウス座標の取得
    if status == 'p1keep': pPos = player.p1_pos
    elif status == 'p2keep': pPos = player.p2_pos

    if self.passMarkerPos[0] - pPos[0] != 0:
      cos = math.cos(math.atan((pPos[1] - self.passMarkerPos[1])/(self.passMarkerPos[0]  - pPos[0])))
      ballX = cos * (common.P_RADIUS + common.BALL_RADIUS)
    else: ballX = 0
       
    if self.passMarkerPos[0] - pPos[0] != 0:
      sin = math.sin(math.atan((pPos[1] - self.passMarkerPos[1])/(self.passMarkerPos[0] - pPos[0])))
      ballY = sin * (common.P_RADIUS + common.BALL_RADIUS)
    else: ballY = 0
        
    if self.passMarkerPos[0] - pPos[0] < 0: 
      ballX = -ballX
      ballY = -ballY

    self.ball_pos[0] = pPos[0] + ballX
    self.ball_pos[1] = pPos[1] - ballY
    self.pygame.draw.circle(self.screen, (255,255,255), self.ball_pos , common.BALL_RADIUS)
    
   
  def updatePassMarker(self,status,player):
    x0 = self.joy1.get_axis(0)
    y0 = self.joy1.get_axis(1)

    x1 = self.joy1.get_axis(3)
    y1 = self.joy1.get_axis(4)

    #パスマーカーの表示
    self.isExistMark = False
    if status == 'p1keep' and (NO_PASS_DIS <= abs(x0) or NO_PASS_DIS <= abs(y0)):
      self.passMarkerPos[0] = player.p1_pos[0] + x0 * MARKER_SPEED
      self.passMarkerPos[1] = player.p1_pos[1] + y0 * MARKER_SPEED
      self.markColor = common.COLOR_JOY_LEFT

      self.drawMarkPass()
      self.isExistMark = True
    if status == 'p2keep' and (NO_PASS_DIS <= abs(x1) or NO_PASS_DIS <= abs(y1)):
      self.passMarkerPos[0] = player.p2_pos[0] + x1 * MARKER_SPEED
      self.passMarkerPos[1] = player.p2_pos[1] + y1 * MARKER_SPEED
      self.markColor = common.COLOR_JOY_RIGHT
      self.drawMarkPass()
      self.isExistMark = True
   
    if status == 'p1pass' or status == 'p2pass':
      self.markColor = common.COLOR_JOY_STOP
      self.drawMarkPass()

