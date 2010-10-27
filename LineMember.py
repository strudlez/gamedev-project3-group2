from pandac.PandaModules import * #basic Panda modules
from pandac.PandaModules import *
import Globals

class LineMember():
    def __init__(self,parent,actor,pos,number):
        self.parent=parent
        self.pos=pos
        self.angle=0
        self.move=0
        
        self.gridX=self.pos.getX()/self.parent.parent.tileSize
        self.gridY=self.pos.getY()/self.parent.parent.tileSize
        
        self.node=render.attachNewNode("LineMember%d" % number)
        self.node.setPos(self.pos)
        actor.instanceTo(self.node)
    def setAngle(self,angle):
        self.angle=angle
        self.node.setH(angle)
    def moveFront(self,angle):
        pass
    def move(self,front):
        if move:
            if not round(self.node.getY(),2)%self.parent.parent.tileSize and not round(self.node.getX(),2)%self.parent.parent.tileSize:
                self.gridX=self.pos.getX()/self.parent.parent.tileSize
                self.gridY=self.pos.getY()/self.parent.parent.tileSize
        else:
            if front.gridX!=self.gridX or front.gridY!=self.gridY
    def moveTo(self):
        angle=self.node.getH()
        if abs(angle-360-self.angle)<abs(angle-self.angle):angle-=360
        elif abs(angle+360-self.angle)<abs(angle-self.angle):angle+=360
        if self.angle>angle:
            angle+=8
            if angle>self.angle:angle=angle
        elif self.angle<angle:
            angle-=8
            if angle<self.angle:angle=self.angle
        angle=angle%360
        self.node.setH(angle)
        
        dist = 0.1
        angle = math.radians(self.angle)
        dx = dist * math.sin(angle)
        dy = dist * -math.cos(angle)
        
        self.node.setPos(self.node.getX() + dx, self.node.getY() + dy, 0)