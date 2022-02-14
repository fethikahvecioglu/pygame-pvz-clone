import sys, pygame
from pygame import image
from pygame.locals import *
import random

import zombie as zombie
import flower as flower

pygame.init()
random.seed()


class Game: 
    def __init__(self):
        self._menubar = MenuBar()
        # Lists of every type of object that actively interacts with the game
        self._flowers = []
        self._zombies = []
        self._slots = []
        self._bullets = []
        self._availableBlocks = []
        self._usedBlocks = []
        self._suns = []
        self._grassmowers = []
        # Screen
        self._font = pygame.font.Font("freesansbold.ttf", 15)
        self._font2 = pygame.font.Font("freesansbold.ttf", 22)
        self._screensize = width, height = 1100, 600
        self._screen = pygame.display.set_mode(self._screensize)
        self._screenimage = pygame.image.load("./assets/Background_0.jpg")
        # Initialization
        self._clickedcoord = (-1, -1)
        self._mousecoord = (-1, -1)
        self._slotclicked = False
        self.start()
        # Time
        self._clock = pygame.time.Clock()
        self._lastsun = 0
        self._lastzombie = 0
        # Win / lose
        self._win = False
        self._lose = False
        self._winimage = pygame.image.load("./assets/win.png")
        self._loseimage = pygame.image.load("./assets/lose.png")
        # Shovel
        self._shovelimg = pygame.image.load("./assets/Shovel/Shovelicon.png")
        self._shovelimg = pygame.transform.scale(self._shovelimg, (50,50))
        self._shovelrect = self._shovelimg.get_rect()
        self._shovelrect.top, self._shovelrect.left = 0, 800
        self._shovelcursor = pygame.image.load("./assets/Shovel/Shovelmouse.png")
        self._shovelcursor = pygame.transform.scale(self._shovelcursor, (int(self._shovelcursor.get_width())*0.4, int(self._shovelcursor.get_height())*0.4))
        self._shovelclicked = False
        # Other
        self._totalamount = 100
        self._zombierand = random.randint(400,1000)
        self._activelanes = [0,0,0,0,0]
        self._paused = False
        self._zombiekillcount = 0
        self._level = 1
        
    def start(self):
        self._menubar.create_slots(self._slots)
        self.create_blocks()
        self.create_grassmower()

    def pause(self, bool): # if bool is True, the only way to exit the game is pygame.QUIT
        while self._paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self._paused = bool

    def game_over(self):
        self._paused = True
        self._lose = True
        self.mainrender()
        self.pause(True)
        
    def win(self):
        if self._zombiekillcount == 50:
            self._level += 1
            self._zombiekillcount = 0

            if self._level == 4:
                self._level = 3
                self._paused = True
                self._win = True
                self.mainrender()
                self.pause(True)

    def game_loop(self):
        while 1:
            self._current_time = pygame.time.get_ticks()
            self.set_mousecoord()
            self.events()
            self.maincooldown()
            self.mainanimation()
            self.mainactions()
            self.win()
            self.mainrender()
            self._clock.tick(60)
    
    # Mouse    
    def set_mousecoord(self):
        self._mousecoord = pygame.mouse.get_pos()

    def update_clickedcoord(self):
        self._clickedcoord = pygame.mouse.get_pos()

    # Capturing events
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._paused = True
                    self.pause(False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.update_clickedcoord()

                    if self.check_sun():
                        self.shovelmouse_del()
                        self._tempsun = self.check_sun()
                        self.remove_sun(self._tempsun)
                        self.update_money()
                        self._slotclicked = False
                        for slot in self._slots:
                            slot.delete_highlight()
                        break

                    if self.check_usedblock():
                        if self._shovelclicked:
                            self._tempusedblock = self.check_usedblock()
                            self.update_money()
                            self._usedBlocks.remove(self._tempusedblock)
                            self._availableBlocks.append(self._tempusedblock)
                            fl = self._tempusedblock.return_fl()
                            self._flowers.remove(fl)
                        self.shovelmouse_del()

                    if self.check_block():
                        self.shovelmouse_del()
                        if self._slotclicked: # If slot is clicked beforehand
                            self._tempblock = self.check_block()
                            self._usedBlocks.append(self._tempblock)
                            self._availableBlocks.remove(self._tempblock)
                            self._tempslot.cooldown_animation(self._current_time)
                            self._slotamount = self._tempslot.return_amount()
                            if self._tempslot._key == "Peas":
                                self.create_peas()
                                self._totalamount -= self._slotamount
                            if self._tempslot._key == "Sunflower":
                                self.create_sunflower()
                                self._totalamount -= self._slotamount
                            if self._tempslot._key == "Ice":
                                self.create_ice()
                                self._totalamount -= self._slotamount

                    if self.check_slot():
                        self.shovelmouse_del()
                        # Var
                        self._tempslot = self.check_slot()
                        index = self._slots.index(self._tempslot)
                        slotlist = self._slots[:index]+self._slots[index+1:]
                        self._clickable = self._tempslot.is_clickable()
                        # Amount checking
                        if self._totalamount >= self._tempslot.return_amount() and self._clickable:
                            # Slot highlight
                            self._tempslot.highlight_slot()
                            for slot in slotlist:
                                slot.delete_highlight()
                            self._slotclicked = True
                        else:
                            pass

                    elif self.check_shovel():
                        pygame.mouse.set_visible(False)
                        self._shovelclicked = True
                        self._slotclicked = False
                        for slot in self._slots:
                            slot.delete_highlight()

                    else:
                        if self._slotclicked or self._shovelclicked:
                            self._tempslot = None
                            self._tempblock = None
                            self._tempusedblock = None
                            for slot in self._slots:
                                slot.delete_highlight()
                            self._slotclicked = False
                            self.shovelmouse_del()


    # Sun & Amount functions
    def update_money(self):
        self._totalamount += 25

    def remove_sun(self, sun):
        self._suns.remove(sun)

    # Animation
    def mainanimation(self):
        self.update_flowersprites()
        self.update_slots()
        self.update_sunsprites()
        self.update_zombiesprites()

    def shovelmouse_del(self):
        pygame.mouse.set_visible(True)
        self._shovelclicked = False
    
    def update_flowersprites(self):
        for fl in self._flowers:
            fl.update_sprite(self._current_time)

    def update_slots(self):
        for slot in self._slots:
            slot.check_cooldown(self._current_time, self._totalamount)

    def update_sunsprites(self):
        for sun in self._suns:
            sun.update_sprite(self._current_time)

    def update_zombiesprites(self):
        for zombie in self._zombies:
            zombie.update_sprite(self._current_time)
                                                                     
    # Rendering
    def render_amount(self):
        self._scoretext = self._font.render(f"{self._totalamount}", True, (0,0,0))
        menutop, menuleft = self._menubar.return_topleft()
        self._screen.blit(self._scoretext, (menuleft + 25, menutop + 68))

    def render_score(self):
        self._score = self._font2.render(f"Score: {self._zombiekillcount} / 50", True, (0,0,0))
        self._screen.blit(self._score, (950,0))

    def render_level(self):
        self._leveltext = self._font2.render(f"Level: {self._level}", True, (0,0,0))
        self._screen.blit(self._leveltext, (950,25))

    def render_grassmowers(self):
        for grass in self._grassmowers:
            grass.render_grass(self._screen)

    def render_flowers(self):
        for flower in self._flowers:
            flower.render_flower(self._screen)
    
    def render_slots(self):
        for slot in self._slots:
            slot.render_slot(self._screen)

    def render_suns(self):
        for sun in self._suns:
            sun.render_sun(self._screen)

    def render_zombies(self):
        for zombie in self._zombies:
            zombie.render_zombie(self._screen)

    def render_bullets(self):
        for bullet in self._bullets:
            bullet.render_bullet(self._screen)
            
    def render_mouse(self):
        if self._shovelclicked:
            self._screen.blit(self._shovelcursor, (self._mousecoord[0] - (int(self._shovelcursor.get_width())/2), self._mousecoord[1] - (int(self._shovelcursor.get_height())/2)))

    def mainrender(self):
        self._screen.blit(self._screenimage, (0,0))
        self.block_mouse()
        self.render_flowers()
        self.render_zombies()
        self.render_bullets()
        self._screen.blit(self._menubar._image, (self._menubar._left, self._menubar._top))
        self._screen.blit(self._shovelimg, (self._shovelrect.left, self._shovelrect.top))
        self.render_amount()
        self.render_slots()
        self.render_grassmowers()
        self.render_suns()
        self.render_score()
        self.render_level()
        if self._win:
            self._screen.blit(self._winimage, (450,190))
        if self._lose:
            self._screen.blit(self._loseimage, (200,190))
        self.render_mouse()
        pygame.display.flip()

    # Actions
    def mainactions(self):
        self.zombieactions()
        self.floweractions()
        self.bulletactions()
        self.grassactions()

    def zombieactions(self):
        for zombie in self._zombies:
            zrect = zombie.return_zrect()
            # Game over check
            if zrect.left <= 195:
                self.game_over()

            zlane = zombie.return_zlane()
            zslowed = zombie.is_slowed()
            zDmg = zombie.return_damage()
            walkFlag = True
            eatFlag = True
            # Flower - Zombie
            for fl in self._flowers:
                frect = fl.return_flowerinstance()[1]
                flane = fl.return_lane()
                if zlane == flane and frect.colliderect(zrect):
                    walkFlag = False
                    eatFlag = False
                    zombie.set_eating(True)
                    if zombie.eat(self._current_time):
                        fl.lower_health(zDmg)
                    break
                    
            if eatFlag: zombie.set_eating(False)
            if walkFlag: zombie.move(self._current_time)

            # Bullet - Zomibe
            for bullet in self._bullets:
                brect = bullet.return_bulletinstance()[1]
                if brect.colliderect(zrect):
                    if type(bullet) == flower.IceBullet and zslowed == False:
                        srate = bullet.return_slowrate()
                        zombie.slow(self._current_time, srate)
                    
                    bDmg = bullet.return_dmg()
                    zombie.update_hp(bDmg)
                    self._bullets.remove(bullet)
                    break

            if zslowed:
                zombie.check_slow(self._current_time)

            # Grassmower - Zombie
            for grass in self._grassmowers:
                grect = grass.return_grassinstance()[1]
                if grect.colliderect(zrect):
                    grass.set_move()
                    self._zombiekillcount += 1
                    self._zombies.remove(zombie)
                    self._activelanes[zlane] -= 1

            zhp = zombie.return_hp()
            if zhp <= 0:
                self._zombiekillcount += 1
                self._zombies.remove(zombie)
                self._activelanes[zlane] -= 1
                    
                
    def bulletactions(self):
        for bullet in self._bullets:
            bullet.move(self._current_time)
            if bullet._rect.left >= 1110:
                self._bullets.remove(bullet)
    
    def floweractions(self):
        for fl in self._flowers:
            lane = fl.return_lane()
            cooldown = fl.return_flowercdown()
            top, left = fl.return_flowercoords()[0], fl.return_flowercoords()[1]
            if type(fl) == flower.Sunflower and cooldown:
                self._suns.append(flower.Sun(False, top, left))
            else:
                key = fl.return_flowerkey()
                if key == "Peas" and cooldown and self._activelanes[lane] > 0:
                    self._bullets.append(flower.PeasBullet(top+6, left+42))
                elif key == "Ice" and cooldown and self._activelanes[lane] > 0:
                    self._bullets.append(flower.IceBullet(top+6, left+42))

            fhp = fl.return_hp()
            if fhp <= 0:
                self._availableBlocks.append(fl.return_block())
                self._flowers.remove(fl)
                self._usedBlocks.remove(fl.return_block())

    def grassactions(self):
        for grass in self._grassmowers:
            movecheck = grass.is_move()
            left = grass.return_grassinstance()[1].left
            if movecheck:
                grass.move(self._current_time)
            if left >= 1100:
                self._grassmowers.remove(grass)
            


    # Creation of flowers
    def create_peas(self):
        top = self._tempblock.return_topleft()[0]
        left = self._tempblock.return_topleft()[1]
        new_peas = flower.Peas(top, left, self._current_time, self._tempblock.return_lane())
        self._flowers.append(new_peas)
        new_peas.setblock(self._tempblock)
        self._tempblock.setflower(new_peas)

    def create_sunflower(self):
        top = self._tempblock.return_topleft()[0]
        left = self._tempblock.return_topleft()[1]
        new_sunflower = flower.Sunflower(top, left, self._current_time, self._tempblock.return_lane())
        self._flowers.append(new_sunflower)
        new_sunflower.setblock(self._tempblock)
        self._tempblock.setflower(new_sunflower)

    def create_ice(self):
        top = self._tempblock.return_topleft()[0]
        left = self._tempblock.return_topleft()[1]
        new_ice = flower.Ice(top, left, self._current_time, self._tempblock.return_lane())
        self._flowers.append(new_ice)
        new_ice.setblock(self._tempblock)
        self._tempblock.setflower(new_ice)


    # Checking if there is an object in the clicked coords
    def check_slot(self):
        for item in self._slots:
            if item.mouse_collusion(self._clickedcoord):
                return item

    def check_flower(self):
        for item in self._flowers:
            if item.mouse_collusion(self._clickedcoord):
                return item

    def check_block(self):
        for item in self._availableBlocks:
            if item.mouse_collusion(self._clickedcoord):
                return item

    def check_usedblock(self):
        for item in self._usedBlocks:
            if item.mouse_collusion(self._clickedcoord):
                return item

    def check_sun(self):
        for item in self._suns:
            if item.mouse_collusion(self._clickedcoord):
                return item

    def check_shovel(self):
        if self._shovelrect.collidepoint(self._clickedcoord):
            return True

    # Block functions
    def create_blocks(self): 
        self._block11 = Block(96, 266, 0)
        self._availableBlocks.append(self._block11)
        self._block12 = Block(96, 345, 0)
        self._availableBlocks.append(self._block12)
        self._block13 = Block(96, 426 ,0)
        self._availableBlocks.append(self._block13)
        self._block14 = Block(96, 512, 0)
        self._availableBlocks.append(self._block14)

        self._block21 = Block(190, 266, 1)
        self._availableBlocks.append(self._block21)
        self._block22 = Block(190, 345, 1)
        self._availableBlocks.append(self._block22)
        self._block23 = Block(190, 426 ,1)
        self._availableBlocks.append(self._block23)
        self._block24 = Block(190, 512, 1)
        self._availableBlocks.append(self._block24)

        self._block31 = Block(290, 266, 2)
        self._availableBlocks.append(self._block31)
        self._block32 = Block(290, 345, 2)
        self._availableBlocks.append(self._block32)
        self._block33 = Block(290, 426 ,2)
        self._availableBlocks.append(self._block33)
        self._block34 = Block(290, 512, 2)
        self._availableBlocks.append(self._block34)

        self._block41 = Block(387, 266, 3)
        self._availableBlocks.append(self._block41)
        self._block42 = Block(387, 345, 3)
        self._availableBlocks.append(self._block42)
        self._block43 = Block(387, 426 ,3)
        self._availableBlocks.append(self._block43)
        self._block44 = Block(387, 512, 3)
        self._availableBlocks.append(self._block44)

        self._block51 = Block(480, 266, 4)
        self._availableBlocks.append(self._block51)
        self._block52 = Block(480, 345, 4)
        self._availableBlocks.append(self._block52)
        self._block53 = Block(480, 426 ,4)
        self._availableBlocks.append(self._block53)
        self._block54 = Block(480, 512, 4)
        self._availableBlocks.append(self._block54)

        
    def block_mouse(self):
        if self._slotclicked:
            for block in self._availableBlocks:
                if block.mouse_collusion(self._mousecoord):
                    self._tempslot.set_fadedrect(block.return_topleft()[0], block.return_topleft()[1])
                    fadedimage = self._tempslot.return_fadedinstance()[0]
                    fadedrect = self._tempslot.return_fadedinstance()[1]
                    block.draw_faded(self._screen, fadedimage, fadedrect)
                    break

    # Time / cooldown functions
    def sun_spawn(self):
        if self._current_time - self._lastsun >= (1000/60) * 400:
            self._suns.append(flower.Sun(True, None, None))
            self._lastsun = self._current_time

    def zombie_spawn(self):
        if self._current_time - self._lastzombie >= (1000/60) * self._zombierand:
            self._lastzombie = self._current_time
            choice = random.randint(1,3)
            if choice == 1:
                new_zombie = zombie.Strong_Zombie()
            elif choice == 2:
                new_zombie = zombie.Weak_Zombie()
            elif choice == 3:
                new_zombie = zombie.Quick_Zombie()

            self._zombies.append(new_zombie)
            zlane = new_zombie.return_zlane()
            self._activelanes[zlane] += 1
            if self._level == 1:
                self._zombierand = random.randint(400,1000)
            elif self._level == 2:
                self._zombierand = random.randint(200,700)
            elif self._level == 3:
                self._zombierand = random.randint(150,450)

    def bullet_cooldown(self):
        for flower in self._flowers:
            flower.check_bulletcooldown(self._current_time)

    def maincooldown(self):
        self.sun_spawn()
        self.zombie_spawn()
        self.bullet_cooldown()

    #Grassmower
    def create_grassmower(self):
        self._grass1 = Grassmower(115, 190)
        self._grass2 = Grassmower(200, 190)
        self._grass3 = Grassmower(300, 190)
        self._grass4 = Grassmower(400, 190)
        self._grass5 = Grassmower(510, 190)
        self._grassmowers.append(self._grass1)
        self._grassmowers.append(self._grass2)
        self._grassmowers.append(self._grass3)
        self._grassmowers.append(self._grass4)
        self._grassmowers.append(self._grass5)


class MenuBar: 
    def __init__(self):
        self._image = pygame.image.load("./assets/MenuBar.png")
        self._heigth = 87
        self._width = 300
        self._top = 0
        self._left = 250

    def create_slots(self, listname):
        self._peas_slot = Slot("./assets/Slot/card_peashooter.png", self._top + 10, self._left + 81, "Peas")
        self._sun_slot = Slot("./assets/Slot/card_sunflower.png", self._top + 10, self._left + 81 + 45 + 9, "Sunflower")
        # self._daisy_slot = Slot()
        self._ice_slot = Slot("./assets/Slot/card_snowpea.png", self._top + 10, self._left + 187, "Ice")
        listname.append(self._peas_slot)
        listname.append(self._sun_slot)
        # listname.append(self._daisy_slot)
        listname.append(self._ice_slot)

    def return_topleft(self):
        return self._top, self._left
      

class Slot(MenuBar, Function):
    def __init__(self, simage, top, left, key):
        # Images
        self._image = pygame.image.load(simage)
        # Size
        self._heigth = 65
        self._width = 45
        self._top = top
        self._left = left
        # Creating rect of the slot
        self._image = pygame.transform.scale(self._image, (self._width, self._heigth))
        self._rect = self._image.get_rect()
        self._rect.top , self._rect.left = top, left
        # Other
        self._key = key
        self._clickable = True
        self._lastupdate = -(1000/60)*601
        self.start()

    def start(self):
        if self._key == "Peas":
            self._amount = 100
            self._peas = flower.Peas(-1, -1, -1, None)
            self._fadedimage = self._peas.return_faded()
            self._fadedrect = self._fadedimage.get_rect()
            self._cooldown = (1000/60)*450

        if self._key == "Sunflower":
            self._amount = 50
            self._sunflower = flower.Sunflower(-1, -1, -1, None)
            self._fadedimage = self._sunflower.return_faded()
            self._fadedrect = self._fadedimage.get_rect()
            self._cooldown = (1000/60)*300

        if self._key == "Ice":
            self._amount = 175
            self._ice = flower.Ice(-1, -1, -1, None)
            self._fadedimage = self._ice.return_faded()
            self._fadedrect = self._fadedimage.get_rect()
            self._cooldown = (1000/60)*600

    # Highlight
    def highlight_slot(self):
        self._rect.top = 4

    def delete_highlight(self):
        self._rect.top = 10

    # Cooldown
    def cooldown_animation(self, current):
        self._image.set_alpha(80)
        self.set_rect()
        self._clickable = False
        self._lastupdate = current

    def set_rect(self):
        self._rect = self._image.get_rect()
        self._rect.top , self._rect.left = self._top, self._left

    def check_cooldown(self, current, totalamount):
        if current - self._lastupdate >= self._cooldown:
            self._clickable = True
            if totalamount < self._amount:
                self._image.set_alpha(150)
            else:
                self._image.set_alpha(255)

    def is_clickable(self):
        return self._clickable

    # Faded
    def set_fadedrect(self, top, left):
        self._fadedrect.top, self._fadedrect.left = top, left

    def return_fadedinstance(self):
        return self._fadedimage, self._fadedrect

    # Amount
    def return_amount(self):
        return self._amount

    # Render
    def return_slotinstance(self):
        return self._image, self._rect

    def render_slot(self, screen):
        screen.blit(self._image, self._rect)


class Block:
    def __init__(self, top, left, lane):
        # Size
        self._heigth = 75
        self._width = 55
        self._top = top
        self._left = left
        # Rect
        self._rect = Rect(self._left, self._top, self._width, self._heigth)
        # Other
        self._lane = lane
        self._flower = None

    def draw_faded(self, screen, image, rect):
        screen.blit(image, rect)

    def return_topleft(self):
        return self._top, self._left

    def return_lane(self):
        return self._lane

    # Shovel
    def unselect(self):
        self._flower = None

    def return_fl(self):
        return self._flower

    def setflower(self, fl):
        self._flower = fl


class Grassmower:
    def __init__(self, top, left):
        self._top = top
        self._left = left
        # Image
        self._image = pygame.image.load("./assets/car.png")
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        self._image = pygame.transform.scale(self._image, (self._width*0.7, self._height*0.7))
        # Rect
        self._rect = self._image.get_rect()
        self._rect.top, self._rect.left = self._top, self._left
        # Move
        self._ismove = False
        self._lastmove = 0

    # Render
    def return_grassinstance(self):
        return self._image, self._rect

    def render_grass(self, screen):
        screen.blit(self._image, self._rect)

    def set_move(self):
        self._ismove = True

    def is_move(self):
        return self._ismove

    def move(self, current):
        if current - self._lastmove >= (1000/60)*0.1:
            self._lastmove = current
            self._rect.left += 3
