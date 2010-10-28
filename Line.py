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
        

        self.cameraDiff=180
        self.cameraAngle=180
        self.cameraDist=6
        self.cameraCurrDist=6
        self.cameraDown=-20
        camera.setH(0)
        camera.setP(self.cameraDown)
        self.turn='r'
        self.canTurn=0
        self.members=[]
        self.frontPos=Vec3(0,0,0)
        
        
        self.pos=[]
        self.actor=Actor("models/panda-model", {"walk": "models/panda-walk4", "eat": "models/panda-eat"})
        #self.actor.setControlEffect("eat", 1)
        self.actor.setScale(.0005)
        #self.actor.setH(self.angle)
        #self.actor.reparentTo(render)
        self.longLine=1
        for i in range(2):
            self.addMember()
        self.longLine=0
    def addMember(self):
        back=None
        if len(self.members):
            back=self.members[-1]
        member=LineMember(self,self.actor,back,len(self.members)+1)
        self.members.append(member)
        if not self.longLine:
            if len(self.members)>=30:
                self.longLine=1
            else:
                self.cameraDist+=1
                self.cameraDown-=2
    def move(self,elapsed,keymap):
        if keymap["add"]:
            keymap["add"]=0
            self.addMember()
        top=self.members[0]
        if keymap["left"] and (self.angle+self.cameraAngle)%360!=270:
            self.angleTo=90+self.cameraAngle
            self.turn='l'
        elif keymap["right"] and (self.angle+self.cameraAngle)%360!=90:
            self.angleTo=270+self.cameraAngle
            self.turn='r'
        elif keymap["forward"] and (self.angle+self.cameraAngle)%360!=180:
            self.angleTo=0+self.cameraAngle
        elif keymap["backwards"] and (self.angle+self.cameraAngle)%360!=0:
            self.angleTo=180+self.cameraAngle
        self.angleTo=self.angleTo%360
        if self.canTurn and not round(top.node.getY(),2)%TILESIZE and not round(top.node.getX(),2)%TILESIZE:
                self.angle=self.angleTo
                self.canTurn=0
        if not self.longLine and (self.cameraAngle-self.angle)%360==180:
            self.cameraAngle=(self.cameraAngle+180)%360
            self.cameraDiff=180 if self.turn=='l' else -180
        
            #print camera.getH(),self.cameraDiff,self.lastAngle
        else:
            self.canTurn=1
        top.moveFront(self.angle)
        for i in range(1,len(self.members)):
            self.members[i].move(self.members[i-1])
        angleTo=self.cameraAngle+self.cameraDiff
        camera.setH(turnAngle(camera.getH(),angleTo,10))
        #camera.setP(-90)
        camera.setP(moveInc(camera.getP(),self.cameraDown,0.07))
        camera.setPos(top.node.getPos())
        self.cameraCurrDist=moveInc(self.cameraCurrDist,self.cameraDist,0.07)
        #camera.setPos(camera,0,-30,0)
        camera.setPos(camera,0,-self.cameraCurrDist,0)
        #camera.setP(-90)
        #camera.lookAt(self.actor)
        #print camera.
