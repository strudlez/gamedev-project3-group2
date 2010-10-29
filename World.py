import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
import sys, math, random
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
import Globals
from Line import Line
from Level import Level,LevelGrid
from LevelWalker import LevelWalker

class World(DirectObject):  #Subclassing here is necessary to accept events

    def __init__(self):
        base.disableMouse()                     #Turn off mouse control, otherwise camera is not repositional
        render.setShaderAuto()
        self.loadModels()
        self.setResolution()
        self.setLights()
        self.loadEnvironment()
        self.setResolution()
        self.setupCollisions()
        camera.setPosHpr(0, 15, 7, 0, 15, 0)
        self.isMoving = False
        
        self.keymap = {"left":0, "right":0, "forward":0, "backwards":0, "add":0}
        self.prevtime = 0
        taskMgr.add(self.move, "moveTask")
        
        self.accept("arrow_up", self.setKey, ["forward", 1])
        self.accept("arrow_up-up", self.setKey, ["forward", 0]) 
        self.accept("arrow_left", self.setKey, ["left", 1])
        self.accept("arrow_left-up", self.setKey, ["left", 0])
        self.accept("arrow_right", self.setKey, ["right", 1])
        self.accept("arrow_right-up", self.setKey, ["right", 0])
        self.accept("arrow_down", self.setKey, ["backwards", 1])
        self.accept("arrow_down-up", self.setKey,["backwards", 0])
        self.accept("a", self.setKey,["add", 1])

        
        self.accept("escape", sys.exit) #Allow the player to press esc to exit the game
        self.level=Level()
        
        self.line=Line(self)
        

    def loadEnvironment(self):
        """Loads the environment model into the world"""
        #Load the environment
        self.env = loader.loadModel("EGGS/environment")
        self.env.reparentTo(render)
        self.env.setScale(4)
        self.env.setPos(-8, 42, 0)


    def setLights(self):
        """Creates a global light"""
        self.dirLight = DirectionalLight("dirLight")
        self.dirLight.setColor((.6, .2, .6, 1))
        #Create a NodePath and attach it directly to the scene
        self.dirLightNP = render.attachNewNode(self.dirLight)
        self.dirLightNP.setHpr(0, -26, 0)
        #The NodePath that calls setLight is what gets illuminated by the light
        render.setLight(self.dirLightNP)
        #Use clearLight() to turn it off
        
        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor((.25, .25, .25, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        render.setLight(self.ambientLightNP)

    def loadModels(self):
        """Loads models into the world"""
        
    
    def setKey(self, key, value):
        self.keymap[key] = value

    def setupCollisions(self):
        """Sets up panda and smiley collision system"""
    
    def setResolution(self):
        """Set the screen resolution"""
        wp = WindowProperties()
        wp.setSize(1024, 768) # there will be more resolutions
        #wp.setFullscreen(True)
        base.win.requestProperties(wp)
    
    def move(self, task): #all methods added to taskMgr get passed task info
        
        """moves the panda depending on the keymap"""
        elapsed = task.time - self.prevtime
        self.line.move(elapsed,self.keymap)
        self.prevtime = task.time
        return Task.cont

    
w = World()
run()
