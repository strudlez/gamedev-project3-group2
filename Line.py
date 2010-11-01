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
    def hitMember(self,x,y):
        for i in range(1,len(self.members)):
            if self.members[i].gridX==x and self.members[i].gridY==y:
                for j in range(i,len(self.members)):
                    self.members[-1].delete()
                    self.members.pop(-1)
                self.members[0].levelWalker.set()
                break
    def move(self,elapsed,keymap):
        if keymap["add"]:
            keymap["add"]=0
            self.addMember()
        top=self.members[0]
        if keymap["left"] and (self.angle-self.cameraAngle)%180!=90:
            self.angleTo=90+self.cameraAngle
            #print (self.angle+self.cameraAngle)%360
            
            self.turn='l'
            keymap["left"]=0
        elif keymap["right"] and (self.angle-self.cameraAngle)%180!=90:
            self.angleTo=270+self.cameraAngle
            self.turn='r'
            keymap["right"]=0
        elif keymap["forward"] and (self.angle-self.cameraAngle)%180!=0:
            self.angleTo=0+self.cameraAngle
            keymap["forward"]=0
        elif keymap["backwards"] and (self.angle-self.cameraAngle)%180!=0:
            self.angleTo=180+self.cameraAngle
            keymap["backwards"]=0
        self.angleTo=self.angleTo%360
        if self.canTurn and not round(top.node.getY(),2)%TILESIZE and not round(top.node.getX(),2)%TILESIZE:
                self.angle=self.angleTo
                self.canTurn=0
        if not self.longLine and (self.cameraAngle-self.angle)%360==180:
            self.cameraAngle=(self.cameraAngle+(90 if self.turn=='l' else -90))%360
            self.cameraDiff=180 if self.turn=='l' else -180
        
            #print camera.getH(),self.cameraDiff,self.lastAngle
        else:
            self.canTurn=1
        ret=top.moveFront(self.angle)
        for i in range(1,len(self.members)):
            self.members[i].move(self.members[i-1])
        if ret:
            print len(self.members)
            self.hitMember(top.gridX,top.gridY)
            print len(self.members)
        angleTo=self.cameraAngle+self.cameraDiff
        camera.setH(turnAngle(camera.getH(),angleTo,TURNSPEED))
        #camera.setP(-90)
        camera.setP(moveInc(camera.getP(),self.cameraDown,0.07))
        camera.setPos(top.node.getPos())
        self.cameraCurrDist=moveInc(self.cameraCurrDist,self.cameraDist,0.07)
        #camera.setPos(camera,0,-30,0)
        camera.setPos(camera,0,-self.cameraCurrDist,0)
        #camera.setP(-90)
        #camera.lookAt(self.actor)
        #print camera.
