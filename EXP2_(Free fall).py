#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

#import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody, vec2)
import pandas as pd

raw_data=[]

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Experiment 2 (Free fall)')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, -9.81), doSleep=True)

# And a static body to hold the ground shape
ground_body = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(50, 1)),
)
WHITE = (255,255,255)
colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}


def pygame_to_box(pos):
    return vec2(pos[0]/20, SCREEN_HEIGHT/20 - pos[1]/20)

def make_box(pos):
    body_box = world.CreateDynamicBody(position=pygame_to_box(pos))
    box = body_box.CreateCircleFixture(radius=0.5, density=1, friction=0.3)
    # body_box = world.CreateDynamicBody(position=pygame_to_box(pos), angle=0)
    # box = body_box.CreatePolygonFixture(box=(1, 1), density=1, friction=0.3)
    return body_box, box

def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
polygonShape.draw = my_draw_polygon

def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
circleShape.draw = my_draw_circle

def get_positions():
    return [bodies[i][0].position for i in range(len(bodies))]
    
def move_body():
    try:
        if keystate[pygame.K_RIGHT]:
            bodies[-1][0].ApplyLinearImpulse((5,0),bodies[-1][0].position, True)
    
        if keystate[pygame.K_LEFT]:
            bodies[-1][0].ApplyLinearImpulse((-5,0),bodies[-1][0].position,  True) 
    
        if keystate[pygame.K_UP]:
            bodies[-1][0].ApplyLinearImpulse((0,5),bodies[-1][0].position,  True)
    except: IndexError
  

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_analysis_screen():
    
    pygame.init()
    pygame.mixer.init()
    
    screen.fill((0, 0, 0, 0))       
    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
 
    
    draw_text(screen, "Your raw data is:", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5)
    draw_text(screen, "[h (meters), t (seconds)]", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*2)

    draw_text(screen, f"{raw_data[0]}", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*3)
    draw_text(screen, f"{raw_data[1]}", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*4)
    draw_text(screen, f"{raw_data[2]}", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*5)
    draw_text(screen, f"{raw_data[3]}", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*6)
    draw_text(screen, f"{raw_data[4]}", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*7)
    
    draw_text(screen, "Recall that:", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*9)
    draw_text(screen, "h = 0.5 * g * t^2", 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/5 + 35*10)


    pygame.display.flip()
    waiting = True
    while waiting:
        pygame.init()
        pygame.mixer.init()
        clock.tick(TARGET_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                waiting = False
                pygame.quit()
            pygame.init()


bodies = []
running = True
frame=0
record = False
taking_measurements=True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            bodies.append(make_box(pos))
            pos = pygame_to_box(pos)
            if len(bodies) == 1:
                record = True
                frame=0
                raw_data.append([round(world.bodies[-1].position[1]-(1.01+bodies[0][1].shape.radius),2)])
                
    
    # Make list of position of ith box (positions) and distance from click to box (dis_to_box)
    positions = [bodies[i][0].position for i in range(len(bodies)-1)]
    dis_to_box = []
    for i, position in enumerate(positions):
        dis_to_box.append(((pos - position).length, i))
        dis_to_box.sort()
    
    # Move body
    #move_body()

    # Delete clicked box
    try:
        if dis_to_box[0][0] < vec2(1,1).length:
            world.DestroyBody(bodies[dis_to_box[0][1]][0])
            bodies.pop(dis_to_box[0][1]) 
            world.DestroyBody(bodies[-1][0])
            bodies.pop(-1) 
    except: IndexError
    
    # Delete all boxes
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_d]:
        try:            
            world.DestroyBody(bodies[-1][0])
            bodies = bodies[:-1]
        except: NameError, IndexError

    if taking_measurements:
        #Draw the world
        screen.fill((0, 0, 0, 0))
        for body in world.bodies:
            for fixture in body.fixtures:
                fixture.shape.draw(body, fixture)
    
        # Make Box2D simulate the physics of our world for one step.
        world.Step(TIME_STEP, 10, 10)
    
        # Flip the screen and try to keep at the target FPS
        pygame.display.flip()
        clock.tick(TARGET_FPS)
    
    
    frame+=1
    try:
        if world.bodies[-1].position[1]<1.01+bodies[0][1].shape.radius and world.bodies[-1].position[1]!=0.0 and record ==True:
            raw_data[-1].append(round(frame/TARGET_FPS,2))
            record = False
    except: IndexError
    if len(raw_data)==5 and len(raw_data[-1])>1:
        taking_measurements=False
        show_analysis_screen()
        running=False
pygame.quit()
print('Done!')

