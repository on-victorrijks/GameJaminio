from colors import *
import pygame as pg

def drawMap(pg,mapData,partData,blockSize):

    sprites = []

    for lineIndex,line in enumerate(mapData):
        for index in range(partData[0],partData[1]+1):
            block = line[index]

            pos = [
                (index - partData[0])*blockSize,
                lineIndex*blockSize
            ]

            if block == '0':
                imagePath = "BLUE" 
                sprites.append(Block(pg, blockSize, imagePath,pos))
            elif block == '1':
                imagePath = "WHITE"
                sprites.append(Block(pg, blockSize, imagePath,pos))
    
    return sprites

class Block(pg.sprite.Sprite):

    def __init__(self,pg,blockSize,imagePath,pos):

        # TO ADD IMAGE SPRITES
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((blockSize, blockSize))
        self.image.fill(imagePath)
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0],pos[1])

