import pygame as pg
import keyManager as km
import painter as painter
import entities as entities
from grid import *
from colors import *
import math

# First init
pg.init()
clock = pg.time.Clock()

# Parameters
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
BLOCK_NBR = 15
FPS = 30
BLOCKSIZE = round(SCREEN_WIDTH/BLOCK_NBR)

screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(BLACK)
timer = clock.tick(FPS)

running = True
# Sprites collector
sprites_collecor = pg.sprite.Group()
player = entities.Player()

# Create Grid
CORE_grid = Grid(71,8)

# Load level 1
CORE_grid.loadLevel("level1")

# frame count
frame = 0



while running:


    # Update level
    if frame % 10 == 0:
        minX,maxX = 0, 10
        mapBlocks = painter.drawMap(pg,CORE_grid.map,[minX,maxX],BLOCKSIZE)

        for block in mapBlocks:
            screen.blit(block.image, (block.rect.x, block.rect.y))
            sprites_collecor.add(block)
    
    # Update player
    screen.blit(player.image, player.rect)

    if frame%100 == 0:
        player.move_right()

    # Draw sprites
    pg.display.update()
    pg.display.flip()

    events = pg.event.get()
    keyAction = km.get(events)

    if keyAction == "exit":
        running = False
        break


    frame += 1

pg.quit()