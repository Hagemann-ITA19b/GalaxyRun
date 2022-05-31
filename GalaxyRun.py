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
shieldpoints = 100
jumping = False
level = 0
facing = "R"
posx = 0
posy = 0
offset_x = 0
offset_y = 0
shaking = False
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
ORANGE = (255, 165, 0)


class Settings(object):
    window_height = 720
    window_width = 1600
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "files")
    player_size = (70,150)
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
    obx1 = -1000
    obx2 = -1500
    title = "Galaxy Run"

class Sounds(object):
    mixer.init()
    blaster_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "blaster.wav"))
    blaster_sound.set_volume(0.01)
    refill_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "refill.mp3"))
    refill_sound.set_volume(0.01)
    jetpack_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "jetpack.wav"))
    jetpack_sound.set_volume(0.01)
    shield_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "darksaber.wav"))
    shield_sound.set_volume(0.01)
    explosion_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "explosion.wav"))
    explosion_sound.set_volume(0.01)
    shields_low = pygame.mixer.Sound(os.path.join(Settings.path_image, "shields_low.mp3"))
    shields_low.set_volume(0.1)
    tk_blast = pygame.mixer.Sound(os.path.join(Settings.path_image, "tkblast.mp3"))
    tk_blast.set_volume(0.01)
    empty_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "empty.wav"))
    empty_sound.set_volume(0.01)
    rocket_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "rocket_fire.wav"))
    rocket_sound.set_volume(0.01)
    player_hit = pygame.mixer.Sound(os.path.join(Settings.path_image, "hurt.wav"))
    player_hit.set_volume(0.01)
    ob_distant = pygame.mixer.Sound(os.path.join(Settings.path_image, "ob_distant.wav"))
    ob_distant.set_volume(0.1)
    death = pygame.mixer.Sound(os.path.join(Settings.path_image, "death.mp3"))
    death.set_volume(1)
    
    

    def play_sound(sound):
        busy = pygame.mixer.Channel(3).get_busy()
        if sound == "blaster":
            pygame.mixer.Channel(1).play(Sounds.blaster_sound)
        if sound == "refill":
            pygame.mixer.Channel(2).play(Sounds.refill_sound)
        if sound == "explosion":
            pygame.mixer.Channel(3).play(Sounds.explosion_sound)
        if sound == "shields_low":
            pygame.mixer.Channel(4).play(Sounds.shields_low)
        if sound == "tk_blast":
            pygame.mixer.Channel(5).play(Sounds.tk_blast)
        if sound == "empty":
            pygame.mixer.Channel(6).play(Sounds.empty_sound)
        if sound == "rocket":
            pygame.mixer.Channel(7).play(Sounds.rocket_sound)
        if sound == "player_hit":
            pygame.mixer.Channel(0).play(Sounds.player_hit)
        if sound == "jetpack":
            pygame.mixer.Channel(7).play(Sounds.jetpack_sound)
        if sound == "shield_hit":
            pygame.mixer.Channel(0).play(Sounds.shield_sound)
        if sound == "jetpack":
            pygame.mixer.Channel(0).play(Sounds.jetpack_sound)
        if sound == "ob_distant" and busy == False:
            pygame.mixer.Channel(3).play(Sounds.ob_distant)
            print("playing")
    

    def play_music(audio):
        mixer.music.unload()
        mixer.music.load(os.path.join(Settings.path_image, audio))
        pygame.mixer.music.set_volume(0.05)
        mixer.music.play()



    

class Background():
    def __init__(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.rectimg = self.image.get_rect()
        self.bgx = 0
        self.bgy = 0
         
    def scroll_r(self, scrollspeed):
        self.bgx = self.bgx - scrollspeed
        if self.bgx <= -Settings.window_width:
            self.bgx = 0

    def scroll_l(self, scrollspeed):
        self.bgx = self.bgx + scrollspeed
        if self.bgx >= Settings.window_width:
            self.bgx = 0
             
    def draw(self, screen):
        screen.blit(self.image,(self.bgx-Settings.window_width,0 + offset_y))
        screen.blit(self.image,(self.bgx,0+offset_y))
        screen.blit(self.image,(self.bgx+Settings.window_width,0 + offset_y))


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
        self.rect.left += self.speed_h
        self.rect.top += self.speed_v
        if self.rect.left <= posy: #0:
                self.speed_h = 2
                self.facing = "R"

        if self.rect.left >= posy:
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
        self.rect.left = self.tkposx
        self.rect.top = self.tkposy
        self.speed_h = randint( 1, 3)
        self.speed_v = 0
        self.health = health
        self.images = []
        self.facing = "L"
        bitmap = pygame.image.load(os.path.join(
            Settings.path_image, f"stormtrooper0.png"))
        self.images.append(bitmap)
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100
        self.platform_y = 0
        self.movecount = 0
        self.getting_hit = getting_hit

        self.jumping = False
        self.velocity_index = 0
        self.velocity = ([-10,-9.5,-9,-8.5,-8,-7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])



    def jump(self):
        if self.jumping == True:
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1
            if self.rect.top >= self.platform_y:
                self.rect.top = self.platform_y
                self.velocity_index = 0
                if self.rect.top == self.platform_y:
                    self.jumping = False



    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1

                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]


    def get_direction(self):
        if self.movecount == 30:
            self.moveright = False
        elif self.movecount == 0:
            self.moveright = True
    
    def move(self):
        self.get_direction()
        if self.moveright == True:
            self.movecount += 1
            self.rect.left += self.speed_h
        elif self.moveright == False:
            self.movecount -= 1
            self.rect.left -= self.speed_h


    def playermove_R(self, speed):
        self.rect.left -= speed

    def playermove_L(self, speed):
        self.rect.left += speed
        
    def update(self):
        self.move()
        if self.rect.left <= posy:
            self.facing = "R"
        if self.rect.left >= posy:
            self.facing = "L"


        if self.facing == "L":
            self.images.clear()
            if self.getting_hit == False:
                for i in range(2):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooper{i}.png"))
                    self.images.append(bitmap)
            elif self.getting_hit == True:
                for i in range(3):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooperL_hit{i}.png"))
                    self.images.append(bitmap)

        elif self.facing == "R":
            self.images.clear()
            if self.getting_hit == False:
                for i in range(2):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooper{i}.png"))
                    rotate = pygame.transform.flip(bitmap, True, False)
                    self.images.append(rotate)
            elif self.getting_hit == True:
                for i in range(3):
                    bitmap = pygame.image.load(os.path.join(
                        Settings.path_image, f"stormtrooperR_hit{i}.png"))
                    self.images.append(bitmap)



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
        self.platform_y = 0
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
        if self.sprinting == True:
            self.speed = 10
            self.score_muliplier = 0.2

        else:
            self.sprinting = False
            self.speed = 5
            self.score_muliplier = 0.1
        

    def pos(self):
        global offset_x                              #Gibt die Startposition an 
        self.rect.left = 50 + offset_x
        self.rect.top = 399
    
    def get_pos(self):
        global posx, posy
        posy = self.rect.left
        posx = self.rect.top

    def moveL(self):
        global facing, score_value
        Player.get_pos(self)
        if score_value < 16:                     #Macht die Border unpassierbar
            self.rect.left = self.rect.left - self.speed
        if lives > 0:
            score_value -= self.score_muliplier   #Spieler wird nach links verschoben
      
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
        if self.rect.left < Settings.window_width // 2:
            self.rect.left = self.rect.left + self.speed
        if self.health > 0:
            score_value += self.score_muliplier
               
       
        if self.shield == False and self.flames_on == False and self.sprinting == False and jumping == False:
            self.images.clear()
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
            Sounds.play_sound("jetpack")
            if self.rect.top <= 570: 
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
        if self.energypoints <= 0:
            if self.playing_shieldlow == False:
                Sounds.play_sound("shields_low")
                self.playing_shieldlow = True
            Game.timer(self)
        if self.passed_time >= 420:
            self.refilling = True
            if self.playing_shieldrefill == False:
                Sounds.play_sound('refill')
                self.playing_shieldrefill = True
            self.energypoints = self.energypoints + 0.5
            if self.energypoints >= 75:
                self.refilling = False
                self.passed_time = 0
                self.playing_shieldrefill = False
                self.playing_shieldlow = False
        
        if self.usefuel == True:
            self.run_fuel = False
            self.passed_fueltime = 0
       
        if self.rect.top == self.platform_y and fuel < Settings.player_fuel:
            fuel += 1

        if self.endurance < 100:
            self.endurance += 1
                        

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
        self.durability = 200

    def playermove_R(self, speed):
            self.rect.left -= speed

    def playermove_L(self, speed):
            self.rect.left += speed
        
    def update(self):
        if self.durability <= 150:
            self.image.fill(YELLOW)
        if self.durability <= 100:
            self.image.fill(ORANGE)
        if self.durability <= 50:
            self.image.fill(RED)
        if self.durability <= 0:
            self.kill()

class Pickups(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.left = randint(Settings.window_width // 2, Settings.window_width - 50)
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
            self.rect.left = posy + 70
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


class Laser(pygame.sprite.Sprite):
    def __init__(self ,dx, dy):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.left = posy 
        self.rect.top = posx
        x = self.rect.left
        y = self.rect.top
        self.angle = math.atan2(dy-y , dx-x) #dx and dy are the coordinates for the cursor
        self.speed = 20
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.x = x
        self.y = y
    
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x) 
        self.rect.y = int(self.y)

    def playermove_R(self, speed):
        self.rect.left -= speed

    def playermove_L(self, speed):
        self.rect.left += speed




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
        global shaking
        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + self.animation_time
            self.imageindex += 1
            self.speed = self.speed + 1
        if self.exploding == False:
            if self.imageindex >= len(self.images):
                self.imageindex = 0
            self.image = self.images[self.imageindex]
        if self.exploding == True:
            shaking = True
            if self.imageindex < len(self.images):
                self.image = self.images[self.imageindex]
                self.rect = self.image.get_rect()
                self.rect.centerx, self.rect.centery = self.x, self.y
            if self.imageindex >= len(self.images):
                self.imageindex = 0
                shaking = False
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
        Sounds.play_sound("explosion")
        self.images.clear()
        for i in range(5):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"explosion{i}.png"))
            bitmap = pygame.transform.scale(bitmap, (250,250))
            self.images.append(bitmap)
        
            
class OB(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.left = randint(int(Settings.obx2),int(Settings.obx1))
        self.rect.top = -100
        self.speed_h = 0
        self.speed_v = randint(40,50)
        self.images = []
        self.exploding = False
        for i in range(3):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"tkbullet{i}.png"))
            bitmap = pygame.transform.scale(bitmap, (170,50))
            bitmap = pygame.transform.rotate(bitmap, 90)
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
                    if self.exploding == True:
                        self.kill()
                self.image = self.images[self.imageindex]

    def move(self):
        self.despawn()
        if Settings.obx1 < 0:
            Settings.obx1 += 0.5
            Settings.obx2 += 0.5
        else:
            Settings.obx1 += 0.1
            Settings.obx2 += 0.1
        self.rect.move_ip(self.speed_h, self.speed_v)

    def explode(self):
        self.speed_h = 0
        self.speed_v = 0
        self.exploding = True
        self.images.clear()
        for i in range(5):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"explosion{i}.png"))
            bitmap = pygame.transform.scale(bitmap, (250,250))
            self.images.append(bitmap)

    def playermove_R(self, speed, sprint_on):
        if sprint_on == False:
            Settings.obx1 = Settings.obx1 - 0.5
            Settings.obx2 = Settings.obx2 - 0.5
        else:
            Settings.obx1 = Settings.obx1 - 1
            Settings.obx2 = Settings.obx2 - 1

    def playermove_L(self, speed, sprint_on):
        if sprint_on == False:
            Settings.obx1 = Settings.obx1 + 0.5
            Settings.obx2 = Settings.obx2 + 0.5
        else:
            Settings.obx1 = Settings.obx1 + 1
            Settings.obx2 = Settings.obx2 + 1

        self.speed_h = 0

    def despawn(self):
        if self.rect.top > Settings.window_height - 100:
            self.kill()

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

class Cutscene():
    def __init__(self, image, text, text2, text3, addedtext, audio, audio2, audio3, texttime1, texttime2, texttime3):
        self.image = image
        self.audio = audio
        self.audio2 = audio2
        self.audio3 = audio3
        self.texttime1 = texttime1
        self.texttime2 = texttime2
        self.texttime3 = texttime3
        self.y = -420
        self.text = text
        self.text2 = text2
        self.text3 = text3
        self.addedtext = addedtext
        self.text_font = pygame.font.Font(None, 30)
        self.text_color = BLACK
        self.text_pos = (10, 600)
        self.text_posx = 10
        self.text_posy = 600
        self.textindex = 0
        self.textlist = self.text.split("#")
        self.textlist.append(self.text)
        self.letter = self.textlist[self.textindex]
        self.fulltext = []
        self.fulltext.append(self.letter)
        self.talk = True
        self.animate_up = True
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = self.texttime1
        self.played_audio = False
        self.dropped_down = False
        self.spokentext = 1
        self.which_audio = 1
        self.end_cutscene = False
        self.up = False


    def next_phrase(self):
        if self.talk == False and self.spokentext < self.addedtext:
            self.fulltext.clear()
            self.textindex = 0
            if self.spokentext == 1:
                self.textlist = self.text2.split("#")
                self.textlist.append(self.text2)
                self.animation_time = self.texttime2
            elif self.spokentext == 2:
                self.textlist = self.text3.split("#")
                self.textlist.append(self.text3)
                self.animation_time = self.texttime3
            self.which_audio = self.which_audio + 1
            self.played_audio = False
            self.talk = True
            self.spokentext = self.spokentext + 1

        if self.spokentext == self.addedtext and self.talk == False:
            self.up = True

            
    def get_pos(self):
        if self.y == -50:
            self.animate_up = True
        if self.y == -100:
            self.animate_up = False
    
    def play_audio(self, audio):
        if audio == 1:
            audio = self.audio
        if audio == 2:
            audio = self.audio2
        if audio == 3:
            audio = self.audio3
        if self.played_audio == False:
            playing_audio =pygame.mixer.Sound(os.path.join(Settings.path_image, audio))
            playing_audio.set_volume(0.01)
            pygame.mixer.Channel(0).play(playing_audio)
            self.played_audio = True

    def animate(self):
        if self.dropped_down == False:
            if self.y < -100:
                self.y += 5
            if self.y == -100:
                self.dropped_down = True
            
        if self.up == True:
            if self.y > -500:
                self.y -= 5
            if self.y == -500:
                self.end_cutscene = True

        if self.dropped_down == True:
            self.get_pos()
            if self.animate_up == True:
                self.y = self.y - 0.5
            elif self.animate_up == False:
                self.y = self.y + 0.5

            if self.talk == True:
                self.play_audio(self.which_audio)
                print(self.which_audio)
                if pygame.time.get_ticks() > self.clock_time:
                    self.clock_time = pygame.time.get_ticks() + self.animation_time
                    self.textindex += 1
                    if self.textindex >= len(self.textlist) -1:
                        self.textindex = len(self.textlist) -2
                        self.talk = False
                        self.next_phrase()
                        

                    self.letter = self.textlist[self.textindex]
                    self.fulltext.append(self.letter)

    
            
        
    def draw(self, screen):
        screen.blit(self.image, (800, self.y))
        pygame.draw.rect(screen, (WHITE), pygame.Rect(self.text_pos[0] - 10, self.text_pos[1] - 10, 1600, 400))
        pygame.draw.rect(screen, (BLACK), pygame.Rect(self.text_pos[0]- 10, self.text_pos[1] -10, 1600, 400),8)
        test = self.text_font.render(" ".join(self.fulltext), 1, (BLACK))
        screen.blit(test, (self.text_posx, self.text_posy))




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
        self.dimmed_background = Background("dimmed_background.png")
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
        self.orbital_bombardment = pygame.sprite.Group()
        self.flames_on = False
        self.sector = 0
        self.spawncount = 0
        self.speed = 1
        self.level = 1
        self.running = True
        self.length = 75
        self.game_started = False
        self.settings_window = False
        self.upgrade_allowed = False
        self.levelup = False
        self.xp = 0
        self.xp_gained = False
        self.xp_pos = -30
        self.current_xp = 0
        self.passed_bartime = 0
        self.run_bar = False
        self.images = []
        self.cutscene_on = False
        self.sc1 = Cutscene(pygame.image.load(os.path.join(Settings.path_image, 'glados2.png')),"H#e#l#l#o# #f#o#r#c#e#d# #v#o#l#u#n#t#e#e#r# #1#2#7#4#0#.#",
                    "#Y#o#u# #d#o#n#'#t# #e#x#a#c#t#l#y# #l#o#o#k# #l#i#k#e# #t#h#e# #s#a#v#i#o#r# #o#f# #h#u#m#a#n#i#t#y#,# #b#u#t# #s#t#i#l#l#,# #y#o#u# #a#r#e# #t#h#e#i#r# #l#a#s#t# #c#h#a#n#c#e#.",
                    "#I#'m# #d#e#t#e#c#t#i#n#g# #s#e#v#e#r#a#l# #h#o#s#t#i#l#e# #s#i#g#n#a#l#s# #a#h#e#a#d#.#G#o#o#d# #l#u#c#k#.#", 3,"sc1_audio1.wav","sc1_audio2.wav", "sc1_audio3.wav", 120,60,80)
        for i in range(2):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"crosshair{i}.png"))
            self.images.append(bitmap)
        self.imageindex = 0
        self.colorindex1 = 0
        self.cursor_rect = self.images[self.imageindex].get_rect()
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100
        self.shake_screen = False
        self.shake = 1
        self.endless_mode = False

        # for controls
        self.changing_keybindings = False
        self.changing_key = None
        self.walkR_key = pygame.K_d
        self.walkL_key = pygame.K_a
        self.jump_key = pygame.K_SPACE
        self.shoot_key = pygame.K_x
        self.sprint_key = pygame.K_LSHIFT
        self.pause_key = pygame.K_p
        self.jetpack_key = pygame.K_w

        self.image = pygame.image.load(os.path.join(Settings.path_image, 'glados2.png'))
        self.allowed_to_jump = False
        self.cutscene_played = None
        
        self.multiply_font1 = False
        self.fontmultiplier1 = 1

        self.d_images = []
        self.d_images.append(pygame.image.load(os.path.join(Settings.path_image, 'deathscreen0.png')))
        self.d_imageindex = 0
        self.deathimg = self.d_images[self.d_imageindex]
        self.game_over = False

    def start_ob(self):
        global shaking
        self.orbital_bombardment.add((OB("glados2.png")))

        if Settings.obx1 > self.player.rect.left - 800:
            self.shake = 1

        if Settings.obx1 > self.player.rect.left - 700:
            self.shake = 2

        if Settings.obx1 > self.player.rect.left - 600:
            self.shake = 3

        if Settings.obx1 > self.player.rect.left - 500:
            self.shake = 4

        if Settings.obx1 > self.player.rect.left - 400:
            self.shake = 5

        if Settings.obx1 > self.player.rect.left - 300:
            self.shake = 6

        if Settings.obx1 > self.player.rect.left - 200:
            self.shake = 7

        if Settings.obx1 > self.player.rect.left - 100:
            self.shake = 8

        if Settings.obx1 > self.player.rect.left:
            self.shake = 9


        if Settings.obx1 < 0:
            Sounds.play_sound("ob_distant")
        if Settings.obx1 > 0 or shaking == True:
            self.screen_shake()
        
        elif self.player.rect.left > Settings.window_width // 2:
            self.player.rect.left -= 1
    
    def screen_shake(self):
        global offset_x, offset_y
        offset_x = randint(-self.shake,self.shake)
        offset_y = randint(-self.shake,self.shake)
        for s in self.stormtroopers:
            s.rect.x+=offset_x
            s.rect.y+=offset_y
        for z in self.stormbies:
            z.rect.x+=offset_x
            z.rect.y+=offset_y
        for a in self.ammocrates:
            a.rect.x+=offset_x
            a.rect.y+=offset_y
        for h in self.healthpacks:
            h.rect.x+=offset_x
            h.rect.y+=offset_y
        for tk in self.tkprojectiles:
            tk.rect.x+=offset_x
            tk.rect.y+=offset_y
        for p in self.platforms:
            p.rect.x+=offset_x
            p.rect.y+=offset_y
        for r in self.rockets:
            r.rect.x+=offset_x
            r.rect.y+=offset_y
        for o in self.orbital_bombardment:
            o.rect.x+=offset_x
            o.rect.y+=offset_y
        self.player.rect.x+=offset_x
        self.player.rect.y+=offset_y
        self.background0.bgx+=offset_x
        self.background1.bgx+=offset_x
        self.background2.bgx+=offset_x
        self.background3.bgx+=offset_x
        self.background4.bgx+=offset_x




    def animate(self):
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + self.animation_time
                self.imageindex += 1
                if self.imageindex >= len(self.images):
                    self.imageindex = 0
                self.image = self.images[self.imageindex]

    def sector_up(self):
        global score_value
        if score_value <= 1:
            if Settings.current_platforms < Settings.max_platforms:
                self.platforms.add(Platform(10, 600,100, 10))
                Settings.current_platforms = Settings.current_platforms + 1
        self.spawncount = round(score_value)%10
        if self.spawncount == 0:
            self.spawn()
        if self.spawncount == 7:
            Settings.current_platforms = 0
            Settings.current_enemys = 0

        if score_value < 2 and not self.cutscene_played == 1:
            self.cutscene_on = True
           

    def spawn(self):
        global score_value
        if Settings.current_enemys < Settings.max_enemys:
            Settings.current_enemys += 1
            if self.endless_mode == False:
                if score_value <= 200:
                    if Settings.current_platforms < Settings.max_platforms:
                        Settings.current_platforms += 1
                        ptx = randint(1500,1800)
                        pty = randint(100, 700)
                        ptl = randint(100,600)
                        self.platforms.add(Platform(ptx,pty ,ptl, 10))
                        self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,ptx + randint(10, ptl - 60),pty - 160, randint(0, 100), False))
                    
                elif score_value > 200 and score_value <= 400:
                    self.platforms.add(Platform(1800, 700 ,randint(100,600), 10))
                    self.stormbies.add(Stormbie("stormbieL0.png",100,1700,1))

            elif self.endless_mode == True:
                if Settings.current_platforms < Settings.max_platforms:
                    Settings.current_platforms += 1
                    ptx = randint(1500,1800)
                    pty = randint(100, 700)
                    ptl = randint(100,600)
                    self.platforms.add(Platform(ptx,pty ,ptl, 10))
                    self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,ptx + randint(10, ptl - 60),pty - 160, randint(0, 100), False))

    def font(self):
        global bullets, offset_x, offset_y
        font = pygame.font.Font(None, 36)


        ammo_pos = 230
        if self.player.weapons_index == 0:
            Ammo = font.render("Ammo: " + str(round(bullets)) + " bullets", 1, (YELLOW))
            for b in range(bullets):
                ammo_pos = ammo_pos + 20
                pygame.draw.rect(self.screen, (YELLOW), pygame.Rect(ammo_pos+offset_x, 10+offset_y, 10, 20))
                pygame.draw.rect(self.screen, (RED), pygame.Rect(ammo_pos+offset_x, 10+offset_y, 10, 15))
                pygame.draw.rect(self.screen, (BLACK), pygame.Rect(ammo_pos+offset_x, 10+offset_y, 10, 20), 2)

        if self.player.weapons_index == 1:
            Ammo = font.render("Ammo: " + str(self.player.rockets) + " rockets", 1, (YELLOW))
            for r in range(self.player.rockets):
                ammo_pos = ammo_pos + 20
                self.rocket_image = pygame.image.load(os.path.join(Settings.path_image, "rocket.png")).convert_alpha()
                self.rocket_image = pygame.transform.scale(self.rocket_image, (30, 30))
                self.screen.blit(self.rocket_image, (ammo_pos+offset_x, 10+offset_y))

        fpscounter = font.render(str(round(self.clock.get_fps())), 1, (YELLOW))
        Fuelprint = font.render("Fuel: " + str(round(fuel)) + " liters", 1, (GREEN))
        scoreprint = font.render("Score: " + str(round(score_value)) + "m", 1, (WHITE))
        levelprint = font.render("Level: " + str(self.level), 1, (WHITE))
        sectorprint = font.render("Sector: " + str(self.sector), 1, (WHITE))

        self.screen.blit(fpscounter, (1570+offset_x, 10+offset_y))
        self.screen.blit(Ammo, (10+ offset_x, 10+offset_y))
        self.screen.blit(Fuelprint, (10+ offset_x, 50+ offset_y))
        self.screen.blit(scoreprint, (1400+ offset_x, 10+ offset_y))
        self.screen.blit(levelprint, (1400+ offset_x, 50+offset_y))
        self.screen.blit(sectorprint, (1400+ offset_x, 90+ offset_y))

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

        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(10+offset_x,75+offset_y,Settings.player_fuel, 11), 2)
        pygame.draw.rect(self.screen, (GREEN), pygame.Rect(10+offset_x, 75+offset_y, fuel, 10))

        
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

        if self.current_xp < self.xp and self.xp_pos > -30:
            self.current_xp = self.current_xp + 0.1

        pygame.draw.rect(self.screen, (GREEN), pygame.Rect(600+offset_x, self.xp_pos+offset_y, self.current_xp * 5 , 30))
        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(600+offset_x, self.xp_pos+offset_y,Settings.next_level * 5, 30), 2)
        xp = font.render("xp: " + str(round(self.current_xp)) + "/" + str(Settings.next_level), 1, (WHITE))
        self.screen.blit(xp, (795+offset_x, self.xp_pos+ 2+offset_y))


        progress = (Settings.obx1+ (Settings.window_width//2))*0.4
        if progress > 320:
            progress = 320
        if progress == 320:
            pygame.draw.rect(self.screen, (RED), pygame.Rect(0+offset_x, 0+offset_y, 1600, 720),4)
            

        pygame.draw.rect(self.screen, (ORANGE), pygame.Rect(10 + offset_x,100 + offset_y,progress, 30)) 
        pygame.draw.rect(self.screen, (RED), pygame.Rect(10 + offset_x, 100 + offset_y, 3200*0.1, 30), 4)
        


        if self.player.energypoints == 0:
            if self.length > 0:
                self.length = self.length - 0.175
            pygame.draw.rect(self.screen, (RED), pygame.Rect(posy, posx - 20, self.length, 11),)
            pygame.draw.rect(self.screen, (150, 0, 0), pygame.Rect(posy, posx - 20, self.length, 11), 2)
        if self.player.energypoints == 75:
            self.length = 75

        pygame.draw.rect(self.screen, (BLUE), pygame.Rect(posy, posx - 20, self.player.energypoints , 11))
        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(posy, posx - 20, self.player.energypoints, 11), 2)


        if self.upgrade_allowed == True:
            self.screen.blit(self.upgrade1, (875, 60))
            self.screen.blit(self.upgrade2, (875, 100))
            self.screen.blit(self.upgrade3, (875, 140))


    def change_screen(self):
        time = 0
        if self.d_imageindex == 2:
            time = 1000
        else:
            time = 300

        if pygame.time.get_ticks() > self.clock_time:
            self.clock_time = pygame.time.get_ticks() + 1000#time
            self.d_imageindex += 1
            if self.d_imageindex >= len(self.d_images):
                self.d_imageindex = 0
            self.deathimg = self.d_images[self.d_imageindex]


    def draw_game_over(self, screen):
        font_death = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)
        scoreprint = font.render("Score: " + str(round(score_value)) + "m", 1, (WHITE))
        levelprint = font.render("Level: " + str(self.level), 1, (WHITE))
        self.d_images.clear()
        for i in range(2):
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"deathscreen{i}.png")) 
            self.d_images.append(bitmap)

        screen.blit(self.deathimg, (0, 0))


        Deathscreen = font_death.render("You died", 1, (RED))
        PressR = font.render("Press R to retry your luck", 1, (WHITE))
        self.screen.blit(scoreprint, (700, 499))
        self.screen.blit(levelprint, (700, 600))
        self.screen.blit(Deathscreen, (485, Settings.window_height // 2 - 100))
        self.screen.blit(PressR, (700, Settings.window_height // 2))
        pygame.display.flip()

        




    def upgrade_menu(self):
        self.colors = [CYAN, MAGENTA]                 #switches between colors
        if pygame.time.get_ticks() > self.clock_time: #
            self.clock_time = pygame.time.get_ticks() #
            self.colorindex1 += 1                      #
        if self.colorindex1 >= len(self.colors):       #
            self.colorindex1 = 0                       #
        self.color = self.colors[self.colorindex1]     #

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
            
                Sounds.play_sound("blaster")
            elif bullets <= 0 and self.player.weapons_index == 0:
                Sounds.play_sound("empty")
            
            if self.player.rockets >= 1 and self.player.weapons_index == 1:
                self.player.rockets = self.player.rockets - 1
                self.rockets.add(Rocket("rocket0.png",self.mx ,self.my))
                print(self.mx, self.my)
                Sounds.play_sound("rocket")
            elif self.player.rockets <= 0 and self.player.weapons_index == 1:
                Sounds.play_sound("empty")
    

    def shoot_dice(self):
        for s in self.stormtroopers:
            shoot_dice = randint(1, 100)
            if shoot_dice == s.trigger and s.getting_hit == False:
                Settings.bullet_size = (100, 15)
                self.tkprojectiles.add(tkprojectile("tkbullet0.png", s.facing,s.tkposy + 80,s.tkposx -50))
                Sounds.play_sound("tk_blast")

                
    def leftclick(self):
        global fuel
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
            if keys [self.walkL_key]:#[pygame.K_a]: 
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
                for o in self.orbital_bombardment:
                    o.playermove_L(self.player.speed,self.player.sprinting)
                self.background0.scroll_l(5 * self.player_speed)
                self.background1.scroll_l(4 * self.player_speed)
                self.background2.scroll_l(3 * self.player_speed)
                self.background3.scroll_l(2 * self.player_speed)
                self.background4.scroll_l(1 * self.player_speed)

            if keys [self.walkR_key]:
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
                for o in self.orbital_bombardment:
                    o.playermove_R(self.player.speed,self.player.sprinting)
                self.background0.scroll_r(5 * self.player_speed)
                self.background1.scroll_r(4 * self.player_speed)
                self.background2.scroll_r(3 * self.player_speed)
                self.background3.scroll_r(2 * self.player_speed)
                self.background4.scroll_r(1 * self.player_speed)
    
            if keys[self.sprint_key]:
                self.player.sprinting = True
                self.player.sprint()
            else:
                self.player.walk()
            if keys[self.jetpack_key]:
                self.player.moveUp()

            
     
                
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
        for o in self.orbital_bombardment:
            o.kill()
        
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
        Settings.obx1 = -1000
        Settings.obx2 = -1500
        Settings.current_platforms = 0
        self.sector_up()
        self.game_over = False
        self.game_started = True
        Sounds.play_music("Soundtrack.mp3")

    def check_figure_collision(self, platform, figure):
        if figure.rect.bottom >= platform.rect.top and figure.rect.bottom <= platform.rect.bottom:
            if figure.rect.right  >= platform.rect.left and figure.rect.left <= platform.rect.right:
                    figure.platform_y = platform.rect.top - 150
                    figure.rect.bottom = platform.rect.top
                    if figure == self.player:
                        self.allowed_to_jump = True
            elif figure == self.player:
                    self.allowed_to_jump = False

        # if figure.rect.top  <= platform.rect.bottom and figure.rect.top >= platform.rect.top:
        #     if figure.rect.right  >= platform.rect.left and figure.rect.left <= platform.rect.right:
        #         figure.rect.top = platform.rect.bottom
        


    def collide(self):
        for pt in self.platforms:
            self.check_figure_collision(pt, self.player)

            for s in self.stormtroopers:
                self.check_figure_collision(pt, s)
            


            for z in self.stormbies:
                self.check_figure_collision(pt, z)

            for a in self.ammocrates:
                if self.check_figure_collision(pt, a):
                    a.on_ground = True

            for h in self.healthpacks:
                if self.check_figure_collision(pt, h):
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
            self.player.rect.top += 10

            
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

            for o in self.orbital_bombardment:
                if pygame.sprite.collide_rect(o, s):
                    s.kill()
                    o.kill()


            for r in self.rockets:
                if pygame.sprite.collide_rect(r, s):
                    s.health = s.health - 100 * Settings.player_damage
                    r.explode()

            if s.rect.top >= 570:
                s.kill()
   
            if pygame.sprite.spritecollide(s, self.flames, False):
                s.health = s.health - 3 * Settings.player_damage
                s.getting_hit = True
            else:
                s.getting_hit = False

        if self.player.rect.top >= 720:
            self.player.kill()
            self.player.health = self.player.health - 3

        for pt in self.platforms:
            for r in self.rockets:
                if pygame.sprite.collide_rect(r, pt):
                    r.explode()
            
            for o in self.orbital_bombardment:
                if pygame.sprite.collide_rect(o, pt):
                    o.explode()
                    pt.durability = pt.durability - 1
                

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
                    
                    Sounds.play_sound("player_hit")
                    if self.player.health <= 0:
                        self.player.kill()
                if self.player.shield == True:
                        Sounds.play_sound("shield_hit")

        if pygame.sprite.spritecollide(self.player, self.orbital_bombardment, True):
            self.player.health = self.player.health - 1

  
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
                    Sounds.play_sound("player_hit")

        for h in self.healthpacks:
            for o in self.orbital_bombardment:
                if pygame.sprite.collide_rect(o, h):
                        h.kill()
                        o.kill()

        for a in self.ammocrates:
            for o in self.orbital_bombardment:
                if pygame.sprite.collide_rect(o, a):
                        a.kill()
                        o.kill()
    


    def reward(self):
        dice6 = randint(1, 2)
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
  
        self.fontcolor = [WHITE, BLUE]
        self.screen.blit(Title, (Settings.window_width // 2 - 150, Settings.window_height // 2 - 100))

        self.background0.scroll_r(5)
        self.background1.scroll_r(4)
        self.background2.scroll_r(3)
        self.background3.scroll_r(2)
        self.background4.scroll_r(1)
        mouse = pygame.mouse.get_pos()



        if Settings.window_width // 2 - 100 <= mouse[0] <= Settings.window_width // 2 + 100 and Settings.window_height // 2 <= mouse[1] <= Settings.window_height // 2 + 100:
            if self.fontmultiplier1 == 0:
                self.multiply_font1 = True
                self.colorindex1 = self.colorindex1 + 1

            if self.fontmultiplier1 == 20:
                self.multiply_font1 = False

            if self.multiply_font1 == True:
                self.fontmultiplier1 = self.fontmultiplier1 + 1

            if self.multiply_font1 == False:
                self.fontmultiplier1 = self.fontmultiplier1 - 1

            if self.colorindex1 >= len(self.fontcolor):
                self.colorindex1 = 0

        else:
            self.multiply_font1 = False
            self.fontmultiplier1 = 1

            self.colorindex1 = 0



        if Settings.window_width // 2 - 100 <= mouse[0] <= Settings.window_width // 2 + 100 and Settings.window_height // 2 +100 <= mouse[1] <= Settings.window_height // 2 + 200:
            if self.fontmultiplier2 == 0:
                self.multiply_font2 = True
                self.colorindex2 = self.colorindex2 + 1

            if self.fontmultiplier2 == 20:
                self.multiply_font2 = False

            if self.multiply_font2 == True:
                self.fontmultiplier2 = self.fontmultiplier2 + 1

            if self.multiply_font2 == False:
                self.fontmultiplier2 = self.fontmultiplier2 - 1

            if self.colorindex2 >= len(self.fontcolor):
                self.colorindex2 = 0

        else:
            self.multiply_font2 = False
            self.fontmultiplier2 = 1

            self.colorindex2 = 0



        if Settings.window_width // 2 - 100 <= mouse[0] <= Settings.window_width // 2 + 100 and Settings.window_height // 2 + 200 <= mouse[1] <= Settings.window_height // 2 + 400:
            if self.fontmultiplier3 == 0:
                self.multiply_font3 = True
                self.colorindex3 = self.colorindex3 + 1

            if self.fontmultiplier3 == 20:
                self.multiply_font3 = False

            if self.multiply_font3 == True:
                self.fontmultiplier3 = self.fontmultiplier3 + 1

            if self.multiply_font3 == False:
                self.fontmultiplier3 = self.fontmultiplier3 - 1

            if self.colorindex3 >= len(self.fontcolor):
                self.colorindex3 = 0

        else:
            self.multiply_font3 = False
            self.fontmultiplier3 = 1

            self.colorindex3 = 0

        self.Button1Font = pygame.font.Font(None, 39 + self.fontmultiplier1)
        Start = self.Button1Font.render("Start Adventure", 1, (self.fontcolor[self.colorindex1]))
        self.screen.blit(Start, ((Settings.window_width // 2 -110) - self.fontmultiplier1*2,Settings.window_height // 2 + 30))

        self.Button2Font = pygame.font.Font(None, 39 + self.fontmultiplier2)
        Endless = self.Button2Font.render("Endless Mode", 1, (self.fontcolor[self.colorindex2]))
        self.screen.blit(Endless, ((Settings.window_width // 2 -100) - self.fontmultiplier2*2,Settings.window_height // 2 + 130))

        self.Button3Font = pygame.font.Font(None, 39 + self.fontmultiplier3)
        Keybindings = self.Button3Font.render("Settings", 1, (self.fontcolor[self.colorindex3]))
        self.screen.blit(Keybindings, ((Settings.window_width // 2 -70) - self.fontmultiplier3*1.5,Settings.window_height // 2 + 230))

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
                    self.images.clear()
                    for i in range(2):
                        bitmap = pygame.image.load(os.path.join(
                            Settings.path_image, f"crosshair{i}.png"))
                        self.images.append(bitmap)
                    print("Starting...")
                    self.endless_mode = False
                    Sounds.play_music("Soundtrack.mp3")
                if Settings.window_width // 2 - 100 <= mouse[0] <= Settings.window_width // 2 + 100 and Settings.window_height // 2 +100 <= mouse[1] <= Settings.window_height // 2 + 200:
                    print("Endless mode")
                    self.images.clear()
                    for i in range(2):
                        bitmap = pygame.image.load(os.path.join(
                            Settings.path_image, f"crosshair{i}.png"))
                        self.images.append(bitmap)
                    self.endless_mode = True
                    self.game_started = True
                if Settings.window_width // 2 - 100 <= mouse[0] <= Settings.window_width // 2 + 100 and Settings.window_height // 2 + 200 <= mouse[1] <= Settings.window_height // 2 + 400:
                    print("Settings")
                    self.settings_window = True




    def cutscene(self):
        self.dimmed_background.draw(self.screen)
        self.player.draw(self.screen)
        Player.animate(self.player)
        self.platforms.draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    self.cutscene_on = False
                    self.game_started = True
            elif event.type == pygame.QUIT:         
                self.running = False
        if score_value < 1:
            self.sc1.animate()
            self.sc1.draw(self.screen)
            self.cutscene_played = 1
            if self.sc1.end_cutscene == True:
                self.cutscene_on = False
                self.game_started = True
        pygame.display.flip()

    # Settings Buttons
    def draw_buttons_settings(self, x, y, text, color, key):
        pygame.draw.rect(self.screen, color, (x, y, 100, 30))
        self.ButtonFont = pygame.font.Font(None, 30)
        Button = self.ButtonFont.render(text, 1, (BLACK))
        Control_key = self.ButtonFont.render(key, 1, (BLACK))
        self.screen.blit(Control_key, (x + 200,y))
        self.screen.blit(Button, (x,y))
    



    def preview_settings(self, screen):

        self.ButtonFont = pygame.font.Font(None, 69)
        keybindings_title = self.ButtonFont.render("Keybindings", 1, (WHITE))
        
        if self.changing_key == "walk_right":
            self.images.clear()
            for i in range(7):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"player_walking_R{i}.png"))
                scaled = pygame.transform.scale(bitmap, (Settings.player_size[0]*2, Settings.player_size[1]*2))
                self.images.append(scaled)

        if self.changing_key == "walk_left":
            self.images.clear()
            for i in range(7):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"player_walking_L{i}.png"))
                scaled = pygame.transform.scale(bitmap, (Settings.player_size[0]*2, Settings.player_size[1]*2))
                self.images.append(scaled)

        if self.changing_key == "jump":
            self.images.clear()
            bitmap = pygame.image.load(os.path.join(
                Settings.path_image, f"jumpR.png"))
            scaled = pygame.transform.scale(bitmap, (Settings.player_size[0]*2, Settings.player_size[1]*2))
            self.images.append(scaled)
        
        if self.changing_key == "jetpack":
            self.images.clear()
            for i in range (2):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"jetpack_R{i}.png"))
                scaled = pygame.transform.scale(bitmap, (Settings.player_size[0]*2, Settings.player_size[1]*2))
                self.images.append(scaled)

        if self.changing_key == "sprint":
            self.images.clear()
            for i in range (7):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"player_sprinting_R{i}.png"))
                scaled = pygame.transform.scale(bitmap, (Settings.player_size[0]*2, Settings.player_size[1]*2))
                self.images.append(scaled)
            self.animation_time = 50
        else:
            self.animation_time = 100
        self.animate()
        
        screen.blit(keybindings_title, (Settings.window_width // 2 - 100, 100))
        screen.blit(self.image, (1000, 200))

    def button_logic(self):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 400 <= mouse[0] <= 400 + 100 and 200 <= mouse[1] <= 200 + 30:
                    self.changing_keybindings = True
                    self.changing_key = "walk_right"
                if 400 <= mouse[0] <= 400 + 100 and 250 <= mouse[1] <= 250 + 30:
                    self.changing_keybindings = True
                    self.changing_key = "walk_left"
                if 400 <= mouse[0] <= 400 + 100 and 300 <= mouse[1] <= 300 + 30:
                    self.changing_keybindings = True
                    self.changing_key = "jump"
                if 400 <= mouse[0] <= 400 + 100 and 350 <= mouse[1] <= 350 + 30:
                    self.changing_keybindings = True
                    self.changing_key = "sprint"
                if 400 <= mouse[0] <= 400 + 100 and 400 <= mouse[1] <= 400 + 30:
                    self.changing_keybindings = True
                    self.changing_key = "jetpack"
                if 400 <= mouse[0] <= 400 + 100 and 450 <= mouse[1] <= 450 + 30:
                    self.changing_keybindings = True
                    self.changing_key = "pause"
                if 400 <= mouse[0] <= 400 + 100 and 500 <= mouse[1] <= 500 + 30:
                    self.changing_keybindings = True
                    self.changing_key = "shoot"

                
            if self.changing_keybindings == True:
                if event.type == pygame.KEYDOWN and not event.key == pygame.K_ESCAPE:
                    if self.changing_key == "walk_right":
                        self.walkR_key = pygame.key.key_code(pygame.key.name(event.key))
                        print(self.walkR_key)
                        self.changing_keybindings = False
                    if self.changing_key == "walk_left":
                        self.walkL_key = pygame.key.key_code(pygame.key.name(event.key))
                        print(self.walkL_key)
                        self.changing_keybindings = False
                    if self.changing_key == "jump":
                        self.jump_key = pygame.key.key_code(pygame.key.name(event.key))
                        print(self.jump_key)
                        self.changing_keybindings = False
                    if self.changing_key == "shoot":
                        self.shoot_key = pygame.key.key_code(pygame.key.name(event.key))
                        print(self.shoot_key)
                        self.changing_keybindings = False
                    if self.changing_key == "pause":
                        self.pause_key = pygame.key.key_code(pygame.key.name(event.key))
                        print(self.pause_key)
                        self.changing_keybindings = False
                    if self.changing_key == "jetpack":
                        self.jetpack_key = pygame.key.key_code(pygame.key.name(event.key))
                        print(self.jetpack_key)
                        self.changing_keybindings = False
                    if self.changing_key == "sprint":
                        self.sprint_key = pygame.key.key_code(pygame.key.name(event.key))
                        print(self.sprint_key)
                        self.changing_keybindings = False
                    


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    self.settings_window = False
                    


    def check_buttons(self):
        self.button_logic()
        self.draw_buttons_settings(400, 200, "walk right", CYAN, pygame.key.name(self.walkR_key))
        self.draw_buttons_settings(400, 250, "walk left", RED, pygame.key.name(self.walkL_key))
        self.draw_buttons_settings(400, 300, "jump", GREEN, pygame.key.name(self.jump_key))
        self.draw_buttons_settings(400, 350, "sprint", MAGENTA, pygame.key.name(self.sprint_key))
        self.draw_buttons_settings(400, 500, "shoot", BLUE, pygame.key.name(self.shoot_key))
        self.draw_buttons_settings(400, 400, "jetpack", PURP, pygame.key.name(self.jetpack_key))
        self.draw_buttons_settings(400, 450, "pause", YELLOW, pygame.key.name(self.pause_key))
        
        pygame.display.flip()


        
    def run(self):
        while self.running:
            self.clock.tick(60)

            if self.game_over == True:
                self.draw_game_over(self.screen)
                self.watch_for_events()
                self.change_screen()

            if self.game_started == True and self.cutscene_on == False:
                self.watch_for_events()
                self.update()
                self.draw()
                self.get_cursor_center()
                pygame.mouse.set_visible(False)

                
            elif self.game_started == False and self.cutscene_on == False and self.settings_window == False and self.game_over == False:
                pygame.mouse.set_visible(True)
                self.draw_start()
                self.event_start()
                
            elif self.cutscene_on == True:
                self.cutscene()
                pygame.mouse.set_visible(True)

            elif self.settings_window == True:
                self.screen.fill(BLUE)
                pygame.mouse.set_visible(True)
                self.preview_settings(self.screen)
                self.check_buttons()
        pygame.quit()       

    def watch_for_events(self):
        global jumping
    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mx, self.my = pygame.mouse.get_pos()
                self.midclick()
            if event.type == pygame.KEYDOWN:
                if event.key == self.pause_key: 
                    self.game_started = False
                if event.key == self.jump_key and self.allowed_to_jump == True:
                    jumping = True
                    for s in self.stormtroopers:
                        s.jumping = True
                if event.key == pygame.K_q:
                    self.player.change_previous_weapon()
                if event.key == pygame.K_e:
                    self.player.change_next_weapon()
                if event.key == pygame.K_r:
                    self.restart()

            elif event.type == pygame.QUIT:         
                self.running = False
        
    def get_cursor_center(self):
        global facing
        self.cursor_rect.center = pygame.mouse.get_pos()
        if self.cursor_rect.center[0] < self.player.rect.center[0]:
            facing = "L"
        elif self.cursor_rect.center[0] > self.player.rect.center[0]:
            facing = "R"

    def check_death(self):
        if self.player.health == 0:
            Sounds.play_music("death.mp3")
        if self.player.health <= 0:
            self.game_over = True
            self.game_started = False

        
        

    def update(self):
        self.check_death()
        self.start_ob()
        self.upgrade_menu()
        self.platforms.update()
        self.stormtroopers.update()
        self.stormbies.update()
        self.projectiles.update()
        self.tkprojectiles.update()
        Game.controls(self)
        Player.refill(self.player)
        Game.hit(self)
        Player.animate(self.player)
        self.flames.update()
        for o in self.orbital_bombardment:
            o.move()
            o.animate()
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
        self.orbital_bombardment.draw(self.screen)
        self.stormtroopers.draw(self.screen) #self.offsetx)
        self.stormbies.draw(self.screen)
        self.player.draw(self.screen)
        self.tkprojectiles.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.ammocrates.draw(self.screen)
        self.healthpacks.draw(self.screen)
        self.flames.draw(self.screen)
        self.rockets.draw(self.screen)
        self.font()
        self.screen.blit(self.image,self.cursor_rect) # draw the cursor
        pygame.display.flip()

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "50, 50"

    game = Game()
    game.run()


#credit to 15.ai for TTS