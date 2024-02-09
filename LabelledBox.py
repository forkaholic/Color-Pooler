from PySide2 import QtWidgets as QtW
from PySide2 import QtGui as QtG
from PySide2 import QtCore as QtC
import NumberTextBox as NTB

class LabelledBox(QtW.QWidget):
    def __init__(self, labelText, value, func):
        super().__init__()

        self.func = func

        layout = QtW.QVBoxLayout()
        label = QtW.QLabel(labelText)
        label.setMinimumWidth(125)
        self.text = NTB.NumberTextBox(value=value, bottom=1)
        label.setFont(self.text.font().setPointSize(5))

        layout.addWidget(label)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def update(self):
        self.func(self.text.getValueAsInt())
