import pygame as pg
from projectile import Projectile

class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.maxHealth = 200
        self.health = 200
        self.attack = 20
        self.armor = 0
        self.speed = 5
        self.jump = 1.5
        self.bullet_pool = pg.sprite.Group()

        self.still  = pg.transform.scale(pg.image.load('../assets/player.png').convert_alpha(), (72, 100))
        self.moving1 = pg.transform.scale(pg.image.load('../assets/player_moving1.png').convert_alpha(), (72, 100))
        self.moving2 = pg.transform.scale(pg.image.load('../assets/player_moving2.png').convert_alpha(), (72, 100))

        self.image = self.still


        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 50
        self.playerBlock = 0
        self.playerH = 0

        # Position
        self.posX = 50

        # Movements
        self.accX = 0
        self.accY = 0
        self.speedX = 0
        self.speedY = 0

    def accelerateX(self, amount):
        self.accX += amount

    def accelerateY(self, amount, mapBlocks, partData):
        if amount <= 0 and not self.mapCollision(mapBlocks, partData):
            return
        self.accY += amount

    def update(self, mapBlocks, partData, blockSize):

        # Before positions
        beforePos = [self.posX, self.rect.y]

        # Speed updating
        self.speedX += self.accX
        self.speedY += self.accY

        # Air resistance & gravity
        self.accX = self.accX*0.65
        if abs(self.accX) < 0.1/100:
            self.accX = 0
            
        if not self.mapCollision(mapBlocks, partData):
            self.accY = self.accY + 0.02 # gravity
        else:
            if self.accY >= 0:
                self.accY = 0
                self.speedY = 0

        self.speedX = self.speedX*0.9
        if abs(self.speedX) < 0.1/100:
            self.speedX = 0

        self.speedY = self.speedY*0.9
        if abs(self.speedY) < 0.1/100:
            self.speedY = 0


        # Updating positions
        if not self.mapCollision(mapBlocks, partData, "X"):
            self.posX += self.speedX
        if not self.mapCollision(mapBlocks, partData, "UY"):
            self.rect.y += self.speedY

        # After pos 
        afterPos = [self.posX, self.rect.y]

        return  [beforePos,afterPos]

    def mapCollision(self, mapBlocks, partData, dimension="Y"):
        isCollision = False

        for block in mapBlocks:
            if partData[0] <= block.column <= partData[1]:
                if block.blockType not in ['0','3','4']:
                    if dimension == "X" and block.line <= self.playerH:
                        temp = pg.sprite.collide_rect(self, block)
                        if temp:
                            isCollision = True
                            break
                    elif dimension == "UY" and block.line <= self.playerH:
                        temp = pg.sprite.collide_rect(self, block)
                        if temp:
                            isCollision = True
                            break             
                    elif dimension == "Y":
                        temp = pg.sprite.collide_rect(self, block)
                        if temp:
                            isCollision = True
                            break



            

        return isCollision

    def shoot_with_m16(self):

        self.bullet_pool.add(Projectile())