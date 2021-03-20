import pygame as pg

class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.maxHealth = 200
        self.health = 200
        self.attack = 20
        self.armor = 0
        self.speed = 5
        self.jump = 1.5
        self.image = pg.transform.scale(pg.image.load('../assets/trump.png').convert_alpha(), (60, 120))
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = 120

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

    def update(self, mapBlocks, partData):

        # Speed updating
        self.speedX += self.accX
        self.speedY += self.accY

        # Air resistance & gravity
        self.accX = self.accX*0.5
        if abs(self.accX) < 0.1/100:
            self.accX = 0
            
        if not self.mapCollision(mapBlocks, partData):
            self.accY = self.accY + 0.01 # gravity
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
        self.rect.x += self.speedX
        self.rect.y += self.speedY

    def mapCollision(self, mapBlocks, partData):
        isCollision = False

        for block in mapBlocks:
            if partData[0] <= block.column <= partData[1]:
                if block.blockType != '0':
                    temp = pg.sprite.collide_rect(self, block)
                    if temp:
                        isCollision = True
                        break

        return isCollision