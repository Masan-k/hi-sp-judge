import CommonConst as common
#------------
#情報表示
#------------
class info:
  def __init__(self,py, sc):
    self.pygame = py
    self.screen = sc
    self.joyCount = py.joystick.get_count()

    if self.joyCount == 1:
      self.joy1 = py.joystick.Joystick(0)
      self.joy1.init()

    elif self.joyCount == 2:
      self.joy1 = py.joystick.Joystick(0)
      self.joy1.init()

      self.joy2 = py.joystick.Joystick(1)
      self.joy2.init()

  def draw(self,status,stageCode,stageName):

    #ステージ＆ステータス
    self.screen.blit(common.FONT_MAIN.render('STAGE', True, (255, 255, 255)), [470, 80]) 
    dispStatus = ""
    dispColor = [0,0,0] 
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

    self.screen.blit(common.FONT_MAIN.render('STAGE', True, (255, 255, 255)), [470, 80]) 
    self.screen.blit(common.FONT_MAIN.render(' : ' + stageCode + "." + stageName, True, (255, 255, 255)), [550, 80]) 

    self.screen.blit(common.FONT_MAIN.render('STATUS', True, (255, 255, 255)), [470, 120]) 
    self.screen.blit(common.FONT_MAIN.render(dispStatus, True, dispColor), [550, 120]) 

    #ゲームパッド
    self.pygame.draw.rect(self.screen, (255,255,255),(500,180,250,250))
    self.pygame.draw.rect(self.screen, (0,0,0),(501,181,248,248))

    #pygame.draw.rect(screen, (255,255,255),(525,200,200,200)) #base
    self.pygame.draw.rect(self.screen, (255,255,255),(525,250,40,150))
    self.pygame.draw.rect(self.screen, (0,0,0),(526,251,38,148))
    self.pygame.draw.rect(self.screen, (255,255,255),(685,250,40,150))
    self.pygame.draw.rect(self.screen, (0,0,0),(686,251,38,148))
    
    self.pygame.draw.rect(self.screen, (255,255,255),(525,250,200,80))
    self.pygame.draw.rect(self.screen, (0,0,0),(526,251,198,78))

    #十字キー
    self.pygame.draw.line(self.screen, (255,255,255), (565, 270), (565, 310))
    self.pygame.draw.line(self.screen, (255,255,255), (545, 290), (585, 290))

    #ボタン(ABXY)
    BTN_DIS = 18
    self.pygame.draw.circle(self.screen, (255,255,255), (685-BTN_DIS,290),10)
    self.pygame.draw.circle(self.screen, (0,0,0), (685-BTN_DIS,290),9)
    self.pygame.draw.circle(self.screen, (255,255,255), (685,290-BTN_DIS),10)
    self.pygame.draw.circle(self.screen, (0,0,0), (685,290-BTN_DIS),9)
    self.pygame.draw.circle(self.screen, (255,255,255), (685+BTN_DIS,290),10)
    self.pygame.draw.circle(self.screen, (0,0,0), (685+BTN_DIS,290),9)
    self.pygame.draw.circle(self.screen, (255,255,255), (685,290+BTN_DIS),10)
    self.pygame.draw.circle(self.screen, (0,0,0), (685,290+BTN_DIS),9)

    #スタートボタン
    self.pygame.draw.rect(self.screen, (255,200,200), (595,280,60,15))
    self.pygame.draw.rect(self.screen, (0,0,0), (596,281,58,13))
    self.screen.blit(common.FONT_SUB.render('RESTART', True, (255, 200, 200)), [600, 280]) 

    #ボタン（RL)
    self.screen.blit(common.FONT_MAIN.render('INFO : INPUT', True, (255, 255, 255)), [565, 190]) 
    self.pygame.draw.rect(self.screen, (255,255,255),(545,230,50,20))
    self.pygame.draw.rect(self.screen, (0,0,0),(546,231,48,18))
    self.pygame.draw.rect(self.screen, (0,255,255),(655,230,50,20))
    self.pygame.draw.rect(self.screen, (0,0,0),(656,231,48,18))
    self.screen.blit(common.FONT_SUB.render('PASS', True, (0, 255, 255)), [665, 232]) 

    #TIPS
    self.screen.blit(common.FONT_SUB.render('TIPS : ', True, (255, 255, 255)), [480, 450]) 
    self.screen.blit(common.FONT_SUB.render('Stage selection is a numerical input on the keyboard.', True, (255, 255, 255)), [480, 470]) 

    #----------------
    # joystickの描画
    #----------------
    if self.joyCount >= 1:
      x0 = self.joy1.get_axis(0)
      y0 = self.joy1.get_axis(1)

      x1 = self.joy1.get_axis(3)
      y1 = self.joy1.get_axis(4)

      self.pygame.draw.circle(self.screen, (0,0,255), (595,365),30)
      self.pygame.draw.circle(self.screen, (0,0,0), (595,365),29)
      self.pygame.draw.circle(self.screen, common.COLOR_JOY_LEFT, (595 + x0*30 ,365 + y0*30),5)
      
      self.pygame.draw.circle(self.screen, (0,255,0),(655,365),30)
      self.pygame.draw.circle(self.screen, (0,0,0),(655,365),29)
      self.pygame.draw.circle(self.screen, common.COLOR_JOY_RIGHT,(655 + x1*30 ,365 + y1*30),5)

