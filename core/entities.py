import pygame as pg
import math
import time

class Player(pg.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()

        # Data
        self.maxHealth = 200
        self.health = 200
        self.attack = 20
        self.armor = 0

        # Bullets
        self.bullet_pool = pg.sprite.Group()

        # Animations
        self.still  = pg.transform.scale(pg.image.load('../assets/player.png').convert_alpha(), (72, 100))
        self.moving1 = pg.transform.scale(pg.image.load('../assets/player_moving1.png').convert_alpha(), (72, 100))
        self.moving2 = pg.transform.scale(pg.image.load('../assets/player_moving2.png').convert_alpha(), (72, 100))
        self.image = self.still

        # Spec.
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

        self.screen = screen

    def accelerateX(self, amount):
        self.accX += amount

    def accelerateY(self, amount, mapBlocks, partData, blockSize):
        if amount <= 0 and not self.mapCollision(mapBlocks, partData, blockSize):
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

        if not self.mapCollision(mapBlocks, partData, blockSize):
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
        collideX = self.mapCollision(mapBlocks, partData, blockSize, "X")
        if collideX == False:
            self.posX += self.speedX
        else:
            self.posX += collideX*10
            self.speedX += collideX*10


        if not self.mapCollision(mapBlocks, partData, blockSize, "UY"):
            self.rect.y += self.speedY

        # After pos 
        afterPos = [self.posX, self.rect.y]

        return  [beforePos,afterPos]

    def mapCollision(self, mapBlocks, partData, blockSize, dimension="Y"):
        isCollision = False

        for block in mapBlocks:
            if partData[0] <= block.column <= partData[1]:
                if block.blockType not in ['0','3','4']:
                    if dimension == "X" and block.line <= self.playerH:
                        temp = pg.sprite.collide_rect(self, block)
                        if temp:
                            if block.column >= math.ceil(self.posX/blockSize)+2:
                                return -1
                            else:
                                return 1
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



class Ennemy(pg.sprite.Sprite):

    def __init__(self, health, attack, armor, ennemyID, x, y, movements):
        super().__init__()

        # Data
        self.maxHealth = 100
        self.health = 100
        self.attack = 10
        self.armor = 0

        # Tour
        self.tourPos = 0
        self.tourDir = 1
        self.shouldTour = True
        self.movements = movements

        # Animations
        self.still  = pg.transform.scale(pg.image.load('../assets/ennemy{}.png'.format(ennemyID)).convert_alpha(), (59, 100))
        self.image = self.still
        self.reversedImage = False

        # Spec. (Position)
        self.rect = self.image.get_rect()
        self.originalX = x
        self.originalY = y
        self.rect.x = x
        self.rect.y = y

        # Movements
        self.speed = 2

    def showHealth(self,player,screen):
        w = 100
        h = 10
        hW = (self.health/self.maxHealth)*w
        pg.draw.rect(screen, (100,100,100), pg.Rect((self.originalX - player.posX + self.tourPos), self.rect.y - 60,w,h), 2)
        pg.draw.rect(screen, (255,0,0), pg.Rect((self.originalX - player.posX + self.tourPos), self.rect.y - 60,hW,h))

    def update(self,player,screen):

        if self.tourDir == 1:
            addTour = 0
            if self.shouldTour:
                self.tourPos += self.speed
        elif self.tourDir == -1:
            addTour = 1
            if self.shouldTour:
                self.tourPos -= self.speed
    

        if abs(self.movements[addTour]) <= abs(self.tourPos):
            self.tourDir = -self.tourDir
            self.image = pg.transform.flip(self.image, True, False)
            self.reversedImage = not self.reversedImage
        
        if self.health < self.maxHealth:
            self.shouldTour = False
            if player.rect.x >= self.rect.x:
                if self.reversedImage:
                    self.image = pg.transform.flip(self.image, True, False)
                    self.reversedImage = not self.reversedImage
                


        self.showHealth(player,screen)

        self.rect.x = self.originalX - player.posX + self.tourPos
        return self.health > 0




class Bullet(pg.sprite.Sprite):

    def __init__(self,x,y,blockSize,dirPlayer):
        super().__init__()
        self.v = 20*dirPlayer
        self.timer = 0
        self.image = pg.transform.scale(pg.image.load('../assets/bullet.png').convert_alpha(), (6, 3))
        self.rect = self.image.get_rect()
        self.rect.x = x + 50
        self.rect.y = y + 64
        self.blockH = math.floor(self.rect.y/blockSize)

    def update(self,player,mapBlocks,ennemies_collector):
        self.rect.x += self.v
        self.timer += 1
        if self.timer >= 90 or self.collidingWithElm(player,mapBlocks,ennemies_collector):
            return False
        return True

    def collidingWithElm(self, player, mapBlocks, ennemies_collector):
        isCollision = False
        for block in mapBlocks:
            if block.line == self.blockH and block.blockType not in ['0','3','4']:
                temp = pg.sprite.collide_rect(self, block)
                if temp:
                    isCollision = True
                    break
        for ennemy in ennemies_collector:
            temp = pg.sprite.collide_rect(self, ennemy)
            if temp:
                ennemy.health -= player.attack
                isCollision = True
                break

        return isCollision

