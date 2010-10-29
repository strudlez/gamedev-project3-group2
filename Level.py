import array

# JUST USE THE LEVELWALKER CUZ THIS DOESN'T HAVE ANY KIND OF GOOD INTERFACE YET

class Level(object):
    def __init__(self):
        self._grids = {'floor1':LevelGrid()} # map of grid identifiers (numbers) to LevelGrid's
        self._warps = {} # map of LevelLocation to LevelLocation objects
                         # (mapping warp source to warp target)

    #def addGrid(self):

    #def addWarp(self, warpName, ):


class LevelGrid(object):
    def __init__(self, width=250,height=250, offsetX=-125,offsetY=-125):
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.width = width
        self.height = height
        self.grid = array.array('H', [0]*width*height)

    def getCell(self, x, y):
        return self.grid[int(y) * self.width + int(x)]

    def setCell(self, x, y, newValue):
        self.grid[int(y) + self.width + int(x)] = newValue