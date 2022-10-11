

class field:

  START_X = 50
  START_Y = 50
  WIDTH = 400
  HEIGHT = 500
  GOAL_ARIA = 150

  def __init__(self, py ,sc):
    self.pygame = py
    self.screen = sc

  def draw(self):

    self.pygame.draw.line(self.screen, (255,255,255), (self.START_X, self.START_Y), (self.START_X + self.WIDTH, self.START_Y))
    self.pygame.draw.line(self.screen, (255,255,255), (self.START_X + self.WIDTH, self.START_Y), (self.START_X + self.WIDTH, self.START_Y + self.HEIGHT))
    self.pygame.draw.line(self.screen, (255,255,255), (self.START_X + self.WIDTH, self.START_Y + self.HEIGHT), (self.START_X, self.START_Y + self.HEIGHT))
    self.pygame.draw.line(self.screen, (255,255,255), (self.START_X, self.START_Y + self.HEIGHT), (self.START_X, self.START_Y))

    self.pygame.draw.line(self.screen, (255,255,255), (self.START_X, self.START_Y + self.GOAL_ARIA), (self.START_X + self.WIDTH , self.START_Y + self.GOAL_ARIA))
    self.pygame.draw.rect(self.screen, (0,0,255), (self.START_X + 2 , self.START_Y + 2, self.WIDTH - 3 , self.GOAL_ARIA - 3))
    self.pygame.draw.rect(self.screen, (0,0,0), (self.START_X + 4 , self.START_Y + 4, self.WIDTH - 7 , self.GOAL_ARIA - 7))
   
