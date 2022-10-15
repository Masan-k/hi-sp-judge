import sys
import pygame
from pygame.locals import *
 
pygame.init()
width = 1200
height = 700
surface = pygame.display.set_mode((width, height))
list = []
for x in pygame.font.get_fonts(): 
  list.append(x)

while True:
  rowCount = 1
  colCount = 1
  surface.fill((0,0,0))
  for i in range(len(list)):
    surface.blit(pygame.font.SysFont(list[i], 20).render(str(i) + ":" + list[i], True, (255, 255, 255)), [colCount*150-120,rowCount*30]) 
    if rowCount*30 >= height-100:
      colCount = colCount +1
      rowCount = 1
    rowCount = rowCount+1

    if i == 127: break
  pygame.display.update()

  for event in pygame.event.get():
    if event.type == pygame.locals.KEYDOWN: 
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()

