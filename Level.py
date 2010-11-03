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
    def __init__(self, width=13,height=13, offsetX=0,offsetY=-1):
        self.offsetX = offsetX
        self.offsetY = offsetY
        #self.width = width
        #self.height = height
        col=open("Grid.txt").read().replace('\n','').split(',')
        self.height=height=len(open("Grid.txt").readlines())
        self.width=width=len(col)/height
        try:
            i=col.index('8')
            self.offsetX=i%height
            self.offsetY=i/height
            col[i]='0'
        except:pass
        self.grid = array.array('H', [0]*width*height)
        for i in range(len(self.grid)):
            self.grid[i]=int(col[i])
    
    def printGrid(self):
        print '-'*self.width
        for y in range(self.height):
            s=''
            for x in range(self.width):
                s+='%d' % self.grid[y * self.width + x]
            print s
            
    def getCell(self, x, y):
        #print x,y
        #return self.grid[(self.height-y-1+self.offsetY) * self.width + x+self.offsetX]
        return self.grid[(y+self.offsetY) * self.width + self.width-x-1+self.offsetX]
    
    def setCell(self, x, y, newValue):
        #self.grid[(self.height-y-1+self.offsetY) * self.width + x + self.offsetX] = newValue
        self.grid[(y+self.offsetY) * self.width + self.width-x-1 + self.offsetX] = newValue