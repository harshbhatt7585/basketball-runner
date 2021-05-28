import pygame 
import random

pygame.init()

# global varibale
width = 700
heigth = 550
screen = pygame.display.set_mode((width,heigth))
fps = 60
clock = pygame.time.Clock()

# colors
red = (255,0,0)
black = (0,0,0)



# images
background = pygame.image.load("assets/images/background.png").convert_alpha()
base = pygame.image.load("assets/images/road.jpg").convert_alpha()
basketball = pygame.image.load("assets/images/basketball.png").convert_alpha()
pole = pygame.image.load("assets/images/pole.png").convert_alpha()
basket = pygame.image.load("assets/images/basket.png").convert_alpha()

# sounds
bounce = pygame.mixer.Sound("assets/sound/bouncing.wav")
extras_pointSound = pygame.mixer.Sound("assets/sound/basket.wav")

def getPoleY(baseY):
    return random.randrange(100, baseY-200)

def moving_base(baseX , baseY, base):
    screen.blit(base, (baseX,baseY))
    screen.blit(base, (baseX+width, baseY))

def collision(poleX, poleY, ballX, ballY):
    if(ballX >= poleX and ballX <= poleX+50 and ballY > poleY):
        return True
    
    elif(ballY <-10):
        return True

    return False

def ScreenText(text, color, x,y, size,style, bold=False, itallic=False):
    font = pygame.font.SysFont(style, size, bold=bold, italic=itallic)
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x,y))

def random_basket(poleY, baseY):
    return random.randrange(poleY+100, baseY-100)

def getHighestScore():
    with open("highest score.txt","r") as f:
        return f.read()

def main():
    gameOn = True
    baseX = 0
    baseY = heigth - 60
    ballX = 120
    ballY = baseY - 60
    gravity = 10
    bouncing = 25
    poleX = 400
    poleY = getPoleY(baseY)
    baseX_vel = 0
    poleX_vel = 0
    score = 0 
    speed = 0
    gameOver = False
    basketY = random_basket(poleY, baseY)
    basket_score = 0
    score = 0
    speed_accelerating = False
    gameSpeed = 0

    try:
        highestScore = int(getHighestScore())
    except:
        highestScore = 0
    

    while gameOn:
        # taking event 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if (gameOver == False):
                        gameSpeed = 0.001
                        bouncing = 25
                        speed = 5
                        baseX_vel = int(speed)    
                        poleX_vel = int(speed) 
            
        basketX = poleX + 35
        screen.blit(background, (0,0))
        screen.blit(basket, (basketX, basketY))
        screen.blit(pole, (poleX,poleY))
        moving_base(baseX, baseY, base)
        screen.blit(basketball, (ballX,ballY))

        # bouncing
        ballY -= bouncing
        bouncing -= 1
        ballY += gravity
        if(ballY > baseY-20):
            pygame.mixer.Sound.play(bounce)
            bouncing = 25

        # moving pole
        poleX += -poleX_vel
        if(poleX <-100):
            poleX = width + 10
            poleY = getPoleY(baseY)
        
        # moving base
        baseX += -baseX_vel
        if(baseX <= -width):
            baseX = 0
        
        # collision of basketball 
        gameOver = collision(poleX, poleY, ballX, ballY)
        if(gameOver):
            ScreenText("Game Over",red, 200,100, 60, "Arial",bold =True)
            speed =0     
            bouncing =0
            gravity =0
            baseX_vel =0
            poleX_vel =0
            gameOver = True
            


        # ball into the basket
        if(ballX+basketball.get_width() >= basketX and ballX <= basketX+basket.get_width()
        and ballY > basketY and ballY <= basketY+basket.get_height()):
            pygame.mixer.Sound.play(extras_pointSound)
            basket_score += 100

        # accelerating 
        speed += gameSpeed
        # speeding up score
        score += int(speed)

        # displaying score
        ScreenText(f"Score {score}",black,10, 40, size=20, style="Calibri")
        ScreenText(f"bakset score {basket_score}",black,10, 10, size=20, style="Calibri")


        # checking highest Score
        if(highestScore < score):
            highestScore = score
        with open("highest score.txt","w") as f:
            f.write(str(highestScore))
        
        ScreenText(f"Highest score {highestScore}",red,width-200, 10, size=14, style="Calibri")
        
        pygame.display.update()  
        clock.tick(fps)

        
if __name__ == "__main__":
    main()
