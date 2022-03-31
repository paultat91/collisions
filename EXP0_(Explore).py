#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

#import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody, vec2)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Experiment 0 (Explore)')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, 0), doSleep=True)

# And a static body to hold the ground shape
ground_body = world.CreateStaticBody(
    position=(0, 0),
    shapes=polygonShape(box=(50, 1)),
)

colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}

def pygame_to_box(pos):
    return vec2(pos[0]/20, SCREEN_HEIGHT/20 - pos[1]/20)

def make_box(pos):
    body_box = world.CreateDynamicBody(position=pygame_to_box(pos), angle=0)
    box = body_box.CreatePolygonFixture(box=(1, 1), density=1, friction=0.3)
    return body_box, box

def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
polygonShape.draw = my_draw_polygon

def get_positions():
    return [bodies[i][0].position for i in range(len(bodies))]
    
def move_body():
    try:
        if keystate[pygame.K_RIGHT]:
            bodies[-1][0].ApplyLinearImpulse((5,0),bodies[-1][0].position, True)
    
        if keystate[pygame.K_LEFT]:
            bodies[-1][0].ApplyLinearImpulse((-5,0),bodies[-1][0].position,  True) 
    
        if keystate[pygame.K_UP]:
            bodies[-1][0].ApplyLinearImpulse((0,3),bodies[-1][0].position,  True)
        
        if keystate[pygame.K_DOWN]:
            bodies[-1][0].ApplyLinearImpulse((0,-5),bodies[-1][0].position,  True)
            
        if keystate[pygame.K_d]:
            bodies[-1][0].ApplyAngularImpulse(-5, True)
                
        if keystate[pygame.K_a]:
            bodies[-1][0].ApplyAngularImpulse(5, True)

        if keystate_prev[pygame.K_g] and not keystate[pygame.K_g]:  
            
            if world.gravity.length>0:
                world.gravity = vec2(0,0)
             
            else:
                world.gravity = vec2(0,-9.81)
                for i in range(len(bodies)):
                    bodies[i][0].ApplyLinearImpulse((0,-1e-200),bodies[-1][0].position,  True)

    except: IndexError
  

bodies = []
running = True
while running:
    keystate_prev = pygame.key.get_pressed()
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            bodies.append(make_box(pos))
            pos = pygame_to_box(pos)
    
    # Make list of position of ith box (positions) and distance from click to box (dis_to_box)
    positions = [bodies[i][0].position for i in range(len(bodies)-1)]
    dis_to_box = []
    for i, position in enumerate(positions):
        dis_to_box.append(((pos - position).length, i))
        dis_to_box.sort()
    


    # Delete clicked box
    try:
        if dis_to_box[0][0] < vec2(1,1).length:
            world.DestroyBody(bodies[dis_to_box[0][1]][0])
            bodies.pop(dis_to_box[0][1]) 
            world.DestroyBody(bodies[-1][0])
            bodies.pop(-1) 
            pos = vec2(-1,-1)
    except: IndexError
    
    # Delete all boxes
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_SPACE]:
        try:            
            world.DestroyBody(bodies[-1][0])
            bodies = bodies[:-1]
        except: NameError, IndexError
    
    # Move body
    move_body()
    if keystate_prev[pygame.K_g] and not keystate[pygame.K_g]:
        pos = vec2(-1,-1)
        
    # Draw the world
    screen.fill((0, 0, 0, 0))
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)

    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')