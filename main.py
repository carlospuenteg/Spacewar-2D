import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

import sys

################################################
#-----DISPLAY-----
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#-----CAPTION-----
pygame.display.set_caption("SPACEWAR 2D")

#-----COLORS-----
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#-----BORDER-----
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

#-----FONTS-----
HEALTH_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 100)

#-----CONSTANTS-----
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

#-----HIT EVENTS-----
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#-----SOUNDS-----
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.mp3'))

#-----SPRITES-----
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

#-----BACKGROUND-----
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

################################################

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #-----DRAW BACKGROUND-----
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    #-----HEALTH TEXT-----
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    #-----DRAW SPACESHIP-----
    WIN.blit(YELLOW_SPACESHIP , (yellow.x, yellow.y))  # Draw a surface . Coords are taken from top left
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    #-----DRAW THE BULLETS-----
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    #-----UPDATE THE DISPLAY-----
    pygame.display.update()

################################################
#-----MOVEMENT OF YELLOW(left) SPACESHIP-----
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.height < BORDER.x: # RIGHT - height because image is rotated
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # LEFT
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < HEIGHT: # LEFT - width because image is rotated
        yellow.y += VEL

#-----MOVEMENT OF RED(right) SPACESHIP-----
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.height < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # LEFT
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT: # LEFT
        red.y += VEL

################################################

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    #-----HANDLE YELLOW BULLETS-----
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    #-----HANDLE RED BULLETS-----
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

################################################

#-----DRAW THE WINNER ON THE DISPLAY-----
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)  # If I put 5000, my computer lags

################################################

#-----MAIN GAME FUNCTION-----
def main():
    # Draw a rectangle for each spaceship
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # Create a list for the bullets
    red_bullets = []
    yellow_bullets = []

    # Store the health of each player/spaceship
    red_health = 10
    yellow_health = 10

    # Clock for the FPS
    clock = pygame.time.Clock()
    
    # Game loop
    run = True
    while run:
        # Refresh at the FPS framerate
        clock.tick(FPS)

        # For each event do:
        for event in pygame.event.get():
            # If the event is 'QUIT', quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)  # Proper way to exit so there are no 'video system not initialized' errors
            
            # If the event is a KEYDOWN
            if event.type == pygame.KEYDOWN:
                # If the key is 'LALT' and there are bullets <= MAX_BULLETS on the screen
                if event.key == pygame.K_LALT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect( # Create a bullet and append it to the yellow_bullets list
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play() # Play the fire sound

                # If the key is 'RALT' and there are bullets <= MAX_BULLETS on the screen
                if event.key == pygame.K_RALT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect( # Create a bullet and append it to the red_bullets list
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play() # Play the fire sound

            # If the event is RED_HIT (the red spaceship was hit):
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play() # Play the bullet hit sound

            # If the event is YELLOW_HIT (the yellow spaceship was hit):
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play() # Play the bullet hit sound

        # Display the winner
        if red_health <= 0 and yellow_health <= 0:
            draw_winner("Tie!") # TIE
        elif red_health <= 0:
            draw_winner("Yellow Wins!") # RED WON
            break
        elif yellow_health <= 0:
            draw_winner("Red Wins!") # YELLOW WON
            break

        # Get the pressed keys
        keys_pressed = pygame.key.get_pressed()
        # Handle the pressed keys
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # Handle the bullets
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Display the game
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # If the while loop breaks, the main() function gets called so the game starts again
    main()

################################################

# We're only going to run the main() function if we run this file directly, not if the file is imported from somewhere else
if __name__ == "__main__": 
    main()