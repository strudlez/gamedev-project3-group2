import Globals
import string
import LevelConstants
from LevelLocation import LevelLocation

class LevelWalker(object):
    def __init__(self, level, location, set = True):
        self._level = level
        self._location = location.copy()
        self._setEnabled = set

    def getModelPos(self):
        '''returns a tuple of x, y, z representing spatial position that
        corresponds to LevelWalker's current position'''
        grid = self._level._grids[self._location.grid]
        print grid.offsetX, grid.offsetY
        return (Globals.TILESIZE * (self._location.x - 1), Globals.TILESIZE * self._location.y, 0)
        # TODO find out why -1 offset is needed on x
    
    def getCell(self):
        return self._level._grids[self._location.grid].getCell(self._location.x, self._location.y)

    def setCell(self, newVal):
        self._level._grids[self._location.grid].setCell(self._location.x, self._location.y, newVal)

    def unset(self):
        if self.getCell()<=1:
            self.setCell(LevelConstants.EMPTY)
            
    def set(self):
        if self.getCell()<=1:
            self.setCell(LevelConstants.LINE_WALKER)
    
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
        col=self._level._grids[self._location.grid].getCell(self._location.x,self._location.y)
        for a in xrange(0, units):
            #col=self._level._grids[self._grid].getCell(self._location.x+dx,self._location.y+dy)
            
            #self._location.x += dx
            #self._location.y += dy
            if col:
                #ret=int(round(self._location.x+dx,2)),int(round(self._location.y+dy,2)),self._level._grids[self._grid].getCell(self._location.x+dx,self._location.y+dy)
                ret=int(round(self._location.x,2)),int(round(self._location.y,2)),self._level._grids[self._location.grid].getCell(self._location.x,self._location.y)
            elif col>1:
                if self._setEnabled:
                    self.unset()
                self._location.x += dx
                self._location.y += dy
                return ret
                    
            #self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),0)
            if self._setEnabled:
                self.unset()
            self._location.x += dx
            self._location.y += dy
            #self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),1)
            if self._setEnabled:
                self.set()
            # TODO IMPLEMENT WARPS
            # if self._level._warps(LevelLocation)
        
        # all done!
        return ret

    def colocated(self, otherWalker):
        '''returns true if this walker is at the same position as other
        walker'''
        return self._location.equals(otherWalker._location)