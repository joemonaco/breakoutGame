import pygame

pygame.init()

#size(TOP LEFT is (0,0) BOTTOM RIGHT is (1080, 720)
window = pygame.display.set_mode((1080,720)) #set windows

pygame.display.set_caption("Breakout")

brickWidth   = 100
brickHeight  = 30

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

paddleX = 540
paddleY = 660
paddleWidth = 100
paddleHeight = 30
paddleVel =  60   #how many pixels the paddles moves

gameOver = False

class Ball(pygame.sprite.Sprite) :

    #Speed of ball in pixels per cycle
    speed = 10.0

    #Represents location of ball in floating points
    x = 0.0
    y = 180.0

    #direction of ball (in degrees)
    direction = 200

    width = 10
    height = 10

    # Constructor. Pass in the color of the block, and its x and y position
    def _init_(self) :

        #Call the parent class (Sprite) constructor
        super()._init_()

        # Image of the ball being created 
        self.image = pygame.Surface([self.width, self.height])

        #Ball color
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff) : "This will bounce the ball off a horizontal surface but not a vertical one"

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self) : "Update the position of the ball"

        # Sine and Cosine converted from degrees
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move image to x and y
        self.rect.x = self.x
        self.rect.y = self.y

        # Did the ball bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
            
        # Did the ball bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # the right of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
            
        # If the ball falls off the bottom of the screen
        if self.y > 600:
            return True
        else:
            return False
create_bricks()
while(not gameOver):
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        paddleX = paddleX + paddleVel
    if keys[pygame.K_LEFT]:
        paddleX = paddleX - paddleVel

    
    window.fill((255,255,255)) # makes window white
    pygame.draw.rect(window, (255,0,0), (paddleX, paddleY, paddleWidth, paddleHeight)) #creates the paddle
    draw_bricks()
    pygame.display.update() #updates screen

pygame.quit()
