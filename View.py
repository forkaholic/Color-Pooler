from PySide2 import QtWidgets as QtW
from PySide2 import QtGui as QtG
from PySide2 import QtCore as QtC

import CustomWidgets as CW

class View(QtW.QWidget):
    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller
        self.cWGWidgets = []

        # Set up basic layout of UI

        # Grid layout for sample
        leftScroll = self._createLeftView()

        # Layout for right side, scrollable color area then buttons
        rightSide = QtW.QWidget()
        rightSide.setFixedWidth(400)
        rightLayout = QtW.QVBoxLayout()

        # Create scrollArea for CWGs
        scrollArea = self._createScroll()

        # Set the layout of the scroll area to vertical
        self.addColor()

        # Add scroll to right layout
        rightLayout.addWidget(scrollArea)
        # rightLayout.setAlignment(scrollWidget, QtC.Qt.AlignTop)

        # Options Layout
        options = self._createOptions()

        # Button layout
        buttons = self._createButtons()

        # Add buttons to right layout
        rightLayout.addWidget(options)
        rightLayout.addWidget(buttons)
        rightSide.setLayout(rightLayout)

        # Add both sides to layout
        layout = QtW.QHBoxLayout()
        layout.addWidget(leftScroll)
        layout.addWidget(rightSide)

        self.setLayout(layout)
    
    def createGrid(self):
        grid = QtW.QGridLayout()
        grid.setSpacing(1)
        return grid

    def grid(self):
        return self.leftSide.layout()
    
    def clearGrid(self):
        
        children = self.leftSide.children()
        for i in range(len(children)-1, 0, -1):
            children[i].setParent(None)


############################## CREATE VIEW OBJECTS

    def _createLeftView(self):
        # Set max/min sizes here self.grid()....
        self.leftSide = QtW.QWidget()
        self.leftSide.setFixedSize(800,800)

        grid = self.createGrid()

        self.leftSide.setLayout(grid)

        leftScroll = QtW.QScrollArea()
        leftScroll.setFixedSize(800,800)
        # leftScroll.setWidgetResizable(True)   
        leftScroll.setWidget(self.leftSide)

        return leftScroll
    
    def _createOptions(self):
        options = QtW.QWidget()
        optionsLayout = QtW.QHBoxLayout()

        rows = CW.LabelledBox("Rows in preview", 10, lambda x: self.controller.setRows(x))

        stitches = CW.LabelledBox("Stitches per row", 10, lambda x: self.controller.setStitches(x))

        window = CW.LabelledBox("Stitchs in preview", 10, lambda x: self.controller.setWindow(x))

        radioLayout = QtW.QVBoxLayout()

        flat = QtW.QRadioButton("Flat")
        flat.toggled.connect(lambda: self.controller.setMode(0))
        circular = QtW.QRadioButton("Circular")
        circular.toggled.connect(lambda: self.controller.setMode(1))
        flat.setChecked(True)

        radioLayout.addWidget(flat)
        radioLayout.addWidget(circular)

        radioWidget = QtW.QWidget()
        radioWidget.setLayout(radioLayout)

        optionsLayout.addWidget(rows)
        optionsLayout.addWidget(stitches)
        optionsLayout.addWidget(window)
        optionsLayout.addWidget(radioWidget)
        options.setLayout(optionsLayout)

        options.setFixedSize(400,100)

        return options


    def _createButtons(self):
        buttons = QtW.QWidget()
        buttonsLayout = QtW.QHBoxLayout()

        add = QtW.QPushButton("Add new Color")
        add.setFixedSize(150, 50)
        add.clicked.connect(self.controller.addButtonPressed)
        buttonsLayout.addWidget(add)

        apply = QtW.QPushButton("Apply Changes")
        add.setFixedSize(150, 50)
        apply.clicked.connect(self.controller.applyButtonPressed)
        buttonsLayout.addWidget(apply)
        
        buttons.setLayout(buttonsLayout)
        
        return buttons
    
    def _createScroll(self):
        # Widget that contans CWG
        scrollWidget = QtW.QWidget()
        # scrollWidget.setGeometry(QtC.QRect(0,0,400,600))
        scrollWidget.setFixedWidth(400)

        # Signify that scrollWidget has scroll bar
        scrollArea = QtW.QScrollArea()
        # scrollArea.setGeometry(QtC.QRect(0, 0, 400, 600))
        scrollArea.setFixedWidth(400)
        scrollArea.setHorizontalScrollBarPolicy(QtC.Qt.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)   
        scrollArea.setWidget(scrollWidget)

        # Scroll layout for colors
        # Layout for scrollable widget
        self._scroll = QtW.QVBoxLayout(scrollWidget)
        return scrollArea

##############################

############################## ABSTRACTION FOR CONTROLLER

    # mode = 0 is flat, 1 is circular
    # Assuming window is less than stitches
    def setGrid(self, colors, rows, stitches, mode, window):
        durations, widgets = self._createGridWidgets(colors)
        values = self._allocateGrid(durations, rows, stitches, mode, window)
        
        for row in range(len(values)):
            for col in range(len(values[0])):
                self.grid().addWidget(widgets[values[row][col]].copy(),row,col)


    def _allocateGrid(self, durations, rows, stitches, mode, window):        
        modifier = True if mode == 0 else False

        def colorGenerator(durations):
            while True:
                # Ouputs color index durations[i] times in a row, 
                # then next color index for durations[i+1] times... etc 
                for i in range(len(durations)):
                    for _ in range(durations[i]):
                        yield i

        currentColor = colorGenerator(durations)
        # passes = [0] * len(durations)

        # window of 10, stitches of 20, flat

        #       NOT VISIBLE   (outWindow)                                  VISIBLE (inWindow)
        
        # 100, 99,  98,  97,  96,  95,  94,  93,  92,  91  #  90,  89,  88,  87,  86,  85,  84,  83,  82,  81
        # 61,  62,  63,  64,  65,  66,  67,  68,  69,  70  #  71,  72,  73,  74,  75,  76,  77,  78,  79,  80
        # 60,  59,  58,  57,  56,  55,  54,  53,  52,  51  #  50,  49,  48,  47,  46,  45,  44,  43,  42,  41
        # 21,  22,  23,  24,  25,  26,  27,  28,  29,  30  #  31,  32,  33,  34,  35,  36,  37,  38,  39,  40
        # 20,  19,  18,  17,  16,  15,  14,  13,  12,  11  #  10,  9,   8,   7,   6,   5,   4,   3,   2,   1

        # window of 10, stitches of 20, circular

        #       NOT VISIBLE   (outWindow)                                  VISIBLE (inWindow)
        
        # 100, 99,  98,  97,  96,  95,  94,  93,  92,  91  #  90,  89,  88,  87,  86,  85,  84,  83,  82,  81
        # 80,  79,  78,  77,  76,  75,  74,  73,  72,  71  #  70,  69,  68,  67,  66,  65,  64,  63,  62,  61
        # 60,  59,  58,  57,  56,  55,  54,  53,  52,  51  #  50,  49,  48,  47,  46,  45,  44,  43,  42,  41
        # 40,  39,  38,  37,  36,  35,  34,  33,  32,  31  #  30,  29,  28,  27,  26,  25,  24,  23,  22,  21
        # 20,  19,  18,  17,  16,  15,  14,  13,  12,  11  #  10,  9,   8,   7,   6,   5,   4,   3,   2,   1


        inWindow = window
        outWindow = stitches - window

        currentStitch = 0
        currentRow = 0
        
        # Check if stitch is in preview
        circularLambda = lambda currentStitch, currentRow, stitches, inWindow: (
            1 if currentRow * stitches <= currentStitch < currentRow * stitches + inWindow else 0
        )
        
        flatLambda = lambda currentStitch, currentRow, stitches, inWindow, outWindow: (
            circularLambda(currentStitch, currentRow, stitches, inWindow) if currentRow % 2 == 0 else (
                2 if currentRow * stitches + outWindow <= currentStitch < (currentRow + 1) * stitches else 0
            )
        )

        grid = [[]]

        for currentStitch in range(rows * stitches):
            # Get color of current stitch
            color = next(currentColor)

            # Check current row
            if (currentRow + 1) * stitches + currentStitch % stitches <= currentStitch:
                currentRow += 1
                grid += [[]]

            flat = flatLambda(currentStitch, currentRow, stitches, inWindow, outWindow)
            circular = circularLambda(currentStitch, currentRow, stitches, inWindow)


            # Determine if the fabric is in flat or circular mode, and whether or not it is in view  
            if not (modifier and flat) and \
               not (not modifier and circular):
                
                # Not in view, continue to next iteration
                continue

            if modifier and flat == 2: grid[-1].append(color)
            else:                      grid[-1].insert(0, color)
            
        grid.reverse()
        return grid
        

    # def clearGrid(self):
    #     (self.grid().removeWidget(x) for x in self.grid().children())

    def _createGridWidgets(self, values):
        durations = []
        widgets = []
        for colors in values:
            widgets += [CW.ColorSample(colors[0], colors[1], colors[2])]
            durations += [colors[3]]
        return (durations, widgets)

    def addColor(self):
        self.cWGWidgets += [CW.ColorWidgetGroup(self)]
        self._scroll.addWidget(self.cWGWidgets[-1], stretch=0)
        self._scroll.setAlignment(self.cWGWidgets[-1], QtC.Qt.AlignTop)

    def getValues(self):
        values = []
        for cWG in self.cWGWidgets:
            values += cWG.getValues()     
        return values

    def upCWG(self, cwg):
        index = self.cWGWidgets.index(cwg)
        if index <= 0: return

        swap = self.cWGWidgets[index-1]
        self.cWGWidgets[index-1] = self.cWGWidgets[index]
        self.cWGWidgets[index] = swap


    def downCWG(self, cwg):
        index = self.cWGWidgets.index(cwg)
        if index >= len(self.cWGWidgets) - 1: return

        swap = self.cWGWidgets[index + 1]
        self.cWGWidgets[index+1] = self.cWGWidgets[index]
        self.cWGWidgets[index] = swap

##############################
