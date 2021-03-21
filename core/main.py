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

# Image loading
healthBarOutliner = pg.transform.scale(pg.image.load("../assets/healthbar.png"), (480, 120)) 
manaBarOutliner = pg.transform.scale(pg.image.load("../assets/mana.png"), (380, 105)) 
slowDownOverlay = pg.transform.scale(pg.image.load("../assets/slowDownOverlay.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)) 
ammo_imgs = {
    0: pg.image.load("../assets/ammo_0.png"),
    1: pg.image.load("../assets/ammo_1.png"),
    2: pg.image.load("../assets/ammo_2.png"),
    3: pg.image.load("../assets/ammo_3.png"),
    4: pg.image.load("../assets/ammo_4.png"),
    5: pg.image.load("../assets/ammo_5.png"),
}
pause_menu = pg.image.load("../assets/pause_menu.png")

# Create Grid
CORE_grid = Grid(117,8)

# HealthBar color
def getHealthBarColor(hW):
    if hW < 0.2:
        return (255,0,0)
    elif 0.2 <= hW < 0.4:
        return (200,55,55)
    elif 0.4 <= hW < 0.6:
        return (150,100,100)
    elif 0.6 <= hW < 0.8:
        return (100,180,100)
    elif 0.8 <= hW:
        return (0,255,0)


SOUND_gunshot = pg.mixer.Sound('../assets/music/gunshot.mp3')
SOUND_bulletTime_in = pg.mixer.Sound('../assets/music/bullettime_in.mp3')
SOUND_bulletTime_out = pg.mixer.Sound('../assets/music/bullettime_out.mp3')
pg.mixer.music.set_volume(0.1)


# Main func.

def run_level(LEVELNAME):

    # Map
    CORE_grid.loadLevel(LEVELNAME)
    # frame count
    frame = 0
    # Bullets
    bullets_collector = []
    ennemies_collector = []
    missiles_collector = []
    bullet_time_regen_coeff = 1

    if LEVELNAME == "level1":
        # Sounds
        pg.mixer.music.load('../assets/music/level1.mp3')
        pg.mixer.music.play(-1)
        # Ennemies
        ennemies_collector.append(entities.Ennemy(100, 40, 2, 1, BLOCKSIZE*5, 380, [-80,80]))
        ennemies_collector.append(entities.Ennemy(100, 40, 2, 2, BLOCKSIZE*14, 620, [-100,100]))
        ennemies_collector.append(entities.Ennemy(100, 40, 2, 2, 2050, 380, [-100,100]))
        ennemies_collector.append(entities.Ennemy(200, 40, 2, 2, 4150, 260, [-100,100]))
        ennemies_collector.append(entities.Ennemy(200, 40, 2, 1, 6800, 380, [-100,100]))
        ennemies_collector.append(entities.Ennemy(200, 50, 2, 1, 7450, 625, [-100,100]))
        ennemies_collector.append(entities.Ennemy(200, 50, 2, 1, 8350, 260, [-100,100]))
        ennemies_collector.append(entities.Ennemy(300, 50, 2, 2, 9050, 505, [-100,100]))
        ennemies_collector.append(entities.Ennemy(300, 60, 2, 1, 12150, 625, [-100,100]))
        ennemies_collector.append(entities.Ennemy(300, 60, 2, 1, 12950, 380, [-100,100]))
    elif LEVELNAME == "level1_boss":
        # Sounds
        pg.mixer.music.load('../assets/music/level1.mp3')
        pg.mixer.music.play(-1)
        # Ennemies
        ennemies_collector.append(entities.Boss(1000, 30, "hillary", 1000, 200))
        bullet_time_regen_coeff = 4
        # Missiles
        for i in range(1,20):
            missiles_collector.append(entities.Missile(300,BLOCKSIZE,i*100))
            missiles_collector.append(entities.Missile(400,BLOCKSIZE,i*175))
            missiles_collector.append(entities.Missile(800,BLOCKSIZE,i*150))
            missiles_collector.append(entities.Missile(400,BLOCKSIZE,i*200))
            missiles_collector.append(entities.Missile(300,BLOCKSIZE,i*250))
            missiles_collector.append(entities.Missile(1000,BLOCKSIZE,i*300))
            missiles_collector.append(entities.Missile(500,BLOCKSIZE,i*360))



    dirPlayer = 1
    sprites_collecor = pg.sprite.Group()
    player = entities.Player(screen)
    lastPlayerHealth = player.health
    updateMap = True
    damageTimer = 0
    slowDownPower = False
    isPause = False



    running = True
    level_result = "failed"
    while running:

        sprites_collecor.empty()

        # Update level
        if updateMap:
            playerBlockX = int(player.posX//BLOCKSIZE)
            playerBlockY = player.rect.y//BLOCKSIZE
            player.playerBlock = playerBlockX
            player.playerH = playerBlockY
            minBlockIndex = playerBlockX-16
            if minBlockIndex < 0:
                minBlockIndex = 0
            minX,maxX = minBlockIndex, playerBlockX+16
            minX_aroundPlayer,maxX_aroundPlayer = playerBlockX-15, playerBlockX+15
            mapBlocks = painter.drawMap(pg,CORE_grid.map,[minX,maxX],BLOCKSIZE,player)

            if mapBlocks == "LEVEL_END":
                level_result = "success"
                break

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
            if dirPlayer == -1:
                player.image = pg.transform.flip(player.image, True, False)

        if player.accX < 0:
            dirPlayer = -1
            screen.blit(pg.transform.flip(player.image, True, False), player.rect)
        elif player.accX > 0:
            dirPlayer = 1
            screen.blit(player.image, player.rect)
        else:
            screen.blit(player.image, player.rect)

        # Key manager
        firstDraw = True
        while True:
            events = pg.event.get()
            keyAction = km.get(events)

            updateMap = True
            if keyAction == "exit":
                running = False
                pg.quit()
                break
            elif keyAction == "onetap_go_up" and not isPause:
                player.accelerateY(-2,mapBlocks,[minX_aroundPlayer,maxX_aroundPlayer],BLOCKSIZE)
            elif keyAction == "go_left" and not isPause:
                player.accelerateX(-0.2)
            elif keyAction == "go_right" and not isPause:
                player.accelerateX(0.2)
            elif keyAction == "go_projectile" and not isPause:
                if player.ammo > 0 and not player.reloading:
                    newBullet = entities.Bullet(player.rect.x,player.rect.y + (random.randint(0,6)-3),BLOCKSIZE,dirPlayer)
                    SOUND_gunshot.play()
                    bullets_collector.append(newBullet)
                    player.ammo -= 1
                    if player.ammo == 0:
                        player.reloading = True
            elif keyAction == "slowDown_switch" and not isPause:
                if not slowDownPower:
                    if player.mana > 0:
                        slowDownPower = True
                        SOUND_bulletTime_in.play()
                        pg.mixer.music.set_volume(0)
                else:
                    slowDownPower = False
                    SOUND_bulletTime_out.play()
                    pg.mixer.music.set_volume(0.1)
            elif keyAction == "pause_switch":
                isPause = not isPause
            else:
                if not isPause:
                    if len(bullets_collector) == 0 and len(ennemies_collector) == 0:
                        updateMap = False

            if not isPause:
                break
            else:
                if firstDraw:
                    # Pause menu
                    screen.blit(pause_menu, (0,0))
                    pg.display.update()
                    firstDraw = False

        
        # Ennemies update
        for ennemy in ennemies_collector:
            isAlive = ennemy.update(player,screen)
            if ennemy.isBoss:
                if frame%30==0:
                    if ennemy.image == ennemy.an1:
                        ennemy.image = ennemy.an2
                    else:
                        ennemy.image = ennemy.an1


            if not isAlive:
                ennemies_collector.remove(ennemy)
                player.mana += 25
                if player.mana > player.maxMana:
                    player.mana = player.maxMana

            screen.blit(ennemy.image, ennemy.rect)

        # Missiles update
        for missile in missiles_collector:
            if missile.v == 0 and missile.frameStart == frame:
                missile.v = 6
            
            isExisting = missile.update(player,mapBlocks)
            if not isExisting:
                missiles_collector.remove(missile)
            
            screen.blit(missile.image, missile.rect)

        # Superpower
        if slowDownPower:
            if player.mana > 0:
                screen.blit(slowDownOverlay, (0,0))
                player.mana -= 1
            else:
                SOUND_bulletTime_out.play()
                slowDownPower = False
                pg.mixer.music.set_volume(0.1)

        # Player update
        playerUpdated = player.update(mapBlocks,[minX_aroundPlayer,maxX_aroundPlayer],BLOCKSIZE,frame)
        if playerUpdated[0] != playerUpdated[1]:
            updateMap = True

        # HUD 
        # Player Mana
        w = 300
        h = 25
        hW = (player.mana/player.maxMana)*w
        pg.draw.rect(screen, (200,200,200), pg.Rect(50,115,w,h))
        pg.draw.rect(screen, (100,100,255), pg.Rect(50,115,hW,h))
        screen.blit(manaBarOutliner, (10,75))

        # Player health
        w = 400
        h = 40
        hW = (player.health/player.maxHealth)*w
        ratio = (player.health/player.maxHealth)
        pg.draw.rect(screen, (200,200,200), pg.Rect(50,50,w,h))
        pg.draw.rect(screen, getHealthBarColor(ratio), pg.Rect(50,50,hW,h))
        screen.blit(healthBarOutliner, (10,10))

        # Player ammo
        screen.blit(ammo_imgs[player.ammo], (10,SCREEN_HEIGHT-165))





        # Bullets update
        for bullet in bullets_collector:
            shouldLive = bullet.update(player,mapBlocks,ennemies_collector)
            if not shouldLive:
                bullets_collector.remove(bullet)
            screen.blit(bullet.image, bullet.rect)

        # show fps
        """
        fps = str(0)
        font = pg.font.SysFont("Arial", 30)
        fps_text = font.render(fps, 1, pg.Color("black"))
        screen.blit(fps_text, (20,SCREEN_HEIGHT - 100))
        """
    
        # Damage took
        if lastPlayerHealth != player.health:
            damageTimer = 50

        if damageTimer > 0:
            pg.draw.rect(screen, (200,0,0), pg.Rect(5,5,SCREEN_WIDTH-10,SCREEN_HEIGHT-10), 4)
            damageTimer -= 1

        if player.health <= 0:
            break

        # Draw sprites
        pg.display.update()
        pg.display.flip()


        lastPlayerHealth = player.health
        if frame%60 == 0:
            player.mana += 1*bullet_time_regen_coeff
            if player.mana > player.maxMana:
                player.mana = player.maxMana
        frame += 1

    if level_result == "success":
        screen.blit(pg.image.load("../assets/success.png"), (0,0))
    else:
        screen.blit(pg.image.load("../assets/gameover.png"), (0,0))
    pg.display.update()

    time.sleep(5)

    return level_result


# Levels manager
levels_status = {
    "level1": False,
    "level1_boss": False,
    "level2": False,
    "final": False
}
levels_names = ["level1","level1_boss","level2","final"]

levelIndex = 0
while levelIndex < len(levels_names):

    LEVELNAME = levels_names[levelIndex]

    if not levels_status[LEVELNAME]:
        result = run_level(LEVELNAME)
        if result == "success":
            levels_status[LEVELNAME] = True
            levelIndex += 1
    else:
        levelIndex += 1

pg.quit()