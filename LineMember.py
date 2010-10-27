from pandac.PandaModules import * #basic Panda modules
from pandac.PandaModules import *
from Globals import *
import math

class LineMember():
    def __init__(self,parent,actor,front,number):
        self.parent=parent
        self.pos=Vec3(0,0,0)
        if front==None:
            self.angle=0
            
        else:
            self.angle=front.angle
            self.pos.setX(front.gridX*self.parent.parent.tileSize)
            self.pos.setY(front.gridY*self.parent.parent.tileSize)        
        
        self.canMove=0
        
        self.gridX=self.pos.getX()/self.parent.parent.tileSize
        self.gridY=self.pos.getY()/self.parent.parent.tileSize
        
        self.node=render.attachNewNode("LineMember%d" % number)
        self.node.setPos(self.pos)
        actor.instanceTo(self.node)
    def setAngle(self,angle):
        self.angle=angle
        self.node.setH(angle)
    def moveFront(self,angle):
        self.angle=angle
        #print round(self.node.getY(),2)%self.parent.parent.tileSize, round(self.node.getX(),2)%self.parent.parent.tileSize
        if not round(self.node.getY(),2)%self.parent.parent.tileSize and not round(self.node.getX(),2)%self.parent.parent.tileSize:
            self.setGrid()
        self.moveTo()
    def move(self,front):
        if not self.canMove:
           # print front.gridX
            if front.gridX!=self.gridX or front.gridY!=self.gridY:
                self.canMove=1
        if self.canMove:
            if not round(self.node.getY(),2)%self.parent.parent.tileSize and not round(self.node.getX(),2)%self.parent.parent.tileSize:
                self.setGrid()
                if front.gridX!=self.gridX:
                    self.angle=270 if front.gridX<self.gridX else 90
                else: self.angle=0 if front.gridY<self.gridY else 180
            self.moveTo()
    def setGrid(self):
        self.gridX=self.node.getX()/self.parent.parent.tileSize
        self.gridY=self.node.getY()/self.parent.parent.tileSize
        
            
    def moveTo(self):
        angle=self.node.getH()
        if abs(angle-360-self.angle)<abs(angle-self.angle):angle-=360
        elif abs(angle+360-self.angle)<abs(angle-self.angle):angle+=360
        if self.angle>angle:
            angle+=TURNSPEED
            if angle>self.angle:angle=angle
        elif self.angle<angle:
            angle-=TURNSPEED
            if angle<self.angle:angle=self.angle
        angle=angle%360
        self.node.setH(angle)
        
        
        angle = math.radians(self.angle)
        dx = CONGASPEED * math.sin(angle)
        dy = CONGASPEED * -math.cos(angle)
        
        self.node.setPos(self.node.getX() + dx, self.node.getY() + dy, 0)