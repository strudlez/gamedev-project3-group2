from pandac.PandaModules import * #basic Panda modules
from pandac.PandaModules import *
from Globals import *
from LevelWalker import LevelWalker,Location
import math
import Globals

class LineMember():
    def __init__(self,parent,actor,front,number):
        self.parent=parent
        self.pos=Vec3(0,0,0)
        if front==None:
            self.angle=0
            
        else:
            self.angle=front.angle
            self.pos.setX(front.gridX*TILESIZE)
            self.pos.setY(front.gridY*TILESIZE)
        
        self.canMove=0
        
        self.gridX=self.pos.getX()/TILESIZE
        self.gridY=self.pos.getY()/TILESIZE
        
        self.levelWalker=LevelWalker(self.parent.parent.level,Location(self.gridX,self.gridY))
        
        self.node=render.attachNewNode("LineMember%d" % number)
        self.node.setPos(self.pos)
        self.node.setH(self.angle)
        actor.instanceTo(self.node)
    def setAngle(self,angle):
        self.angle=angle
        self.node.setH(angle)
    def moveFront(self,angle):
        self.angle=angle
        if not round(self.node.getY(),2)%TILESIZE and not round(self.node.getX(),2)%TILESIZE:
            self.setGrid()
            dir={0:'U',180:'D',270:'L',90:'R'}[self.angle]
            self.levelWalker.walk(dir)
        self.moveTo()
    def move(self,front):
        if not self.canMove:
            if front.gridX!=self.gridX or front.gridY!=self.gridY:
                self.canMove=1
        if self.canMove:
            if not round(self.node.getY(),2)%TILESIZE and not round(self.node.getX(),2)%TILESIZE:
                self.setGrid()
                if front.gridX!=self.gridX:
                    self.angle=270 if front.gridX<self.gridX else 90
                else: self.angle=0 if front.gridY<self.gridY else 180
                
                dir={0:'U',180:'D',270:'L',90:'R'}[self.angle]
                self.levelWalker.walk(dir)

            self.moveTo()
    def setGrid(self):
        self.gridX=self.node.getX()/TILESIZE
        self.gridY=self.node.getY()/TILESIZE
        
        
            
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
        self.node.setH(self.angle)
        
        
        angle = math.radians(self.angle)
        dx = Globals.CONGASPEED * math.sin(angle)
        dy = Globals.CONGASPEED * -math.cos(angle)
        
        self.node.setPos(self.node.getX() + dx, self.node.getY() + dy, 0)
        Globals.CONGASPEED=0