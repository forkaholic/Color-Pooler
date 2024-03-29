from PySide2 import QtWidgets as QtW

from sys import exit
from View import View

class Controller:
    def __init__(self, argv):
        # Create app before anything else
        self.app = QtW.QApplication(argv)
        self.app.setApplicationName("Color Pooler")

        self.stitches = 10
        self.window = 10
        self.mode = 0

        # Create full MVC arch
        self.view = View(self)

        # Show window containing initial view
        self.view.show()

        # Enable app, exit after window is closed
        exit(self.app.exec_())

    def addButtonPressed(self):
        self.view.addColor()

    def applyButtonPressed(self):
        self.view.clearGrid()
        if len(self.view.cWGWidgets) == 0: return
        values = self.view.getValues()
        if self.stitches < self.window:
            self.window = self.stitches
        self.view.setGrid(values, self.stitches, self.mode, self.window)        

    def setMode(self, mode):
        self.mode = mode

    def setStitches(self, stitches):
        self.stitches = stitches

    def setWindow(self, window):
        self.window = window




