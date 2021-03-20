import pygame as pg
import keyManager as km
import painter as painter
import entities as entities
from grid import *
from colors import *
import math
import time
import random 
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
pg.display.set_caption('El famoso Trump')


# Level 1 - Loading
"""
intro_level1 = pg.transform.scale(pg.image.load("../assets/intro_level1.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)) 
brighten = 255/30
screen.blit(intro_level1, (0,0))
pg.display.update()
time.sleep(1)
for i in range(30):
    intro_level1.fill((brighten, brighten, brighten), special_flags=pg.BLEND_RGB_ADD)
    screen.blit(intro_level1, (0,0))
    pg.display.update()
    time.sleep(0.2/30)
"""

running = True
# Sprites collector
sprites_collecor = pg.sprite.Group()
player = entities.Player(screen)
updateMap = True

# Create Grid
CORE_grid = Grid(71,8)

# Load level 1
CORE_grid.loadLevel("level1")

# frame count
frame = 0

# bullets
bullets_collector = []


while running:

    sprites_collecor.empty()

    # Update level
    if updateMap:
        playerBlockX = int(player.posX//BLOCKSIZE)
        playerBlockY = player.rect.y//BLOCKSIZE
        player.playerBlock = playerBlockX
        player.playerH = playerBlockY
        minBlockIndex = playerBlockX-15
        if minBlockIndex < 0:
            minBlockIndex = 0
        minX,maxX = minBlockIndex, playerBlockX+15
        minX_aroundPlayer,maxX_aroundPlayer = playerBlockX-15, playerBlockX+15
        mapBlocks = painter.drawMap(pg,CORE_grid.map,[minX,maxX],BLOCKSIZE,player)

        for block in mapBlocks:
            screen.blit(block.image, (block.rect.x, block.rect.y))
            sprites_collecor.add(block)
        
        updateMap = False
    

    # verif direction of acceleration
    if player.accX != 0:
        if frame%10 == 0:
            if player.image == player.moving1:
                player.image = player.moving2
            else:
                player.image = player.moving1
    else:
        player.image = player.still

    if player.accX < 0:
        dirPlayer = -1
        screen.blit(pg.transform.flip(player.image, True, False), player.rect)
    else:
        dirPlayer = 1
        screen.blit(player.image, player.rect)

    # Update player
    events = pg.event.get()
    keyAction = km.get(events)

    updateMap = True
    if keyAction == "exit":
        running = False
        break
    elif keyAction == "onetap_go_up":
        player.accelerateY(-1,mapBlocks,[minX_aroundPlayer,maxX_aroundPlayer],BLOCKSIZE)
    elif keyAction == "go_left":
        player.accelerateX(-0.2)
    elif keyAction == "go_right":
        player.accelerateX(0.2)
    elif keyAction == "go_projectile":
        newBullet = entities.Bullet(player.rect.x,player.rect.y + (random.randint(0,6)-3),BLOCKSIZE,dirPlayer)
        bullets_collector.append(newBullet)
    else:
        if len(bullets_collector) == 0:
            updateMap = False
    
    # Player update
    playerUpdated = player.update(mapBlocks,[minX_aroundPlayer,maxX_aroundPlayer],BLOCKSIZE)
    if playerUpdated[0] != playerUpdated[1]:
        updateMap = True

    # Bullets update
    for bullet in bullets_collector:
        shouldLive = bullet.update(mapBlocks)
        if not shouldLive:
            bullets_collector.remove(bullet)
        screen.blit(bullet.image, bullet.rect)


    # show fps
    fps = str(len(bullets_collector))
    font = pg.font.SysFont("Arial", 18)
    fps_text = font.render(fps, 1, pg.Color("red"))
    screen.blit(fps_text, (10,0))
  

    # Draw sprites
    pg.display.update()
    pg.display.flip()



    frame += 1

pg.quit()