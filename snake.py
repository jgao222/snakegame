import sys
import numpy as np
import pygame
from pygame import display
from pygame.locals import *
from collections import deque
import random

# init and opttions
pygame.init()
pygame.key.set_repeat()

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


def handle_input(key: int):
    global input_buffer
    global vy, vx
    global paused
    if key == K_p:
        paused = not paused
        return

    # keys = first_two_keys(keys)
    # if len(input_buffer):
    #     keys = input_buffer.append(keys)
    # print(keys)
    if len(input_buffer) < 2:
        input_buffer.append(key)

def execute_input_buffer():
    global vx, vy
    if len(input_buffer):
        if input_buffer[0] == K_UP and vy != 1:
            vx, vy = INPUT_DIRECTIONS["UP"]
        elif input_buffer[0] == K_DOWN and vy != -1:
            vx, vy = INPUT_DIRECTIONS["DOWN"]
        elif input_buffer[0] == K_LEFT and vx != 1:
            vx, vy = INPUT_DIRECTIONS["LEFT"]
        elif input_buffer[0] == K_RIGHT and vx != -1:
            vx, vy = INPUT_DIRECTIONS["RIGHT"]
        input_buffer.pop(0)


def update_position():
    global hpx, hpy
    global body
    if vx != 0 or vy != 0:
        hpx += vx
        hpy += vy
        spaces[hpx, hpy] = 1
        body.append((hpx, hpy))
        while len(body) > snake_length:
            spaces[body[0]] = 0
            body.popleft()


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
        trigger_game_over()
    # are we colliding with ourself?
    for i in range(len(body) - 1):
        if (hpx, hpy) == body[i]:
            # temporary fail measure
            trigger_game_over()
    # are we eating an apple?
    if (hpx, hpy) == (apx, apy):
        snake_length += 1
        apx, apy = random.randint(0, GRID_RESOLUTION-1), \
                          random.randint(0, GRID_RESOLUTION-1)
        update_score()


def trigger_game_over():
    global hpx, hpy
    global vx, vy
    global snake_length
    hpx, hpy = int(GRID_RESOLUTION / 2), int(GRID_RESOLUTION / 2)
    vx, vy = 0, 0
    snake_length = 1
    update_score()

def update_score():
    pygame.display.set_caption("snakegame | SCORE: " + str(snake_length - 1))


# def first_two_keys(keys: list):
#     out = []
#     for i in range(len(keys)):
#         if keys[i]:
#             out.append(i)
#         if len(out) == 2:
#             break
#     return out


# overall game stuff
UNIT_PIXELS = 30
GRID_RESOLUTION = 25
SCREEN_RESOLUTION = GRID_RESOLUTION * UNIT_PIXELS
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
update_score() # init the score, which is based on length
running = True
paused = False

# input stuff
input_buffer = []
INPUT_DIRECTIONS = {"UP": (0, -1), "DOWN": (0, 1),
                    "LEFT": (-1, 0), "RIGHT": (1, 0)}

while running:
    clock.tick(15)
    one_input = True
    # do main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # checking if pause the game
            print("handling input")
            handle_input(event.key)

    if not paused:
        # print(vy, vx)
        execute_input_buffer()
        check_collision()
        update_position()
        render()
