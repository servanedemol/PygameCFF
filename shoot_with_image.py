import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Click the Target")

APPLE_IMAGE = pygame.image.load(os.path.join('assets','apple.png'))

score = 0
white = (255,255,255)

'''def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((9*screen_width/10),(screen_height/10))
    screen.blit(TextSurf, TextRect)
  '''

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf = largeText.render(text, True, white)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((9*screen_width/10),(screen_height/10))
    screen.blit(TextSurf, TextRect)

# Target properties
class Target:
    def __init__(self):
        self.color = (255, 0, 0)
        self.radius = 25
        self.x_pos = screen_width // 2
        self.y_pos = screen_height // 2
        self.type = 0
    
    def __init__(self, image):
        #self.color = (255, 0, 0)
        self.img= pygame.transform.scale(image, (25,25))
        self.radius = 25
        self.x_pos = screen_width // 2
        self.y_pos = screen_height // 2
        self.type = 1

    def draw(self):
        if (self.type==0):
            pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)
        elif (self.type==1):
            screen.blit(self.img,(self.x_pos,self.y_pos))


# Game loop
running = True
shoot_target=Target(APPLE_IMAGE)
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (mouse_x - shoot_target.x_pos)**2 + (mouse_y - shoot_target.y_pos)**2 <= shoot_target.radius**2:
                # Target hit!
                print("Hit!")
                shoot_target.x_pos = random.randint(30,750)
                shoot_target.y_pos = random.randint(30,550)
                #shoot_target.radius = random.randint(5,45)
                score+=1
                print("Score:" + str(score))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw target
    # pygame.draw.circle(screen, shoot_target.color, (shoot_target.x_pos, shoot_target.y_pos), shoot_target.radius)
    shoot_target.draw()

    # Draw the score
    message_display("Score:" + str(score))

    # Update display
    pygame.display.flip()


# Quit Pygame
pygame.quit()