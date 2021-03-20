import pygame as pg
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

def get(events,context=None):
    action = None

    pressed_key= pg.key.get_pressed()
    if pressed_key[K_DOWN] == 1:
        action = "go_down"
    elif pressed_key[K_LEFT] == 1:
        action = "go_left"
    elif pressed_key[K_RIGHT] == 1:
        action = "go_right"

    for event in events:

        if event.type == KEYDOWN:

            if event.key == K_UP:
                action = "onetap_go_up"
            elif event.key == K_DOWN:
                action = "go_down"
            elif event.key == K_LEFT:
                action = "go_left"
            elif event.key == K_RIGHT:
                action = "go_right"

        elif event.type == QUIT:
            action = "exit"


    return action