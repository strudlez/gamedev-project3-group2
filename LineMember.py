from pandac.PandaModules import * #basic Panda modules

from pandac.PandaModules import *

class LineMember():
    def __init__(self,parent,actor,pos):
        self.parent=parent
        self.pos=pos
        self.node=NodePath()
        
        
        actor.instanceTo(self.node)
        #self.node.reparentTo(render)

