import string

class LevelWalker(object):
    def __init__(self, level, location, grid='floor1'):
        self._level = level
        self._location = location
        self._grid=grid
        
    
    def getCell(self):
        return self._level._grids[self._grid].getCell(self._location.x, self._location.y)
    
    def unset(self):
        self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),0)
    def set(self):
        self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),1)
    
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
        
        # walk forward one unit at a time
        for a in xrange(0, units):
            if self._level._grids[self._grid].getCell(self._location.x+dx,self._location.y+dy)==1:
                return int(round(self._location.x+dx,0)),int(round(self._location.y+dy,0))
            #self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),0)
            self.unset()
            self._location.x += dx
            self._location.y += dy
            #self._level._grids[self._grid].setCell(int(round(self._location.x,2)),int(round(self._location.y,2)),1)
            self.set()
            # TODO IMPLEMENT WARPS
            # if self._level._warps(LevelLocation)
        
        # all done!
        return None
class Location:
    def __init__(self,x,y):
        self.x=x
        self.y=y