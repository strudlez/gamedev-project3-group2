from LineMember import LineMember
from LineLeaver import LineLeaver
from direct.actor.Actor import Actor #for animated models
from pandac.PandaModules import * #basic Panda modules
import math
import random
from Globals import *
import Globals
import LevelConstants
from Partier import Partier
from direct.filter.CommonFilters import CommonFilters
from LevelWalker import LevelWalker
from LevelLocation import LevelLocation

class Line:
    def __init__(self,parent):
        self.parent=parent
        self.angle=90
        self.angleTo=90
        
        self.cameraDiff=180
        self.cameraAngle=0
        self.cameraDist=70
        self.cameraCurrDist=self.cameraDist
        self.cameraDown=-70
        camera.setH((self.cameraAngle+self.cameraDiff)%360)
        camera.setP(self.cameraDown)
        self.turn='r'
        self.canTurn=0
        self.members=[]
        self.frontPos=Vec3(0,0,0)
        self.topX=0
        self.topY=0
        
        self.dashX=0
        self.dashY=0
        
        self.congaDash=0
        
        self.pos=[]
        #self.actor=Actor("models/panda-model", {"walk": "models/panda-walk4", "eat": "models/panda-eat"})
        self.playerActor=Actor("models/player", {"walk": "models/conga"})
        self.playerActor.loop("walk")
        colors=['white','yellow','black','purple','blue','red']
        colors=['yellow','purple','blue','red']
        self.walkers=[]
        for i in colors:
            self.walkers.append(Actor("models/%s" %i , {"walk": "models/conga"}))
            self.walkers[-1].loop("walk")
        
        self.longLine=1
        self.staticCam=1
        for i in range(1):
            self.addMember()
        self.longLine=0
        
        #~ self.longLine=1
        #~ self.cameraDown=-90
        #~ camera.setP(-90)
        #~ camera.setH(90)
        #~ self.cameraAngle=0
        #~ self.cameraDist=100
        #~ self.cameraCurrDist=self.cameraDist
        
    def addMember(self):
        back=None
        if len(self.members):
            back=self.members[-1]
        actor=self.walkers[random.randint(0,len(self.walkers)-1)]
        if len(self.members)==0:
            actor=self.playerActor
        member=LineMember(self,actor,back,len(self.members)+1)
        self.members.append(member)
        for i in self.members:
            i.levelWalker.set()
        if not self.longLine:
            if self.cameraDown<=-40:
                self.staticCam=1
            if self.cameraDown<=-75:
                self.longLine=1
                self.cameraDown=-75
            else:
                self.cameraDist+=Globals.CAMERA_MOVE
                self.cameraDown-=Globals.CAMERA_MOVE_ANGLE
        if self.congaDash: Globals.CONGASPEED=0.8
        else: Globals.CONGASPEED=Globals.CONGASTEP*(len(self.members))/4+0.1

    def hitPartier(self,x,y):
        self.parent.sc+=200
        print 'hit partier'
        temp = LevelWalker(Globals.currentLevel, LevelLocation(self.members[0].levelWalker._location.grid,x,y), set = False)
        # scan the partiers list for nearest partier
        w = self.members[0].levelWalker
        for partier in Partier.all:
            if partier.collidesWith(temp):
                partier.destroy()
                self.addMember()
                break
        
    def hitMember(self,x,y):
        x=self.members[0].levelWalker._location.x
        y=self.members[0].levelWalker._location.y
        for i in range(1,len(self.members)):
            #if self.members[i].gridX==x and self.members[i].gridY==y:
            if self.members[i].levelWalker._location.x==x and self.members[i].levelWalker._location.y==y:
                for j in range(i,len(self.members)):
                    self.parent.sc-=50
                    self.parent.leaving.append(LineLeaver(self.members[i].actor,self.members[i].node.getPos(),(self.members[i].angle+180)%360,len(self.parent.leaving)))
                    self.members[i].delete()
                    self.members.pop(i)
                break
        for i in self.members:
            self.members[0].levelWalker.set()
        if self.congaDash: Globals.CONGASPEED=0.8
        else: Globals.CONGASPEED=Globals.CONGASTEP*(len(self.members))/4+0.1
        
    def hitWall(self):
        self.parent.sc-=200
        self.members.reverse()
        num=int(math.ceil(len(self.members)/4.0))
        if not self.congaDash:
            for i in range(0,num):
                self.parent.leaving.append(LineLeaver(self.members[-1].actor,self.members[-1].node.getPos(),self.members[-1].angle+random.randint(-45,45),len(self.parent.leaving)))
                if(len(self.members)<=1):
                    break
                self.members[-1].delete()
                self.members.pop(-1)
        else:
            self.members[-1].actor=self.playerActor
            self.members[-1].node.getChildren().clear()
            pos=self.members[-1].node.getPos()
            hpr=self.members[-1].node.getHpr()
            self.members[-1].node.removeNode()
            self.members[-1].node=render.attachNewNode("LineMember%d" % self.members[0].number)
            self.members[-1].node.setPos(pos)
            self.members[-1].node.setHpr(hpr)
            self.walkers[random.randint(0,len(self.walkers)-1)].instanceTo(self.members[-1].node)
            self.stopDash()
        for i in self.members:
            #i.node.setH((self.members[0].angle+180)%360)
            #i.angle=(i.angle+180)%360
            
            i.angle=(i.angle+180)%360
            i.levelWalker.unset()
            dir={0:'U',180:'D',270:'L',90:'R'}[i.angle]
            i.levelWalker.walk(dir)
        self.angleTo=self.angle=self.members[0].angle
        self.members[0].actor=self.playerActor
        self.members[0].node.getChildren().clear()
        pos=self.members[0].node.getPos()
        hpr=self.members[0].node.getHpr()
        self.members[0].node.removeNode()
        self.members[0].node=render.attachNewNode("LineMember%d" % self.members[0].number)
        self.members[0].node.setPos(pos)
        self.members[0].node.setHpr(hpr)
        self.playerActor.instanceTo(self.members[0].node)
        if self.congaDash: Globals.CONGASPEED=0.8
        else: Globals.CONGASPEED=Globals.CONGASTEP*(len(self.members)-1)/4+0.1

    def hitDoor(self):
        self.parent.sc+=500
        if self.congaDash:
            doors=self.parent.doors
            door=None
            dist=-1
            top=self.members[0]
            for i in doors:
                d=math.sqrt((top.node.getX()-i.node.getX())**2 + (top.node.getY()-i.node.getY())**2)
                
                if dist==-1 or d<dist:
                    dist=d
                    door=i
            dir=1
            x,y=top.levelWalker._location.x,top.levelWalker._location.y
            for x,y in ((x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)):
                if Globals.currentLevel._grids[top.levelWalker._location.grid].getCell(x, y)==LevelConstants.DOOR:
                    Globals.currentLevel._grids[top.levelWalker._location.grid].setCell(x, y,0)
            top.levelWalker.set()
            if top.angle!=door.node.getH():dir=-1
            door.fall(dir)
            
        else: self.hitWall()
    def stopDash(self):
        self.congaDash=0
        Globals.CONGASPEED=Globals.CONGASTEP*(len(self.members)-1)/4+0.1

    def move(self,elapsed,keymap):
        top=self.members[0]
        self.parent.congp.setScale(.001*self.parent.cong,0,0.028)
        self.parent.timer.setText("Timer: %i"%self.parent.time)
        if(self.parent.sc<0):
            self.parent.sc=0
        self.parent.score.setText("Score: %i"%self.parent.sc)
        if self.congaDash and abs(self.dashX-top.levelWalker._location.x)+abs(self.dashY-top.levelWalker._location.y)>=8:
                self.stopDash()
        if(self.parent.time!=0):
            self.parent.time-=.02
        if(self.parent.cong>=300):
            self.parent.dash.setText("(Space to Dash)")
        if(self.parent.cong<300):
            self.parent.cong+=.2+.1*len(self.members)
        elif keymap['dash']:
            self.parent.cong=0
            keymap['dash']=0
            Globals.CONGASPEED=0.8
            self.congaDash=1
            self.dashX=top.levelWalker._location.x
            self.dashY=top.levelWalker._location.y
            self.parent.dash.setText("")
        self.parent.length.setText("Length: %i"%len(self.members))
        self.parent.SpeedUp.setText("SpeedUp: %i"%(4-len(self.members)%4))
        if(self.parent.max < len(self.members)):
            self.parent.max = len(self.members)
        self.parent.mlength.setText("Max Length: %i"%self.parent.max)
        if keymap["add"]:
            keymap["add"]=0
            self.addMember()
        
        #if keymap["left"] and (self.angle-self.cameraAngle)%180!=90:
        for i in range(int(Globals.CONGASPEED/Globals.CONGASTEP)):
            if keymap["left"] and (self.angle-self.cameraAngle)%360!=270:
                if COLLIDE_DEBUG:Globals.CONGASPEED = TILESIZE
                self.angleTo=90+self.cameraAngle
                #print (self.angle+self.cameraAngle)%360
                
                self.turn='l'
                keymap["left"]=0
            #elif keymap["right"] and (self.angle-self.cameraAngle)%180!=90:
            elif keymap["right"] and (self.angle-self.cameraAngle)%360!=90:
                if COLLIDE_DEBUG:Globals.CONGASPEED = TILESIZE
                self.angleTo=270+self.cameraAngle
                self.turn='r'
                keymap["right"]=0
            #elif keymap["forward"] and (self.angle-self.cameraAngle)%180!=0:
            elif keymap["forward"] and (self.angle-self.cameraAngle)%360!=180:
                if COLLIDE_DEBUG:Globals.CONGASPEED = TILESIZE
                self.angleTo=0+self.cameraAngle
                keymap["forward"]=0
            #elif keymap["backwards"] and (self.angle-self.cameraAngle)%180!=0:
            elif keymap["backwards"] and (self.angle-self.cameraAngle)%360!=0:
                if COLLIDE_DEBUG:Globals.CONGASPEED = TILESIZE
                self.angleTo=180+self.cameraAngle
                keymap["backwards"]=0
            self.angleTo=self.angleTo%360
            gridX=int(round(top.node.getX()/Globals.TILESIZE,2))
            gridY=int(round(top.node.getY()/Globals.TILESIZE,2))
            if self.canTurn and not round(top.node.getY(),2)%TILESIZE and not round(top.node.getX(),2)%TILESIZE:
            
                    self.topX=gridX
                    self.topY=gridY
                    self.angle=self.angleTo
                    self.canTurn=0
            if not self.staticCam and (self.cameraAngle-self.angle)%360==180:
                self.cameraAngle=(self.cameraAngle+(90 if self.turn=='l' else -90))%360
                self.cameraDiff=180 if self.turn=='l' else -180
            
                #print camera.getH(),self.cameraDiff,self.lastAngle
            else:
                self.canTurn=1
            
            congaspeed=Globals.CONGASPEED
            ret=top.moveFront(self.angle)
            if len(self.members)>1:
                for i in range(1,len(self.members)):
                    if COLLIDE_DEBUG:Globals.CONGASPEED=congaspeed
                    self.members[i].move(self.members[i-1])
            if ret:
                x,y,type=ret
                if type==LevelConstants.LINE_WALKER:
                    self.hitMember(top.levelWalker._location.x,top.levelWalker._location.y)
                elif type==LevelConstants.WALL or type==LevelConstants.FURNITURE:
                    self.hitWall()
                    top=self.members[0]
                    break
                elif type==LevelConstants.DOOR:
                    self.hitDoor()
                    top=self.members[0]
                    break
                elif type == LevelConstants.PARTIER:
                    self.hitPartier(x,y)
                    top = self.members[0]
                    break
                
        angleTo=self.cameraAngle+self.cameraDiff
        camera.setH(turnAngle(camera.getH(),angleTo,TURNSPEED))
        
        camera.setP(moveInc(camera.getP(),self.cameraDown,0.07))
        camera.setPos(top.node.getPos())
        curDist=self.cameraCurrDist=moveInc(self.cameraCurrDist,self.cameraDist,0.07)
        x,y=top.levelWalker._location.x,top.levelWalker._location.y
        
        camera.setPos(camera,0,-curDist,0)
        
        
