import pygame
import random
from entities import Player, Enemy,Explosion,ExplosionDamage,HitAni,Rat
from helpers import *


class Level(object):
    LEVEL_START_TIMEOUT = 60
    HIT_COOLDOWN = 60
    PLAYER_IMG = pygame.image.load("Elon.png")
    ENEMY_IMG = pygame.image.load("Enemy.png")
    BULLET_IMG = pygame.image.load("NewBullet.png")
    ROCKET_IMG = pygame.image.load("Falcon_x_mini.png")
    EXPLOSION_SHEET = pygame.image.load("explosion.png")
    EXPLOSIONDMG_IMG = pygame.image.load("explosion_mask.png")
    RAT_IMG= pygame.image.load("Scope.png")

    def __init__(self,screen,level):
        self.frame = 0
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()
        self.state = "play" # "play", "won", "lost"
        self.score = 0
        

        ###########################################
        #For displaying wave survival text
        self.wave_screen_size = pygame.display.Info()

        #Display Counters
        self.killcounter=0
        self.alivecounter=0

        #Wave logic setup
        self.new_wave=False #New wave check
        self.wave_counter= 0 #Wave counter for display and logic
        self.enemy_counter=3 #For adding 3 more enemies each wave
        self.starting_enemies=5 #1st wave enemy number
        self.enemy_health=25 #Enemy health that get greater with each wave
        self.enemies = [] #Enemy list
        self.time_between_waves = 180 #Timer between waves = 3 seconds


        #First wave append
        for i in range(self.starting_enemies):
            self.alivecounter+=1
            self.enemies.append(Enemy(self,self.enemy_health))

        #PlayerHitCd
        self.hitcooldown = 60.0*5
        self.currenthitcd = self.hitcooldown
        ###########################################

        #Objects
        self.player = Player(self)
        self.rat = Rat(self)
        self.bullets = []
        self.rockets = []
        self.explosions = []
        self.explosiondmg = []

    def update(self):


        #Wave logic
        if(self.new_wave):
            #Pre-new wave
            #Timer
            self.time_between_waves -=1

            #Text display
            wave_passed_text = render_text("You passed wave %s"%(self.wave_counter+1), 96)
            self.screen.blit(wave_passed_text, center((self.wave_screen_size.current_w,self.wave_screen_size.current_h), wave_passed_text))
            wavecd_text = render_text("%s sec"%(int(self.time_between_waves/60+1)), 50)
            self.screen.blit(wavecd_text, center((self.wave_screen_size.current_w,self.wave_screen_size.current_h+200), wavecd_text))

            #New wave
            if self.time_between_waves <= 0:
                self.wave_counter+=1
                self.enemy_counter=3*self.wave_counter
                self.enemy_health=25*self.wave_counter
                self.hitcooldown-=self.hitcooldown*0.1
                self.currenthitcd = self.hitcooldown

                #Enemy append + alive counter
                for i in range(self.starting_enemies+self.enemy_counter):
                    self.alivecounter+=1
                    self.enemies.append(Enemy(self,self.enemy_health))
                self.new_wave=False
                self.time_between_waves = 180

        #Update
        self.frame += 1
        self.player.update()
        self.rat.update()
        for bullet in self.bullets:
            bullet.update()
        for enemy in self.enemies:
            enemy.update(self.player)
        for e in self.explosions:
            e.update()
        for rocket in self.rockets:
            rocket.update()
        for dmg in self.explosiondmg:
            dmg.update()


        #Rocket explosion logic
        ##Had to use 2 different objects because I couldnt figure out how to make animation collidion
        for rocket in self.rockets:
            if not rocket.alive:
                self.explosions.append(Explosion(rocket))
                self.explosiondmg.append(ExplosionDamage(self,rocket.x,rocket.y))
        
                
        #Collisions + mem. clear + draw()
        self.check_collisions()
        self.clear_dead_entities()

        self.player.draw()
        self.rat.draw()
        for bullet in self.bullets:
            bullet.draw()
        for enemy in self.enemies:
            enemy.draw()
        for e in self.explosions:
            e.draw()
        for rocket in self.rockets:
            rocket.draw()
        for dmg in self.explosiondmg:
            dmg.draw()

        #Info display
        k_a_text = " | ".join([str(self.killcounter),str(self.alivecounter)])
        k_a_text = render_text("Kills/Left alive: %s"%k_a_text,20)
        self.screen.blit(k_a_text,(20,25))
        health = render_text("Health: %d"%self.player.health, 20)
        self.screen.blit(health, (20, 60))
        wave_counter_text = render_text("Current wave: %d"%(self.wave_counter+1),20)
        self.screen.blit(wave_counter_text,(self.sw-150,25))
        rocketcd_text = render_text("Rocket cooldown: %d"%self.player.rocket_cooldown,20)
        self.screen.blit(rocketcd_text,(20,95))

        #Exit/New wave
        esc_key = pygame.key.get_pressed()
        if esc_key[pygame.K_ESCAPE]:
            self.state="return"
        if not self.player.alive:
            self.state = "lost"
        if len(self.enemies) == 0:
            self.state = "wave_passed"
            self.new_wave = True



    def check_collisions(self):
        if self.frame < self.LEVEL_START_TIMEOUT:
            return False
        for dmg in self.explosiondmg:
            for enemy in self.enemies:
                if dmg.collided_with(enemy):
                    dmg.alive=False
                    enemy.hit()
            if dmg.collided_with(self.player):
                self.player.hit()
        for enemy in self.enemies:
            for bullet in self.bullets:
                if bullet.collided_with(enemy):
                    bullet.alive = False
                    self.explosions.append(HitAni(bullet))
                    enemy.hit()

            if self.player.collided_with(enemy):
                self.currenthitcd-=1
                if self.currenthitcd<=0:
                    self.player.hit()
                    self.explosions.append(HitAni(self.player))
                    self.currenthitcd=self.hitcooldown



    def clear_dead_entities(self):
        for i, bullet in enumerate(self.bullets):
            if not bullet.alive:
                del self.bullets[i]

        for i, enemy in enumerate(self.enemies):
            if not enemy.alive:
                #CounterLogic
                self.killcounter+=1
                self.alivecounter-=1
                del self.enemies[i]

        for i, rocket in enumerate(self.rockets):
            if not rocket.alive:
                del self.rockets[i]

        for i, explosion in enumerate(self.explosions):
            if not explosion.alive:
                del self.explosions[i]

        for i, dmg in enumerate(self.explosiondmg):
            if not dmg.alive:
                del self.explosiondmg[i]