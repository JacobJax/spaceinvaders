import pygame
from pygame import mixer
import random
import math

# initialize game
pygame.init()

# set the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')
# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# change icon and name
pygame.display.set_caption('space invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# create player
player_img = pygame.image.load('spaceship (1).png')
playerX = 370
playerY = 480
playerX_change = 0

# create enemies
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(1, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(0.3)

# create bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = -8
bullet_state = 'ready'


def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collided(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    return distance < 27

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 40)
textX = 15
textY = 15

game_over_font = pygame.font.Font('freesansbold.ttf', 70)
def game_over_text():
    over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.3
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0


    playerX += playerX_change

    # player border system
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # handle enemies
    for i in range(number_of_enemies):

        # game over
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        enemyY[i] +=enemyY_change[i]

        # enemy border system
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3

        # collision system
        collided = is_collided(enemyX[i], bulletX, enemyY[i], bulletY)
        if collided:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

            bulletY = 480
            bullet_state = 'ready'
            score_value += 1

            enemyX[i] = random.randint(1, 730)
            enemyY[i] = random.randint(50, 150)

        draw_enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change


    draw_player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()