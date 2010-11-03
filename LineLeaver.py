from pandac.PandaModules import * #basic Panda modules
from pandac.PandaModules import *
from Globals import *
import Globals
import math

class LineLeaver():
    def __init__(self,actor,pos,angle,number):
        self.dead=0
        self.frame=0
        self.deadOn=45
        
        self.node=render.attachNewNode("LineLeaver%d" % number)
        #self.node.setLightOff()
        self.node.setShaderOff()
        self.node.setPos(pos)
        self.angle=angle
        self.node.setH(self.angle)
        
        actor.instanceTo(self.node)
        self.dx = Globals.CONGASTEP * math.sin(angle)
        self.dy = Globals.CONGASTEP * -math.cos(angle)
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        
    
    def delete(self):
        self.node.removeNode()
        
    def move(self):
        self.frame+=1
        
        self.node.setPos(self.node.getX() + self.dx, self.node.getY() + self.dy, self.node.getZ())
        if self.frame==self.deadOn:self.dead=1
        color=1-float(self.frame)/self.deadOn
        self.node.setAlphaScale(color)