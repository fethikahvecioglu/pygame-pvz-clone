import pygame
from pygame import image
from pygame.locals import *
import random


class Zombies():
    def __init__(self, ):
        # Var
        self._hp = None
        # Sprite
        self._activesprite = None
        self._eatingsprites = []
        self._walkingsprites = []
        self._currentsprite = None
        self._lastsprite = None
        self._lastmove = None
        self._image = self._sprites[self._currentsprite]
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = None, None
        self._lane = None
        self._key = None
        self._eat = False
        self._Damage = None
        self._lasteat = None
        self._temp = None
        # Slow
        self._slowed = None
        self._lastslow = None
        self._slowrate = None
        self._slowimage = pygame.image.load("./assets/freeze.png")
        self._slowimage = pygame.transform.scale(self._slowimage, (self._image.get_width(),self._image.get_height()))
        self._slowimage.set_alpha(125)
        
    def start(self):
        self._lane = random.randint(0,4)
        if self._lane == 0:
            self._rect.top = 80
        elif self._lane == 1:
            self._rect.top = 179
        elif self._lane == 2:
            self._rect.top = 279
        elif self._lane == 3:
            self._rect.top = 376
        elif self._lane == 4:
            self._rect.top = 475
        
    def sprite_initialization(self):
        pass

    def update_sprite(self, current):
        if self._currentsprite <= 10:
            if self._key == "Quick_Zombie":
                if self._eat: 
                    self._temp = 21 
                    self._activesprite = self._eatingsprites
                else: 
                    self._temp = 22
                    self._activesprite = self._walkingsprites

            if self._key == "Weak_Zombie":
                if self._eat: 
                    self._temp = 11
                    self._activesprite = self._eatingsprites
                else:
                    self._temp = 21
                    self._activesprite = self._walkingsprites
            
            if self._key == "Strong_Zombie":
                if self._eat:
                    self._temp = 11
                    self._activesprite = self._eatingsprites
                else:
                    self._temp = 15
                    self._activesprite = self._walkingsprites

        if current - self._lastsprite >= (1000/60) * 6 * self._slowrate:
            self._currentsprite += 1
            self._lastsprite = current
            if self._currentsprite - self._temp >= 0:
                self._currentsprite = 0
            self._image = self._activesprite[self._currentsprite]

    def return_zrect(self):
        return self._rect

    def update_hp(self, n):
        self._hp -= n

    def return_hp(self):
        return self._hp
    
    def return_zlane(self):
        return self._lane

    def return_damage(self):
        return self._Damage

    def return_lastslow(self):
        return self._lastslow

    def is_slowed(self):
        return self._slowed

    def check_slow(self, current):
        if self._slowed:
            if current - self._lastslow > (1000/60) * 100:
                self._slowed = False
                self.fast()

    def eat(self, current):
        if current - self._lasteat >= (1000/60) * 60 * self._slowrate:
            self._lasteat = current
            return True
        else:
            return False

    def set_eating(self, bool):
        self._eat = bool

    def slow(self, current, slowrate):
        self._lastslow = current
        self._slowed = True
        self._slowrate = slowrate

    def fast(self):
        self._slowed = False
        self._slowrate = 1
    
    # Render
    def render_zombie(self, screen):
        if self._slowed:
            freezezombie = pygame.Surface((self._image.get_width(),self._image.get_height()))
            freezezombie.blit(self._image, (0,0))
            freezezombie.blit(self._slowimage, (0,0))
            freezecolor = freezezombie.get_at((0,0))
            freezezombie.set_colorkey(freezecolor)
            screen.blit(freezezombie, self._rect)
        else:
            screen.blit(self._image, self._rect)

    def return_zombieinstance(self):
        return self._image, self._rect


class Quick_Zombie(Zombies):
    def __init__(self):
        self._key = "Quick_Zombie"
        self._hp = 100
        self._Damage = 10
        self._left = 1101
        # Var
        self._lastsprite = 0
        self._lastmove = 0
        self._eat = False
        self._lasteat = 0
        self._slowed = False
        self._lastslow = 0
        self._slowrate = 1
        # Sprite
        self._temp = 22
        self._walkingsprites = []
        self._eatingsprites = []
        self.sprite_initialization()
        self._activesprite = self._walkingsprites
        self._image = self._activesprite[self._currentsprite]
        self._slowimage = pygame.image.load("./assets/freeze.png")
        self._slowimage = pygame.transform.scale(self._slowimage, (self._image.get_width(),self._image.get_height()))
        self._slowimage.set_alpha(125)
        # Rect
        self._rect = self._image.get_rect()
        self._rect.left = self._left
        self.start()

    def sprite_initialization(self):
        self._currentsprite = 0
        for i in range(22):
            zomimage = pygame.image.load("./assets/Images/Zombie/ZombieWalk/Zombie_" + str(i) + ".png")
            zomimage = pygame.transform.scale(zomimage, (int(zomimage.get_width())*7/10,int(zomimage.get_height())*7/10))
            self._walkingsprites.append(zomimage)
        for i in range(21):
            zomimage2 = pygame.image.load("./assets/Images/Zombie/ZombieAttack/ZombieAttack_" + str(i) + ".png")
            zomimage2 = pygame.transform.scale(zomimage2, (int(zomimage2.get_width())*7/10,int(zomimage2.get_height())*7/10))
            self._eatingsprites.append(zomimage2)

    
    # Actions
    def move(self, current):
        if current - self._lastmove >= (1000/60) * 3 * self._slowrate:
            self._lastmove = current
            self._rect.left -= 1


class Weak_Zombie(Zombies):
    def __init__(self):
        self._key = "Weak_Zombie"
        self._hp = 100
        self._Damage = 10
        self._left = 1101
        # Var
        self._lastsprite = 0
        self._lastmove = 0
        self._eat = False
        self._lasteat = 0
        self._slowed = False
        self._lastslow = 0
        self._slowrate = 1
        # Sprite
        self._temp = 21
        self._walkingsprites = []
        self._eatingsprites = []
        self.sprite_initialization()
        self._activesprite = self._walkingsprites
        self._image = self._activesprite[self._currentsprite]
        self._slowimage = pygame.image.load("./assets/freeze.png")
        self._slowimage = pygame.transform.scale(self._slowimage, (self._image.get_width(),self._image.get_height()))
        self._slowimage.set_alpha(125)
        # Rect
        self._rect = self._image.get_rect()
        self._rect.left = self._left
        self.start()

    def sprite_initialization(self):
        self._currentsprite = 0
        for i in range(21):
            zomimage = pygame.image.load("./assets/Images/ConeheadZombie/ConeheadZombie/ConeheadZombie_" + str(i) + ".png")
            zomimage = pygame.transform.scale(zomimage, (int(zomimage.get_width())*7/10,int(zomimage.get_height())*7/10))
            self._walkingsprites.append(zomimage)
        for i in range(11):
            zomimage2 = pygame.image.load("./assets/Images/ConeheadZombie/ConeheadZombieAttack/ConeheadZombieAttack_" + str(i) + ".png")
            zomimage2 = pygame.transform.scale(zomimage2, (int(zomimage2.get_width())*7/10,int(zomimage2.get_height())*7/10))
            self._eatingsprites.append(zomimage2)
    
    # Actions
    def move(self, current):
        if current - self._lastmove >= (1000/60) * 6 * self._slowrate:
            self._lastmove = current
            self._rect.left -= 1


class Strong_Zombie(Zombies):
    def __init__(self):
        self._key = "Strong_Zombie"
        self._hp = 150
        self._WaitingTime = 5
        self._Damage = 20
        self._left = 1101
        # Var
        self._lastsprite = 0
        self._lastmove = 0
        self._eat = False
        self._lasteat = 0
        self._slowed = False
        self._lastslow = 0
        self._slowrate = 1
        # Sprite
        self._temp = 15
        self._walkingsprites = []
        self._eatingsprites = []
        self.sprite_initialization()
        self._activesprite = self._walkingsprites
        self._image = self._activesprite[self._currentsprite]
        self._slowimage = pygame.image.load("./assets/freeze.png")
        self._slowimage = pygame.transform.scale(self._slowimage, (self._image.get_width(),self._image.get_height()))
        self._slowimage.set_alpha(125)
        # Rect
        self._rect = self._image.get_rect()
        self._rect.left = self._left
        self.start()

    def sprite_initialization(self):
        self._currentsprite = 0
        for i in range(15):
            zomimage = pygame.image.load("./assets/Images/BucketheadZombie_Image/BucketheadZombie/BucketheadZombie_" + str(i) + ".png")
            zomimage = pygame.transform.scale(zomimage, (int(zomimage.get_width())*7/10,int(zomimage.get_height())*7/10))
            self._walkingsprites.append(zomimage)
        for i in range(11):
            zomimage2 = pygame.image.load("./assets/Images/BucketheadZombie_Image/BucketheadZombieAttack/BucketheadZombieAttack_" + str(i) + ".png")
            zomimage2 = pygame.transform.scale(zomimage2, (int(zomimage2.get_width())*7/10,int(zomimage2.get_height())*7/10))
            self._eatingsprites.append(zomimage2)
    
    # Actions
    def move(self, current):
        if current - self._lastmove >= (1000/60)* 6 * self._slowrate:
            self._lastmove = current
            self._rect.left -= 1
