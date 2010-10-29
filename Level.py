import array

# JUST USE THE LEVELWALKER CUZ THIS DOESN'T HAVE ANY KIND OF GOOD INTERFACE YET

class Level(object):
    def __init__(self):
        self._grids = {} # map of grid identifiers (numbers) to LevelGrid's
        self._warps = {} # map of LevelLocation to LevelLocation objects
                         # (mapping warp source to warp target)

    #def addGrid(self):

    #def addWarp(self, warpName, ):


class LevelGrid(object):
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        self.width = 0
        self.height = 0
        self.grid = array.array('H', 0)

    def getCell(self, x, y):
        return self.grid[y * self.width + x]

    def setCell(self, x, y, newValue):
        self.grid[y + self.width + x] = newValue