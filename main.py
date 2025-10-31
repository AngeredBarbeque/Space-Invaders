# Space invaders

import pygame
import random

# Initializing pygame
pygame.init()

# Display
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("Space Invaders")
pygame_icon = pygame.image.load("Resources\\ufo-1.png")
# 32x32 image
pygame.display.set_icon(pygame_icon)

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
        

player = Player(768)

running = True
while running:
    screen.fill((0,0,0))

    # loop events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -0.6
            if keys[pygame.K_RIGHT]:
                player.change = 0.6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0

    player.move()
    #show items
    player.player_set()

    pygame.display.flip()