class LevelLocation(object):
    def __init__(self, grid = None, x = 0, y = 0):
        self.grid = grid
        self.x = x
        self.y = y

    def copy(self):
        '''makes a duplicate LevelLocation'''
        return LevelLocation(self.grid, self.x, self.y)

    def equals(self, other):
        return (self.grid == other.grid and self.x == other.x and self.y == other.y)