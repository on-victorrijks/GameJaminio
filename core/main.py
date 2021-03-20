import pygame as pg
import keyManager as km

# First init
pg.init()
clock = pg.time.Clock()

# Parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
timer = clock.tick(FPS)

running = True
while running:

    events = pg.event.get()
    keyAction = km.get(events)

    if keyAction == "exit":
        running = False
        break

    screen.fill((255, 255, 255))
    pg.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    pg.display.flip()

pg.quit()