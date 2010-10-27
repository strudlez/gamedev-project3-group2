from LineMember import LineMember
from direct.actor.Actor import Actor #for animated models
from pandac.PandaModules import * #basic Panda modules
import math
from Globals import *

class Line:
    def __init__(self,parent):
        self.parent=parent
        self.angle=90
        self.angleTo=90
        self.canTurn=0
        self.members=[]
        self.frontPos=Vec3(0,0,0)
        
        self.pos=[]
        self.actor=Actor("models/panda-model", {"walk": "models/panda-walk4", "eat": "models/panda-eat"})
        #self.actor.setControlEffect("eat", 1)
        self.actor.setScale(.0005)
        #self.actor.setH(self.angle)
        #self.actor.reparentTo(render)
        for i in range(2):
            self.addMember()
    def addMember(self):
        back=None
        if len(self.members):
            back=self.members[-1]
        member=LineMember(self,self.actor,back,len(self.members)+1)
        self.members.append(member)
        
    def move(self,elapsed,keymap):
        if keymap["add"]:
            keymap["add"]=0
            self.addMember()
        top=self.members[0]
        if keymap["left"] and self.angle!=270:
            self.angleTo=90
        elif keymap["right"] and self.angle!=90:
            self.angleTo=270
        elif keymap["forward"] and self.angle!=180:
            self.angleTo=0
        elif keymap["backwards"] and self.angle!=0:
            self.angleTo=180
        if self.canTurn and not round(top.node.getY(),2)%TILESIZE and not round(top.node.getX(),2)%TILESIZE:
                self.angle=self.angleTo
                self.canTurn=0
        else:
            self.canTurn=1
        top.moveFront(self.angle)
        for i in range(1,len(self.members)):
            self.members[i].move(self.members[i-1])
        camera.setH(180)
        camera.setP(0)
        camera.setPos(top.node.getPos())
        camera.setPos(camera,0,0,30)
        camera.setP(-90)
        #camera.lookAt(self.actor)
        #print camera.