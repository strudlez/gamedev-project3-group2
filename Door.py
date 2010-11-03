class Door:
    def __init__(self,actor,num,x,y,angle):
        self.falling=0
        self.fallDir=1
        self.dead=0
        self.node=render.attachNewNode("Door%d" % num)
        self.node.setScale(1.5)
        actor.instanceTo(self.node)
        
        self.node.setPos(x,y,0)
        self.node.setH(angle)
    def delete(self):
        self.node.removeNode()
    def fall(self,dir):
        if self.falling:return
        self.falling=1
        self.fallDir=dir*3
    
    def move(self):
        if self.falling and not self.dead:
            self.node.setP(self.node.getP()+self.fallDir)
            if self.node.getP()>90:
                self.node.setP(90)
                #self.dead=1
            elif self.node.getP()<-90:
                self.node.setP(-90)
                #self.dead=1
    def unDie(self):
        self.falling=0
        self.dead=0
        self.setP(0)