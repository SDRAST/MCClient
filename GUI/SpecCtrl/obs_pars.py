"""
Observations Parameters Block
"""
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
def stdSizePolicyMinimum(widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
def stdSizePolicyPreferred(widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
def stdSizePolicyExpanding(widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)

class TitledSpinbox(QtWidgets.QFrame):
  """
  Spinbox with Title
  """
  def __init__(self, parent, name, 
               title = "spinbox", minval = 0, maxval = 100):
    """
    Args:
      parent - the object which it is part of
      name   - unique widget name
      title  - the label above the spinbox
      minval - minimum allowed integer
      maxval - maximum allowed integer
    """
    QtWidgets.QFrame.__init__(self)
    stdSizePolicyMinimum(self)
    tspLayout = QtWidgets.QVBoxLayout(self)
    self.setObjectName(_fromUtf8(name))
    self.title = QtWidgets.QLabel(self)
    self.title.setEnabled(True)
    font = QtGui.QFont()
    font.setPointSize(8)
    self.title.setFont(font)
    self.title.setObjectName(_fromUtf8("title"))
    self.title.setText(QtWidgets.QApplication.translate(
                                                      parent.name, title, None))
    tspLayout.addWidget(self.title)
    self.value = QtWidgets.QSpinBox(self)
    font = QtGui.QFont()
    font.setPointSize(8)
    self.value.setFont(font)
    self.value.setMinimum(minval)
    self.value.setMaximum(maxval)
    self.value.setObjectName(_fromUtf8("value"))
    tspLayout.addWidget(self.value)

class MultiVChecks(QtWidgets.QFrame):
  """
  Checkbuttons laid out vertically
  """
  def __init__(self, parent, name, number=1, 
               enabled = [True],
               checkable = [True], 
               label = ["label"],
               tooltip = ["checkbox tooltip"]):
    """
    Args:
      parent    - the object which it is part of
      name      - unique widget name
      number    - of buttons
      enabled   - list of bool, one state for each button
      checkable - list of bool, True if user can change state
      label     - list of labels, one for each button
      tooltips  - list of tooltip textx
    """
    QtWidgets.QFrame.__init__(self)
    vChecksLayout = QtWidgets.QVBoxLayout(self)
    stdSizePolicyExpanding(self)
    self.setObjectName(_fromUtf8(name))
    self.buttonGroup = QtWidgets.QButtonGroup(self) # vChecksLayout)
    self.buttonGroup.setObjectName(_fromUtf8(name+"_bg"))
    self.button = {}
    for index in list(range(number)):
        self.button[index] = QtWidgets.QCheckBox(self)
        self.button[index].setToolTip(tooltip[index])
        self.button[index].setEnabled(enabled[index])
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button[index].setFont(font)
        self.button[index].setCheckable(checkable[index])
        self.button[index].setObjectName(_fromUtf8("button[index]"))
        self.button[index].setText(QtWidgets.QApplication.translate(
                                              parent.name, label[index], None))
        self.buttonGroup.addButton(self.button[index])
        vChecksLayout.addWidget(self.button[index])

class MultiHChecks(QtWidgets.QFrame):
  """
  Checkbuttons laid out horizontally
  """
  def __init__(self, parent, name, number=1,
               enabled=[True],
               checkable=[True],
               label="label",
               tooltip="check tooltip"):
    """
    Args:
      parent    - the object which it is part of
      name      - unique widget name
      number    - of buttons
      enabled   - list of bool, one state for each button
      checkable - list of bool, True if user can change state
      label     - list of labels, one for each button
      tooltips  - list of tooltip textx
    """
    QtWidgets.QFrame.__init__(self)
    hChecksLayout = QtWidgets.QHBoxLayout(self)
    stdSizePolicyMinimum(self)
    self.setObjectName(_fromUtf8(name))
    self.buttonGroup = QtWidgets.QButtonGroup(hChecksLayout)
    self.buttonGroup.setObjectName(_fromUtf8(name+"_bg"))
    self.button = {}
    for index in list(range(number)):
        self.button[index] = QtWidgets.QCheckBox(parent)
        self.button[index].setToolTip(tooltip[index])
        self.button[index].setEnabled(enabled[index])
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button[index].setFont(font)
        self.button[index].setCheckable(checkable[index])
        self.button[index].setObjectName(_fromUtf8("button[index]"))
        self.button[index].setText(QtWidgets.QApplication.translate(
                                              parent.name, label[index], None))
        self.buttonGroup.addButton(self.button[index])
        hChecksLayout.addWidget(self.button[index])

class ObsParsFrame(QtWidgets.QFrame):
   """
   observing paramaters
   """
   def __init__(self, parent):
     """
     """
     QtWidgets.QFrame.__init__(self)
     stdSizePolicyMinimum(self)
     self.name = "obsParsFrame"
     self.parent = parent
     self.setObjectName(_fromUtf8(self.name))
     obsParsGrid = QtWidgets.QGridLayout(self)
     # check column (each item two rows deep)
     self.mode_select = MultiVChecks(self, "mode_select", number=4,
                                     enabled=[True, True, True, True],
                                     checkable=[True, True, True, True],
                                     label=["TLPW", "BMSW", "PSSW", "BPSW"],
                                     tooltip=["Total power, no switching",
                                              "Beam switching (chopping)",
                                              "Position switching (nodding)",
                                              "Beam and position switching\n"
                                              "(chopping and nodding)"])
     obsParsGrid.addWidget(self.mode_select,         0, 0, 4, 1)
     """
     self.nod_select = MultiVChecks(self, "nod_select", number=2,
                                    enabled=[True, True],
                                    checkable=[True, True],
                                    label=["PSSW", "BPSW"],
                                    tooltip=["Position switching (nodding)",
                                             "Beam and position switching\n"
                                             "(chopping and nodding)"])
     obsParsGrid.addWidget(self.nod_select,         2, 0, 2, 1)
     """
     # scans and cycles column (each item two rows deep)
     scan_total = TitledSpinbox(self, "num scans", "Scans", 1, 100)
     obsParsGrid.addWidget(scan_total,          0, 1, 2, 1)
     
     cycles_total = TitledSpinbox(self, "num cycles", "Cycles", 1, 50)
     obsParsGrid.addWidget(cycles_total,        2, 1, 2, 1)
     # info column
     scansDoneLabel = QtWidgets.QLabel(self)
     scansDoneLabel.setEnabled(True)
     font = QtGui.QFont()
     font.setPointSize(8)
     scansDoneLabel.setFont(font)
     scansDoneLabel.setObjectName(_fromUtf8("scansDoneLabel"))
     scansDoneLabel.setText(QtWidgets.QApplication.translate(
                                          parent.name, "Scans done", None))
     obsParsGrid.addWidget(scansDoneLabel, 0, 2, 1, 1)
     
     scansDoneValue = QtWidgets.QLabel(self)
     scansDoneValue.setEnabled(True)
     font = QtGui.QFont()
     font.setPointSize(8)
     scansDoneValue.setFont(font)
     scansDoneValue.setObjectName(_fromUtf8("timePerScanLabel"))
     scansDoneValue.setText(QtWidgets.QApplication.translate(
                                          parent.name, "0", None))
     obsParsGrid.addWidget(scansDoneValue, 1, 2, 1, 1)
     
     sigBeamLabel = QtWidgets.QLabel(self)
     sigBeamLabel.setEnabled(True)
     font = QtGui.QFont()
     font.setPointSize(8)
     sigBeamLabel.setFont(font)
     sigBeamLabel.setObjectName(_fromUtf8("sigBeamLabel"))
     sigBeamLabel.setText(QtWidgets.QApplication.translate(
                                          parent.name, "Signal Beam", None))
     obsParsGrid.addWidget(sigBeamLabel, 2, 2, 1, 1)

     sigBeamInd = MultiHChecks(self, "sig_beam", number=2,
               enabled=[True, True],
               checkable=[False, False],
               label=["1", "2"],
               tooltip=["source in left beam", "source in right beam"])
     obsParsGrid.addWidget(sigBeamInd, 3, 2, 1, 1)

