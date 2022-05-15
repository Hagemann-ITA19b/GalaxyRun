from datetime import datetime
import pygame
import os
from random import randint
from pygame import mixer
import time
import math

#Parameter
bullets = 20
score_value = 0
count = 1
maxcount = 20 
lives = 3
fuel = 200
endurance = 100
# spawncount = 5
# count = 0
shieldpoints = 100
# tkposy = 0
# tkposx = 0
jumping = False
shield_active = False
level = 0
facing = "R"
posx = 0
posy = 0

BLACK = (0, 0, 0) 
GRAY = (127, 127, 127) 
WHITE = (255, 255, 255)
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 
CYAN = (0, 255, 255) 
MAGENTA = (255, 0, 255)
PURP = (123, 32, 251)
#CYAN = (1, 227, 242)

class Settings(object):
    window_height = 720
    window_width = 1600
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "files")
    player_size = (70,150) #70, 150
    bullet_size = (100, 50)
    melee_size = (70, 70)
    stormtrooper_size = (70,150)
    max_platforms = 1
    current_platforms = 0
    current_enemys = 0
    max_enemys = 1
    start_rockets = 5
    player_maxhealth = 3
    next_level = 100
    player_damage = 1
    player_fuel = 200
    title = "Galaxy Run"

# Musik

mixer.init()
pygame. mixer.init()
blaster_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "blaster.wav"))
refill_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "refill.mp3"))
jetpack_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "jetpack.wav"))
darksaber_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "darksaber.wav"))

  
mixer.music.load(os.path.join(Settings.path_image, "Soundtrack.mp3"))
  

pygame.mixer.music.set_volume(0.4)
mixer.music.play()



class Background():
    def __init__(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.rectimg = self.image.get_rect()
        self.bgx = 0
         
    def scroll_r(self, scrollspeed):
        self.bgx = self.bgx - scrollspeed
        if self.bgx <= -Settings.window_width:
            self.bgx = 0

    def scroll_l(self, scrollspeed):
        self.bgx = self.bgx + scrollspeed
        if self.bgx >= Settings.window_width:
            self.bgx = 0
             
    def draw(self, screen):
        screen.blit(self.image,(self.bgx-Settings.window_width,0))
        screen.blit(self.image,(self.bgx,0))
        screen.blit(self.image,(self.bgx+Settings.window_width,0))


class Stormbie(pygame.sprite.Sprite):
    def __init__(self, filename,health, zposx, zposy):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.stormtrooper_size)
        self.rect = self.image.get_rect()
        self.zposx = zposx
        self.zposy = zposy
        self.rect.left = self.zposx#randint(300, Settings.window_width)
        self.rect.top = self.zposy #570
        self.speed_h = 3
        self.speed_v = 0
        self.health = health
        self.images = []
        self.facing = "L"
        for i in range(3):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"stormbieL{i}.png"))
            self.images.append(bitmap)
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100

    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1

                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]

    def update(self):
        self.rect.move_ip(self.speed_h, self.speed_v)
        self.move()

        if self.facing == "L":
            self.images.clear()
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"stormbieL{i}.png"))
                self.images.append(bitmap)
        elif self.facing == "R":
            self.images.clear()
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"stormbieR{i}.png"))
                self.images.append(bitmap)
            
    

    def move(self):
        # Stormbie.get_pos(self)
        self.rect.left += self.speed_h
        self.rect.top += self.speed_v
        # for i in range(0, Settings.window_width):
        if self.rect.left <= posy: #0:
                self.speed_h = 2
                self.facing = "R"

        if self.rect.left >= posy: #Settings.window_width:
                self.speed_h = -2
                self.facing = "L"

    def playermove_R(self, speed):
        self.rect.left -= speed

    def playermove_L(self, speed):
        self.rect.left += speed
               


class Stormtrooper(pygame.sprite.Sprite):
    def __init__(self, filename, health, tkposx, tkposy, trigger, getting_hit):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.stormtrooper_size)
        self.rect = self.image.get_rect()
        self.tkposx = tkposx
        self.tkposy = tkposy
        self.trigger = trigger
        self.rect.left = self.tkposx#randint(300, Settings.window_width)
        self.rect.top = self.tkposy #570
        self.speed_h = randint( 1, 3)
        self.speed_v = 0
        self.health = health
        self.images = []
        self.facing = "L"
        for i in range(1):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"stormtrooperR{i}.png"))
            self.images.append(bitmap)
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100
        self.platfrom_y = 0
        self.getting_hit = getting_hit

    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1

                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]


    def move(self):
        self.rect.left += self.speed_h
        self.rect.top += self.speed_v

        if self.rect.left <= 0:
                self.speed_h = 2
        if self.rect.left >= Settings.window_width:
                self.speed_h = -2

    def playermove_R(self, speed):
        self.rect.left -= speed

    def playermove_L(self, speed):
        self.rect.left += speed
        
    def update(self):
        if self.rect.left <= posy:
            self.facing = "R"
        if self.rect.left >= posy:
            self.facing = "L"


        if self.facing == "L":
            self.images.clear()
            if self.getting_hit == False:
                for i in range(3):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooperR{i}.png"))
                    self.images.append(bitmap)
            elif self.getting_hit == True:
                for i in range(3):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooperL_hit{i}.png"))
                    self.images.append(bitmap)

        elif self.facing == "R":
            self.images.clear()
            if self.getting_hit == False:
                for i in range(3):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooperL{i}.png"))
                    self.images.append(bitmap)
            elif self.getting_hit == True:
                for i in range(3):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooperR_hit{i}.png"))
                    self.images.append(bitmap)


        #self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class Player(pygame.sprite.Sprite):
    def __init__(self, filename, speed, endurance):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.rect = self.image.get_rect()
        Player.pos(self)
        self.weapons = ["blaster", "rockets"]
        self.weapons_index = 0
        self.health = Settings.player_maxhealth
        self.rockets = Settings.start_rockets
        self.shield = False
        self.sprinting = False
        self.flames_on = False
        self.energypoints = 75
        self.passed_time = 0
        self.passed_fueltime = 0
        self.endurance = endurance
        self.score_muliplier = 0.1
        self.playing_shieldrefill = False
        self.playing_shieldlow = False
        self.invincible = False
        self.passed_invtime = 0
        self.run_inv = False
        self.run_fuel = False
        self.images = []
        self.usefuel = False
        self.refilling = False
        if facing == "R":
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"player_standing_R{i}.png")).convert()
                self.images.append(bitmap)
        if facing == "L":
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"player_standing_L{i}.png")).convert()
                self.images.append(bitmap)


        self.speed = speed
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100
        self.platform_y = 570
        self.velocity_index = 0
        self.velocity = ([-10,-9.5,-9,-8.5,-8,-7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])


    def change_next_weapon(self):
        self.weapons_index += 1
        if self.weapons_index >= len(self.weapons):
            self.weapons_index = 0
    def change_previous_weapon(self):
        self.weapons_index -= 1
        if self.weapons_index < 0:
            self.weapons_index = len(self.weapons) - 1
    def get_invincible(self):
        self.invincible = True
        self.run_inv = True
        self.passed_invtime = 0


    def invincible_off(self):
        if self.passed_invtime >= 90:
            self.invincible = False
    
    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]
                    
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def sprint(self):
        if self.endurance > 0 and self.sprinting == True:
            self.speed = 10
            self.endurance = self.endurance - 1
            self.score_muliplier = 0.2

        else:
            self.sprinting = False
            self.speed = 5
            self.score_muliplier = 0.1
        

    def pos(self):                              #Gibt die Startposition an 
        self.rect.left = 50
        self.rect.top = 399
    
    def get_pos(self):
        global posx, posy
        posy = self.rect.left
        posx = self.rect.top

    def moveL(self):
        global facing, score_value
        Player.get_pos(self)
        # if self.rect.left > 75:
        if score_value < 16:                     #Macht die Border unpassierbar
            self.rect.left = self.rect.left - self.speed
        if lives > 0:
            score_value -= self.score_muliplier#0.1    #Spieler wird nach links verschoben
      
        if self.shield == False and self.flames_on == False and self.sprinting == False and jumping == False:
                self.images.clear()
                for i in range(7):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"player_walking_L{i}.png"))
                    self.images.append(bitmap)

        if self.shield == False and self.flames_on == False and self.sprinting == True:
                self.images.clear()
                for i in range(7):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"player_sprinting_L{i}.png"))
                    self.images.append(bitmap)


    def moveR(self):
        global facing, score_value, jumping
        Player.get_pos(self)
        if self.rect.left < Settings.window_width // 2:#Settings.window_width - 50:    #Macht die Border unpassierbar
            self.rect.left = self.rect.left + self.speed
        if self.health > 0:
            score_value += self.score_muliplier#0.1
                #Spieler wird nach rechts verschoben
       
        if self.shield == False and self.flames_on == False and self.sprinting == False and jumping == False:
            self.images.clear()###
            for i in range(7):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"player_walking_R{i}.png"))
                    self.images.append(bitmap)
        if self.shield == False and self.flames_on == False and self.sprinting == True:
                self.images.clear()
                for i in range(7):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"player_sprinting_R{i}.png"))
                    self.images.append(bitmap)
            

    def moveUp(self):
        global fuel
        Player.get_pos(self)
        if fuel > 0:
            pygame.mixer.unpause()
            jetpack_sound.play()
            if self.rect.top <= 570: 
                # if self.rect.top >= 1:
                    self.rect.top = self.rect.top - 13
                    self.in_air = True
                    self.images.clear()
                    if facing == "R":
                        for i in range(2):
                            bitmap = pygame.image.load(os.path.join(
                                Settings.path_image, f"jetpack_R{i}.png"))
                            self.images.append(bitmap)
                    if facing == "L":
                        for i in range(2):
                            bitmap = pygame.image.load(os.path.join(
                                Settings.path_image, f"jetpack_L{i}.png"))
                            self.images.append(bitmap)
                    self.usefuel = True
                    fuel -= 1

                    if fuel <= 0:
                        pygame.mixer.pause()

                       
    def block(self):
        if self.energypoints > 0 and self.refilling == False:
            self.energypoints = self.energypoints - 0.25
            self.shield = True
       
            self.images.clear()
            for i in range(16):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"player_shielding{i}.png"))
                self.images.append(bitmap)
        else:
            self.shield = False

    def walk(self):
        self.sprinting = False
        self.speed = 5
        self.score_muliplier = 0.1


    def refill(self):
        global fuel
        global endurance
        Game.invtimer(self)
        
        self.datetime = datetime.now()

        if self.energypoints <= 0:
            if self.playing_shieldlow == False:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'shields_low.mp3')))
                self.playing_shieldlow = True
            Game.timer(self)
        if self.passed_time >= 420:
            self.refilling = True
            if self.playing_shieldrefill == False:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'refill.mp3')))
                self.playing_shieldrefill = True
            self.energypoints = self.energypoints + 0.5 #0.25
            if self.energypoints >= 75:
                self.refilling = False
                self.passed_time = 0
                self.playing_shieldrefill = False
                self.playing_shieldlow = False
        
        if self.usefuel == True:
            self.run_fuel = False
            self.passed_fueltime = 0
       
        if self.rect.top == self.platform_y and fuel < Settings.player_fuel: #and #self.usefuel == False:
        #    self.run_fuel = True
         #   print(self.passed_fueltime)
          #  if fuel < 200:
           #     Game.fueltimer(self)
            #    if self.passed_fueltime >= 300:
                    fuel += 1#0.4
              #      if fuel >= 200:
               #         self.passed_fueltime = 0
                #        self.run_fuel = False
        if self.endurance < 100:
                        self.endurance += 1
                        #print(self.endurance)

    def flamethrower_on(self):
                if facing == "R":
                    self.images.clear()
                    for i in range(2):
                        bitmap = pygame.image.load(os.path.join(
                            Settings.path_image, f"flamethrowing_R{i}.png"))
                        self.images.append(bitmap)
                if facing == "L":
                    self.images.clear()
                    for i in range(2):
                        bitmap = pygame.image.load(os.path.join(
                            Settings.path_image, f"flamethrowing_L{i}.png"))
                        self.images.append(bitmap)
                self.flames_on = True
    
    def flamethrower_off(self):
        self.flames_on = False
                
        
    def jump(self):
        global jumping, endurance
        
        if jumping == True:
            if self.flames_on == False:
                self.images.clear()
                if facing == "R":
                    self.images.append(pygame.image.load(os.path.join(Settings.path_image,"jumpR.png")))
                if facing == "L":
                    self.images.append(pygame.image.load(os.path.join(Settings.path_image,"jumpL.png")))
            
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1
            if self.rect.top >= self.platform_y:
                self.rect.top = self.platform_y
                self.velocity_index = 0
                if self.rect.top == self.platform_y:
                    jumping = False
        Player.get_pos(self)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def playermove_R(self, speed):
            self.rect.left -= speed

    def playermove_L(self, speed):
            self.rect.left += speed

class Pickups(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.left = randint(0, Settings.window_width - 50)
        self.rect.top = 0
        self.speed_h = 3
        self.speed_v = 5
        self.on_ground = False
        self.platform_y = 670
        self.velocity_index = 0
        self.velocity = ([-7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5])

    def update(self):
        if self.rect.top < self.platform_y and self.on_ground == False:
            self.rect.top += self.speed_v
            if self.rect.top == self.platform_y:
                self.on_ground = True

        if self.on_ground == True:
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1
            if self.rect.top >= self.platform_y:
                self.rect.top = self.platform_y
                self.velocity_index = 0

    def playermove_R(self, speed):
        self.rect.left -= speed

    def playermove_L(self, speed):
        self.rect.left += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Flame(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,150))
        self.rect = self.image.get_rect()
        self.rect.left = posy 
        self.rect.top = posx
        self.speed_h = 10
        self.speed_v = 0
        self.facing = facing
        self.faced = False
        # self.flames_on = False
        self.images = []
        if facing == "R":
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"flameR{i}.png"))
                self.images.append(bitmap)
        if facing == "L":
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"flameL{i}.png"))
                self.images.append(bitmap)

        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100

    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]


    def update(self):
        global facing
        self.facing = facing
        self.rect.top = posx 
        if self.facing == "R":
            self.rect.left = posy + 70#75
        if self.facing == "L":
                self.rect.left = posy - 50
        
        if self.facing == "R":
            self.images.clear()
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"flameR{i}.png"))
                self.images.append(bitmap)
        if self.facing == "L":
            self.images.clear()
            for i in range(2):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"flameL{i}.png"))
                self.images.append(bitmap)

   
class projectile(pygame.sprite.Sprite):
    def __init__(self, filename, dx, dy): #delta x and delta y
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.bullet_size)
        self.rect = self.image.get_rect()
        self.rect.left = posy + 70
        self.rect.top = posx + 50
        x = self.rect.left
        y = self.rect.top
        self.angle = math.atan2(dy-y , dx-x) #dx and dy are the coordinates for the cursor
        self.dx = math.cos(self.angle) * 30
        self.dy = math.sin(self.angle) * 30
        self.speed_h = 10
        self.speed_v = 0
        self.x = x
        self.y = y        
        self.images = []
        for i in range(4):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"bullet{i}.png"))
            self.images.append(bitmap)
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100

    def animate(self):

            if pygame.time.get_ticks() > self.clock_time:
                
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]

    def move(self):
        self.x = self.x + self.dx 
        self.y = self.y + self.dy 
        self.rect.x = int(self.x) 
        self.rect.y = int(self.y) 

class Rocket(pygame.sprite.Sprite):
    def __init__(self, filename, dx, dy): #delta x and delta y
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = posy + 70
        self.rect.top = posx + 50
        x = self.rect.left
        y = self.rect.top
        self.angle = math.atan2(dy-y , dx-x) #dx and dy are the coordinates for the cursor
        self.speed = 20
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.x = x
        self.y = y
        self.exploding = False
        self.images = []
        for i in range(2):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"rocket{i}.png"))
            bitmap = pygame.transform.scale(bitmap, (50,20))
            bitmap = pygame.transform.rotate(bitmap, self.angle)
            self.images.append(bitmap)
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 90
        

    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                self.speed = self.speed + 1
            if self.exploding == False:
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]
            if self.exploding == True:
                if self.imageindex < len(self.images):
                    self.image = self.images[self.imageindex]
                    self.rect = self.image.get_rect()
                    self.rect.centerx, self.rect.centery = self.x, self.y
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                    self.kill()
                    self.exploding = False
    def move(self):
        if self.exploding == False:
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.rect.x = int(self.x) 
            self.rect.y = int(self.y)

    def playermove_R(self, speed):
        self.rect.left -= speed

    def playermove_L(self, speed):
        self.rect.left += speed

    def explode(self):
        
        self.exploding = True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'explosion.wav')))
        self.images.clear()
        for i in range(5):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"explosion{i}.png"))
            bitmap = pygame.transform.scale(bitmap, (250,250))
            self.images.append(bitmap)
            




class tkprojectile(pygame.sprite.Sprite):
    def __init__(self, filename, facing, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.bullet_size)
        self.rect = self.image.get_rect()
        self.rect.left = y
        self.rect.top = x
        self.speed_h = 10
        self.speed_v = 0
        self.facing = facing
        self.faced = False
        self.images = []
        if facing == "R":
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"tkbulletR{i}.png"))
                self.images.append(bitmap)
        if facing == "L":
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"tkbullet{i}.png"))
                self.images.append(bitmap)

        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100

    def update(self):
        if self.facing == "R":
            self.rect.move_ip(self.speed_h, self.speed_v)
        if self.facing == "L":
            self.rect.move_ip(-self.speed_h, self.speed_v)

    
    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1

                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]

    def playermove_R(self, speed):
        self.rect.left -= speed

    def playermove_L(self, speed):
        self.rect.left += speed

class Game(object): 
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background0 = Background("0.png")
        self.background1 = Background("1.png")
        self.background2 = Background("2.png")
        self.background3 = Background("3.png")
        self.background4 = Background("4.png")
        self.stormtroopers = pygame.sprite.Group()
        self.player = Player("player_standing_R0.png", 5, 100)
        self.tkprojectiles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.ammocrates = pygame.sprite.Group()
        self.healthpacks= pygame.sprite.Group()
        self.stormbies = pygame.sprite.Group()
        self.flames = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.flames_on = False
        self.sector = 0
        self.spawncount = 0
        self.speed = 1
        self.level = 1
        self.running = True
        self.length = 75
        self.game_started = False
        self.upgrade_allowed = False
        self.levelup = False
        self.xp = 0
        self.xp_gained = False
        self.xp_pos = -30
        self.current_xp = 0
        self.passed_bartime = 0
        self.run_bar = False
        self.cursors = []
        for i in range(2):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"crosshair{i}.png"))
            self.cursors.append(bitmap)
        self.imageindex = 0
        self.colorindex = 0
        self.cursor_rect = self.cursors[self.imageindex].get_rect()
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100



    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                if self.imageindex >= len(self.cursors):
                    self.imageindex = 0
                self.cursor = self.cursors[self.imageindex]
    def sector_up(self):
        global score_value
        self.spawncount = round(score_value)%10
        if self.spawncount == 0:
            self.spawn()
        if self.spawncount == 7:
            Settings.current_platforms = 0
            Settings.current_enemys = 0
        if score_value <= 1:
            self.platforms.add(Platform(10, 600,100, 10))
           

    def spawn(self):
        global score_value
        if Settings.current_enemys < Settings.max_enemys:
            Settings.current_enemys += 1
            if score_value <= 200:
                if Settings.current_platforms < Settings.max_platforms:
                    Settings.current_platforms += 1
                    self.platforms.add(Platform(randint(1500,1800), randint(100, 700),randint(100,600), 10))
                self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,1700,1, randint(0, 100), False))
            elif score_value > 200 and score_value <= 400:
                self.platforms.add(Platform(1800, 700 ,randint(100,600), 10))
                self.stormbies.add(Stormbie("stormbieL0.png",100,1700,1))

    def font(self):
        global bullets
        font = pygame.font.Font(None, 36)
        font_death = pygame.font.Font(None, 72)

        ammo_pos = 230
        if self.player.weapons_index == 0:
            Ammo = font.render("Ammo: " + str(round(bullets)) + " bullets", 1, (YELLOW))
            for b in range(bullets):
                ammo_pos = ammo_pos + 20
                pygame.draw.rect(self.screen, (YELLOW), pygame.Rect(ammo_pos, 10, 10, 20))
                pygame.draw.rect(self.screen, (RED), pygame.Rect(ammo_pos, 10, 10, 15))
                pygame.draw.rect(self.screen, (BLACK), pygame.Rect(ammo_pos, 10, 10, 20), 2)

        if self.player.weapons_index == 1:
            Ammo = font.render("Ammo: " + str(self.player.rockets) + " rockets", 1, (YELLOW))
            for r in range(self.player.rockets):
                ammo_pos = ammo_pos + 20
                self.rocket_image = pygame.image.load(os.path.join(Settings.path_image, "rocket.png")).convert_alpha()
                self.rocket_image = pygame.transform.scale(self.rocket_image, (30, 30))
                self.screen.blit(self.rocket_image, (ammo_pos, 10))



        
        Fuelprint = font.render("Fuel: " + str(round(fuel)) + " liters", 1, (GREEN))
        scoreprint = font.render("Score: " + str(round(score_value)) + "m", 1, (WHITE))
        levelprint = font.render("Level: " + str(self.level), 1, (WHITE))
        sectorprint = font.render("Sector: " + str(self.sector), 1, (WHITE))
        self.screen.blit(Ammo, (10, 10))
        self.screen.blit(Fuelprint, (10, 50))
        self.screen.blit(scoreprint, (1400, 10))
        self.screen.blit(levelprint, (1400, 50))
        self.screen.blit(sectorprint, (1400, 90))
        shealthcolor = (255, 0, 0)
        for s in self.stormtroopers:
            if s.health == 100:
                shealthcolor = (GREEN)
            elif s.health == 50:
                shealthcolor = (YELLOW)
            elif s.health == 25:
                shealthcolor = (RED)
            pygame.draw.rect(self.screen, (shealthcolor), pygame.Rect(s.tkposx, s.tkposy, s.health, 11))
            pygame.draw.rect(self.screen, (BLACK), pygame.Rect(s.tkposx, s.tkposy, s.health, 11), 2)

        zhealthcolor = (GREEN)
        for z in self.stormbies:
            if z.health == 100:
                zhealthcolor = (GREEN)
            elif z.health == 50:
                zhealthcolor = (YELLOW)
            elif z.health == 25:
                zhealthcolor = (RED)
            pygame.draw.rect(self.screen, (zhealthcolor), pygame.Rect(z.zposx, z.zposy, z.health, 11))
            pygame.draw.rect(self.screen, (BLACK), pygame.Rect(z.zposx, z.zposy, z.health, 11), 2)


     
        if self.player.health >= 3:
            Healthcolor = (0, 255, 0)
        elif self.player.health == 2:
            Healthcolor = (255, 255, 0)
        elif self.player.health == 1:
            Healthcolor = (255, 0, 0)

        health_pos = posy - 25
        for h in range(self.player.health):
            health_pos = health_pos + 25
            pygame.draw.rect(self.screen, (Healthcolor), pygame.Rect(health_pos, posx - 10, 25, 11))
            pygame.draw.rect(self.screen, (BLACK), pygame.Rect(health_pos, posx- 10, 25, 11), 2)

        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(10,75,Settings.player_fuel, 11), 2)
        pygame.draw.rect(self.screen, (GREEN), pygame.Rect(10, 75, fuel, 10))

        
        if self.xp_gained == True and self.run_bar == False and self.passed_bartime== 0:#xpbar animate down
            if self.xp_pos < 10:
                self.xp_pos = self.xp_pos + 1
                if self.xp_pos == 10:
                    if self.passed_bartime == 0:
                        self.xp_gained = False
                        self.run_bar = True
                        print("xp bar run")


        if self.run_bar == False or self.passed_bartime == 0:
            self.passed_bartime = 0
            if self.xp_gained == False and self.xp_pos > - 30: #xpbar animate up
                self.xp_pos = self.xp_pos - 1

        if self.current_xp < self.xp and self.xp_pos > -30:# and self.xp_gained == False:
            self.current_xp = self.current_xp + 0.1

        pygame.draw.rect(self.screen, (GREEN), pygame.Rect(600, self.xp_pos, self.current_xp * 5 , 30))
        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(600, self.xp_pos,Settings.next_level * 5, 30), 2)
        xp = font.render("xp: " + str(round(self.current_xp)) + "/" + str(Settings.next_level), 1, (WHITE))
        self.screen.blit(xp, (795, self.xp_pos+ 2))

 
        if self.player.energypoints == 0:
            if self.length > 0:
                self.length = self.length - 0.175
            
            pygame.draw.rect(self.screen, (RED), pygame.Rect(posy, posx - 20, self.length, 11),)
            pygame.draw.rect(self.screen, (150, 0, 0), pygame.Rect(posy, posx - 20, self.length, 11), 2)
        if self.player.energypoints == 75:
            self.length = 75
      


        pygame.draw.rect(self.screen, (BLUE), pygame.Rect(posy, posx - 20, self.player.energypoints , 11))
        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(posy, posx - 20, self.player.energypoints, 11), 2)

        
        if self.player.health <= 0:
            pygame.draw.rect(self.screen, (BLACK), pygame.Rect(0,0, 1600, 720))
            Deathscreen = font_death.render("You died", 1, (RED))
            PressR = font.render("Press R retard", 1, (WHITE))
            self.screen.blit(scoreprint, (700, 499))
            self.screen.blit(levelprint, (700, 600))
            self.screen.blit(Deathscreen, (485, Settings.window_height // 2 - 100))
            self.screen.blit(PressR, (700, Settings.window_height // 2 + 30))

        if self.upgrade_allowed == True:
            self.screen.blit(self.upgrade1, (875, 60))
            self.screen.blit(self.upgrade2, (875, 100))
            self.screen.blit(self.upgrade3, (875, 140))

    
    def upgrade_menu(self):
        self.colors = [CYAN, MAGENTA]                 #switches between colors
        if pygame.time.get_ticks() > self.clock_time: #
            self.clock_time = pygame.time.get_ticks() #
            self.colorindex += 1                      #
        if self.colorindex >= len(self.colors):       #
            self.colorindex = 0                       #
        self.color = self.colors[self.colorindex]     #


        if self.levelup == True:
            self.upgrade_allowed = True
        font = pygame.font.Font(None, 36)
        keys = pygame.key.get_pressed()
        if self.upgrade_allowed == True:
            self.upgrade1 = font.render(str(self.player.health)+ "health" + "+ 1", 1, (self.color))
            self.upgrade2 = font.render("damage up", 1, (self.color))
            self.upgrade3 = font.render("fuel + 20", 1, (self.color))

            if keys[pygame.K_1]:
                self.upgrade_allowed = False
                self.levelup = False
                Settings.player_maxhealth = Settings.player_maxhealth + 1
                self.player.health = Settings.player_maxhealth

            if keys[pygame.K_2]:
                self.upgrade_allowed = False
                self.levelup = False
                Settings.player_damage = Settings.player_damage + 0.5

            if keys[pygame.K_3]:
                self.upgrade_allowed = False
                self.levelup = False
                Settings.player_fuel = Settings.player_fuel + 50
        



    def get_pos(self):
        global posx, posy
        for s in self.stormtroopers:
            s.tkposx = s.rect.left
            s.tkposy = s.rect.top
        
        for z in self.stormbies:
            z.zposx = z.rect.left
            z.zposy = z.rect.top

        posy = self.player.rect.left
        posx = self.player.rect.top

    def shoot_bullet(self):
            global bullets
            if bullets >= 1 and self.player.weapons_index == 0:
                bullets -= 1
                self.projectiles.add(projectile("bullet0.png",self.mx ,self.my))
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'blaster.wav')))
            elif bullets <= 0 and self.player.weapons_index == 0:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'empty.wav')))
            
            if self.player.rockets >= 1 and self.player.weapons_index == 1:
                self.player.rockets = self.player.rockets - 1
                self.rockets.add(Rocket("rocket0.png",self.mx ,self.my))
                print(self.mx, self.my)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'rocket_fire.wav')))
            elif self.player.rockets <= 0 and self.player.weapons_index == 1:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'empty.wav')))
    

    def shoot_dice(self):
        for s in self.stormtroopers:
            shoot_dice = randint(1, 100)
            if shoot_dice == s.trigger and s.getting_hit == False:
                Settings.bullet_size = (100, 15)
                self.tkprojectiles.add(tkprojectile("tkbullet0.png", s.facing,s.tkposy + 80,s.tkposx -50))
                pygame.mixer.Channel(4).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'tkblast.mp3')))

                
    def leftclick(self):
        global shield_active, fuel
        leftclick = pygame.mouse.get_pressed() == (1, 0, 0)
        rightclick = pygame.mouse.get_pressed() == (0, 0, 1)
        
        if leftclick == True:
            if self.player.refilling == False:
                if self.player.energypoints > 0:
                    self.player.energypoints = self.player.energypoints - 0.25
                    self.usefuel = True
                    Player.flamethrower_on(self.player)
                    if self.flames_on == False:
                        self.flames.add(Flame("bullet0.png"))
                        self.flames_on = True
                if self.player.energypoints == 0:
                    self.usefuel = False
                    Player.flamethrower_off(self.player)
                    self.flames_on = False
                    for f in self.flames:
                        f.kill()
                

        else:
            self.flames_on = False
            self.player.flamethrower_off()
            self.usefuel = False #work in progress
        
            self.flames_on = False
            for f in self.flames:
                f.kill()
            self.player.images.clear()
            if facing == "R":
                for i in range(2):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"player_standing_R{i}.png"))
                    self.player.images.append(bitmap)
                
            if facing == "L":
                for i in range(2):
                    bitmap = pygame.image.load(os.path.join(
                            Settings.path_image, f"player_standing_L{i}.png"))
                    self.player.images.append(bitmap)
        
        if rightclick == True:
            self.player.block()
        else:
            self.player.shield = False
  

    def midclick(self):
        midclick = pygame.mouse.get_pressed() == (0, 1, 0)
        if midclick == True:
            self.shoot_bullet()
  
    def timer(self):
        if self.passed_time <= 420: #60(ticks) * 5(seconds) = 300
            self.passed_time = self.passed_time+ 1
    
    def fueltimer(self):
        if self.run_fuel == True:
                self.passed_fueltime = self.passed_fueltime+ 1

    def invtimer(self):
        if self.run_inv == True:
            if self.passed_invtime <= 90:
                self.passed_invtime = self.passed_invtime+ 1

    def xpabrtimer(self):
            if self.run_bar == True:
                if self.passed_bartime <= 90:
                    self.passed_bartime = self.passed_bartime+ 1
                if self.passed_bartime >= 90:
                    self.run_bar = False

                    
                

    def controls(self):
            global jumping
            if self.player.speed == 5:
                self.player_speed = 1
            elif self.player.speed == 10:
                self.player_speed = 2
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: 
                self.player.moveL()
                for s in self.stormtroopers:
                    s.playermove_L(self.player.speed)
                for z in self.stormbies:
                    z.playermove_L(self.player.speed)
                for a in self.ammocrates:
                    a.playermove_L(self.player.speed)
                for h in self.healthpacks:
                    h.playermove_L(self.player.speed)
                for tk in self.tkprojectiles:
                    tk.playermove_L(self.player.speed)
                for p in self.platforms:
                    p.playermove_L(self.player.speed)
                for r in self.rockets:
                    r.playermove_L(self.player.speed)
                self.background0.scroll_l(5 * self.player_speed)
                self.background1.scroll_l(4 * self.player_speed)
                self.background2.scroll_l(3 * self.player_speed)
                self.background3.scroll_l(2 * self.player_speed)
                self.background4.scroll_l(1 * self.player_speed)

            if keys[pygame.K_d]:
                self.player.moveR()
                for s in self.stormtroopers:
                    s.playermove_R(self.player.speed)
                for z in self.stormbies:
                    z.playermove_R(self.player.speed)
                for a in self.ammocrates:
                    a.playermove_R(self.player.speed)
                for h in self.healthpacks:
                    h.playermove_R(self.player.speed)
                for tk in self.tkprojectiles:
                    tk.playermove_R(self.player.speed)
                for p in self.platforms:
                    p.playermove_R(self.player.speed)
                for r in self.rockets:
                    r.playermove_R(self.player.speed)
                self.background0.scroll_r(5 * self.player_speed)
                self.background1.scroll_r(4 * self.player_speed)
                self.background2.scroll_r(3 * self.player_speed)
                self.background3.scroll_r(2 * self.player_speed)
                self.background4.scroll_r(1 * self.player_speed)
            if keys[pygame.K_LSHIFT]:
                self.player.sprinting = True
                self.player.sprint()
            else:
                self.player.walk()
            if keys[pygame.K_w]:
                self.player.moveUp()
            if keys[pygame.K_r]:
                #self.reload()
                self.restart()
            if keys[pygame.K_p]:
                self.game_started = False
        
    def restart(self):
        global bullets, fuel, score_value, lives, spawncount, count, level
        for s in self.stormtroopers:
            s.kill()
        for p in self.projectiles:
            p.kill()
        for tkp in self.tkprojectiles:
            tkp.kill()
        for a in self.ammocrates:
            a.kill()
        for h in self.healthpacks:
            h.kill()
        for f in self.flames:
            f.kill()
        for z in self.stormbies:
            z.kill()
        for pt in self.platforms:
            pt.kill()
        self.level = 1
        self.xp = 0
        self.current_xp = 0
        score_value = 0
        self.player.energypoints = 75
        self.player.endurance = 100
        self.player.rockets = Settings.start_rockets
        bullets = 20
        fuel = 200
        self.player.health = Settings.player_maxhealth
        self.sector = 0
        self.player.rect.x = 50
        self.player.rect.y = 300
        pygame.mixer.music.rewind()


    def collide(self):
        for pt in self.platforms:
           
            if self.player.rect.bottom >= pt.rect.top and self.player.rect.bottom <= pt.rect.bottom:
                if self.player.rect.right  >= pt.rect.left and self.player.rect.left <= pt.rect.right:
                    self.player.platform_y = pt.rect.top - 150
                    self.player.rect.bottom = pt.rect.top
                    #self.player.on_ground = True
                # else:
                #     self.player.platform_y = 570

            # if self.player.rect.top  <= pt.rect.bottom and self.player.rect.top >= pt.rect.top:
            #     if self.player.rect.right  >= pt.rect.left and self.player.rect.left <= pt.rect.right:
            #         self.player.rect.top = pt.rect.bottom
            #         self.player.on_ground = True

            for s in self.stormtroopers:
                if s.rect.bottom >= pt.rect.top and s.rect.bottom <= pt.rect.bottom:
                    if s.rect.right  >= pt.rect.left and s.rect.left <= pt.rect.right:
                        s.platform_y = pt.rect.top - 150
                        s.rect.bottom = pt.rect.top

                if s.rect.top  <= pt.rect.bottom and s.rect.top >= pt.rect.top:
                    if s.rect.right  >= pt.rect.left and s.rect.left <= pt.rect.right:
                        s.rect.top = pt.rect.bottom


            for z in self.stormbies:
                if z.rect.bottom >= pt.rect.top and z.rect.bottom <= pt.rect.bottom:
                    if z.rect.right  >= pt.rect.left and z.rect.left <= pt.rect.right:
                        z.platform_y = pt.rect.top - 150
                        z.rect.bottom = pt.rect.top

                if z.rect.top  <= pt.rect.bottom and z.rect.top >= pt.rect.top:
                    if z.rect.right  >= pt.rect.left and z.rect.left <= pt.rect.right:
                        z.rect.top = pt.rect.bottom

            for a in self.ammocrates:
                if a.rect.bottom >= pt.rect.top and a.rect.bottom <= pt.rect.bottom:
                    if a.rect.right  >= pt.rect.left and a.rect.left <= pt.rect.right:
                        a.platform_y = pt.rect.top
                        a.rect.bottom = pt.rect.top
                        a.on_ground = True

            for h in self.healthpacks:
                if h.rect.bottom >= pt.rect.top and h.rect.bottom <= pt.rect.bottom:
                    if h.rect.right  >= pt.rect.left and h.rect.left <= pt.rect.right:
                        h.platform_y = pt.rect.top
                        h.rect.bottom = pt.rect.top
                        h.on_ground = True

    def countdown(time_sec): #FÜR SPÄTER
        while time_sec:
            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            time_sec -= 1

    def gravity(self):
        if jumping == False:
            self.get_pos()
            self.player.rect.top += 10

            if self.player.rect.top >= 7770:#570:
                self.player.rect.top = 7770
            
        for s in self.stormtroopers:
            s.rect.top += 10
            if s.rect.top >= 570:
                s.rect.top = 570

        for z in self.stormbies:
            z.rect.top += 10
            if z.rect.top >= 570:
                z.rect.top = 570

   

    def hit(self):
        for s in self.stormtroopers:
            if s.health <=0:
                s.kill()
                self.spawncount = self.spawncount - 1
                self.reward()

            if pygame.sprite.spritecollide(s, self.projectiles, True):
                s.health = s.health - 25 * Settings.player_damage
                s.getting_hit = True
            else:
                s.getting_hit = False


            for r in self.rockets:
                if pygame.sprite.spritecollide(s, self.rockets, False):
                    s.health = s.health - 100 * Settings.player_damage
                    r.explode()
            if s.rect.top >= 570:
                s.kill()
   
            if pygame.sprite.spritecollide(s, self.flames, False):
                s.health = s.health - 3 * Settings.player_damage
                s.getting_hit = True
            else:
                s.getting_hit = False

        if self.player.rect.top >= 570:
            self.player.kill()
            self.player.health = self.player.health - 3

        for pt in self.platforms:
            for r in self.rockets:
                if pygame.sprite.spritecollide(pt,self.rockets, False):
                    r.explode()
                

        for z in self.stormbies:
            if pygame.sprite.spritecollide(z, self.projectiles, True):
                z.health = z.health - 25 * Settings.player_damage
                if z.health <=0:
                    z.kill()
                    self.reward()

            if pygame.sprite.spritecollide(z, self.flames, False):
                z.health = z.health - 10 * Settings.player_damage
                if z.health <=0:
                    z.kill()
                    self.reward()

        if pygame.sprite.spritecollide(self.player, self.tkprojectiles, True): #and self.player.shield == False:
                self.player.invincible_off()
                if self.player.shield == False and self.player.invincible == False:
                    self.player.get_invincible()
                    self.player.health = self.player.health - 1
                    
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'hurt.wav')))
                    if self.player.health <= 0:
                        self.player.kill()
                if self.player.shield == True:
                        pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'darksaber.wav')))
        
        if pygame.sprite.spritecollide(self.player, self.rockets, False) :
            for r in self.rockets:
                if r.exploding == True:
                    self.player.invincible_off()
                    if self.player.shield == False and self.player.invincible == False:
                        self.player.get_invincible()
                        self.player.health = self.player.health - 1


        if pygame.sprite.spritecollide(self.player, self.stormbies, False):
                self.player.invincible_off()
                if self.player.invincible == False:
                    self.player.get_invincible()
                    self.player.health = self.player.health - 1
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'hurt.wav')))
        
    
    def reward(self):
        dice6 = randint(1, 6)
        self.xp = self.xp + 5
        self.xp_gained = True
        if self.xp == Settings.next_level:
            self.level = self.level + 1
            self.levelup = True
            self.current_xp = 0
            self.xp = 0

        if dice6 == 1:
            self.ammocrates.add(Pickups("ammocrate.png"))
        elif dice6 == 2:
            self.healthpacks.add(Pickups("healthpack.png"))

        elif dice6 == 3:
            pass
            #self.fuelpacks.add(Pickups("fuelpack.png"))


    def pickup(self):
        if pygame.sprite.spritecollide(self.player, self.ammocrates, True):
            global bullets
            bullets = bullets + 4
            self.player.rockets = self.player.rockets + 1
        if self.player.health < Settings.player_maxhealth:
            if pygame.sprite.spritecollide(self.player, self.healthpacks, True):
                self.player.health = self.player.health + 1
       

    def draw_start(self):
        Titlefont = pygame.font.Font(None, 72)
        self.background4.draw(self.screen)
        self.background3.draw(self.screen)
        self.background2.draw(self.screen)
        self.background1.draw(self.screen)
        self.background0.draw(self.screen)
        Title = Titlefont.render("Galaxy Run", 1, (WHITE))
        self.Startfont = pygame.font.Font(None, 39)
        Start = self.Startfont.render("Start Adventure", 1, (WHITE))
        
        self.screen.blit(Title, (Settings.window_width // 2 - 150, Settings.window_height // 2 - 100))
        #pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(Settings.window_width // 2 - 100,Settings.window_height // 2 , 200, 100),)
        self.screen.blit(Start, (Settings.window_width // 2 - 100,Settings.window_height // 2 + 30))
        self.background0.scroll_r(5)
        self.background1.scroll_r(4)
        self.background2.scroll_r(3)
        self.background3.scroll_r(2)
        self.background4.scroll_r(1)
        pygame.display.flip()

    def event_start(self):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                        self.running = False
                elif event.type == pygame.QUIT:         
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Settings.window_width // 2 - 100 <= mouse[0] <= Settings.window_width // 2 + 100 and Settings.window_height // 2 <= mouse[1] <= Settings.window_height // 2 + 100:
                    self.game_started = True
                    print("Starting...")
        if Settings.window_width // 2 - 100 <= mouse[0] <= Settings.window_width // 2 + 100 and Settings.window_height // 2 <= mouse[1] <= Settings.window_height // 2 + 100: #bugged
                pygame.draw.rect(self.screen, (0,0,255), pygame.Rect(Settings.window_width // 2 - 100,Settings.window_height // 2 , 200, 100),)
                self.Startfont = pygame.font.Font(None, 100)
                Start = self.Startfont.render("Start Adventure", 1, (BLACK))
                self.screen.blit(Start, (Settings.window_width // 2 - 100,Settings.window_height // 2 + 30))
                pygame.display.flip()
                

    def run(self):
        while self.running:
            self.clock.tick(60)                         
            if self.game_started == True:
                self.watch_for_events()
                self.update()
                self.draw()
                self.get_cursor_center()
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)
                self.draw_start()
                self.event_start()
        pygame.quit()       

    def watch_for_events(self):
        global jumping
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mx, self.my = pygame.mouse.get_pos()
                self.midclick()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    self.running = False
                if event.key == pygame.K_SPACE:
                    jumping = True
                if event.key == pygame.K_q:
                    self.player.change_previous_weapon()
                if event.key == pygame.K_e:
                    self.player.change_next_weapon()

            elif event.type == pygame.QUIT:         
                self.running = False
        
    def get_cursor_center(self):
        global facing
        self.cursor_rect.center = pygame.mouse.get_pos()
        if self.cursor_rect.center[0] < self.player.rect.center[0]:
            facing = "L"
        elif self.cursor_rect.center[0] > self.player.rect.center[0]:
            facing = "R"
        

    def update(self):
        self.upgrade_menu()
        self.stormtroopers.update()
        self.stormbies.update()
        self.projectiles.update()
        self.tkprojectiles.update()
        Game.controls(self)
        Player.refill(self.player)
        Game.hit(self)
        Player.animate(self.player)
        self.flames.update()
        for tk in self.tkprojectiles:
            tk.animate()
        for p in self.projectiles:
            p.move()
            p.animate()
        for r in self.rockets:
            r.move()
            r.animate()
        for s in self.stormtroopers:
            s.animate()
        for z in self.stormbies:
            z.animate()
        for f in self.flames:
            f.animate()
        self.gravity()
        self.collide()
        self.leftclick()
        self.ammocrates.update()
        self.healthpacks.update()
        Game.pickup(self)
        Game.get_pos(self)
        self.player.jump()
        self.sector_up()
        self.shoot_dice()
        self.animate()
        self.xpabrtimer()


    def draw(self):
        self.background4.draw(self.screen)
        self.background3.draw(self.screen)
        self.background2.draw(self.screen)
        self.background1.draw(self.screen)
        self.background0.draw(self.screen)
        self.platforms.draw(self.screen)
        self.stormtroopers.draw(self.screen)
        self.stormbies.draw(self.screen)
        self.player.draw(self.screen)
        self.tkprojectiles.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.ammocrates.draw(self.screen)
        self.healthpacks.draw(self.screen)
        self.flames.draw(self.screen)
        self.rockets.draw(self.screen)
        self.font()
        self.screen.blit(self.cursor,self.cursor_rect) # draw the cursor
        pygame.display.flip()

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "50, 50"

    game = Game()
    game.run()