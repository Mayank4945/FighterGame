import pygame
from fighter3 import Fighter

pygame.init()

#create game window
WIDTH = 1200
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fighter")

#set framerate 
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

#define game variables
intro_timer = 3
last_count_update = pygame.time.get_ticks() 
score = [0,0] #player scores [P1,P2]
round_over = False
ROUND_OVER_TIME = 4000

#define fighter variables
HERO_SIZE = 162
HERO_HEIGHT = 5
HERO_POSITION=[72,69]
HERO_DATA = [HERO_SIZE,HERO_HEIGHT,HERO_POSITION]
VILLAIN_SIZE = 128
VILLAIN_SCALE = 5
VILLAIN_OFFSET=[40,80]
VILLAIN_DATA = [VILLAIN_SIZE,VILLAIN_SCALE,VILLAIN_OFFSET]

#load background image
bg_image = pygame.image.load("background69.jpeg").convert_alpha()

#load spritesheets
hero_sheet = pygame.image.load("sprites\warrior1.png").convert_alpha()
villain_sheet = pygame.image.load("KaalaJaaduwala.png").convert_alpha()

#load victory image
victory_img = pygame.image.load("victory9.png").convert_alpha()

#load defeat image
defeat_img = pygame.image.load("defeat2.png").convert_alpha()

#define number of steps in each animation
HERO_ANIMATION_STEPS = [10,8,1,7,7,3,7]
VILLAIN_ANIMATION_STEPS = [8,8,13,13,17,5,10]

#define font
count_font=pygame.font.Font("Turok.ttf", 80)
score_font=pygame.font.Font("Turok.ttf", 30)

#function for drawing text
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))

#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image,(WIDTH,HEIGHT))
    screen.blit(scaled_bg,(0,0)) 

#function for drawing fighter health bars
def draw_health_bar(health,x,y):
    ratio = health / 100
    pygame.draw.rect(screen,BLACK,(x - 5,y - 5,412,39))
    pygame.draw.rect(screen,RED,(x,y, 400, 30))
    pygame.draw.rect(screen,YELLOW, (x,y,400 * ratio,30))

#create two instances of fighters
fighter_1 = Fighter(1,200, 310,False,HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS)
fighter_2 = Fighter(2,900, 590,True,VILLAIN_DATA, villain_sheet,VILLAIN_ANIMATION_STEPS)



#game loop
run = True
while run:

    clock.tick(FPS)
    #draw background
    draw_bg()

    #show player health
    draw_health_bar(fighter_1.health,20,30)
    draw_health_bar(fighter_2.health,770,30)
    draw_text("P1: " + str(score[0]), score_font, BLACK, 372, 60)
    draw_text("P2: " + str(score[1]), score_font, BLACK, 770, 60)
    draw_text("A:Move Left ",score_font,WHITE,20,80)
    draw_text("D:Move Right",score_font,WHITE,20,100)
    draw_text("Space:Jump",score_font,WHITE,20,120)
    draw_text("Enter:Attack",score_font,WHITE,20,140)
    if intro_timer <= 0:
        #move fighters
        fighter_1.move(WIDTH,HEIGHT,screen,fighter_2,round_over) 
        fighter_2.move(WIDTH,HEIGHT,screen,fighter_1,round_over)
    else:
        #display count timer
        draw_text(str(intro_timer),count_font,WHITE, WIDTH / 2 , HEIGHT / 2)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_timer -= 1
            last_count_update = pygame.time.get_ticks()
            

    

    #update fighters
    fighter_1.update()
    fighter_2.update23()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    
    #check for player defeat
    if round_over ==False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            

        elif fighter_2.alive == False:
            score[0] +=1
            round_over = True
            round_over_time = pygame.time.get_ticks()  
            
    else:
        if fighter_1.alive == True:
            screen.blit(victory_img,(269,135))
        elif fighter_2.alive == True:
            screen.blit(defeat_img,(300,135))
        if pygame.time.get_ticks() - round_over_time> ROUND_OVER_TIME:
            round_over = False
            intro_timer = 3
            fighter_1 = Fighter(1,200, 310,False,HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS)
            fighter_2 = Fighter(2,900, 590,True,VILLAIN_DATA, villain_sheet,VILLAIN_ANIMATION_STEPS)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()


#exit pygam
pygame.quit()