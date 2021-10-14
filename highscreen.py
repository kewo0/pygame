import pygame
from entities import HighScoreScreen,Xbtn


#Just simple display of objects from entities script
class HighScreen(object):
    HIGHSCORE_IMG = pygame.image.load("highscore_empty.png")
    XBTN_IMG = pygame.image.load("x_btn.png")

    def __init__(self,screen,score, timestamp):
        self.frame = 0
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()
        self.score = score
        self.timestamp = timestamp
        self.state = "imhigh"

        self.highscorescreen = HighScoreScreen(self,self.score,self.timestamp)
        self.x_btn = Xbtn(self, self.highscorescreen.w,self.highscorescreen.h)

    def update(self):
        self.highscorescreen.update()
        self.x_btn.update()

        if self.x_btn.state == "highded":
            self.state = "imdown"

        self.highscorescreen.draw()
        self.x_btn.draw()