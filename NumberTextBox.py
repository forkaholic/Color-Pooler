from PySide2 import QtWidgets as QtW
from PySide2 import QtGui as QtG

class NumberTextBox(QtW.QLineEdit):

    def __init__(self, parent=None, value=0, bottom=0, top=255):
        super().__init__(str(value), parent)
        self.setFixedSize(40,40)
        self.textChanged.connect(self.apply)
        self.setValidator(QtG.QIntValidator(bottom, top))

    def apply(self):
        self.parent().update()

    def getValueAsInt(self):
        val = 0
        if self.text().isnumeric(): 
            val = int(self.text())
        return val
    
