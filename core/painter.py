from colors import *
import pygame as pg

def drawMap(pg,mapData,partData,blockSize):

    sprites = []

    for line in mapData:
        for index in range(partData[0],partData[1]+1):
            block = line[index]

            if block == '0':
                imagePath = "BLUE"
                sprites.append(Block(pg, blockSize, imagePath))
            elif block == '1':
                imagePath = "WHITE"
                sprites.append(Block(pg, blockSize, imagePath))
    
    return sprites

class Block(pg.sprite.Sprite):

    def __init__(self,pg,blockSize,imagePath):

        # TO ADD IMAGE SPRITES
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((blockSize, blockSize))
        self.image.fill(imagePath)
        self.rect = self.image.get_rect()
        self.rect.center = (blockSize / 2, blockSize / 2)

