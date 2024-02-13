from PySide2 import QtWidgets as QtW
from PySide2 import QtCore as QtC
from PySide2 import QtGui as QtG

class ColorWidgetGroup(QtW.QWidget):
    def __init__(self, controller, r=255, g=255, b=255, length=10):
        super().__init__()
        # True parent is VBox, setting it as View regardless
        self.controller = controller
        
        layout = QtW.QHBoxLayout()
        
        self.setGeometry(0,0,350,50)
        self.setContentsMargins(0,5,0,5)

        self.textBoxes = [
            NumberTextBox(self, r),   # R
            NumberTextBox(self, g),   # G
            NumberTextBox(self, b),   # B
            NumberTextBox(self, length, top=1000)     # Count
        ]
        
        self.colorSample = ColorSample(r, g, b)
        self.colorSample.setFixedSize(40,40)

        close = QtW.QPushButton("X")
        close.setFixedSize(20,20)
        close.clicked.connect(self.delete)

        upDown = UpDownWidget(self)

        layout.addWidget(self.textBoxes[0])
        layout.addWidget(self.textBoxes[1])
        layout.addWidget(self.textBoxes[2])
        layout.addWidget(self.colorSample)
        layout.addWidget(self.textBoxes[3])
        layout.addWidget(close)
        layout.addWidget(upDown)
        
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
        
    def up(self):
        self.controller.upCWG(self)

    def down(self):
        self.controller.downCWG(self)

    def delete(self):
        self.controller.cWGWidgets.remove(self)
        self.setParent(None)

    def apply(self):
        self.controller.apply()

class ColorSample(QtW.QWidget):
    def __init__(self, r=0, g=0, b=0, size=40):
        super(ColorSample, self).__init__()
        self.setGeometry(QtC.QRect(0,0,size,size))
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
    
class LabelledBox(QtW.QWidget):
    def __init__(self, labelText, value, updateValueFunc, applyFunc):
        super().__init__()

        self.updateValueFunc = updateValueFunc
        self.applyFunc = applyFunc

        layout = QtW.QVBoxLayout()
        label = QtW.QLabel(labelText)
        label.setMinimumWidth(125)
        self.text = NumberTextBox(value=value, bottom=1)
        label.setFont(self.text.font().setPointSize(5))

        layout.addWidget(label)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def apply(self):
        self.applyFunc()

    def update(self):
        self.updateValueFunc(self.text.getValueAsInt())


class AdjustableLabelBox(QtW.QWidget):
    def __init__(self, text, value, func, applyFunc):
        super().__init__()

        layout = QtW.QHBoxLayout()

        self.lb = LabelledBox(text, value, func, applyFunc)

        ud = UpDownWidget(self)

        layout.addWidget(self.lb)
        layout.addWidget(ud)

        self.setLayout(layout)

    def up(self):
        self.lb.text.setText(str(int(self.lb.text.text()) + 1))

    def down(self):
        self.lb.text.setText(str(int(self.lb.text.text()) - 1))

class NumberTextBox(QtW.QLineEdit):

    def __init__(self, parent=None, value=0, bottom=0, top=255):
        super().__init__(str(value), parent)
        self.setFixedSize(40,40)
        self.textChanged.connect(self.updateColor)
        self.setValidator(QtG.QIntValidator(bottom, top))
        self.returnPressed.connect(self.apply)

    def apply(self):
        self.parent().apply()

    def updateColor(self):
        self.parent().update()

    def getValueAsInt(self):
        val = 0
        if self.text().isnumeric(): 
            val = int(self.text())
        return val

class UpDownWidget(QtW.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QtW.QVBoxLayout()
        up = QtW.QPushButton("▲")
        down = QtW.QPushButton("▼")
        
        up.clicked.connect(self.up)
        down.clicked.connect(self.down)

        layout.addWidget(up)
        layout.addWidget(down)

        self.setLayout(layout)

    def up(self):
        self.controller.up()

    def down(self):
        self.controller.down()
