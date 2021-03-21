from colors import *
import pygame as pg

blockSize = 120

loadedImages = {
    "floor_level1": pg.transform.scale(pg.image.load("../assets/floor_level1.png"), (blockSize, blockSize)),
    "lamp_level1": pg.transform.scale(pg.image.load("../assets/lamp_level1.png"), (blockSize, blockSize)),
    "tube_level1": pg.transform.scale(pg.image.load("../assets/tube_level1.png"), (blockSize, blockSize)),
    "floor_level1boss": pg.transform.scale(pg.image.load("../assets/floor_level1boss.png"), (blockSize, blockSize)),
    "sand_level2": pg.transform.scale(pg.image.load("../assets/sand_level2.png"), (blockSize, blockSize)),
    "cloud1_level2": pg.transform.scale(pg.image.load("../assets/cloud1_level2.png"), (blockSize, blockSize)),
    "cloud2_level2": pg.transform.scale(pg.image.load("../assets/cloud2_level2.png"), (blockSize, blockSize)),
    "bg_q_final": pg.transform.scale(pg.image.load("../assets/bg_q_final.png"), (blockSize, blockSize)),
    "floor_final": pg.transform.scale(pg.image.load("../assets/floor_final.png"), (blockSize, blockSize)),
    "colonne_final_top": pg.transform.scale(pg.image.load("../assets/colonne_final_top.png"), (blockSize, blockSize)),
    "colonne_final": pg.transform.scale(pg.image.load("../assets/colonne_final.png"), (blockSize, blockSize)),
    "colonne_bottom": pg.transform.scale(pg.image.load("../assets/colonne_bottom.png"), (blockSize, blockSize)),
}

def drawMap(pg,mapData,partData,blockSize,player):

    sprites = []

    for lineIndex,line in enumerate(mapData):
        for index in range(partData[0],partData[1]+1):
            try:
                block = line[index]
            except:
                return "LEVEL_END"

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
            elif block == '7':
                imageID = "floor_level1boss" 
                blockType = '7'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == '8':
                color = (227,81,59)
                blockType = '8'
                sprites.append(Block(pg, blockSize, color,pos,blockType,column,lineIndex,isFill=True))
            elif block == 't':
                imageID = "sand_level2" 
                blockType = 't'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == 's':
                color = (240,199,132)
                blockType = '8'
                sprites.append(Block(pg, blockSize, color,pos,blockType,column,lineIndex,isFill=True))
            elif block == '9':
                color = (188,232,235)
                blockType = '9'
                sprites.append(Block(pg, blockSize, color,pos,blockType,column,lineIndex,isFill=True))
            elif block == 'm':
                imageID = "cloud1_level2" 
                blockType = 'm'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == '%':
                imageID = "cloud2_level2" 
                blockType = '%'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == 'l':
                imageID = "bg_q_final" 
                blockType = 'l'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == 'h':
                color = (92,31,31)
                blockType = 'h'
                sprites.append(Block(pg, blockSize, color,pos,blockType,column,lineIndex,isFill=True))
            elif block == 'p':
                imageID = "floor_final" 
                blockType = 'p'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == 'n':
                color = (51,16,16)
                blockType = 'n'
                sprites.append(Block(pg, blockSize, color,pos,blockType,column,lineIndex,isFill=True))
            elif block == ';':
                imageID = "colonne_final_top" 
                blockType = ';'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == '/':
                imageID = "colonne_final" 
                blockType = '/'
                sprites.append(Block(pg, blockSize, imageID,pos,blockType,column,lineIndex))
            elif block == ':':
                imageID = "colonne_bottom" 
                blockType = ':'
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