import sys
import pygame
import random
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #LEFT BTN
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #RIGHT BTN
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #ENTER BTN

pygame.init()
pygame.mixer.music.load("bgMusic.wav")
size = width, height = 1080, 720
speed = [8, 8]


#COLORS
black = 0, 0, 0
level1Color = 23,90,189
level2Color = 190,204,0
level3Color = 230,93,235
level4Color = 249,237,75
level5Color = 255,83,48
levelColors = [black, level1Color, level2Color, level3Color, level4Color, level5Color] 

window = pygame.display.set_mode(size)
level = 1
brickHits = []
brickWidth = 100
brickHeight = 30


life1 = pygame.image.load("heart.png")
life2 = pygame.image.load("heart.png")
life3 = pygame.image.load("heart.png")
heartX = 10
heartY = 10
lifeCount = 3

paddleX = 490
paddleY = 660
paddleWidth = 100
paddleHeight = 30
paddleVel =  22  #how many pixels the paddles moves

score = 0
powerUpString = ""
powerup = pygame.Rect(0,0,15,15)

bricks = []
def create_bricks():
    brickY = 10
    for i in range(7): # makes 7 rows
        brickX = 140
        for j in range(8): # makes 8 columns
            bricks.append(pygame.Rect(brickX,brickY,brickWidth,brickHeight)) #makes new brick object
            brickHits.append(level)
            brickX += brickWidth + 2 # x space between each brick
        brickY += brickHeight + 2 # y space between each brick

#loops through each brick object and draws it to the screen
def draw_bricks():
    global level
    for brick in bricks:
        pygame.draw.rect(window,levelColors[level], brick)


def movePaddleWithBall(keys):
    global paddleX
    global paddleVel
    global ballrect

    if GPIO.input(11):
        if not (paddle.right > 1080): # width of paddle added to screen dimension
            paddleX = paddleX + paddleVel
            ballrect.x = paddleX + 30
    if GPIO.input(7):
        if not (paddle.left < 0): # width of paddle added to screen dimension
            paddleX = paddleX - paddleVel
            ballrect.x = paddleX - 30

def checkKeyPress(keys):
    global paddleX
    global paddleVel

    if GPIO.input(11):
        if not (paddle.right > 1080): # width of paddle added to screen dimension
           paddleX = paddleX + paddleVel
    if GPIO.input(7):
        if not (paddle.left < 0): # width of paddle added to screen dimension
            paddleX = paddleX - paddleVel


def playerWins():
    print("YOU WIN")


ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()


def checkSidesCollision():
    if ballrect.left-15 < 0 or ballrect.right + 15 > width:
        speed[0] = -speed[0]
    if ballrect.top - 15  < 0:
        speed[1] = -speed[1]


Clock = pygame.time.Clock()

chanceToAppear = 0.01
powerUpDrop = False
powerUpY = 200
powerUpX = 500

#possible powerups
def extendPaddle():
    global paddleWidth
    global paddleHeight
    global powerUpString
    powerUpString = "Extend Paddle!"
    paddleWidth = 200
    paddleHeight = 30

def shrinkPaddle():
    global paddleWidth
    global paddleHeight
    global powerUpString
    powerUpString = "Shrink Paddle!"
    paddleWidth = 60
    paddleHeight = 30

def fastBall():
    global powerUpString
    global speed
    powerUpString = "Faster Ball!"
    speed = [12, 12]

def slowBall():
    global powerUpString
    global speed
    powerUpString = "Slower Ball!"
    speed = [5, 5]

powerUpActive = False

extendColor = (173,255,47)
shrinkColor = (204,0,0)
fastColor = (102,0,204)
slowColor = (255,255,255)
powerupColors = [extendColor, shrinkColor, fastColor, slowColor]
powerupIndex = 0
def checkPowerUp():

    global chanceToAppear
    global powerup
    global powerUpDrop
    global powerUpX
    global powerUpY
    global paddle
    global powerUpActive
    global powerupIndex
    global seconds

    if random.random() < chanceToAppear and not powerUpDrop and not powerUpActive:
        powerUpDrop = True
        powerUpY = 200
        powerUpX = random.randint(1, 1080)
        powerupIndex = random.randint(0,3)

    if powerUpDrop:
        powerup =  pygame.Rect(powerUpX,powerUpY,15,15)
        powerUpY += 10
        
    if powerup.colliderect(paddle) :
        powerup.x = -100
        powerup.y = -100
        powerUpActive = True
        time = pygame.time.get_ticks()
        if powerupIndex == 0:
            extendPaddle()
        elif powerupIndex == 1:
            shrinkPaddle()
        elif powerupIndex == 2:
            fastBall()
        elif powerupIndex == 3:
            slowBall()
        powerUpDrop = False
        
    if powerup.y >= height:
        powerUpDrop = False

brickBreak = pygame.mixer.Sound("breakBrick.wav")

def checkBrickCollision():
    global score
    global level
    global bricksBroken
    for i in range(len(bricks)):
        brick = bricks[i]
        if brick.colliderect(ballrect):
            speed[1] = -speed[1]
            if brickHits[i] == 1:
                pygame.mixer.Sound.play(brickBreak)
                bricks[i].x = -100
                bricks[i].y = -100
                score+= level
                bricksBroken += 1
            else:
                brickHits[i]-=1


def resetDefaults():
    global speed
    global paddleWidth
    global paddleHeight
    global powerUpString
    powerUpString = ""
    speed = [8,8]
    paddleWidth = 100
    paddleHeight = 30


def showHearts():
    global lifeCount
    global window
    global heartX

    if lifeCount == 3:
        window.blit(life1, (heartX, 10))
        window.blit(life2, (heartX+ 40, 10))
        window.blit(life2, (heartX+80, 10))
    elif lifeCount == 2:
        window.blit(life1, (heartX, 10))
        window.blit(life2, (heartX+ 40, 10))
    elif lifeCount == 1:
        window.blit(life1, (heartX, 10))


create_bricks()



def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def gameOverMenu():
    global window
    playAgain = False

    while not playAgain:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        window.fill((0,204,204))
        largeText = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = text_objects("GAME OVER!", largeText)
        TextRect.center = ((width/2),(height/2) - 60)

        largeText = pygame.font.Font('freesansbold.ttf',30)
        enterSurf, enterRect = text_objects("Press Enter to Play Again", largeText)
        enterRect.center = ((width/2) ,(height/2) + 100)

        window.blit(TextSurf, TextRect)
        window.blit(enterSurf, enterRect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            playAgain = True
        pygame.display.update()

    runGame()

def mainMenu():

    global window
    mainMenu = True

    while mainMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        window.fill((0,204,204))
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects("Breakout!  RaspPi Edition", largeText)
        TextRect.center = ((width/2),(height/2) - 60)

        largeText = pygame.font.Font('freesansbold.ttf',30)
        enterSurf, enterRect = text_objects("Press Enter to Play", largeText)
        enterRect.center = ((width/2) ,(height/2) + 100)

        window.blit(TextSurf, TextRect)
        window.blit(enterSurf, enterRect)
        keys = pygame.key.get_pressed()
        if GPIO.input(29):
            mainMenu = False
        pygame.display.update()

bricksBroken = 0
paddle = pygame.Rect(paddleX,paddleY,paddleWidth,paddleHeight)
start_ticks = pygame.time.get_ticks() #starter tick
def runGame():
    global window
    global ballrect
    global score
    global speed
    global lifeCount
    global paddle
    global level
    global bricksBroken
    global powerupIndex
    global powerUpActive
    global powerUpString

    # pygame.mixer.music.play(-1)
    nextLevel = False
    gameStart = False
    gameOver = False
    timeTick = 0
    while not gameOver:
        ticks = Clock.tick(60)
        # print("TICKS: ")
        # print(ticks)
        paddle = pygame.Rect(paddleX,paddleY,paddleWidth,paddleHeight)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                quit()

        if not gameStart:
            ballrect.x = paddleX + 30
            ballrect.y = paddleY - 40

            keys = pygame.key.get_pressed()
            movePaddleWithBall(keys)
            if GPIO.input(29):
                gameStart = True
                ballrect.move(speed)
        else:
            checkPowerUp()

            if powerUpActive:
                timeTick+=1
                print(timeTick)
                if timeTick > 700:
                    timeTick = 0
                    powerUpActive = False
                    print("DONE WITH POWERUP")
                    resetDefaults()
            if bricksBroken == len(bricks):
                playerWins()
                level+=1
                bricksBroken = 0
                nextLevel = True
                gameOver = True

            ballrect = ballrect.move(speed)
            checkSidesCollision()

            #checks if left or right arrow key pressed
            keys = pygame.key.get_pressed()
            checkKeyPress(keys)

            #bounces ball off paddle
            if ballrect.colliderect(paddle):
                speed[1] = -speed[1]

            #if ball goes under the paddle
            if ballrect.y >= height:
                gameStart = False
                lifeCount -= 1
                if lifeCount == 0:
                    gameOver = True

            #check for collision with bricks
            checkBrickCollision()

        paddle = pygame.Rect(paddleX,paddleY,paddleWidth,paddleHeight) #sets paddle
        window.fill((0,204,204))
        draw_bricks()

        # font = pygame.font.Font(None, 36)
        font = pygame.font.Font('freesansbold.ttf',30)
        scoreText = font.render(str(score), 1, (0,0,0))
        scoreTextpos = scoreText.get_rect()
        scoreTextpos.x = 500
        scoreTextpos.y = 300

        powerUpText = font.render(str(powerUpString), 1, (0,0,0))
        powerUpTextPos = powerUpText.get_rect()
        powerUpTextPos.x = 500
        powerUpTextPos.y = 400

        font = pygame.font.Font('freesansbold.ttf',30)
        TextSurf, TextRect = text_objects("Level " + str(level), font)
        TextRect.center = ((width - 70),(15))

        pygame.draw.rect(window, black, paddle) #creates the paddle
        pygame.draw.rect(window, powerupColors[powerupIndex], powerup) #creates the powerup block

        window.blit(TextSurf, TextRect)
        window.blit(ball, ballrect)
        window.blit(scoreText,scoreTextpos)
        window.blit(powerUpText,powerUpTextPos)
        showHearts()

        pygame.display.flip()

    if nextLevel:
        bricks.clear()
        brickHits.clear()
        create_bricks()
        runGame()
    else:
        powerUpActive = False
        bricksBroken = 0
        bricks.clear()
        brickHits.clear()
        score = 0
        level = 1
        lifeCount = 3
        create_bricks()
        gameOverMenu()

mainMenu()
runGame()
pygame.quit()
quit()
