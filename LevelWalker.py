import string
from Globals import *

class LevelWalker(object):
    def __init__(self, level, location, grid='floor1'):
        self._level = level
        self._location = location
        self._grid=grid
        
    
    def getCell(self):
        return self._level._grids[self._grid].getCell(self._location.x, self._location.y)
    
    def unset(self):
        grid=self._level._grids[self._grid]
        if grid.getCell(self._location.x,self._location.y)<=1:
            grid.setCell(self._location.x,self._location.y,0)
    def set(self):
        grid=self._level._grids[self._grid]
        if grid.getCell(self._location.x,self._location.y)<=1:
            grid.setCell(self._location.x,self._location.y,1)
    
    def walk(self, direction, units = 1):
        '''walks across the level in the direction the specified number of
        units.  Throws an exception if it walks off the side of a grid'''
        dir = string.upper(direction)
        if not (dir in ['U', 'R', 'L', 'D']):
            raise Exception('invalid direction')
        # fix walking backwards to look like walking forwards in opposite
        # direction
        if units < 0:
            units *= -1
            dir = {'U':'D', 'D':'U', 'L':'R', 'R':'L'}[dir]

        dx, dy = {'U':(0, -1), 'D':(0, 1), 'L':(-1, 0), 'R':(1, 0)}[dir]
        ret=None
        # walk forward one unit at a time
        col=self._level._grids[self._grid].getCell(self._location.x,self._location.y)
        for a in xrange(0, units):
            #col=self._level._grids[self._grid].getCell(self._location.x+dx,self._location.y+dy)
            
            #self._location.x += dx
            #self._location.y += dy
            if col:
                #ret=int(round(self._location.x+dx,2)),int(round(self._location.y+dy,2)),self._level._grids[self._grid].getCell(self._location.x+dx,self._location.y+dy)
                ret=int(round(self._location.x,2)),int(round(self._location.y,2)),self._level._grids[self._grid].getCell(self._location.x,self._location.y)
            if col>1:
                self.unset()
                self._location.x += dx
                self._location.y += dy
                return ret
                    
            #self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),0)
            self.unset()
            self._location.x += dx
            self._location.y += dy
            #self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),1)
            self.set()
            if COLLIDE_DEBUG:self._level._grids[self._grid].printGrid()
            # TODO IMPLEMENT WARPS
            # if self._level._warps(LevelLocation)
        
        # all done!
        return ret
class Location:
    def __init__(self,x,y):
        self.x=x
        self.y=y
