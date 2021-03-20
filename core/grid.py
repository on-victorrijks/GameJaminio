class Grid():

    def __init__(self, sizeX, sizeY, level_name=None):
        self.area = sizeX*sizeY
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.map = sizeY * [[0]*sizeX]
        self.loadLevel(level_name)

    def loadLevel(self,level_name):
        if level_name != None:
            mapData = open("./levels/{}.txt".format(level_name), "r")
            lines = mapData.readlines()
            lines = [x.strip().split() for x in lines]
            self.map = lines
