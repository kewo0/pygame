import pygame
import random
import math
from helpers import *
from datetime import datetime

class Geometry(object):

    @classmethod
    def get_direction_from_angle(cls, angle, length):
        """ Return x,y direction vector from angle and length"""
        rad_angle = math.radians(angle)
        x = length * math.cos(rad_angle)
        y = length * math.sin(rad_angle)
        return x,y

    @classmethod
    def get_angle_from_line(cls, x1, y1, x2, y2):
        """ Return angle in degrees from two points: 
            
            Params: 
            x1, y1 coordinates for point 1
            x2, y2 coordinates for point 2
        """
        dirx = x2 - x1
        diry = y2 - y1
        rad_angle = math.atan2(diry, dirx)
        deg_angle = rad_angle * 180/math.pi
        return deg_angle % 360

 
class Entity(pygame.sprite.Sprite):
    """
    Main game entity
    Image is defined as a class level variable. Subclasses override their 
    images from the level. Image loading is implemented inside the level
    """
    # Placeholder transparent image
    image = pygame.Surface((100,100), pygame.SRCALPHA, 32)
 
    def __init__(self, level):
        """ Child classes have to configure their images before calling the 
        super().__init__() method, otherwise the object will be initialized 
        with a transparent image
        """

        self.level = level
        self.screen = level.screen
        self.sw, self.sh = self.screen.get_size()
        self.w, self.h = (100,100)
        self.x, self.y = self.sw/2, self.sh/2
        self.angle = random.randint(0,360)
        self.vel = 1
        self.dir = Geometry.get_direction_from_angle(self.angle, self.vel)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.drawn = None

        self.alive = True
 
    def handle_events(self):
        pass
 
    def update(self):
        self.handle_events()
        self.update_direction()
        self.move()
 
 
    def move(self):
        self.x += self.dir[0]
        self.y += self.dir[1]
 
    def update_direction(self):
        self.dir = Geometry.get_direction_from_angle(self.angle, self.vel)
 
    def draw(self):
        img = pygame.transform.scale(self.image, (self.w, self.h))
        img = pygame.transform.rotate(img, -self.angle)
        self.rect = img.get_rect(center = (self.x, self.y))
        self.drawn = self.screen.blit(img, self.rect)
        self.mask = pygame.mask.from_surface(img)

    def collided_with(self, obj):
        return pygame.sprite.collide_mask(self, obj)

#####################################################################################################
#####################################################################################################
#####################################################################################################

#Button

#Buttons differ based to names they were passed on from homescreen script

class Button:
   
    def __init__(self, homescreen, name):
        self.homescreen = homescreen
        self.name = name
        self.screen = homescreen.screen
        if self.name == "startbtn":
            self.image = homescreen.BTN_START
        elif name == "highscorebtn":
            self.image = homescreen.BTN_HIGHSCORE
        elif name == "exitbtn":
            self.image = homescreen.BTN_EXIT
        self.w, self.h = (300,75)
        self.sw, self.sh = self.screen.get_size()
        self.x = self.sw/2
        self.angle=0
        self.drawn = None
        self.rect = self.image.get_rect()
        self.state = "button" # "startgame", "highscore", "exitgame"

        self.didiclick_start=False
        self.didiclick_highscore=False
        self.didiclick_exit=False

        self.spawnpoints()
        

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        self.clickme(mouse_pressed, mouse_pos)
    
    def update(self):
        self.handle_events()

    def draw(self):
        img = pygame.transform.scale(self.image, (self.w, self.h))
        img = pygame.transform.rotate(img, -self.angle)
        self.rect = img.get_rect(center = (self.x, self.y))
        self.drawn = self.screen.blit(img, self.rect)
        self.mask = pygame.mask.from_surface(img)

#Spawn for different buttons
    def spawnpoints(self):
        if self.name=="startbtn":
            self.y = (self.sh/2)-100
        elif self.name=="highscorebtn":
            self.y = self.sh/2
        elif self.name=="exitbtn":
            self.y = (self.sh/2)+100

    
#Checks if mouse hovers over the button and clicks it, clicked button changes the state of the button (i think it may be useless because of =>),
#didiclick logic checks which button is clicked.
    def clickme(self, mouse_pressed, mouse_pos):
        if mouse_pos[0] > (self.x-self.w/2) and mouse_pos[0] < self.x+self.w/2:
            if mouse_pos[1] > (self.y-self.h/2) and mouse_pos[1] < self.y + self.h/2:
                if mouse_pressed[0]:
                    if self.name == "startbtn":
                        self.state = "startgame"
                        self.didiclick_start=True
                    if self.name == "highscorebtn":
                        self.state = "highscore"
                        self.didiclick_highscore=True
                    if self.name == "exitbtn":
                        self.state = "exitgame"
                        self.didiclick_exit=True
#####################################################################################################
#####################################################################################################
#####################################################################################################

#Highscore screen, INVISIBLE AT THE MOMENT BECAUSE TEXT GETS COVERED BY THE SPRITE, so it only shows up the highscore and exit button sprite

class HighScoreScreen:
    def __init__(self,homescreen,score,timestamp):
        self.homescreen = homescreen
        self.screen = homescreen.screen
        self.image = homescreen.HIGHSCORE_IMG
        self.w, self.h = (500,500)
        self.sw, self.sh = self.screen.get_size()
        self.x, self.y = self.sw/2, self.sh/2
        self.angle=0
        self.drawn = None
        self.rect = self.image.get_rect()
        self.score = score
        self.time = datetime.fromtimestamp(int(float(timestamp)))
        self.time = self.time.strftime("%d/%m/%Y, %H:%M:%S")
        self.high_size = pygame.display.Info()

    def draw(self):
        img = pygame.transform.scale(self.image, (self.w, self.h))
        img = pygame.transform.rotate(img, -self.angle)
        self.rect = img.get_rect(center = (self.x, self.y))
        self.drawn = self.screen.blit(img, self.rect)
        self.mask = pygame.mask.from_surface(img)

    def update(self):
        #Printed text in same line ignoring the /n therefore has to be split
        '''personalbest_text = render_text(("PERSONAL BEST[ ]%s [ ]%s kills"%(self.time,self.score)),30)
        self.screen.blit(personalbest_text, center((self.high_size.current_w,self.high_size.current_h), personalbest_text))'''

        personalbest_text = render_text("PERSONAL BEST",30)
        self.screen.blit(personalbest_text,center((self.high_size.current_w,self.high_size.current_h-100), personalbest_text))
        personalbest_time = render_text(self.time,30)
        self.screen.blit(personalbest_time,center((self.high_size.current_w,self.high_size.current_h), personalbest_time))
        personalbest_score = render_text("%s kills"%self.score,30)
        self.screen.blit(personalbest_score,center((self.high_size.current_w,self.high_size.current_h+100), personalbest_score))
        
        

    
#Button for exiting highscore screen
class Xbtn:
    def __init__(self,homescreen,x,y):
        self.homescreen = homescreen
        self.screen = homescreen.screen
        self.image = homescreen.XBTN_IMG
        self.w, self.h = (50,50)
        self.sw, self.sh = self.screen.get_size()
        self.x, self.y = self.sw/2+x/2-15,self.sh/2-y/2+15
        self.angle=0
        self.drawn = None
        self.rect = self.image.get_rect()
        self.state = "highalive"

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        self.xclickme(mouse_pressed, mouse_pos)

    def update(self):
        self.handle_events()
        
    def draw(self):
        img = pygame.transform.scale(self.image, (self.w, self.h))
        img = pygame.transform.rotate(img, -self.angle)
        self.rect = img.get_rect(center = (self.x, self.y))
        self.drawn = self.screen.blit(img, self.rect)
        self.mask = pygame.mask.from_surface(img)

    def xclickme(self, mouse_pressed, mouse_pos):
        if mouse_pos[0] > (self.x-self.w/2) and mouse_pos[0] < self.x+self.w/2:
            if mouse_pos[1] > (self.y-self.h/2) and mouse_pos[1] < self.y + self.h/2:
                if mouse_pressed[0]:
                    self.state = "highded"
    

#####################################################################################################
#####################################################################################################
#####################################################################################################

#Standard bullet from LV
class Bullet(Entity):
    def __init__(self, level, x, y, angle):
        self.image = level.BULLET_IMG
        super().__init__(level)
        self.w, self.h = (20, 13)
        self.angle = angle
        self.x, self.y = x,y
        self.vel = 10

    def handle_events(self):
        if self.x <= 0 or self.x >= self.sw:
            self.alive = False
        if self.y <= 0 or self.y >= self.sh:
            self.alive = False
            
#Almost same as bullet, difference is that it dies at certain cordinates
class Rocket(Entity):
    def __init__(self,level,x,y,angle,destination_x,destination_y):
        self.image = level.ROCKET_IMG
        super().__init__(level)
        self.w, self.h = (40,14)
        self.angle = angle
        self.x, self.y = x,y
        self.des_x, self.des_y = destination_x,destination_y
        self.vel = 5
    
    def handle_events(self):
        if self.x <= 0 or self.x >= self.sw:
            self.alive = False
        if self.y <= 0 or self.y >= self.sh:
            self.alive = False

        #Cordinates checked, when self cordinates arrive to passed on cordinates rocket dies
        #Had to create a pocket by adding +2 space because for some reason passed cordinates were getting ignores
        #Bug: Sometimes rocket sometimes still ignores the given pocket and flies off the screen 
        if self.x < self.des_x+2 and self.x > self.des_x-2 and self.y< self.des_y+2 and self.y > self.des_y-2:
            self.alive=False

class ExplosionDamage(Entity):
    ALIVE_DURATION=1

    def __init__(self,level,x,y):
        self.image = level.EXPLOSIONDMG_IMG
        super().__init__(level)
        self.w, self.h = 128,128
        self.angle = 0
        self.x, self.y = x,y
        self.vel = 0
        self.alive_duration = self.ALIVE_DURATION

    def handle_events(self):
        if self.x <= 0 or self.x >= self.sw:
            self.alive = False
        if self.y <= 0 or self.y >= self.sh:
            self.alive = False
        self.time_to_die()

    def time_to_die(self):
        self.alive_duration-=1
        if self.alive_duration <=0:
            self.alive=False
            self.alive_duration=self.ALIVE_DURATION

class Explosion(pygame.sprite.Sprite):
    FRAMES = 56

    def __init__(self,entity):
        self.level = entity.level
        self.screen = self.level.screen
        self.sw, self.sh = self.screen.get_size()
        self.w, self.h = 128,128
        self.x, self.y = entity.x, entity.y
        self.image = self.level.EXPLOSION_SHEET
        self.sheet = self.level.EXPLOSION_SHEET
        self.animation_frames = []
        self.create_animation_frames()
        self.drawn = None
        self.alive = True 
        self.frame = 0

    def update(self):
        self.image = self.animation_frames[(self.frame // 4)%len(self.animation_frames)]
        if self.frame >= self.FRAMES:
            self.alive = False
        self.frame += 1

    def draw(self):
        if self.alive:
            img = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = img.get_rect(center=(self.x, self.y))
            self.drawn = self.screen.blit(img, self.rect)

    def create_animation_frames(self):
        for b in [0, 128, 256, 384]:
            for a in [0, 128, 256, 384]:
                img = pygame.Surface((128,128), pygame.SRCALPHA, 32)
                img.blit(self.sheet, (0,0), (a,b,128,128))
                self.animation_frames.append(img)

class HitAni(Explosion):
    def __init__(self, entity):
        super().__init__(entity)
        self.w = 32
        self.h = 32


#####################################################################################################
#####################################################################################################
#####################################################################################################
class Player(Entity):
    """Handles all the logic for the player object"""
    SHIP_VELOCITY = 5
    CANNON_COOLDOWN = 8
    ROCKET_COOLDOWN = 10
    TP_COOLDOWN = 0
    TPCD_GLOBAL = 0
    HP_RESPAWN = 600
    HP_START = 0
 
    def __init__(self, level):

        self.image = level.PLAYER_IMG
        self.mask_img = level.PLAYER_IMG

        '''
        self.image = level.SHIP_OFF
        self.mask_img = level.SHIP_OFF
        '''
        super().__init__(level)

        '''
        self.image_on = level.SHIP_ON
        self.image_off = level.SHIP_OFF
        '''

        self.w, self.h = (120, 90)
        self.angle = 0
        self.x,self.y = self.sw/2,self.sh/2
        self.cannon_cooldown = self.CANNON_COOLDOWN
        self.rocket_cooldown = 0
        self.health = 100
 
    def handle_events(self):
        '''
        if self.HP_START == 1:
            self.revive_healthpack()
        '''
        # calculate direction from mouse position
        mousepos = pygame.mouse.get_pos()
        self.angle = Geometry.get_angle_from_line(self.x, self.y, mousepos[0], mousepos[1])

        mouse_pressed = pygame.mouse.get_pressed()
        self.fire(mouse_pressed)
        self.fire_rocket(mouse_pressed, mousepos)
        #self.teleport_pls(mouse_pressed,mousepos)
        #self.respawn_my_healthpack()

        
        keys = pygame.key.get_pressed()
        self.vel = 0
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.y -= self.SHIP_VELOCITY
            self.x -= self.SHIP_VELOCITY
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            self.y -= self.SHIP_VELOCITY
            self.x += self.SHIP_VELOCITY
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.y += self.SHIP_VELOCITY
            self.x -= self.SHIP_VELOCITY
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.y += self.SHIP_VELOCITY
            self.x += self.SHIP_VELOCITY
        elif keys[pygame.K_w]:
            self.y -= self.SHIP_VELOCITY
        elif keys[pygame.K_s]:
            self.y += self.SHIP_VELOCITY
        elif keys[pygame.K_a]:
            self.x -= self.SHIP_VELOCITY
        elif keys[pygame.K_d]:
            self.x += self.SHIP_VELOCITY
        

        '''
        if self.vel == 0:
            self.image = self.image_off
        else:
            self.image = self.image_on
        '''
        
    def fire(self, mouse_pressed):
        self.cannon_cooldown -= 1
        if self.cannon_cooldown <= 0:
            if mouse_pressed[0]:
                bullet_dir = Geometry.get_direction_from_angle(self.angle, self.w/2)
                bullet_x = self.x + bullet_dir[0]
                bullet_y = self.y + bullet_dir[1]
                self.level.bullets.append(Bullet(self.level, bullet_x, bullet_y, self.angle))
                self.cannon_cooldown = self.CANNON_COOLDOWN

    def fire_rocket(self,mouse_pressed, mousepos):
        if self.rocket_cooldown <=0:
            if mouse_pressed[2]:
                rocket_dir = Geometry.get_direction_from_angle(self.angle, self.w/2)
                rocket_x = self.x + rocket_dir[0]
                rocket_y = self.y + rocket_dir[1]
                self.level.rockets.append(Rocket(self.level, rocket_x, rocket_y, self.angle, mousepos[0],mousepos[1]))
                self.rocket_cooldown = self.ROCKET_COOLDOWN
        else:
            if self.rocket_cooldown > 0:
                self.rocket_cooldown -=1

    def draw(self):
        if self.alive:
            img = pygame.transform.scale(self.image, (self.w, self.h))
            img = pygame.transform.rotate(img, -self.angle)
            self.rect = img.get_rect(center = (self.x, self.y))
            self.drawn = self.screen.blit(img, self.rect)
            maskimg = pygame.transform.scale(self.mask_img, (self.w, self.h))
            maskimg = pygame.transform.rotate(maskimg, -self.angle)
            self.mask = pygame.mask.from_surface(maskimg)

    def hit(self):
        self.health -= 5
        if self.health <= 0:
            self.alive = False
    '''
    def respawn_my_healthpack(self):
        if self.HP_START == 1:
            if self.HP_RESPAWN >= 1:
                self.HP_RESPAWN -= 1
            else:
                self.HP_RESPAWN=600
                self.HP_START=0
    '''

    '''def teleport_pls(self, mouse_pressed, mousepos):
        if self.TP_COOLDOWN <=0:
            if mouse_pressed[2]:
                self.x = mousepos[0]
                self.y = mousepos[1]
                self.TP_COOLDOWN = 600
        else:
            print(self.TP_COOLDOWN)
            if self.TP_COOLDOWN > 0:
                self.TP_COOLDOWN -= 1
                self.TPCD_GLOBAL = self.TP_COOLDOWN/60'''

#####################################################################################################
#####################################################################################################
#####################################################################################################

class Enemy(Entity):
    """Handles all the logic for the asteroid object"""
    PLAYER_DEAD_ZONE = 100
 
    def __init__(self, level,health):
        self.image = level.ENEMY_IMG
        self.mask_img = level.ENEMY_IMG
        super().__init__(level)
        self.w, self.h = (75 , 75)
        self.vel = 2
        self.radius = 30
        self.init_random_position()
        self.health = health
 
    def update(self,player):
        '''
        dirx = self.dir[0]
        diry = self.dir[1]
        '''
        
        self.angle = Geometry.get_angle_from_line(self.x,self.y,player.x,player.y)
        self.dir = Geometry.get_direction_from_angle(self.angle, self.vel)

        self.handle_events()
        self.update_direction()
        self.move()
        #self.pos = project(self.pos, angle, self.speed * dt)
        #self.rect.center = self.pos

    def handle_events(self):
        '''
        dirx = self.dir[0]
        diry = self.dir[1]
        if self.x < self.radius or self.x > self.sw - self.radius:
            dirx *= -1
        if self.y < self.radius or self.y > self.sh - self.radius:
            diry *= -1
        
        self.angle = Geometry.get_angle_from_line(0,0,self.ex,self.ey)
        self.dir = Geometry.get_direction_from_angle(self.angle, self.vel)
        '''

    '''
    def move_towards_player2(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,
                                      player.rect.y - self.rect.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)
        '''
    def hit(self):
        self.health -=50
        if self.health <= 0:
            self.alive=False

    def init_random_position(self):
        """
        Create x,y coordinates that are at least PLAYER_DEAD_ZONE pixels away
        from the player (center of the screen)."""
        left = random.randint(-200, self.sw/2)
        right = random.randint(self.sw/2, self.sw+200)
        top = random.randint(-200, self.sh/2)
        bottom = random.randint(self.sh/2, self.sh +200 )
        
        #spawnL = False
        #spawnR = False
        spawnT = 1
        spawnB = 2
        spawnL = 3
        spawnR = 4
        spawnDecision = random.choice([spawnT,spawnB,spawnL,spawnR])
        
        if spawnDecision == 1:
            self.x = random.randint(-500, self.sw+500)
            self.y = random.randint(-500,0)
        elif spawnDecision == 2:
            self.x = random.randint(-500, self.sw+500)
            self.y = random.randint(self.sh,self.sh+500)
        elif spawnDecision == 3:
            self.x = random.randint(-500, 0)
            self.y = random.randint(-500,self.sh+500)
        elif spawnDecision == 4:
            self.x = random.randint(self.sw, self.sw+500)
            self.y = random.randint(-500,self.sh+500)
        '''
        while not spawnT and not spawnB:
            if top > 0 and left> 0 or top > 0 and right < self.sw:
                top = random.randint(-200, 0)
            else:
                spawnT=True
            if bottom < self.sh and left > 0 or bottom < self.sh and right < self.sw:
                bottom = random.randint(self.sh, self.sh +200 )
            else:
                spawnB=True
        self.x = random.choice( [left, right] )
        self.y = random.choice( [top, bottom] )
        '''


#####################################################################################################
#####################################################################################################
#####################################################################################################

class Rat(Entity):
    def __init__(self, level):
        self.image = level.RAT_IMG
        super().__init__(level)
        self.w,self.h = 25,25
        self.angle = 0
        self.vel = 0

    def update(self):
        mousepos=pygame.mouse.get_pos()
        self.Follow(mousepos)

    def Follow(self,mousepos):
        self.x = mousepos[0]
        self.y = mousepos[1]