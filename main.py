# Space invaders

import pygame
import random
import math

# Initializing pygame
pygame.init()

# Display
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("Space Invaders")
pygame_icon = pygame.image.load("Resources\\ufo-1.png")
# 32x32 image
pygame.display.set_icon(pygame_icon)

class Bullet:
    def __init__(self, x=0, y=0):
        self.state = "Ready"
        self.x = x
        self.y = y
        self.change = -2
        self.img = pygame.image.load('Resources\\bullet.png')
        #If sprite needs rotating
        #self.rotated = pygame.transform.rotate.(self.img, angle)

    def shoot(self):
        #screen.blit(self.rotated, self.x,self.y)
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
        self.x_change = 0.6
        self.y_change = 40

    def enemy_set(self):
        screen.blit (self.img, (self.x, self.y))

    
    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 0.6
            self.y += self.y_change
        elif self.x >= 1536:
            self.x_change = -0.6
            self.y += self.y_change

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        if distance < 27:
            #CoNTINUE


player = Player(768)
enemy = Enemy(random.randint(0, 1536), random.randint(0, 336))
bullet = Bullet()


running = True
while running:
    screen.fill((0,0,0))

    # loop events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_a]:
                player.change = -1
            if keys[pygame.K_d]:
                player.change = 1
            if keys[pygame.K_SPACE]:
                if bullet.state == "Ready":
                    bullet.x = player.x
                    bullet.y = player.y
                    bullet.state = "Fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.change = 0

    player.move()
    enemy.move()
    bullet.move()
    #show items
    player.player_set()
    enemy.enemy_set()
    if bullet.state == "Fire":
        bullet.shoot()

    pygame.display.flip()