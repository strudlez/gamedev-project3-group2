from LineMember import LineMember
from direct.actor.Actor import Actor #for animated models
import math

class Line:
    def __init__(self,parent):
        self.parent=parent
        self.dir='l'
        self.angle=90
        self.angleTo=90
        self.canTurn=0
        self.members=[]
        self.pos=[]
        self.actor=Actor("models/panda-model", {"walk": "models/panda-walk4", "eat": "models/panda-eat"})
        self.actor.setControlEffect("eat", 1)
        self.actor.setScale(.0005)
        self.actor.setH(self.angle)
        self.actor.reparentTo(render)
    def move(self,elapsed,keymap):
        """if keymap["left"] and self.dir!='r':
            self.dir='l'
            self.angle=90
        elif keymap["right"] and self.dir!='l':
            self.dir='r'
            self.angle=270
        elif keymap["forward"] and self.dir!='d':
            self.dir='u'
            self.angle=0
        elif keymap["backwards"] and self.dir!='u':
            self.dir='d'
            self.angle=180"""
        if keymap["left"]:
            self.angleTo=self.angle+90
            keymap["left"]=0
        if keymap["right"]:
            self.angleTo=self.angle-90
            keymap["right"]=0
        self.angleTo=self.angleTo%360
        if self.canTurn and not round(self.actor.getY(),2)%self.parent.tileSize and not round(self.actor.getX(),2)%self.parent.tileSize:
                self.angle=self.angleTo
                self.canTurn=0
        else:
            self.canTurn=1
        
        angle=self.actor.getH()
        if abs(angle-360-self.angle)<abs(angle-self.angle):angle-=360
        elif abs(angle+360-self.angle)<abs(angle-self.angle):angle+=360
        if self.angle>angle:
            angle+=8
            if angle>self.angle:angle=angle
        elif self.angle<angle:
            angle-=8
            if angle<self.angle:angle=self.angle
        angle=angle%360
        self.actor.setH(angle)
        dist = 0.1
        angle = math.radians(self.angle)
        dx = dist * math.sin(angle)
        dy = dist * -math.cos(angle)
        self.actor.setPos(self.actor.getX() + dx, self.actor.getY() + dy, 0)
        
        
        camera.setPos(self.actor,0,10000,2000)
        camera.lookAt(self.actor)
