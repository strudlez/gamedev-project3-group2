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
from Partier import Partier
from LevelLocation import LevelLocation
from Line import Line
from Level import Level,LevelGrid
from LevelWalker import LevelWalker
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from Door import Door

class World(DirectObject):  #Subclassing here is necessary to accept events

    def __init__(self):
        self.loadModels()
        self.setLights()
        self.loadEnvironment()
        self.setupCollisions()
        camera.setPosHpr(0, 15, 7, 0, 15, 0)
        self.isMoving = False
        
        self.keymap = {"left":0, "right":0, "forward":0, "backwards":0, "add":0, "dash":0}
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
        self.accept("space", self.setKey,["dash", 1])
        self.accept("space-up", self.setKey,["dash", 0])
        self.max = 0
        self.cong= 1
        self.time=200

        self.CP = OnscreenText(text = "ConGo Power: ", pos = (-1, .8), scale = 0.07, fg=(1,1,1,1))
        self.dash = OnscreenText(text = "", pos = (-1, .6), scale = 0.07, fg=(1,1,1,1))
        self.length = OnscreenText(text = 'Length: ', pos = (-.5, .8), scale = 0.07, fg=(1,1,1,1))
        self.mlength = OnscreenText(text = 'Max Length: ', pos = (0, .8), scale = 0.07, fg=(1,1,1,1))
        self.SpeedUp = OnscreenText(text = 'SpeedUp: ', pos = (.5, .8), scale = 0.07, fg=(1,1,1,1))
        self.timer = OnscreenText(text = 'Timer: ', pos = (1, .8), scale = 0.07, fg=(1,1,1,1))
        self.score = OnscreenText(text = 'Score: ', pos = (-.3, -.9), scale = 0.1, fg=(1,1,1,1))
        self.congp = OnscreenImage(image = 'textures/green.png', pos = (-1, 0,.7), scale = (.001*1,0,0.028))
        
        
        self.accept("escape", sys.exit) #Allow the player to press esc to exit the game
        self.level=Level()

        Globals.currentLevel = self.level
        
        self.line=Line(self)
        self.leaving=[]

        partierTest = Partier(LevelLocation('floor1', 2, 2))
        

    def loadEnvironment(self):
        """Loads the environment model into the world"""
        #Load the environment
        self.env = loader.loadModel("models/level")
        self.env.reparentTo(render)
        self.env.setScale(2)
        self.env.setPos(0, 0, 0)
        self.env.setP(270)
        
        
        self.doorModel=loader.loadModel("models/door")
        self.doors=[]
        self.doors.append(Door(self.doorModel,1,38,-12,0))
        self.doors.append(Door(self.doorModel,2,20,-6,90))
        self.doors.append(Door(self.doorModel,3,4,18,0))
        

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
        self.ambientLight.setColor((0.5, 0.5, 0.5, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        render.setLight(self.ambientLightNP)

    def loadModels(self):
        """Loads models into the world"""
        
    def setKey(self, key, value):
        self.keymap[key] = value

    def setupCollisions(self):
        """Sets up panda and smiley collision system"""
    
    def move(self, task): #all methods added to taskMgr get passed task info
        
        """moves the panda depending on the keymap"""
        elapsed = task.time - self.prevtime
        
        self.line.move(elapsed,self.keymap)
        for i in range(len(self.leaving)-1,-1,-1):
            self.leaving[i].move()
            if self.leaving[i].dead:
                self.leaving[i].delete()
                self.leaving.pop(i)
        for i in range(len(self.doors)-1,-1,-1):
            self.doors[i].move()
            if self.doors[i].dead:
                self.doors[i].delete()
                self.doors.pop(i)
        self.prevtime = task.time
        return Task.cont
