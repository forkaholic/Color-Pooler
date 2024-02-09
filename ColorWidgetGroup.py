from PySide2 import QtWidgets as QtW
from PySide2 import QtGui as QtG
from PySide2 import QtCore as QtC
from NumberTextBox import NumberTextBox as NTB

class ColorWidgetGroup(QtW.QWidget):
    
    def __init__(self, controller, r=255, g=255, b=255, length=10):
        super().__init__()
        # True parent is VBox, setting it as View regardless
        self.controller = controller
        
        layout = QtW.QHBoxLayout()
        self.setGeometry(QtC.QRect(0,0,350,100))
        self.setContentsMargins(0,5,0,5)

        self.textBoxes = [
            NTB(self, r),   # R
            NTB(self, g),   # G
            NTB(self, b),   # B
            NTB(self, length, top=1000)     # Count
            #,up button,
            #down button
        ]
        
        self.colorSample = ColorSample(r, g, b)

        close = QtW.QPushButton("X")
        close.setFixedSize(20,20)
        close.clicked.connect(self.delete)

        layout.addWidget(self.textBoxes[0])
        layout.addWidget(self.textBoxes[1])
        layout.addWidget(self.textBoxes[2])
        layout.addWidget(self.colorSample)
        layout.addWidget(self.textBoxes[3])
        layout.addWidget(close)

        self.setLayout(layout)

    def __len__(self):
        return len(self.textBoxes)

    def getValues(self):
        return [[i.getValueAsInt() for i in self.textBoxes]]

    def update(self):
        func = lambda x: self.textBoxes[x].getValueAsInt() 
        r = func(0)
        g = func(1)
        b = func(2)
        self.colorSample.setPalette(r, g, b)
        
    def delete(self):
        self.controller.cWGWidgets.remove(self)
        self.setParent(None)

class ColorSample(QtW.QWidget):
    def __init__(self, r=0, g=0, b=0, size=40):
        super(ColorSample, self).__init__()
        self.setMinimumSize(size, size)
        self.setAutoFillBackground(True)
        self.setPalette(r, g, b)

    def setPalette(self, r, g, b):
        palette = QtG.QPalette()
        palette.setColor(
            QtG.QPalette.Window,
            QtG.QColor(r, g, b, 255)
        )
        super().setPalette(palette)
    
    def copy(self):
        cs = ColorSample()
        r,g,b,_ = self.palette().color(QtG.QPalette.Window).getRgb()
        cs.setPalette(r,g,b)
        return cs