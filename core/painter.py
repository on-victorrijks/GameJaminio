from colors import *
import pygame as pg

def drawMap(pg,mapData,partData,blockSize,player):

    sprites = []

    for lineIndex,line in enumerate(mapData):
        for index in range(partData[0],partData[1]+1):
            block = line[index]
            column = index
            pos = [
                (index)*blockSize - player.posX,
                lineIndex*blockSize
            ]

            if block == '0':
                imagePath = "BLUE" 
                blockType = '0'
                sprites.append(Block(pg, blockSize, imagePath,pos,blockType,column,lineIndex))
            elif block == '1':
                imagePath = "WHITE"
                blockType = '1'
                sprites.append(Block(pg, blockSize, imagePath,pos,blockType,column,lineIndex))
    
    return sprites

class Block(pg.sprite.Sprite):

    def __init__(self,pg,blockSize,imagePath,pos,blockType,column,line):

        # TO ADD IMAGE SPRITES
        pg.sprite.Sprite.__init__(self)
        self.blockType = blockType
        self.image = pg.Surface((blockSize, blockSize))
        self.image.fill(imagePath)
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0],pos[1]+blockSize/2)
        self.column = column
        self.line = line

