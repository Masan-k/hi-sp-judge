import CommonConst as common
import numpy as np
from enum import Enum
STAMINA_MAX = 100
class InputMode(Enum):
  PAD = 1
  KEY = 2

class player:


  def __init__(self,py, sc):
    self.pygame = py
    self.screen = sc
    self.joyCount = py.joystick.get_count()

    if self.joyCount == 1:
      self.joy1 = py.joystick.Joystick(0)
      self.joy1.init()
      self.user2InputMode = InputMode.KEY 

    elif self.joyCount == 2:
      self.joy1 = py.joystick.Joystick(0)
      self.joy1.init()

      self.joy2 = py.joystick.Joystick(1)
      self.joy2.init()
      self.user2InputMode = InputMode.PAD

  def init(self):
    self.p1_pos = [100,500]
    self.p3_pos = [100,400]

    self.p2_pos = [400,500]
    self.p4_pos = [400,400]
    
    self.p1_stamina = 100
    self.p2_stamina = 100

  def update(self, status):
    x0 = self.joy1.get_axis(0)
    y0 = self.joy1.get_axis(1)

    x1 = self.joy1.get_axis(3)
    y1 = self.joy1.get_axis(4)

    #P1加速設定
    if self.joy1.get_button(9) == 0:
      sp0 = 3
      if self.p1_stamina < STAMINA_MAX: self.p1_stamina = self.p1_stamina + 2
    elif status != 'p1keep':
      if self.p1_stamina > 0:
        sp0 = 5
        self.p1_stamina = self.p1_stamina - 4 
        if self.p1_stamina < 0: self.p1_stamina = 0
      else:
        sp0 = 3
    else:
      if self.p1_stamina < STAMINA_MAX: self.p1_stamina = self.p1_stamina + 2

    #P2加速設定
    if self.joy1.get_button(10) == 0:
      sp1 = 3
      if self.p2_stamina < STAMINA_MAX: self.p2_stamina = self.p2_stamina + 2
    elif status != 'p2keep': 
      if self.p2_stamina > 0:
        sp1 = 5
        self.p2_stamina = self.p2_stamina - 4 
        if self.p2_stamina < 0: self.p2_stamina = 0
      else:
        sp1 = 3
    else:
      if self.p2_stamina < STAMINA_MAX: self.p2_stamina = self.p2_stamina + 2

    #体力ゲージの表示
    self.pygame.draw.rect(self.screen, common.COLOR_JOY_LEFT,(526,330,38, 69))
    self.pygame.draw.rect(self.screen, (0,0,0),(526,330,38, 69 * (STAMINA_MAX-self.p1_stamina)/100))
    self.pygame.draw.rect(self.screen, common.COLOR_JOY_RIGHT,(686,330,38, 69))
    self.pygame.draw.rect(self.screen, (0,0,0),(686,330,38, 69 * (STAMINA_MAX-self.p2_stamina)/100))
    
    p1Array = np.array(self.p1_pos)
    p2Array = np.array(self.p2_pos)
    p3Array = np.array(self.p3_pos)
    p4Array = np.array(self.p4_pos)

    #P1移動
    if status != 'p1keep' and status != 'getPoint':
      next_p1_pos = [0,0]
      next_p1_pos[0] = self.p1_pos[0] + x0*sp0
      next_p1_pos[1] = self.p1_pos[1] + y0*sp0

      if status == 'p2keep':
        p12norm = np.linalg.norm(np.array(next_p1_pos) - p2Array) - common.BALL_RADIUS * 2
      else:
        p12norm = np.linalg.norm(np.array(next_p1_pos) - p2Array) 

      p13norm = np.linalg.norm(np.array(next_p1_pos) - p3Array) 
      p14norm = np.linalg.norm(np.array(next_p1_pos) - p4Array) 

      if p12norm > common.P_RADIUS * 2 and p13norm  > common.P_RADIUS * 2 and p14norm  > common.P_RADIUS * 2:
        self.p1_pos[0] = self.p1_pos[0] + x0*sp0
        self.p1_pos[1] = self.p1_pos[1] + y0*sp0
   
    #P2移動
    if status != 'p2keep' and status != 'getPoint':
      next_p2_pos = [0,0]
      next_p2_pos[0] = self.p2_pos[0] + x1*sp1
      next_p2_pos[1] = self.p2_pos[1] + y1*sp1

      if status == 'p1keep':
        p21norm = np.linalg.norm(np.array(next_p2_pos) - p1Array) - common.BALL_RADIUS * 2
      else:
        p21norm = np.linalg.norm(np.array(next_p2_pos) - p1Array) 

      p23norm = np.linalg.norm(np.array(next_p2_pos) - p3Array) 
      p24norm = np.linalg.norm(np.array(next_p2_pos) - p4Array) 

      if p21norm > common.P_RADIUS * 2 and p23norm > common.P_RADIUS * 2 and p24norm > common.P_RADIUS * 2:
        self.p2_pos[0] = self.p2_pos[0] + x1*sp1
        self.p2_pos[1] = self.p2_pos[1] + y1*sp1

    #自キャラの描画
    if status == 'p1keep' or status == 'getPoint': 
      self.pygame.draw.circle(self.screen, common.COLOR_JOY_STOP, self.p1_pos , common.P_RADIUS)
    else:
      self.pygame.draw.circle(self.screen, common.COLOR_JOY_LEFT, self.p1_pos , common.P_RADIUS)

    if status == 'p2keep' or status == 'getPoint': 
      self.pygame.draw.circle(self.screen, common.COLOR_JOY_STOP, self.p2_pos , common.P_RADIUS)
    else:
      self.pygame.draw.circle(self.screen, common.COLOR_JOY_RIGHT, self.p2_pos , common.P_RADIUS)


    if self.user2InputMode == InputMode.PAD:
      #P3
      joy2x0 = self.joy2.get_axis(0)
      joy2y0 = self.joy2.get_axis(1)
      joy2x1 = self.joy2.get_axis(3)
      joy2y1 = self.joy2.get_axis(4)

      sp3 = 3
      next_p3_pos = [0,0]
      next_p3_pos[0] = self.p3_pos[0] + joy2x0 * sp3
      next_p3_pos[1] = self.p3_pos[1] + joy2y0 * sp3

      if status == 'p1keep':
        p31norm = np.linalg.norm(np.array(next_p3_pos) - p1Array) - common.BALL_RADIUS * 2
      else:
        p31norm = np.linalg.norm(np.array(next_p3_pos) - p1Array)

      if status == 'p2keep':
        p32norm = np.linalg.norm(np.array(next_p3_pos) - p2Array) - common.BALL_RADIUS * 2
      else:
        p32norm = np.linalg.norm(np.array(next_p3_pos) - p2Array) 

      p34norm = np.linalg.norm(np.array(next_p3_pos) - p4Array) 

      #プレイヤー通しの重複回避処理
      if p31norm > common.P_RADIUS * 2 and p32norm > common.P_RADIUS * 2 and p34norm > common.P_RADIUS * 2:
        self.p3_pos[0] = self.p3_pos[0] + joy2x0*sp3
        self.p3_pos[1] = self.p3_pos[1] + joy2y0*sp3

        #ディスクをキャッチプレイヤーに他プレイやーが接していた場合、
        #レシーバーから離れるのはOKだが近づくのはNG
      else:
        if status == "p1keep":
          now_p31norm = np.linalg.norm(np.array(self.p3_pos) - p1Array)
          if common.P_RADIUS*2 <= now_p31norm and now_p31norm <= common.P_RADIUS*2 + common.BALL_RADIUS*2 :
            next_p31norm = np.linalg.norm(np.array(next_p3_pos) - p1Array)
            if common.next_p31norm > common.P_RADIUS*2:
              self.p3_pos[0] = self.p3_pos[0] + joy2x0*sp3
              self.p3_pos[1] = self.p3_pos[1] + joy2y0*sp3

        elif status == "p2keep":
          now_p32norm = np.linalg.norm(np.array(self.p3_pos) - p2Array)
          if common.P_RADIUS*2 <= now_p32norm and now_p32norm <= common.P_RADIUS*2 + common.BALL_RADIUS*2 :
            next_p32norm = np.linalg.norm(np.array(next_p3_pos) - p2Array)
            if next_p32norm > common.P_RADIUS*2:
              self.p3_pos[0] = self.p3_pos[0] + joy2x0*sp3
              self.p3_pos[1] = self.p3_pos[1] + joy2y0*sp3
      
      #P4移動
      sp4 = 3
      next_p4_pos = [0,0]
      next_p4_pos[0] = self.p4_pos[0] + joy2x1 * sp4
      next_p4_pos[1] = self.p4_pos[1] + joy2y1 * sp4

      if status == 'p1keep':
        p41norm = np.linalg.norm(np.array(next_p4_pos) - p1Array) - common.BALL_RADIUS * 2
      else:
        p41norm = np.linalg.norm(np.array(next_p4_pos) - p1Array)

      if status == 'p2keep':
        p42norm = np.linalg.norm(np.array(next_p4_pos) - p2Array) - common.BALL_RADIUS * 2
      else:
        p42norm = np.linalg.norm(np.array(next_p4_pos) - p2Array) 

      p43norm = np.linalg.norm(np.array(next_p4_pos) - p3Array) 

      if p41norm > common.P_RADIUS * 2 and p42norm > common.P_RADIUS * 2 and p43norm > common.P_RADIUS * 2:
        self.p4_pos[0] = self.p4_pos[0] + joy2x1*sp4
        self.p4_pos[1] = self.p4_pos[1] + joy2y1*sp4

        #ディスクをキャッチプレイヤーに他プレイやーが接していた場合、
        #レシーバーから離れるのはOKだが近づくのはNG
      else:
        if status == "p1keep":
          now_p41norm = np.linalg.norm(np.array(self.p4_pos) - p1Array)
          if common.P_RADIUS*2 <= now_p41norm and now_p41norm <= common.P_RADIUS*2 + common.BALL_RADIUS*2 :
            next_p41norm = np.linalg.norm(np.array(next_p4_pos) - p1Array)
            if next_p41norm > common.P_RADIUS*2:
              self.p4_pos[0] = self.p4_pos[0] + joy2x1*sp4
              self.p4_pos[1] = self.p4_pos[1] + joy2y1*sp4

        elif status == "p2keep":
          now_p42norm = np.linalg.norm(np.array(p4_pos) - p2Array)
          if common.P_RADIUS*2 <= now_p42norm and now_p42norm <= common.P_RADIUS*2 + common.BALL_RADIUS*2 :
            next_p42norm = np.linalg.norm(np.array(next_p4_pos) - p2Array)
            if next_p42norm > P_RADIUS*2:
              self.p4_pos[0] = self.p4_pos[0] + joy2x1*sp4
              self.p4_pos[1] = self.p4_pos[1] + joy2y1*sp4

    #P3の描画
    self.pygame.draw.circle(self.screen, common.COLOR_DIFENSE, self.p3_pos , common.P_RADIUS)
    self.pygame.draw.circle(self.screen, common.COLOR_DIFENSE, self.p4_pos , common.P_RADIUS)


