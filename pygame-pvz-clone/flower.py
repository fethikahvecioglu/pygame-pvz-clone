import pygame
from pygame import image
from pygame.locals import *
import random


class Flower(): 
    def __init__(self):
        self._hp = None
        self._ReactionRate = None
        self._sprites = []
        # Faded
        self._rect = None
        self._fadedimage = None
        # Sprites
        self._lastsprite = None
        self._key = None
        self._isbullet = True
        self._lane = None
        self._block = None

    def render_flower(self, screen):
        screen.blit(self._image, self._rect)

    def mouse_collusion(self, clickedcoord):
        if self._rect.collidepoint(clickedcoord):
            return True
        else:
            return False

    def setblock(self, block):
        self._block = block

    def return_block(self):
        return self._block

    def return_faded(self):
        return self._fadedimage

    def return_flowerinstance(self):
        return self._image, self._rect

    def return_flowerkey(self):
        return self._key

    def return_flowercdown(self):
        return self._isbullet

    def return_flowercoords(self):
        return self._rect.top, self._rect.left

    def return_lane(self):
        return self._lane

    def return_hp(self):
        return self._hp

    def lower_health(self, dmg):
        self._hp -= dmg

    def sprite_initialization(self):
        pass

    def update_sprite(self, current):
        if self._key == "Sunflower": n = 18
        if self._key == "Ice": n = 15
        if self._key == "Peas": n = 13
        if current - self._lastsprite >= (1000/60)*4:
            self._currentsprite += 1
            self._lastsprite = current
            self._image = self._sprites[self._currentsprite % n]

    def check_bulletcooldown(self, current):
        if self._key == "Sunflower": n = 900
        if self._key == "Ice": n = 150
        if self._key == "Peas": n = 100
        if current - self._lastbullet >= (1000/60) * n:
            self._lastbullet = current
            self._isbullet = True
        else:
            self._isbullet = False


class Bullet:
    def __init__(self, top, left):
        self._Damage = 10
        # Image
        self._left = left
        self._top = top
        self._image = None
        self._rect = None
        self._rect.top, self._rect.left = None, None
        # Var
        self._lastmove = 0

    def move(self, current):
        if current - self._lastmove >= (1000/60)*2:
            self._lastmove = current
            self._rect.left += 5

    def return_dmg(self):
        return self._Damage
        
    def return_bulletinstance(self):
        return self._image, self._rect

    def render_bullet(self, screen):
        screen.blit(self._image, self._rect)


class IceBullet(Bullet):
    def __init__(self, top, left):
        self._Damage = 10
        # Image
        self._left = left
        self._top = top
        self._image = pygame.image.load("./assets/Images/PeaIce_0.png")
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = self._top, self._left
        # Var
        self._lastmove = 0
        self._slowrate = 2

    def return_slowrate(self):
        return self._slowrate
    

class PeasBullet(Bullet):
    def __init__(self, top, left):
        self._Damage = 10
        # Image
        self._left = left
        self._top = top
        self._image = pygame.image.load("./assets/Images/PeaNormal_0.png")
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = self._top, self._left
        # Var
        self._lastmove = 0
        


    

class Ice(Flower):  # Ice will be freeze the zombies for certain amount of time thanks to its special action method.
    def __init__(self, top, left, current, lane):
        self._hp = 100
        self._top = top
        self._left = left
        # Faded image
        self._fadedimage = pygame.image.load("./assets/Images/SnowPea_0.png")
        self._fadedimage.set_alpha(128)
        # Real image
        self._lastsprite = 0
        self._sprites = []
        self.sprite_initialization()
        self._image = self._sprites[self._currentsprite]
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = top, left
        # Var
        self._key = "Ice"
        # Bullet
        self._isbullet = False
        self._lastbullet = current
        self._lane = lane

    def sprite_initialization(self):
        self._currentsprite = 0
        for i in range(15):
            self._sprites.append(pygame.image.load("./assets/Images/SnowPea_Image/SnowPea_" + str(i) + ".png"))
    
    

class Peas(Flower):
    def __init__(self, top, left, current, lane):
        self._hp = 100
        self._top = top
        self._left = left
        # Faded image
        self._fadedimage = pygame.image.load("./assets/Images/Peashooter_0.png")
        self._fadedimage.set_alpha(128)
        # Real image
        self._lastsprite = 0
        self._sprites = []
        self.sprite_initialization()
        self._image = self._sprites[self._currentsprite]
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = top, left
        # Var
        self._key = "Peas"
        self._isbullet = False
        self._lastbullet = current
        self._lane = lane

    def sprite_initialization(self):
        self._currentsprite = 0
        for i in range(13):
            self._sprites.append(pygame.image.load("./assets/Images/Peashooter_Image/Peashooter_" + str(i) + ".png"))

    
class Sunflower(Flower):   #Sunflower will create sun symbols which enable us to collect energy to obtain new flowers. Its action method is generating energy after certain interval.
    def __init__(self, top, left, current, lane):
        self._hp = 100
        self._top = top
        self._left = left
        # Faded image
        self._fadedimage = pygame.image.load("./assets/Images/SunFlower_0.png")
        self._fadedimage.set_alpha(128)
        # Real image
        self._lastsprite = 0
        self._sprites = []
        self.sprite_initialization()
        self._image = self._sprites[self._currentsprite]
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = top, left
        # Var
        self._key = "Sunflower"
        # Var
        self._isbullet = False
        self._lastbullet = current
        self._lane = lane

    def sprite_initialization(self):
        self._currentsprite = 0
        for i in range(18):
            self._sprites.append(pygame.image.load("./assets/Images/SunFlower_Image/SunFlower_" + str(i) + ".png"))


class Sun():
    def __init__(self, randomized, top, left):
        self._temptop = top
        self._templeft = left
        self._randomized = randomized
        self.start()
        # Sprite
        self._lastsprite = 0
        self._sprites = []
        self.sprite_initialization()
        # Image
        self._image = self._sprites[self._currentsprite]
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = self._top, self._left
        # Var
        self._ifstop = False

    def start(self):
        if self._randomized:
            self._top = -85
            self._left = random.randint(200,950)
            self._stoppoint = random.randint(100,500)
        else:
            self._top, self._left = self._temptop, self._templeft

    def sprite_initialization(self):
        self._currentsprite = 0
        for i in range(22):
            self._sprites.append(pygame.image.load("./assets/Images/Sun/Sun_" + str(i) + ".png"))

    def update_sprite(self, current):
        if self._randomized:
            self.motion_check()
            if current - self._lastsprite >= (1000/60)*2:
                self._currentsprite += 1
                self._lastsprite = current
                self._image = self._sprites[self._currentsprite % 22]
                if self._ifstop == False:
                    self._rect.top += 3
        else:
            if current - self._lastsprite >= (1000/60)*2:
                self._currentsprite += 1
                self._lastsprite = current
                self._image = self._sprites[self._currentsprite % 22]

    def motion_check(self):
        if self._rect.top >= self._stoppoint:
            self._ifstop = True

    def render_sun(self, screen):
        screen.blit(self._image, self._rect)

    def return_suninstance(self):
        return self._image, self._rect

    def mouse_collusion(self, clickedcoord):
        if self._rect.collidepoint(clickedcoord):
            return True
        else:
            return False




