import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
import sys, math, random, cPickle, bullet
from direct.gui.OnscreenImage import OnscreenImage

class Partier(DirectObject):    
    
    def __init__(self, pos, happy, mass):
    self.mass = 0
    self.happiness = happy
    self.curpos=pos
    
    def move(self):
        pass
        
                