#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:23:57 2020

@author: paul
"""

import pygame

WIDTH = 1000
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

PLAYER_ACC = 1
PLAYER_FRICTION = -.1
AIR_RESISTANCE = -.01
g = 9.81

vec = pygame.math.Vector2
class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.Surface((0, 0))
        self.image.fill(WHITE)
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.mass = 1
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
             
    def update(self):
        self.acc = vec(0, g/FPS)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_s]:
            # create a plain rectangle for the sprite image
            self.image = pygame.Surface((10, 10))
            self.image.fill(GREEN)
            # find the rectangle that encloses the image
            self.rect = self.image.get_rect()
            # center the sprite on the screen
            self.mass = 1
            self.pos = vec(WIDTH / 3, HEIGHT / 3)
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            
        if keystate[pygame.K_z] and self.pos.y==HEIGHT:
            self.pos.x += -10*PLAYER_ACC
        if keystate[pygame.K_c] and self.pos.y==HEIGHT:
            self.pos.x += 10*PLAYER_ACC  
            
        if keystate[pygame.K_a] and self.pos.y==HEIGHT:
            self.acc.x += -PLAYER_ACC
        if keystate[pygame.K_d] and self.pos.y==HEIGHT:
            self.acc.x += PLAYER_ACC      
        if (keystate[pygame.K_w]) and self.pos.y==HEIGHT:
            self.vel.y = -g   
        if keystate[pygame.K_e] and self.pos.y==HEIGHT:
            self.vel = vec(g,-g)
        if keystate[pygame.K_q] and self.pos.y==HEIGHT:
            self.vel = vec(-g,-g)
            
        if self.pos.y==HEIGHT:  
            self.acc.x += self.vel.x * (PLAYER_FRICTION)
        else:
            self.acc.x += self.vel.x * (AIR_RESISTANCE)
        self.vel += self.acc      
        self.pos += self.vel + .5 * self.acc   
 
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.vel.y = 0

        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.x > WIDTH:
            self.pos.x = 0

        self.rect.midbottom = self.pos
        
        #if keystate[pygame.K_SPACE]:
         #   self.remove_internal()

class Player2(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.Surface((0, 0))
        self.image.fill(BLACK)
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.mass = 100
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def update(self):
        self.acc = vec(0, g/FPS)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_DOWN]:
            # create a plain rectangle for the sprite image
            self.image = pygame.Surface((100, 100))
            self.image.fill(GREEN)
            # find the rectangle that encloses the image
            self.rect = self.image.get_rect()
            # center the sprite on the screen
            self.mass = 100
            self.pos = vec(2*WIDTH / 3, HEIGHT / 3)
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            
        if keystate[pygame.K_LEFT] and self.pos.y==HEIGHT:
            self.acc.x += -PLAYER_ACC
        if keystate[pygame.K_RIGHT] and self.pos.y==HEIGHT:
            self.acc.x += PLAYER_ACC  
        if (keystate[pygame.K_UP]) and self.pos.y==HEIGHT:
            self.vel.y = -g   
          
        if self.pos.y==HEIGHT:  
            self.acc.x += self.vel.x * (PLAYER_FRICTION)
        else:
            self.acc.x += self.vel.x * (AIR_RESISTANCE)
        self.vel += self.acc      
        self.pos += self.vel + .5 * self.acc   
 
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.vel.y = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.x > WIDTH:
            self.pos.x = 0

                
        self.rect.midbottom = self.pos
        
        # if keystate[pygame.K_SPACE]:
        #     self.image.fill(BLACK)
        #     self.remove()
            
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PHYSICS 1 WORLD")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
player2 = Player2()
all_sprites.add(player)
all_sprites.add(player2)
# Game loop
running = True
t_start = pygame.time.get_ticks()
collision_count = 0
keystate = pygame.key.get_pressed()
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    
    if pygame.sprite.collide_rect(player, player2):
        collision_count += 1
        p = player.vel
        player.vel = ((player.mass - player2.mass)/(player.mass + player2.mass))*player.vel + (2*player2.mass/(player.mass + player2.mass))*player2.vel
        player2.vel = ((player2.mass - player.mass)/(player.mass + player2.mass))*player2.vel + (2*player.mass/(player.mass + player2.mass))*p
    if keystate[pygame.K_SPACE]:
        player.remove()
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
