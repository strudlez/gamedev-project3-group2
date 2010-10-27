from pandac.PandaModules import * #basic Panda modules

from pandac.PandaModules import *

class LineMember():
    def __init__(self,parent,actor,pos,number):
        self.parent=parent
        self.pos=pos
        self.angle=0
        self.node=render.attachNewNode("LineMember%d" % number)
        self.node.setPos(self.pos)
        actor.instanceTo(self.node)
    setAngle(self,angle):
        self.angle=angle
        self.node.setH(angle)
    