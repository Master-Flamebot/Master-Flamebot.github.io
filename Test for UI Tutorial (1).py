#import requests
import pygame
import time
import random
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.joystick.init()
pygame.camera.init()
j = pygame.joystick.Joystick(0)
j.init()
print ( j.get_name())

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
bright_red = (255,0,0)

green = (0,200,0)
bright_green = (0,255,0)

blue = (0,0,200)
bright_blue = (0,0,255)

block_color = (53,115,255)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Racing Game")
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
thingImg = pygame.image.load('enemy.png')
PowerupImg = pygame.image.load('upgrade.png')
bulletImg = pygame.image.load('bullet.png')

pause = False
button1 = 0#1
button2 = 0#2
z = 0#3
leftvert = 0
rightvert = 0
righthorz = 0
ammo = 0
status = 0

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    #pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    gameDisplay.blit(thingImg,(thingx,thingy))

def Powerups(Powerupx, Powerupy, Powerupw, Poweruph, color):
    #pygame.draw.rect(gameDisplay, color, [Powerupx, Powerupy, Powerupw, Poweruph])
    gameDisplay.blit(PowerupImg,(Powerupx,Powerupy))

def bullets(bulletx, bullety, bulletw, bulleth, color):
    gameDisplay.blit(bulletImg,(bulletx,bullety))

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def Joysticks():
    pygame.event.pump()

    global leftvert
    global rightvert
    global righthorz
    global button1
    global button2
    global z
    global status

    button1 = j.get_button(0)#1
    button2 = j.get_button(1)#2
    z = j.get_button(2)#3
    
    rightvert = j.get_axis(3)
    rightvert = rightvert * -100
    rightvert = int(rightvert)
    #print (rightvert)

    righthorz = j.get_axis(2)
    righthorz = righthorz * -100
    righthorz = int(righthorz)
    #print (righthorz)

    leftvert = j.get_axis(1)
    leftvert = leftvert * -100
    leftvert = int(leftvert)
    #print (leftvert)
    #print (leftvert , rightvert , righthorz)

    leftvert = leftvert + 100
    leftvert = leftvert * 180
    leftvert = leftvert / 200
    #r = requests.get('http://10.42.0.111:10/left/{}'.format( leftvert ))

    rightvert = rightvert + 100
    rightvert = rightvert * 180
    rightvert = rightvert / 200
    #r = requests.get('http://10.42.0.111:10/right/{}'.format( rightvert ))

    righthorz = righthorz + 100
    righthorz = righthorz * 180
    righthorz = righthorz / 200

    #payload = {'left': leftvert,'right': rightvert,'up': righthorz,'button1':button1,'button2':button2,'button3':z}
    #requests.get('http://10.42.0.111:10/left/',params=payload)
    #status = requests.get('http://10.42.0.111:10/status/')

def Joystick_values(leftvert_val,rightvert_val,righthorz_val):
    global ammo
    global status
    
    font = pygame.font.SysFont(None, 25)
    text1 = font.render("Left: "+str(leftvert_val), True, black)
    text2 = font.render("right: "+str(rightvert_val), True, black)
    text3 = font.render("up: "+str(righthorz_val), True, black)
    text4 = font.render("ammo: "+str(ammo), True, black)
    #text5 = font.render("status: "+str(status.text), True, black)
    
    gameDisplay.blit(text1,(0,100))
    gameDisplay.blit(text2,(100,100))
    gameDisplay.blit(text3,(200,100))
    gameDisplay.blit(text4,(100,50))
    #gameDisplay.blit(text5,(200,50))
    

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()
    
def crash():
    message_display('You Crashed')

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

def unpause():
    global pause
    pause = False
    

def paused():

    
    while pause:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)


        
        
        
        pygame.display.update()
        clock.tick(15)


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Racing Game", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)


        
        
        
        pygame.display.update()
        clock.tick(15)

    
def game_loop():
    global pause
    global leftvert
    global rightvert
    global righthorz
    global ammo
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    state = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 130
    thing_height = 115

    Powerup_startx = random.randrange(0, display_width)
    Powerup_starty = -900
    Powerup_speed = 5
    Powerup_width = 50
    Powerup_height = 50

    bullet_startx = x
    bullet_starty = y
    bullet_speed = -7
    bullet_width = 20
    bullet_height = 20

    thingCount = 1
    bulletCount = 0
    ammo = 0

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_SPACE:
                    bulletCount += 1
                    if bullet_starty < display_height-600 and ammo > 0:
                        bullet_startx = x
                        bullet_starty = y
                        ammo += -1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        Joysticks()
        leftvert_val = leftvert
        rightvert_val = rightvert
        righthorz_val = righthorz

####        if righthorz == 0:
####            x_change = 0
####            
####        if righthorz > 0 and righthorz < 40:
####            x_change = -1
####        if righthorz < 0 and righthorz > -40:
####            x_change = 1
####
####        if righthorz > 40 and righthorz < 60:
####            x_change = -2
####        if righthorz < -40 and righthorz > -60:
####            x_change = 2
####
####        if righthorz > 60 and righthorz < 80:
####            x_change = -3
####        if righthorz < -60 and righthorz > -80:
####            x_change = 3
####
####        if righthorz > 80 and righthorz < 100:
####            x_change = -4
####        if righthorz < -80 and righthorz > -99:
####            x_change = 4
####
####        if righthorz == 100:
####            x_change = -5
####        if righthorz == -99:
####            x_change = 5

            
        

        x += x_change
        gameDisplay.fill(white)

        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed

        #Powerups(Powerupx, Powerupy, Powerupw, Poweruph, color)
        Powerups(Powerup_startx, Powerup_starty, Powerup_width, Powerup_height, green)
        Powerup_starty += Powerup_speed

        #bullets(bulletx, bullety, bulletw, bulleth, color)
        bullets(bullet_startx, bullet_starty, bullet_width, bullet_height, color)
        bullet_starty += bullet_speed
        
        car(x,y)
        things_dodged(dodged)
        Joystick_values(leftvert_val,rightvert_val,righthorz_val)

        if state == 1:
            state = 0
            thing_speed += -2

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += .75

        if Powerup_starty > display_height:
            Powerup_starty = 0 - Powerup_height
            Powerup_startx = random.randrange(0, display_width)

        if bullet_starty < thing_starty+thing_height:
            
            #print('y crossover')

            if bullet_startx > thing_startx and bullet_startx < thing_startx + thing_width or bullet_startx+bullet_width > thing_startx and bullet_startx + bullet_width < thing_startx+thing_width and thing_starty > 0:
                thing_starty = -600 - thing_height
                thing_startx = random.randrange(0,display_width)
                dodged += 1
                #print('x crossover')
                #crash()

        if y < Powerup_starty + Powerup_height:
            
            if x > Powerup_startx and x < Powerup_startx + Powerup_width or x + car_width > Powerup_startx and x + car_width < Powerup_startx + Powerup_width and state == 0:         
                Powerup_starty = -600 - Powerup_height
                Powerup_startx = random.randrange(0, display_width)
                state = 1
                ammo += 1
                
        if thing_speed < 1:
            thing_speed = 1
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
