# python import
import sys

# panda imports
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

# game imports
from World import World
from Menu import Menu

class MasterControl(DirectObject):
    def __init__(self):
        # game/engine initialization stuff
        base.disableMouse()
        render.setShaderAuto()
        self.setResolution()

        self._updateFunc = self.titleMenu().next
        taskMgr.add(self.update, 'MasterControl update task')
        
    def update(self, task):
        self._updateFunc()
        return task.cont

    def titleMenu(self):
        m = Menu([
              ('Play', 0, 'menu_play'),
              ('Quit', 1, 'menu_quit')
            ])
        while True:
            yield
            if m.getSelected():
                s = m.getSelection()
                if s == 0:
                    m.destroy()
                    self._updateFunc = self.playGame().next
                elif s == 1:
                    sys.exit()

    def playGame(self):
        w = World()
        while True:
            yield
            # TODO this never ends, OMG!

    def destroy(self):
        taskMgr.remove(self.update)

    def setResolution(self):
        """Set the screen resolution"""
        wp = WindowProperties()
        #wp.setSize(1024, 768) # there will be more resolutions
        #wp.setFullscreen(True)
        base.win.requestProperties(wp)