from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib

class PictureAnimation(DirectObject):
    def __init__(self, picList, period, position = (0, 0)):
        self._rootNode = aspect2d.attachNewNode('menuRootNode')
        self._rootNode.setPos((position[0], 0, position[1]))

        self._period = period

        self.pics = []
        for pic in picList:
            a = OnscreenImage(image = pic, parent = self._rootNode, scale=(1.335,1,1))
            a.setTransparency(TransparencyAttrib.MAlpha)
            a.hide()
            self.pics.append(a)

        self._index = 0
        self.isDone = False

        self._updateTask = None

    def play(self):
        self.pics[0].show()
        self._updateTask = taskMgr.add(self.update, 'pictureAnimationTask')

    def update(self, task):
        #print 'updating'
        if task.time >= (self._index + 1) * self._period:
            #print 'time to switch'
            if self._index >= len(self.pics) - 1:
                self.isDone = True
                self._updateTask = None
                return task.done
            self.pics[self._index].hide()
            self._index += 1
            self.pics[self._index].show()
        return task.cont

    def destroy(self):
        self._rootNode.removeNode()
        if self._updateTask:
            taskMgr.remove(self._updateTask)