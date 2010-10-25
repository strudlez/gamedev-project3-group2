class ModelMetadata(object):
    def __init__(self):
        self._h = 0
        self._p = 0
        self._r = 0
        self._x = 0
        self._y = 0
        self._z = 0
        self._scale = 0

    def getPos(self):
        return (self._x, self._y, self._z)

    def getHpr(self):
        return (self._h, self._p, self._r)

    def getScale(self):
        return self._scale

    def setPos(self, newTuple):
        self._x, self._y, self._z = newTuple

    def setHpr(self, newTuple):
        self._h, self._p, self._r = newTuple

    def setScale(self, newScale):
        self._scale = newScale