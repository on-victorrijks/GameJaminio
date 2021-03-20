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
updateMap = True

# Create Grid
CORE_grid = Grid(71,8)

# Load level 1
CORE_grid.loadLevel("level1")

# frame count
frame = 0




while running:

    sprites_collecor.empty()

    # Update level
    if updateMap:
        playerBlockX = player.rect.x//BLOCKSIZE
        minBlockIndex = playerBlockX-5
        if minBlockIndex < 0:
            minBlockIndex = 0
        minX,maxX = minBlockIndex, playerBlockX+5
        minX_aroundPlayer,maxX_aroundPlayer = playerBlockX-2, playerBlockX+2
        mapBlocks = painter.drawMap(pg,CORE_grid.map,[minX,maxX],BLOCKSIZE)

        for block in mapBlocks:
            screen.blit(block.image, (block.rect.x, block.rect.y))
            sprites_collecor.add(block)
        
        updateMap = False
    
    # Update player
    events = pg.event.get()
    keyAction = km.get(events)

    updateMap = True
    if keyAction == "exit":
        running = False
        break
    elif keyAction == "onetap_go_up":
        player.accelerateY(-0.7,mapBlocks,[minX_aroundPlayer,maxX_aroundPlayer])
    elif keyAction == "go_left":
        player.accelerateX(-0.1)
    elif keyAction == "go_right":
        player.accelerateX(0.1)
    else:
        updateMap = False
    
    playerUpdated = player.update(mapBlocks,[minX_aroundPlayer,maxX_aroundPlayer])
    if playerUpdated[0] != playerUpdated[1]:
        updateMap = True

    screen.blit(player.image, player.rect)

    

    # Draw sprites
    pg.display.update()
    pg.display.flip()



    frame += 1

pg.quit()