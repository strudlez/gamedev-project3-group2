from pandac.PandaModules import * #basic Panda modules

from pandac.PandaModules import *

class LineMember():
    def __init__(self,parent,actor):
        self.parent=parent
        self.node=NodePath()
        
        self.pos=Vec3
        actor.instanceTo(self.node)
        #self.node.reparentTo(render)

