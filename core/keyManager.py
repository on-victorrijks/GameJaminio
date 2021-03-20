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

    for event in events:
        if event.type == KEYDOWN:

            if event.key == K_DOWN:
                action = "go_down"

        elif event.type == QUIT:
            action = "exit"

    return action