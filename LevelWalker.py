import string

class LevelWalker(object):
    def __init__(self, level, location):
        self._level = level
        self._location = location

    def getCell(self):
        return self._level._grids[self._grid].getCell(self._x, self._y)

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

        dx, dy = {'U':(0, -1), 'D':(0, 1), 'L':(-1, 0), 'R':(1, 0)}

        # walk forward one unit at a time
        for a in xrange(0, units):
            self._location.x += dx
            self._location.y += dy
            # TODO IMPLEMENT WARPS
            # if self._level._warps(LevelLocation)

        # all done!