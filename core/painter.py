from colors import *
import pygame as pg

blockSize = 120

loadedImages = {
    "floor_level1": pg.transform.scale(pg.image.load("../assets/floor_level1.png"), (blockSize, blockSize)),
    "lamp_level1": pg.transform.scale(pg.image.load("../assets/lamp_level1.png"), (blockSize, blockSize)),
    "tube_level1": pg.transform.scale(pg.image.load("../assets/tube_level1.png"), (blockSize, blockSize)),
}

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
                color = (38,38,38)
                blockType = '0'
                sprites.append(Block(pg, blockSize, color,pos,blockType,column,lineIndex,isFill=True))
            elif block == '1':
                imageID = "floor_level1" 
                blockType = '1'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == '2':
                color = (9,13,48)
                blockType = '2'
                sprites.append(Block(pg, blockSize, color,pos,blockType,column,lineIndex,isFill=True))
            elif block == '3':
                imageID = "lamp_level1" 
                blockType = '3'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == '4':
                imageID = "tube_level1" 
                blockType = '4'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
    
    return sprites

class Block(pg.sprite.Sprite):

    def __init__(self,pg,blockSize,fillData,pos,blockType,column,line,isFill=False):

        # TO ADD IMAGE SPRITES
        pg.sprite.Sprite.__init__(self)
        self.blockType = blockType

        if isFill:
            self.image = pg.Surface((blockSize, blockSize))
            self.image.fill(fillData)
        else:
            self.image = loadedImages[fillData]

        self.rect = self.image.get_rect()
        self.rect.center = (pos[0],pos[1]+blockSize/2)
        self.column = column
        self.line = line