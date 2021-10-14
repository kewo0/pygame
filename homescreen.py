import pygame
from entities import Button

class HomeScreen(object):
    BTN_START = pygame.image.load("btn_start.png")
    BTN_HIGHSCORE = pygame.image.load("btn_highscore.png")
    BTN_EXIT = pygame.image.load("btn_exit.png")
    

    def __init__ (self,screen):
        self.frame = 0
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()
        self.state = "home" # "startgame", "highscore", "exitgame"

        self.btn_start = Button(self, "startbtn")
        self.btn_highscore = Button(self, "highscorebtn")
        self.btn_exit = Button(self, "exitbtn")

    def update(self):
        self.btn_start.update()
        self.btn_highscore.update()
        self.btn_exit.update()

        #Whole logic behind buttons, basicly changes the state of homescreen based on predefined states in the buttons,
        if self.btn_start.didiclick_start:
            self.state = self.btn_start.state
            self.btn_start.didiclick_start = False
        elif self.btn_highscore.didiclick_highscore:
            self.state = self.btn_highscore.state
            self.btn_highscore.didiclick_highscore = False
        elif self.btn_exit.didiclick_exit:
            self.state = self.btn_exit.state
            self.btn_exit.didiclick_exit = False

        self.btn_start.draw()
        self.btn_highscore.draw()
        self.btn_exit.draw()
