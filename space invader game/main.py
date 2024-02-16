import pygame
import random
from pygame import mixer #music module

mixer.init()
pygame.init()


screenwidth=800
screenheight=600
screen = pygame.display.set_mode((screenwidth,screenheight)) #setting display dimensions

pygame.display.set_caption('aircraft shooter game') #setting window title i.e. on top left of display window

icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon) #setting title image icon on top left of display
background = pygame.image.load('space_background.png')

mixer.music.load('synthwave-bg.mp3') #load bg music
mixer.music.play(-1)  #  play bg music


enemyimg=[]
enemyX=[]
enemyY=[]
enemy_speedX=[]
enemy_speedY=[]
enemy_direction=[]

no_of_enemies=6

for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,screenwidth-64))
    enemyY.append(random.randint(20,100))
    enemy_speedX.append(random.randrange(1,3))
    enemy_speedY.append(40)
    enemy_direction.append(1)

spaceshipimg = pygame.image.load('player.png')
spaceshipX = (screenwidth-64)/2
spaceshipY = screenheight-110
spaceship_speed = 4  #spaceship speed using cursor key left and right in pixels/loop cycle

bulletimg = pygame.image.load('bullet.png')
bulletX = spaceshipX + 16
bulletY = spaceshipY 
bullet_speed=7
check_space = False

score = 0
font_score = pygame.font.SysFont('Lucida Fax', 28) #creating a font object
def Score_txt():
    score_img=font_score.render(f'Score: {score}',False,'white')
    screen.blit(score_img, (10,10))

font_gameover = pygame.font.SysFont('Arial', 80, 'bold')
def gameover():
    gameover_img=font_gameover.render('**GAME OVER**',True,'white')
    # mixer.music.load('game-over.mp3')
    # mixer.music.play()
    screen.blit(gameover_img, ((screenwidth/2)-250,(screenheight/2)-80))
    
    



running = True
while running:
    screen.blit(background, (0,0)) #setting img background on display ( image  and coordinates are specified)

    for event in pygame.event.get():       #setting up the exit button using QUIT event
        if event.type==pygame.QUIT:
            running=False         

    # screen.blit(str(score), (10,10))         
    
    if event.type==pygame.KEYDOWN: #when any key is pressed...

        #moving spaceship with left and right cursor keys
        # print('any key pressed')
        if event.key==pygame.K_LEFT:
            spaceshipX -= spaceship_speed
        if event.key==pygame.K_RIGHT:
            spaceshipX += spaceship_speed
        if event.key == pygame.K_LCTRL:
            if check_space == False:
                bullet_sound=mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = spaceshipX + 16 
                check_space=True
                


            
    ##stopping spaceship from going outside the window
    #when it goes out of bound, it comes back of another side
    if spaceshipX<=-64:
        spaceshipX=screenwidth
    if spaceshipX>screenwidth:
        spaceshipX=0            
            ### OR ###
    # #setting movement max and min
    # if spaceshipX<=0:
    #     spaceshipX=0
    # if spaceshipX>=736:
    #     spaceshipX=736
    
    #setting enemy movement
    for i in range(no_of_enemies):
        if enemyX[i]<=0:
            enemy_direction[i] = 1
            enemyY[i] += enemy_speedY[i]
        elif enemyX[i]>=(screenwidth-64):
            enemy_direction[i] = -1
            enemyY[i] += enemy_speedY[i]

        enemyX[i] += enemy_direction[i]*enemy_speedX[i]
        
        # collision
        if bulletX>=enemyX[i]-10 and (((bulletX-enemyX[i])**2)+((bulletY-enemyY[i])**2))**0.5<=40:
            collision_sound=mixer.Sound('collision.mp3')
            collision_sound.play()
            bulletY=spaceshipY
            check_space=False
            enemyX[i] = random.randint(0,screenwidth-64)
            enemyY[i] = random.randint(20,100)
            score+=1
        
        # player hit by enemy
        if enemyY[i] >= spaceshipY-63:
            for j in range(no_of_enemies):
                enemyY[j]=5000  #disappearing alien when reaches spaceship level
            gameover()
            break
        
        screen.blit(enemyimg[i], (enemyX[i],enemyY[i])) #displaying enemy image

        


    if bulletY==0:
        bulletY=spaceshipY
        check_space=False
        

    if check_space :
        bulletY-=bullet_speed
        screen.blit(bulletimg, (bulletX, bulletY)) 
        
        
    Score_txt()
    screen.blit(spaceshipimg, (spaceshipX,spaceshipY)) #displaying player image

    pygame.display.update()  #updates changes in display after every loop cycle


