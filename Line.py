from LineMember import LineMember

class Line:
    def __init__(self,parent):
        self.parent=parent
        self.dir='l'
        self.angle=0
        self.members=[]
    def move(self,elapsed,keymap):
        if self.keymap["left"] and self.dir!='r': self.dir='l'
        elif self.keymap["right"] and self.dir!='l': self.dir='r'
        elif self.keymap["forward"] and self.dir!='d': self.dir='u'
        elif self.keymap["back"] and self.dir!='u': self.dir='d'
