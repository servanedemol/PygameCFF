import pygame
import os
pygame.font.init() #initializes the pygame font library
pygame.mixer.init() #initializes the pygame sound effect library

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans',30)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

pygame.display.set_caption("Spy Game")

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),
    90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIDTH,HEIGHT))

BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Assets_Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Assets_Grenade+1.mp3')

def draw_window(y,r, y_bullets, r_bullets, yellow_score, red_score):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK, BORDER)

    # display the scores
    red_health_text = HEALTH_FONT.render("Health: "+ str(red_score),1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_score),1, WHITE)

    WIN.blit (red_health_text, (WIDTH - red_health_text.get_width()-10 , 10))
    WIN.blit (yellow_health_text, (10 , 10))
    
    #blit is to draw surfaces on the screen
    WIN.blit(YELLOW_SPACESHIP,(y.x,y.y))
    WIN.blit(RED_SPACESHIP,(r.x,r.y))
   

    for bullet in y_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    for bullet in r_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    pygame.display.update()

def yellow_handle_movements(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        #move the yellow ship to the left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width - VEL < BORDER.x: # RIGHT
        #move the yellow ship to the right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        #move the yellow ship up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y+ yellow.height+ VEL < HEIGHT-15: # DOWN
        #move the yellow ship down
        yellow.y += VEL

def red_handle_movements(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x: # LEFT
        #move the red ship to the left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x - VEL + red.width < WIDTH : # RIGHT
        #move the red ship to the right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0 : # UP
        #move the yellow ship up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT-15 : # DOWN
        #move the yellow ship down
        red.y += VEL

# draw all the bullets and check collisions
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        # check if the bullet hits the red ship
        if red.colliderect(bullet):
            #post an event
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        # check if the bullets is out of the window
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            #post an event
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        # check if the bullets is out of the window
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    

# define a main a function for all the code that takes care of the main game loop to redraw the window and check collisions
def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    #health variables for the ships
    red_health=10
    yellow_health = 10
    
    #create a list of all the bullets
    yellow_bullets = []
    red_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        #check for all the events that can occur
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v and len(yellow_bullets)<MAX_BULLETS:
                    #create a new bullet for the yellow ship
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2 - 2, 10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_SLASH and len(red_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(red.x-5,red.y+red.height//2 - 2, 10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()  

            if event.type == RED_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()

            winner_text=""
                   
            if yellow_health<=0:
                winner_text="Red Wins!"

            if red_health<=0:
                winner_text="Yellow Wins!"

            if winner_text!="":
                draw_winner(winner_text)
                run=False

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movements(keys_pressed,yellow)
        red_handle_movements(keys_pressed,red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red) 
        

        #yellow.x += 1 
        draw_window(yellow,red, yellow_bullets, red_bullets, yellow_health, red_health)
    main()

if __name__ == "__main__":
    main()