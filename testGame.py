import sys, pygame
pygame.init()

size = width, height = 1080, 720
speed = [17, 20]
black = 0, 0, 0

window = pygame.display.set_mode(size)

brickWidth = 100
brickHeight = 30

score = 0

powerup = pygame.Rect(0,0,15,15)

bricks = []
def create_bricks():
    brickY = 10
    for i in range(7): # makes 7 rows
        brickX = 125
        for j in range(8): # makes 8 columns
            bricks.append(pygame.Rect(brickX,brickY,brickWidth,brickHeight)) #makes new brick object
            brickX += brickWidth + 2 # x space between each brick
        brickY += brickHeight + 2 # y space between each brick

#loops through each brick object and draws it to the screen
def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(window,(0,255,0), brick)



ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()


paddleX = 490
paddleY = 660
paddleWidth = 100
paddleHeight = 30
paddleVel =  60   #how many pixels the paddles moves

create_bricks()

gameStart = False
gameOver = False
while not gameOver:
    #paddle = pygame.Rect(paddleX,paddleY,paddleWidth,paddleHeight)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if not gameStart:
        ballrect.x = paddleX + 30
        ballrect.y = paddleY - 40
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            gameStart = True
    else:
        if score == len(bricks):
            print("YOU WIN!")

        ballrect = ballrect.move(speed)
        if ballrect.left-15 < 0 or ballrect.right + 15 > width:
            speed[0] = -speed[0]
        if ballrect.top - 15  < 0:
            speed[1] = -speed[1]

        #checks if left or right arrow key pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            paddleX = paddleX + paddleVel
        if keys[pygame.K_LEFT]:
            paddleX = paddleX - paddleVel

        #bounces ball off paddle
        if ballrect.colliderect(paddle):
            speed[1] = -speed[1]

        #if ball goes under the paddle
        if ballrect.y >= height:
            gameStart = False

        #check for collision with bricks
        for i in range(len(bricks)):
            brick = bricks[i]
            if brick.colliderect(ballrect):
                speed[1] = -speed[1]
                bricks[i].x = -100
                bricks[i].y = -100
                score+= 1

    font = pygame.font.Font(None, 36)
    text = font.render(str(score), 1, (0,0,0))
    textpos = text.get_rect()
    textpos.x = 500
    textpos.y = 300
    paddle = pygame.Rect(paddleX,paddleY,paddleWidth,paddleHeight) #sets paddle equal to
    window.fill((255,255,255))
    draw_bricks()
    pygame.draw.rect(window, (255,0,0), paddle) #creates the paddle
    window.blit(text, textpos)
    window.blit(ball, ballrect)
    pygame.display.flip()

pygame.quit()
