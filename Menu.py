from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib

class Menu(DirectObject):

    MENU_TEXT = 0
    MENU_VAL = 1
    MENU_IMAGE = 2

    MENU_X = 0
    MENU_Y = 0
    MENU_DX = 0
    MENU_DY = -.4
    IMAGE_SCALE = .2

    IMAGE_SELECTED = 0
    IMAGE_DESELECTED = 1

    KEY_FORWARD = 'arrow_down'
    KEY_BACKWARD = 'arrow_up'
    KEY_SELECT = 'enter'

    def __init__(self, menuOptions = None, position = (0, 0)):

        if menuOptions != None:
            self._menuOptions = menuOptions
        else:
            self._menuOptions = [
              ('Play', 0, 'menu_play'),
              ('Quit', 1, 'menu_quit')
            ]

        self._selection = 0
        self._selected = False

        self._rootNode = aspect2d.attachNewNode('menuRootNode')
        self._rootNode.setPos((position[0], 0, position[1]))

        self._menuImages = []

        x = self.MENU_X
        y = self.MENU_Y
        for item in self._menuOptions:
            filename = 'textures/' + item[self.MENU_IMAGE]
            df = filename + '_deselected.png'
            sf = filename + '_selected.png'
            deselected = OnscreenImage(image = df, pos = (x, 0, y), parent = self._rootNode)
            selected = OnscreenImage(image = sf, pos = (x, 0, y), parent = self._rootNode)
            self._menuImages.append((selected, deselected))
            selected.hide()
            for i in [selected, deselected]:
                i.setScale(self.IMAGE_SCALE)
                i.setTransparency(TransparencyAttrib.MAlpha)
            x += self.MENU_DX
            y += self.MENU_DY

        self.accept(self.KEY_FORWARD, self.moveForward)
        self.accept(self.KEY_BACKWARD, self.moveBackward)
        self.accept(self.KEY_SELECT, self.makeSelection)

        self.setSelectionIndex(self._selection)

    def setSelectionIndex(self, newSelection):
        self._setMenuItemState(self._selection, False)
        self._selection = newSelection
        self._setMenuItemState(self._selection, True)

    def getSelectionIndex(self):
        return self._selection

    def getSelection(self):
        '''returns the value corresponding to the menu item currently selected.
        Use this method instead of getSelectionIndex.'''
        return self._menuOptions[self._selection][self.MENU_VAL]

    def getLen(self):
        return len(self._menuOptions)

    def moveForward(self):
        a = self.getSelectionIndex()
        a += 1
        if a < self.getLen():
            self.setSelectionIndex(a)

    def moveBackward(self):
        a = self.getSelectionIndex()
        a -= 1
        if a >= 0:
            self.setSelectionIndex(a)

    def makeSelection(self):
        self._selected = True
        self._setMenuItemState(self._selection, False)
        # TODO do some animation to show selection was made?
        self.ignore(self.KEY_BACKWARD)
        self.ignore(self.KEY_FORWARD)

    def _setMenuItemState(self, index, selected):
        if index < 0 or index > self.getLen():
            raise Exception('menu item index out of range')
        a = self._menuImages[index]
        if selected == True:
            a[self.IMAGE_SELECTED].show()
            a[self.IMAGE_DESELECTED].hide()
        elif selected == False:
            a[self.IMAGE_SELECTED].hide()
            a[self.IMAGE_DESELECTED].show()
        else:
            raise Exception('Invalid selection state: must be true or false')

    def getSelected(self):
        return self._selected

    def destroy(self):
        self._rootNode.removeNode()
        self.ignoreAll()