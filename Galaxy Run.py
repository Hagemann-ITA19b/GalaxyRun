import pygame
import os
from random import randint
from pygame import mixer
import time

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
flamethrower_is_active = False
BLACK = (0, 0, 0) 
GRAY = (127, 127, 127) 
WHITE = (255, 255, 255)
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 
CYAN = (0, 255, 255) 
MAGENTA = (255, 0, 255)

class Settings(object):
    window_height = 720
    window_width = 1600
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "files")
    player_size = (70,150) #70, 150
    bullet_size = (100, 50)
    melee_size = (70, 70)
    stormtrooper_size = (70,150)
    title = "Galaxy Run"


# Musik

mixer.init()
pygame. mixer.init()
blaster_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "blaster.wav"))
refill_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "refill.mp3"))
jetpack_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "jetpack.wav"))
darksaber_sound = pygame. mixer. Sound(os.path.join(Settings.path_image, "darksaber.wav"))

  
mixer.music.load(os.path.join(Settings.path_image, "Soundtrack.mp3"))
  
#mixer.set_volume(0.1) #Immer noch extremst laut !!!
pygame.mixer.music.set_volume(0.4)
mixer.music.play()





class Background():
    def __init__(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.rectimg = self.image.get_rect()

        self.bgx = 0
         
    def scroll_r(self):
        self.bgx = self.bgx - 5
        if self.bgx <= -Settings.window_width:
            self.bgx = 0

    def scroll_l(self):
        self.bgx = self.bgx + 5
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
                print("!!1")


class Stormtrooper(pygame.sprite.Sprite):
    def __init__(self, filename, health, tkposx, tkposy, trigger):
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
        
    def update(self):
        if self.rect.left <= posy:
            self.facing = "R"
        if self.rect.left >= posy:
            self.facing = "L"


        if self.facing == "L":
            self.images.clear()
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"stormtrooperR{i}.png"))
                self.images.append(bitmap)
        elif self.facing == "R":
            self.images.clear()
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"stormtrooperL{i}.png"))
                self.images.append(bitmap)


        self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        

class Player(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.player_size)
        self.rect = self.image.get_rect()
        Player.pos(self)
        self.health = 33
        self.shield = False
        self.sprinting = False
        self.flames_on = False
        self.shieldpoints = 75
        self.passed_time = 0
        self.passed_fueltime = 0
        self.endurance = 100
        self.score_muliplier = 0.1
        self.playing_shieldrefill = False
        self.playing_shieldlow = False
        self.invincible = False
        self.passed_invtime = 0
        self.run_inv = False
        self.run_fuel = False
        self.images = []
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


        self.speed = 5
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.clock_time = pygame.time.get_ticks()
        self.animation_time = 100


        self.platform_y = 570
        self.velocity_index = 0
        self.velocity = ([-10,-9.5,-9,-8.5,-8,-7.5, -7, -6.5, -6, -5.5, -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])

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
        print(self.speed)

    def pos(self):                              #Gibt die Startposition an 
        self.rect.left = 50
        self.rect.top = 570
    
    def get_pos(self):
        global posx, posy
        posy = self.rect.left
        posx = self.rect.top

    def moveL(self):
        global facing, score_value
        Player.get_pos(self)
        if self.rect.left > -75:                     #Macht die Border unpassierbar
            self.rect.left = self.rect.left - self.speed
            if lives > 0:
                score_value -= self.score_muliplier#0.1    #Spieler wird nach links verschoben
            facing = "L"
            if self.shield == False and self.flames_on == False and self.sprinting == False:
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
        global facing, score_value
        Player.get_pos(self)
        if self.rect.left < Settings.window_width - 50:    #Macht die Border unpassierbar
            self.rect.left = self.rect.left + self.speed
            if self.health > 0:
                score_value += self.score_muliplier#0.1
                #Spieler wird nach rechts verschoben
            facing = "R"
            if self.shield == False and self.flames_on == False and self.sprinting == False:
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
            print(self.speed)

        

    def moveUp(self):
        global fuel
        Player.get_pos(self)
        if fuel > 0:
            pygame.mixer.unpause()
            jetpack_sound.play()
            if self.rect.top <= 570: 
                if self.rect.top >= 1:
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
                    
                    fuel -= 1

                    if fuel <= 0:
                        pygame.mixer.pause()

                       
    def gravity(self):
        if jumping == False:
            Player.get_pos(self)
            self.rect.top += 10

            if self.rect.top >= 570:
                self.rect.top = 570
            


    def block(self):
        if self.shieldpoints > 0:
            self.shieldpoints = self.shieldpoints - 0.25
            self.shield = True
            print("Shield is active")
            print(self.shieldpoints)
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
        
        if self.shieldpoints <= 0:
            if self.playing_shieldlow == False:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'shields_low.mp3')))
                self.playing_shieldlow = True
            Game.timer(self)
        if self.passed_time >= 420:
            print(self.passed_time)
            if self.playing_shieldrefill == False:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'refill.mp3')))
                self.playing_shieldrefill = True
            self.shieldpoints = self.shieldpoints + 0.5 #0.25
            if self.shieldpoints >= 75:
                self.passed_time = 0
                self.playing_shieldrefill = False
                self.playing_shieldlow = False

        if self.rect.top == 570 and fuel < 200:
            self.run_fuel = True
            print(self.passed_fueltime)
            if fuel < 200:
                Game.fueltimer(self)
                if self.passed_fueltime >= 300:
                    fuel += 0.4
                    if fuel >= 200:
                        self.passed_fueltime = 0
                        self.run_fuel = False
                    
                    if self.endurance < 100:
                        self.endurance += 0.1
                        #print(self.endurance)

                 
  

    def flamethrower(self):
            if self.rect.top == 570:
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
                    
                self.rect = self.image.get_rect()
                self.rect.left = posy
                self.rect.top = posx
                self.flames_on = True
                # flamethrower_is_active = True
                
           
        
    def jump(self):
        global jumping, endurance
        if jumping == True:
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1
            if self.rect.top >= self.platform_y:
                self.rect.top = self.platform_y
                self.velocity_index = 0
                if self.rect.top == 570:
                    jumping = False
        Player.get_pos(self)


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
        if self.rect.top < 670 and self.on_ground == False:
            self.rect.top += self.speed_v
            if self.rect.top == 670:
                self.on_ground = True

        if self.on_ground == True:
            self.rect.top += self.velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(self.velocity) -1:
                self.velocity_index = len(self.velocity) - 1
            if self.rect.top >= self.platform_y:
                self.rect.top = self.platform_y
                self.velocity_index = 0

            

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
    def __init__(self, filename, facing):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.bullet_size)
        self.rect = self.image.get_rect()
        self.rect.left = posy + 70
        self.rect.top = posx + 50
        self.speed_h = 10
        self.speed_v = 0
        self.facing = facing
        self.faced = False

        self.images = []
        if facing == "R":
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"bullet{i}.png"))
                self.images.append(bitmap)
        if facing == "L":
            for i in range(3):
                bitmap = pygame.image.load(os.path.join(
                    Settings.path_image, f"bulletL{i}.png"))
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
        if self.facing == "R":
            self.rect.move_ip(self.speed_h, self.speed_v)
        if self.facing == "L":
                projectile.change_direction_L(self)
                self.rect.move_ip(-self.speed_h, self.speed_v)
        
    def change_direction_L(self):
        if facing == "L" and self.faced == False:
            self.rect.left = posy - 75
            self.faced = True

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



                
class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("background.png")
        self.stormtroopers = pygame.sprite.Group()
        self.player = Player("player_standing_R0.png")
        self.tkprojectiles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.ammocrates = pygame.sprite.Group()
        self.healthpacks= pygame.sprite.Group()
        self.stormbies = pygame.sprite.Group()
        self.flames = pygame.sprite.Group()
        self.sector = 0
        self.running = True
        self.length = 75

    def sector_up(self):
        global score_value
        if self.player.rect.x >= 1550:
            self.sector = self.sector + 1
            self.player.rect.x = -10
            self.player.rect.y = self.player.rect.y
            
            for s in self.stormtroopers:
                s.kill()
            for a in self.ammocrates:
                a.kill()
            for h in self.healthpacks:
                h.kill()
            for b in self.stormbies:
                b.kill()
            for p in self.projectiles:
                p.kill()
            for t in self.tkprojectiles:
                t.kill()
            
            self.spawn()
        elif self.player.rect.x == -75:
            self.sector = self.sector - 1
            self.player.rect.x = 1550
            self.player.rect.y = 570
           
            self.spawn()

    def spawn(self):
        
        if self.sector == 1:
            self.stormtroopers.add(Stormtrooper("stormtrooperL0.PNG",100,1000,570, randint(0, 100)))
           
            self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,1300,570, randint(0, 100)))
            
            self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,1500,570, randint(0, 100)))
            
        elif self.sector == 2:
            self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,1500,570, randint(0, 100)))
            self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,1500,570, randint(0, 100)))

        elif self.sector <= 4:
            for i in range(randint(1, self.sector)):
                self.stormtroopers.add(Stormtrooper("stormtrooperL0.png",100,1500,570, randint(0, 100)))
        
        elif self.sector >= 5:
            for i in range(randint(1, 10)):
                self.stormbies.add(Stormbie("stormtrooperL0.png",100,randint(500, 1500),570))
           
        
            
            

    def font(self):
        global bullets
        font = pygame.font.Font(None, 36)
        font_death = pygame.font.Font(None, 72)


        bullet_pos = 230
        for b in range(bullets):
            bullet_pos = bullet_pos + 20
            pygame.draw.rect(self.screen, (YELLOW), pygame.Rect(bullet_pos, 10, 10, 20))
            pygame.draw.rect(self.screen, (RED), pygame.Rect(bullet_pos, 10, 10, 15))
            pygame.draw.rect(self.screen, (BLACK), pygame.Rect(bullet_pos, 10, 10, 20), 2)

        Ammo = font.render("Ammo: " + str(round(bullets)) + " bullets", 1, (YELLOW))
        Fuelprint = font.render("Fuel: " + str(round(fuel)) + " liters", 1, (GREEN))
        scoreprint = font.render("Score: " + str(round(score_value)) + "m", 1, (WHITE))
        levelprint = font.render("Level: " + str(level), 1, (WHITE))
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


        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(10,75, 200, 11), 2)
        pygame.draw.rect(self.screen, (GREEN), pygame.Rect(10, 75, fuel, 10))
        pygame.draw.rect(self.screen, (BLUE), pygame.Rect(10, 200, self.player.endurance, 10))
 


        if self.player.shieldpoints == 0:
            if self.length > 0:
                self.length = self.length - 0.175
            
            pygame.draw.rect(self.screen, (RED), pygame.Rect(posy, posx - 20, self.length, 11),)
            pygame.draw.rect(self.screen, (150, 0, 0), pygame.Rect(posy, posx - 20, self.length, 11), 2)
        if self.player.shieldpoints == 75:
            self.length = 75
      


        pygame.draw.rect(self.screen, (BLUE), pygame.Rect(posy, posx - 20, self.player.shieldpoints , 11))
        pygame.draw.rect(self.screen, (BLACK), pygame.Rect(posy, posx - 20, self.player.shieldpoints, 11), 2)

        
        if self.player.health <= 0:
            pygame.draw.rect(self.screen, (BLACK), pygame.Rect(0,0, 1600, 720))
            Deathscreen = font_death.render("You died", 1, (RED))
            PressR = font.render("Press R retard", 1, (WHITE))
            self.screen.blit(scoreprint, (700, 499))
            self.screen.blit(levelprint, (700, 600))
            self.screen.blit(Deathscreen, (485, Settings.window_height // 2 - 100))
            self.screen.blit(PressR, (700, Settings.window_height // 2 + 30))



    def get_pos(self):
        for s in self.stormtroopers:
            s.tkposx = s.rect.left
            s.tkposy = s.rect.top
        
        for z in self.stormbies:
            z.zposx = z.rect.left
            z.zposy = z.rect.top

    def shoot(self):
            global bullets
            Settings.bullet_size = (100, 15)
            if bullets >= 0.5:
                bullets -= 1
                self.projectiles.add(projectile("bullet0.png", facing))
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'blaster.wav')))
            else:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'empty.wav')))
    


    def shoot_dice(self):
        for s in self.stormtroopers:
            shoot_dice = randint(1, 100)
            if shoot_dice == s.trigger:
                Settings.bullet_size = (100, 15)
                self.tkprojectiles.add(tkprojectile("tkbullet0.png", s.facing,s.tkposy + 80,s.tkposx -50))
                pygame.mixer.Channel(4).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'tkblast.mp3')))

                

    def leftclick(self):
        global flamethrower_is_active, shield_active, fuel
        leftclick = pygame.mouse.get_pressed() == (1, 0, 0)
        rightclick = pygame.mouse.get_pressed() == (0, 0, 1)
        
        if leftclick == True:
            if fuel >= 5:
                    fuel = fuel - 5
                    Player.flamethrower(self.player)
                    if self.flames_on == False:
                        self.flames.add(Flame("bullet0.png"))
                        self.flames_on = True

        else:
            self.flames_on = False
            self.player.flames_on = False
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
        rightclick = pygame.mouse.get_pressed() == (0, 0, 1)
        if midclick == True:
            self.shoot()
  
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
            
            
                
        

    def controls(self):
            global jumping
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: 
                self.player.moveL()
                self.background.scroll_l()
            if keys[pygame.K_d]:
                self.player.moveR()
                self.background.scroll_r()
            if keys[pygame.K_SPACE]:
                jumping = True
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
        level = 1
        score_value = 0
        self.player.shieldpoints = 75
        self.player.endurance = 100
        
        bullets = 20
        fuel = 200
        self.player.health = 3
        self.sector = 0
        self.player.rect.x = 50
        self.player.rect.y = 570
        pygame.mixer.music.rewind()
       
    def countdown(time_sec): #FÜR SPÄTER
        while time_sec:
            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            time.sleep(1)
            time_sec -= 1
        print("stop")

 


    def hit(self):
        for s in self.stormtroopers:
            if pygame.sprite.spritecollide(s, self.projectiles, True):
                s.health = s.health - 25
                if s.health ==0:
                    s.kill()
                    self.reward()
    
            if pygame.sprite.spritecollide(s, self.flames, False):
                s.health = s.health - 5
                if s.health ==0:
                    s.kill()
                    self.reward()
        
        for z in self.stormbies:
            if pygame.sprite.spritecollide(z, self.projectiles, True):
                z.health = z.health - 25
                if z.health ==0:
                    z.kill()
                    self.reward()

            if pygame.sprite.spritecollide(z, self.flames, False):
                z.health = z.health - 10
                if z.health ==0:
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
                
        if pygame.sprite.spritecollide(self.player, self.stormbies, False):
                self.player.invincible_off()
                if self.player.invincible == False:
                    self.player.get_invincible()
                    self.player.health = self.player.health - 1
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(os.path.join(Settings.path_image, 'hurt.wav')))

            
    def reward(self):
        dice6 = randint(1, 2)
                   
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
        if self.player.health < 3:
            if pygame.sprite.spritecollide(self.player, self.healthpacks, True):
                self.player.health = self.player.health + 1
       




    def get_statement(self):
        pass


    def run(self):
        while self.running:
            self.clock.tick(60)                         
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()       

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                self.midclick()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    self.running = False
            elif event.type == pygame.QUIT:         
                self.running = False


    def update(self):
        # self.background.update()
        self.stormtroopers.update()
        self.stormbies.update()
        self.projectiles.update()
        self.tkprojectiles.update()
        Game.controls(self)
        Player.gravity(self.player)
        Player.refill(self.player)
        Game.hit(self)
        Player.animate(self.player)
        self.flames.update()
        for tk in self.tkprojectiles:
            tk.animate()
        for p in self.projectiles:
            p.animate()
        for s in self.stormtroopers:
            s.animate()
        for z in self.stormbies:
            z.animate()
        for f in self.flames:
            f.animate()
        
        self.leftclick()
        self.ammocrates.update()
        self.healthpacks.update()
        Game.pickup(self)
        Game.get_pos(self)
        self.player.jump()
        self.sector_up()
        self.shoot_dice()
        
        self.get_statement()
 
        
        
        
        


        

    def draw(self):
        self.background.draw(self.screen)
        self.stormtroopers.draw(self.screen)
        self.stormbies.draw(self.screen)
        self.player.draw(self.screen)
        self.tkprojectiles.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.ammocrates.draw(self.screen)
        self.healthpacks.draw(self.screen)
        self.flames.draw(self.screen)
        
        self.font()
        pygame.display.flip()

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "50, 50"

    game = Game()
    game.run()