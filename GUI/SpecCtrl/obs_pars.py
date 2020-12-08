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
               title = "spinbox", minval = 0, maxval = 100, real=False):
    """
    Args:
      parent - the object which it is part of
      name   - unique widget name
      title  - the label above the spinbox
      minval - minimum allowed integer
      maxval - maximum allowed integer
    """
    QtWidgets.QFrame.__init__(self)
    stdSizePolicyPreferred(self)
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
    if real:
      self.value = QtWidgets.QDoubleSpinBox(self)
    else:
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

class TitledTextDisplay(QtWidgets.QFrame):
  """
  """
  def __init__(self, parent, name, title="title", value=False):
    QtWidgets.QFrame.__init__(self)
    stdSizePolicyPreferred(self)
    indLayout = QtWidgets.QVBoxLayout(self)
    self.label = QtWidgets.QLabel(self)
    self.label.setEnabled(True)
    font = QtGui.QFont()
    font.setPointSize(8)
    self.label.setFont(font)
    self.label.setObjectName(_fromUtf8(name+"Label"))
    self.label.setText(QtWidgets.QApplication.translate(
                                          parent.name, title, None))
    indLayout.addWidget(self.label)
    #       scan value (1,2)
    self.value = QtWidgets.QLabel(self)
    self.value.setEnabled(True)
    font = QtGui.QFont()
    font.setPointSize(8)
    self.value.setFont(font)
    self.value.setObjectName(_fromUtf8(name+"Value"))
    self.value.setText(QtWidgets.QApplication.translate(
                                          parent.name, "0", None))
    indLayout.addWidget(self.value)


class ObsParsFrame(QtWidgets.QFrame):
   """
   observing paramaters
   """
   def __init__(self, parent):
     """
     This is the grid layout
          0       1             2      3
         ------  --------   -------  --------
      0 |      | | scans  | | Scan || Record |
        |  m   | |        | |      ||        |
      1 |  o   | |        | |   0  ||        |
        |  d   |  --------   ------  --------
      2 |  e   | |        | |  Signal beam   |
        |  s   | | cycles |  ----------------
      3 |      | |        | | beam chk btn   |
         ------   --------   ----------------
      4 |spec/ | | recs/  | | integration    |
        | scan | |   scan | |    time        |
         ------  |        | |                |
      5 |switch| |        | |                |
        | state| |        | |                |
         ------   --------   ----------------
     """
     QtWidgets.QFrame.__init__(self)
     stdSizePolicyMinimum(self)
     self.setFrameShape(QtWidgets.QFrame.StyledPanel)
     self.setFrameShadow(QtWidgets.QFrame.Raised)
     self.name = "obsParsFrame"
     self.parent = parent
     self.setObjectName(_fromUtf8(self.name))
     obsParsGrid = QtWidgets.QGridLayout(self)
     
     # modes column (at 0,0 four rows deep)
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
     
     # scan and cycle column (at 0,1 and 2,1 each two rows deep)
     self.numScans = TitledSpinbox(self, "num scans", "Scans", 1, 100)
     obsParsGrid.addWidget(self.numScans,     0, 1, 2, 1)
     
     self.num_cycles = TitledSpinbox(self, "num cycles", "Cycles", 1, 50)
     obsParsGrid.addWidget(self.num_cycles, 2, 1, 2, 1)
     
     # info columns (at 0,2  1,2  2,2  3,2 each 1x1)
     self.scan = TitledTextDisplay(  self, "scan",   "Scan",   0)
     obsParsGrid.addWidget(self.scan,         0, 2, 2, 1)
     self.record = TitledTextDisplay(self, "record", "Record", 0)
     obsParsGrid.addWidget(self.record,       0, 3, 2, 1)
     
     #        signal beam label (2,2)
     sigBeamLabel = QtWidgets.QLabel(self)
     sigBeamLabel.setEnabled(True)
     font = QtGui.QFont()
     font.setPointSize(8)
     sigBeamLabel.setFont(font)
     sigBeamLabel.setObjectName(_fromUtf8("sigBeamLabel"))
     sigBeamLabel.setText(QtWidgets.QApplication.translate(
                                          parent.name, "Signal Beam", None))
     obsParsGrid.addWidget(sigBeamLabel, 2, 2, 1, 2)
     #         signal beam indicator (3,2)
     self.sigBeamInd = MultiHChecks(self, "sig_beam", number=2,
                                    enabled=[False,False],
                                    checkable=[True, True],
                                    label=["1", "2"],
                        tooltip=["source in left beam", "source in right beam"])
     obsParsGrid.addWidget(self.sigBeamInd, 3, 2, 1, 2)
     #         cross switch label (4,0)
     crossedLabel = QtWidgets.QLabel(self)
     font = QtGui.QFont()
     font.setPointSize(8)
     crossedLabel.setFont(font)
     crossedLabel.setObjectName(_fromUtf8("minutesLabel"))
     crossedLabel.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Beams Xed", None))
     obsParsGrid.addWidget(crossedLabel, 4, 0, 1, 1)
     #         spectra per scan (4,1 two rows deep)
     self.recsPerScan = TitledSpinbox(self, "recsPerScan", title="recs/scan",
                                      minval=1, maxval=100)
     self.recsPerScan.value.setValue(4)
     obsParsGrid.addWidget(self.recsPerScan, 4, 1, 2, 1)
     #         integr time (4,2 two rows deep)
     self.secsPerRec = TitledSpinbox(self, "secPerRec", title="secs/record",
                                     minval=1, maxval=60, real=True)
     self.secsPerRec.value.setValue(5.0)
     obsParsGrid.addWidget(self.secsPerRec, 4, 2, 2, 2)
     #         cross switch state (5,0)
     self.crossed = QtWidgets.QCheckBox(self)
     self.crossed.setToolTip("Beam switch state")
     self.crossed.setEnabled(False)
     font = QtGui.QFont()
     font.setPointSize(8)
     self.crossed.setFont(font)
     self.crossed.setCheckable(True)
     self.crossed.setObjectName(_fromUtf8("crossed"))
     obsParsGrid.addWidget(self.crossed, 5, 0, 1, 1)
     
     

