import sys
import numpy as np
import pygame
from pygame.locals import *
from collections import deque
import random

pygame.init()


def render():
    # do the rendering
    screen.fill(black)
    # redraw everything here
    for i in range(len(spaces)):
        for j in range(len(spaces[0])):
            if spaces[i, j] == 1:
                pygame.draw.rect(screen, green, pygame.Rect(GRID_STEP*i,
                                                            GRID_STEP*j,
                                                            RWIDTH,
                                                            RWIDTH))
    pygame.draw.rect(screen, red, pygame.Rect(GRID_STEP*apx,
                                              GRID_STEP*apy,
                                              RWIDTH,
                                              RWIDTH))
    pygame.display.flip()


def handle_input(keys: dict):
    global vy, vx
    if keys[K_UP] and vy != 1:
        vy = -1
        vx = 0
    elif keys[K_DOWN] and vy != -1:
        vy = 1
        vx = 0
    elif keys[K_LEFT] and vx != 1:
        vy = 0
        vx = -1
    elif keys[K_RIGHT] and vx != -1:
        vy = 0
        vx = 1


def update_position():
    global hpx, hpy
    global body
    if vx != 0 or vy != 0:
        hpx += vx
        hpy += vy
        spaces[hpx, hpy] = 1
        body.append((hpx, hpy))
        # print(body)
        while len(body) > snake_length:
            spaces[body[0]] = 0
            body.popleft()
            # print(body)


def check_collision():
    global snake_length
    global apx, apy
    global hpx, hpy
    global vx, vy
    # are we colliding with a wall?
    nextx = hpx + vx
    nexty = hpy + vy
    if nextx >= GRID_RESOLUTION or nextx < 0 or \
            nexty >= GRID_RESOLUTION or nexty < 0:
        hpx, hpy = int(GRID_RESOLUTION / 2), int(GRID_RESOLUTION / 2)
        vx, vy = 0, 0
        snake_length = 1
    # are we colliding with ourself?
    for i in range(len(body) - 2):
        if (hpx, hpy) == body[i]:
            # temporary fail measure
            snake_length = 1
    # are we eating an apple?
    if (hpx, hpy) == (apx, apy):
        snake_length += 1
        apx, apy = random.randint(0, GRID_RESOLUTION-1), \
                          random.randint(0, GRID_RESOLUTION-1)


SCREEN_RESOLUTION = 1024
GRID_RESOLUTION = 25
GRID_STEP = int(SCREEN_RESOLUTION / GRID_RESOLUTION)
RWIDTH = GRID_STEP - 1

screen = pygame.display.set_mode((SCREEN_RESOLUTION, SCREEN_RESOLUTION))
spaces = np.zeros((GRID_RESOLUTION, GRID_RESOLUTION))
clock = pygame.time.Clock()

green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
vx, vy = 0, 0
hpx, hpy = int(GRID_RESOLUTION / 2), int(GRID_RESOLUTION / 2)


# initialize the player
body = deque()
body.append((hpx, hpy))
spaces[hpx, hpy] = 1
apx, apy = random.randint(0, GRID_RESOLUTION-1), \
                          random.randint(0, GRID_RESOLUTION-1)
snake_length = 1
running = True
paused = False

while running:
    clock.tick(15)
    one_input = True
    # do main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_p] and paused == False:
        paused = True
    elif keys[K_p]:
        paused = False
    if not paused:
        handle_input(keys)
                # print(vy, vx)
        check_collision()
        update_position()
        render()
