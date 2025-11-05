# Space invaders

import pygame
import random
import math
from pygame import mixer

# Initializing pygame
pygame.init()

# set up background 
background = pygame.image.load("Resources\\Background-1.jpg")
scaled_background = pygame.transform.scale(background, (1600,1200))


#background music
mixer.music.load("Resources\\background.wav")
mixer.music.play(-1)

#score text
score_font = pygame.font.Font('Resources\\Sixtyfour-Regular-VariableFont_BLED,SCAN.ttf', 64)

# Display
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("Bean Goblin")
pygame_icon = pygame.image.load("Resources\\bullet.png")
# 32x32 image
pygame.display.set_icon(pygame_icon)

class Button():
    def __init__(self,x,y,img,scale):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width()*scale),int(self.img.get_height()*scale)))
        self.rect = self.img.get_rect()
        self.scale = scale

    def draw(self):
        pos = pygame.mouse.get_pos()
        print(pos)
        if self.rect.collidepoint(pos):
            print("Hover")
        screen.blit(self.img, (self.x, self.y))

        

class Bullet:
    def __init__(self, x=0, y=0):
        self.state = "Ready"
        self.x = x
        self.y = y
        self.change = -4
        self.img = pygame.image.load('Resources\\bullet.png')
        #If sprite needs rotating
        #self.rotated = pygame.transform.rotate.(self.img, angle)

    def shoot(self):
        #screen.blit(self.rotated, self.x,self.y)
        self.change = -4
        screen.blit(self.img, (self.x,self.y))

    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.state = "Ready"



class Player:
    def __init__(self, x, change=0):
        self.img = pygame.image.load("Resources\\spaceship.png")
        self.x = x
        self.y = 1200-64
        self.change = change
        self.score = 0
        

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 1536:
            self.x = 1536


class Enemy:
    def __init__(self,x,y):
        self.img = pygame.image.load('Resources\\alien.png')
        self.x = x
        self.y = y
        self.x_change = 6
        self.y_change = 800

    def enemy_set(self):
        screen.blit (self.img, (self.x, self.y))

    
    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 6
            self.y += self.y_change
        elif self.x >= 1536:
            self.x_change = -6
            self.y += self.y_change

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        if distance < 48:
            return True
        return False
    
    def lose(self):
        if self.y > 1136:
            return True
        return False

enemies = []
player = Player(768)
for i in range(6):
    x = random.randint(0, 1536)
    y = random.randint(0, 336)
    enemies.append(Enemy(x,y))
bullet = Bullet()

lost = False
running = True
aliens = 7
while running:
    screen.fill((0,0,0))
    screen.blit(scaled_background, (0,0))
    score_display = score_font.render(f'Round: {aliens-6} | Beaned: {player.score}', True, (255,50,255))
    screen.blit(score_display, (20,20))
    # loop events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_a]:
                player.change = -2
            if keys[pygame.K_d]:
                player.change = 2
            if keys[pygame.K_SPACE]:
                if bullet.state == "Ready":
                    bullet.x = player.x
                    bullet.y = player.y
                    bullet.state = "Fire"
                    mixer.Sound('Resources\\laser.wav').play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.change = 0

    
    player.move()
    for enemy in enemies:
        enemy.move()
        if enemy.lose():
            enemies = []

            lost = True
            
    if lost:
        end_font = pygame.font.Font('Resources\\Times New Roman Regular.ttf', 128)
        end_display = end_font.render(f'GAME OVER', True, (255,30,30))
        mixer.Sound('Resources\\death.mp3').play()
        screen.blit(end_display,(400,500))
        button = Button(650, 650, 'Resources\\button.png', 0.2)
        button.draw()

    else:
        bullet.move()
        for i, enemy in enumerate(enemies):
            if enemy.is_hit(bullet):
                bullet.state = "Ready"
                if random.random() >= 0.90:
                    mixer.Sound('resources\\background.wav').play()
                else:
                    mixer.Sound('Resources\\explosion.wav').play()
                enemies.pop(i)
                bullet.x = player.x
                bullet.y = player.y
                bullet.change = 0
                if enemies == []:
                    for i in range(aliens):
                        x = random.randint(0, 1536)
                        y = random.randint(0, 336)
                        enemies.append(Enemy(x,y))
                    aliens = round(aliens * 1.5)
                player.score += 1
        #show items
        player.player_set()
        for enemy in enemies:
            enemy.enemy_set()
        if bullet.state == "Fire":
            bullet.shoot()
    pygame.display.flip()