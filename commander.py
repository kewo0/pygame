#libraries
import os
from datetime import datetime
import pygame
from helpers import *
from homescreen import HomeScreen
from highscreen import HighScreen
from level import Level

def main():
    pygame.font.init()
    pygame.init()
    WELCOME_DURATION = 1250

    win_width = 1600
    win_height = 900
    size = (win_width,win_height)

    BG = load_fig("spacebg1.jpg", size)

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Commander")
    clock = pygame.time.Clock()


    welcome_text = render_text("Watch out for the Enemies!", 96)
    gameover_text = render_text("YOU LOST!", 96)



    state = "mainmenu"
    welcome_timeout = WELCOME_DURATION
    done = False
    dt=0
    current_level = 1
    while not done:

        if state == "game":
            pygame.mouse.set_visible(False)

        else:
            pygame.mouse.set_visible(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        #1.1. Starts up the HomeScreen and changes state to "home"
        if state == "mainmenu":
            #welcome_timeout -=dt
            state="home"
            homescreen = HomeScreen(screen)
        
        #2. Choose: Start game, highscore or exit.
        elif state == "home":

            #Starts the game
            if homescreen.state=="startgame":
                state="game"
                level = Level(screen,current_level)

            #Opens a text file containing timestamp and highscreen, splits them and shoves them in to the list
            #Starts the HighScore screen and passes the list contents to it
            elif homescreen.state=="highscore":
                
                highscore_file = open("highscore.txt", "r")
                splitfilecontent = highscore_file.read().split(" ") #split
                highscore_file.close()
                homescreen.state="home"
                state="high"
                highestscreen = HighScreen(screen, splitfilecontent[1], splitfilecontent[0])

            #Exits the game
            elif homescreen.state=="exitgame":
                done=True


        #Checking if user wants to close the highscore screen
        elif state=="high":
            if highestscreen.state=="imdown":
                state="home"

        #Game save logic 
        elif state == "game":
            
            #Opens file for writing, in case highscore file is empty fills it with 0,0
            highscore_file = open("highscore.txt", "w") #open file
            if os.stat("highscore.txt").st_size ==0: #if file is empty
                highscore_file.write("0 0") #write 0 0
            highscore_file.close()

            #Oopens file for reading, pulling out timestamp and previous highscore for comparison
            highscore_file = open("highscore.txt", "r")
            splitfilecontent = highscore_file.read().split(" ") #split
            current_highscore = int(splitfilecontent[1]) #[1] = level.killcounter
            highscore_file.close()

            #If player lost
            if level.state == "lost":
                #Gets and joins the current date(timestamp) and highscore
                now = datetime.now() #now is datetime
                timestamp = datetime.timestamp(now) #now to timestamp
                highscorecontents = " ".join([str(timestamp), str(level.killcounter)]) #join timestamp and killcounter

                #If current highscore is better than the previous one, writes the new joined text (tstamp and score) to a highscore file
                if current_highscore<level.killcounter:
                    highscore_file = open("highscore.txt", "w")
                    highscore_file.write(highscorecontents)
                    highscore_file.close()

                state = "gameover"
                current_level = 1

            #Wave passed text
            elif level.state == "wave passed":
                level_passed_text = render_text("You passed wave %s"%current_level, 96)
                current_level += 1
                level.state="play"

            #Same thing as lost, this if if player decides to quit the game via ESC button.
            elif level.state == "return":
                now = datetime.now() #now is datetime
                timestamp = datetime.timestamp(now) #now to timestamp
                highscorecontents = " ".join([str(timestamp), str(level.killcounter)]) #join timestamp and killcounter
                if current_highscore<level.killcounter:
                    highscore_file = open("highscore.txt", "w")
                    highscore_file.write(highscorecontents)
                    highscore_file.close()

                state="mainmenu"

        #You lost timeout
        elif state == "gameover":
            welcome_timeout -= dt
            if welcome_timeout - dt <= 0:
                state = "mainmenu"
                welcome_timeout = WELCOME_DURATION


        '''elif state == "level_passed":
            welcome_timeout -= dt
            if welcome_timeout - dt <= 0:
                state = "welcome"
                welcome_timeout = WELCOME_DURATION'''


        screen.blit(BG, (0,0))
        '''if state == "welcome":
            screen.blit(welcome_text, center(size, welcome_text))
            timeout = render_text("%.2f"%(welcome_timeout/1000), 48)
            screen.blit( timeout, middle_x(size, timeout, 200))
            level_text = render_text("LEVEL %d"%(current_level), 48)
            screen.blit( level_text, middle_x(size, timeout, win_height/4*3))'''

        
        
        #Updates
        if state == "game":
            level.update()

        elif state == "home":
            homescreen.update()

        elif state == "high":
            highestscreen.update()
            
        if state == "gameover":
            screen.blit(gameover_text, center(size, gameover_text))
        '''
        if state == "level_passed":
            screen.blit(level_passed_text, center(size, level_passed_text))'''

        pygame.display.flip()

        dt=clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
