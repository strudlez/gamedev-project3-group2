from pandac.PandaModules import * #basic Panda modules

from pandac.PandaModules import *

class LineMember(NodePath):
    def __init__(self,actor):
        actor.instanceTo(self)
        self.reparentTo(render)

