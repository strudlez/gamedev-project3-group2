# python import
import sys
from direct.gui.OnscreenText import OnscreenText
# panda imports
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

# game imports
from World import World
from Menu import Menu
from PictureAnimation import PictureAnimation
import Globals

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

        self.startAnim = PictureAnimation([
          'titlescreen0001.png',
          'titlescreen0002.png',
          'titlescreen0003.png',
          'titlescreen0004.png'
        ], 1)

        while True:
            yield
            if m.getSelected():
                s = m.getSelection()
                if s == 0:
                    m.destroy()
                    self._updateFunc = self.getReady().next
                elif s == 1:
                    sys.exit()

    def getReady(self):
        self.startAnim.play()
        while not self.startAnim.isDone:
            yield
        self.startAnim.destroy()
        self._updateFunc = self.playGame().next
        yield

    def playGame(self):
        w = World()
        while True:
            yield
            if w.time <= 0:
                w.destroy()
                self._updateFunc = self.youWinScreen().next
            if w.dead:
                w.destroy()
                self._updateFunc = self.gameOverScreen().next

    def gameOverScreen(self):
        s = PictureAnimation([
          'gameover.png'
        ], 5)
        s.play()
        self.max = OnscreenText(text = 'Max Length: %i'%Globals.MAX, pos = (.4, -.9), scale = 0.1, fg=(1,1,1,1))
        self.score = OnscreenText(text = 'Score: %i'%Globals.SCORE, pos = (-.4, -.9), scale = 0.1, fg=(1,1,1,1))
        while not s.isDone:
            yield
        s.destroy()
        self._updateFunc = self.titleMenu().next
        self.score.destroy()
        self.max.destroy()
        
        yield
        

    def youWinScreen(self):
        s = PictureAnimation([
          'youwin.png'
        ], 5)
        s.play()
        self.max = OnscreenText(text = 'Max Length: %i'%Globals.MAX, pos = (.4, -.9), scale = 0.1, fg=(1,1,1,1))
        self.score = OnscreenText(text = 'Score: %i'%Globals.SCORE, pos = (-.4, -.9), scale = 0.1, fg=(1,1,1,1))
        while not s.isDone:
            yield
        s.destroy()
        self._updateFunc = self.titleMenu().next
        self.score.destroy()
        self.max.destroy()
        yield

    def destroy(self):
        taskMgr.remove(self.update)

    def setResolution(self):
        """Set the screen resolution"""
        base.disableMouse()
        wp = WindowProperties()
        wp.setSize(1024, 768) # there will be more resolutions
        wp.setFullscreen(True)
        
        base.win.requestProperties(wp)