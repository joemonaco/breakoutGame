import pygame

pygame.init()

#size(TOP LEFT is (0,0) BOTTOM RIGHT is (1080, 720)
window = pygame.display.set_mode((1080,720)) #set windows

pygame.display.set_caption("Breakout")

brickWidth = 100
brickHeight = 30
ball = pygame.Rect(300,660 - 16,16,16) # make a ball object

ball_vel = [20,-20] #velcoties for the balll

bricks = []
def create_bricks():
    brickY = 30
    for i in range(7): # makes 7 rows
        brickX = 100
        for j in range(8): # makes 8 columns 
            bricks.append(pygame.Rect(brickX,brickY,brickWidth,brickHeight)) #makes new brick object
            brickX += brickWidth + 10 # x space between each brick
        brickY += brickHeight + 5 # y space between each brick 

#loops through eahc brick object and draws it to the screen
def draw_bricks(): 
    for brick in bricks:
        pygame.draw.rect(window, (0,255,0), brick)



#moves the ball
def move_ball():
    ball.left += ball_vel[0]
    ball.top  += ball_vel[1]
    
    #checks the x position of the ball
    if ball.left <= 0:
        ball.left = 0
        ball_vel[0] = -ball_vel[0]
    elif ball.left >= 1060:
        ball.left = 1060
        ball_vel[0] = -ball_vel[0]
    
    #cehcks the y pistion of the ball
    if ball.top < 0:
        ball.top = 0
        ball_vel[1] = -ball_vel[1]
    elif ball.top >= 700:
        ball.top = 700
        ball_vel[1] = -ball_vel[1]




paddleX = 540
paddleY = 660
paddleWidth = 100
paddleHeight = 30
paddleVel =  60   #how many pixels the paddles moves

gameOver = False





paddle = pygame.Rect((paddleX, paddleY, paddleWidth, paddleHeight))
create_bricks()
while(not gameOver):
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        paddleX = paddleX + paddleVel
        if paddleX > self.screenwidth - self.width:
            paddleX = self.screenwidth - self.width
    if keys[pygame.K_LEFT]:
        paddleX = paddleX - paddleVel


    move_ball()
    window.fill((255,255,255)) # makes window white
    pygame.draw.rect(window, (255,0,0), (paddleX, paddleY, paddleWidth, paddleHeight)) #creates the paddle
    pygame.draw.circle(window, (0,0,255), (ball.left + 8, ball.top + 8), 8) #draws the ball
    draw_bricks()
    pygame.display.update() #updates screen

pygame.quit()
