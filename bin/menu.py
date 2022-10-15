import pygame
import pygame.locals
import sys

SELECT_COLOR = (255,127,80)
KEEP_COLOR = (255,255,255)

CURSOR_WIDTH = 60 
CURSOR_WIDTH_LONG = 93 
CURCOR_THICKNESS = 3

BTN_HEIGHT = 32
START_POS_D1 = (170,250+BTN_HEIGHT)
START_POS_D2 = (170,350+BTN_HEIGHT)

class menu:

  def __init__(self,py, sc):
    self.pygame = py
    self.screen = sc
    self.joyCount = py.joystick.get_count()

    self.FONT_TITLE = py.font.SysFont("purisa",50)
    self.FONT_SELECT = py.font.SysFont("ubuntumono",30)
    self.FONT_RUN = py.font.SysFont("chilanka",40)

    self.cursorCol = 1
    self.cursorRow = 1
    self.cursorColD1 = 1
    self.cursorColD2 = 1

    self.status = "run"

    if self.joyCount == 1:
      self.joy1 = py.joystick.Joystick(0)
      self.joy1.init()

  def update(self):
    self.screen.fill((0,0,0))
    self.screen.blit(self.FONT_TITLE.render('TWO VS TWO', True, (255, 255, 255)), [200, 50]) 

    self.screen.blit(self.FONT_SELECT.render('D1:', True, (255, 255, 255)), [70, 250]) 
    self.screen.blit(self.FONT_SELECT.render('NONE', True, (255, 255, 255)), [170, 250]) 
    self.screen.blit(self.FONT_SELECT.render('MARK', True, (255, 255, 255)), [270, 250]) 
    self.screen.blit(self.FONT_SELECT.render('ZONE', True, (255, 255, 255)), [370, 250]) 

    self.screen.blit(self.FONT_SELECT.render('D2:', True, (255, 255, 255)), [70, 350]) 
    self.screen.blit(self.FONT_SELECT.render('NONE', True, (255, 255, 255)), [170, 350]) 
    self.screen.blit(self.FONT_SELECT.render('MARK', True, (255, 255, 255)), [270, 350]) 
    self.screen.blit(self.FONT_SELECT.render('ZONE', True, (255, 255, 255)), [370, 350]) 
    self.screen.blit(self.FONT_RUN.render('PLAY', True, (255, 255, 255)), [350, 500]) 
    
    for event in self.pygame.event.get():
      if event.type == self.pygame.locals.KEYDOWN: 
        if event.key == self.pygame.locals.K_ESCAPE:
          self.pygame.quit()
          sys.exit()

        if event.key == self.pygame.locals.K_LEFT:
          if self.cursorCol > 1 and self.cursorRow < 3:
            self.cursorCol = self.cursorCol - 1 
            if self.cursorRow == 1:self.cursorColD1 = self.cursorCol
            elif self.cursorRow == 2:self.cursorColD2 = self.cursorCol

        if event.key == self.pygame.locals.K_RIGHT:
          if self.cursorCol < 3 and self.cursorRow < 3:
            self.cursorCol = self.cursorCol + 1 
            if self.cursorRow == 1:self.cursorColD1 = self.cursorCol
            elif self.cursorRow == 2:self.cursorColD2 = self.cursorCol

        if event.key == self.pygame.locals.K_UP:
          if self.cursorRow > 1:
            self.cursorRow = self.cursorRow - 1

          if self.cursorRow == 1:
            self.cursorCol = self.cursorColD1

        if event.key == self.pygame.locals.K_DOWN:
          if self.cursorRow < 3:
            self.cursorRow = self.cursorRow + 1
          elif self.cursorRow == 2:
            self.cursorRow = self.cursorRow + 1

          if self.cursorRow == 2:
            self.cursorCol = self.cursorColD2

        if event.key == self.pygame.locals.K_RETURN:
          self.status = "decision"

    self.screen.blit(self.FONT_RUN.render('cursorRow >> ' + str(self.cursorRow), True, (255, 255, 255)), [500, 500]) 
    self.screen.blit(self.FONT_RUN.render('cursorCol >> ' + str(self.cursorCol), True, (255, 255, 255)), [500, 550]) 
    
    if self.cursorRow == 3:
      self.pygame.draw.line(self.screen, SELECT_COLOR, (350, 500+40), (350 + CURSOR_WIDTH_LONG ,500+40), width = CURCOR_THICKNESS)

    if self.cursorRow == 1:
      colorD1 = SELECT_COLOR
      colorD2 = KEEP_COLOR
    elif self.cursorRow == 2:
      colorD1 = KEEP_COLOR
      colorD2 = SELECT_COLOR
    elif self.cursorRow == 3:
      colorD1 = KEEP_COLOR
      colorD2 = KEEP_COLOR
    else:
      print("Value error coursorRow >> " + self.cursorRow)

    cursorXd1 = START_POS_D1[0]+(self.cursorColD1-1)*100
    cursorYd1 = START_POS_D1[1]
    self.pygame.draw.line(self.screen, colorD1, (cursorXd1, cursorYd1), (cursorXd1 + CURSOR_WIDTH ,cursorYd1), width = CURCOR_THICKNESS)

    cursorXd2 = START_POS_D2[0]+(self.cursorColD2-1)*100
    cursorYd2 = START_POS_D2[1]
    self.pygame.draw.line(self.screen, colorD2, (cursorXd2, cursorYd2), (cursorXd2 + CURSOR_WIDTH ,cursorYd2), width = CURCOR_THICKNESS)
