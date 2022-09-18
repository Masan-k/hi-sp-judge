import pygame,sys
import pygame.locals

pygame.init()
joy = pygame.joystick.Joystick(0)      
joy.init()

SCREEN_SIZE = (800, 600)
FIELD_WIDTH = 600
FIELD_HEIGHT = 400

screen = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.Font(None,30)

while True:
  pygame.display.update()
  screen.fill((0,0,0))
  x0 = joy.get_axis(0)*100
  y0 = joy.get_axis(1)*100

  x1 = joy.get_axis(3)*100
  y1 = joy.get_axis(4)*100

  screen.blit(font.render('joy.get_axis(0) : ' + str(x0) , True, (255, 255, 255)), [10, 10]) 
  screen.blit(font.render('joy.get_axis(1) : ' + str(y0) , True, (255, 255, 255)), [10, 30]) 

  pygame.draw.rect(screen,(100,100,100),(100,100,200,200))
  pygame.draw.circle(screen,(255,0,0),(200 + x0 ,200 + y0),10)
  
  pygame.draw.rect(screen,(100,100,100),(400,100,200,200))
  pygame.draw.circle(screen,(255,0,0),(500 + x1 ,200 + y1),10)

  screen.blit(font.render('joy.get_button(4) : ' + str(joy.get_button(4)) , True, (255, 255, 255)), [10, 50]) 
  screen.blit(font.render('joy.get_button(5) : ' + str(joy.get_button(5)) , True, (255, 255, 255)), [10, 70]) 
  
  #キー入力処理
  for event in pygame.event.get():
    if event.type == pygame.locals.KEYDOWN: 
      #終了処理
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()
