import requests
import pygame
import time
import random
import math
from pygame.locals import *
display_width = 800
display_height = 600

pygame.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0)
j.init()
print ( j.get_name())

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
bright_red = (255,0,0)

green = (0,200,0)
bright_green = (0,255,0)

blue = (0,0,200)
bright_blue = (0,0,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("The Game")
clock = pygame.time.Clock()

pause = False

class Player:
    Pickup_1 = 0
    Pickup_1_amount = 10
    Pickup_2 = 0
    Pickup_2_amount = 1
    Pickup_3 = 0
    Pickup_3_amount = 2
    
    def __init__(self, Maxhealth, speed, damage, attackType, weakness):
        
        self.name = Player
        self.Maxhealth = Maxhealth
        self.Currenthealth = Maxhealth
        self.speed = speed
        self.damage = damage
        self.attackType = attackType
        self.weakness = weakness
        self.score = 0
        
    def Pickup_1_affect(self):
        self.Currenthealth = int(self.Currenthealth + self.Pickup_1_amount)

    def Pickup_2_affect(self):
        self.speed = int(self.speed + self.Pickup_2_amount)

    def Pickup_3_affect(self):
        self.damage = int(self.damage + self.Pickup_3_amount)

    def hit(self, enemy_num):
        self.Currenthealth = self.Currenthealth - enemy_num.damage

    def kill(self, enemy_num):
        self.score = self.score + enemy_num.points
        

class Enemies:

    powerup_amount = 1
    num_of_enemies = 0

    def __init__(self, name, health, speed, damage):
        self.name = name
        self.health = health
        self.speed = speed
        self.damage = damage

        Enemies.num_of_enemies += 1

    @property
    def display_attributes(self):
        return '{} = health:{}, speed:{}, damage:{}'.format(self.name, self.health, self.speed, self.damage)

    def powerup_affect(self):
        self.damage = int(self.damage + self.powerup_amount)

    def __repr__(self):
        return "Enemies('{}', {}, {}, {})".format(self.name, self.health, self.speed, self.damage)

    @classmethod
    def set_powerup_amount(cls, amount):
        cls.powerup_amount = amount

class CommonGrunt(Enemies):
    powerup_amount = 1

    def __init__(self, name, health, speed, damage, weakness):
        Enemies.__init__(self, name, health, speed, damage)
        self.weakness = weakness
        self.points = 1

    def __repr__(self):
        return "CommonGrunt('{}', {}, {}, {}, '{}')".format(self.name, self.health, self.speed, self.damage, self.weakness)

    def alive(self, status):
        self.status = status

    
##---------All-Class-Objects--------##
        
Player = Player(100, 4, 1, 'normal', 'fire')
PlayerImg = pygame.image.load('upgrade.png')

Grunt_1 = CommonGrunt('first', 10, 2, 1, 'fire')
Grunt_1Img = pygame.image.load('bullet.png')
Grunt_2 = CommonGrunt('second', 20, .5, 2, 'fire')
Grunt_2Img = pygame.image.load('bullet2.xcf')

##----------------------------------##
def PlayerPlacement(PlayerImg,x,y):
    gameDisplay.blit(PlayerImg,(x,y))

def Player_value_Display():
    font = pygame.font.SysFont(None, 25)
    text1 = font.render("Health: "+str(Player.Currenthealth), True, black)
    text2 = font.render("Score: "+str(Player.score), True, black)

    gameDisplay.blit(text1,(0,100))
    gameDisplay.blit(text2,(100,100))

def Grunt_1Placement(x2,y2):
    gameDisplay.blit(Grunt_1Img,(x2,y2))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def rot_center(image, angle):
    #"""rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

        
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), y+(h/2) )
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def Game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("THE Game", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,Game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)
        
        pygame.display.update()
        clock.tick(15)

def Game_loop():
    Grunt_1.alive(True)
    print(Grunt_1.status)
    
    x = (display_width / 2)
    y = (display_height / 2)

    x2 = 0
    y2 = 0

    

    x_change = 0
    y_change = 0

    side2 = 0
    x2_change = 0
    y2_change = 0

    Grunt_1_startx = 0
    Grunt_1_starty = 0

    

    side2 = random.randrange(1,5)
    if side2 == 1:
        x2 = 0
        y2 = random.randrange(0,600)
    if side2 == 2:
        x2 = 800
        y2 = random.randrange(0,600)
    if side2 == 3:
        x2 = random.randrange(0,800)
        y2 = 0
    if side2 == 4:
        x2 = random.randrange(0,800)
        y2 = 600

    
    
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = Player.speed * -1
                    print('x_change = -5')
                if event.key == pygame.K_RIGHT:
                    x_change = Player.speed
                    print('x_change = 5')
                if event.key == pygame.K_UP:
                    y_change = Player.speed * -1
                    print('y_change = -5')
                if event.key == pygame.K_DOWN:
                    y_change = Player.speed
                    print('y_change = 5')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change = 0
                    print('x_change = 0')
                if event.key == pygame.K_RIGHT:
                    x_change = 0
                    print('x_change = 0')
                        
                if event.key == pygame.K_UP:
                    y_change = 0
                    print('y_change = 0')
                if event.key == pygame.K_DOWN:
                    y_change = 0
                    print('y_change = 0')

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        angle = math.atan2(x - mouse[0], y - mouse[1])
        angle = math.degrees(angle)
        print(angle)
        PlayerImg = pygame.transform.rotate(pygame.image.load('upgrade.png'), angle)
        
        x += x_change
        y += y_change

        gameDisplay.fill(white)
        PlayerPlacement(PlayerImg,x,y)
        Grunt_1Placement(x2,y2)
        Player_value_Display()

        

        if Grunt_1.status == False:
            side2 = random.randrange(1,5)
            if side2 == 1:
                x2 = 0
                y2 = random.randrange(0,600)
            if side2 == 2:
                x2 = 800
                y2 = random.randrange(0,600)
            if side2 == 3:
                x2 = random.randrange(0,800)
                y2 = 0
            if side2 == 4:
                x2 = random.randrange(0,800)
                y2 = 600
            Grunt_1.alive(True)
        else:
            if x2 < x:
                x2 = x2 + Grunt_1.speed

            if x2 > x:
                x2 = x2 - Grunt_1.speed

            if x2 == x:
                x2 = x2

            if y2 < y:
                y2 = y2 + Grunt_1.speed

            if y2 > y:
                y2 = y2 - Grunt_1.speed

            if y2 == y:
                y2 = y2

        if x2 < x+50 and x2 >= x or x2+20 < x+50 and x2+20 >= x:
            if y2 < y+50 and y2 >= y or y2+20 < y+50 and y2+20 >= y:
                print('hit')
                Player.hit(Grunt_1)
                Player.kill(Grunt_1)
                print(Player.Currenthealth)
                Grunt_1.alive(False)
                print(Grunt_1.status)

        pygame.display.update()
        clock.tick(60)
        

Game_intro()
Game_loop()
pygame.quit()
quit()




