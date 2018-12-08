import pygame

pygame.init()

#size(TOP LEFT is (0,0) BOTTOM RIGHT is (1080, 720)
window = pygame.display.set_mode((1080,720)) #set windows

pygame.display.set_caption("Breakout")


paddleX = 540
paddleY = 660
paddleWidth = 100
paddleHeight = 30
paddleVel = 40 #How many pixels the paddles moves

gameOver = False

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
    pygame.display.update() #updates screen

pygame.quit()
