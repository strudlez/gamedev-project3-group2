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
        self.node.setPos(pos)
        self.angle=(angle+180)%360
        self.node.setH(self.angle)
        actor.instanceTo(self.node)
        self.dx, self.dy = {0:(0, -Globals.CONGASTEP), 180:(0, Globals.CONGASTEP), 270:(-Globals.CONGASTEP, 0), 90:(Globals.CONGASTEP, 0)}[self.angle]
        
    
    def delete(self):
        self.node.removeNode()
        
    def move(self):
        self.frame+=1
        
        self.node.setPos(self.node.getX() + self.dx, self.node.getY() + self.dy, 0)
        if self.frame==self.deadOn:self.dead=1
        color=1-float(self.frame)/self.deadOn
        self.node.setColorScale(color,color,color,color)