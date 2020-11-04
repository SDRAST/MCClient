# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, 
        NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets

from stdPalette    import stdPalette
from startPalette  import startPalette
from closePalette  import closePalette
from offsetPalette import offsetPalette
from tabPalette    import tabPalette
from bsPalette     import bsPalette
from bs2Palette    import bs2Palette

from obs_pars import ObsParsFrame

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Observatory(object):
    def stdSizePolicyMinimum(self, widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def stdSizePolicyPreferred(self, widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def stdSizePolicyMinimumPreferred(self, widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def stdSizePolicyExpanding(self, widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def stdSizePolicyMinimumExpanding(self, widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
    
    def stdSizePolicyFixed(self, widget):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
        
    def pmLabelPalette(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        return palette
    
    def palette70K(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        return palette
    
    def palette12K(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        return palette
    
    def load1Palette(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(20, 19, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 19, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 19, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(197, 197, 197))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 19, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 19, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 19, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(197, 197, 197))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        return palette
    
    def load2Palette(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        return palette

    def observing_parameters_block(self, Observatory):
        
        # start: observing parameters block
        self.obsParsGLayout = QtWidgets.QGridLayout(self.frame_11)
        self.obsParsGLayout.setObjectName(_fromUtf8("obsParsGLayout"))
        
        # start: cycles and time/scan layout
        
        self.cyclesTimePerScanGridLayout = QtWidgets.QGridLayout()
        self.cyclesTimePerScanGridLayout.setObjectName(_fromUtf8("cyclesTimePerScanGridLayout"))
        #    label row
        self.cyclesLabel = QtWidgets.QLabel(self.frame_11)
        self.cyclesLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cyclesLabel.setFont(font)
        self.cyclesLabel.setObjectName(_fromUtf8("cyclesLabel"))
        self.cyclesLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "cycles", None))
        self.cyclesTimePerScanGridLayout.addWidget(self.cyclesLabel, 0, 0, 1, 1)
        
        self.timePerScanLabel = QtWidgets.QLabel(self.frame_11)
        self.timePerScanLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.timePerScanLabel.setFont(font)
        self.timePerScanLabel.setObjectName(_fromUtf8("timePerScanLabel"))
        self.timePerScanLabel.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "time/scan(s):", None))
        self.cyclesTimePerScanGridLayout.addWidget(self.timePerScanLabel, 0, 1, 1, 1)
        # spinbox row
        self.cycles = QtWidgets.QSpinBox(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cycles.setFont(font)
        self.cycles.setMinimum(1)
        self.cycles.setMaximum(99)
        self.cycles.setObjectName(_fromUtf8("cycles"))
        #self.cycles.valueChanged.connect() <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.cyclesTimePerScanGridLayout.addWidget(self.cycles, 1, 0, 1, 1)
        
        self.tperscan = QtWidgets.QSpinBox(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tperscan.setFont(font)
        self.tperscan.setMinimum(10)
        self.tperscan.setMaximum(99999)
        self.tperscan.setObjectName(_fromUtf8("tperscan"))
        self.cyclesTimePerScanGridLayout.addWidget(self.tperscan, 1, 1, 1, 1)
        # end: cycles and time/scan layout
        self.obsParsGLayout.addLayout(self.cyclesTimePerScanGridLayout, 0, 0, 1, 1)
        
        # start: scans and timer labels
        self.scansTimerVLayout = QtWidgets.QVBoxLayout()
        self.scansTimerVLayout.setObjectName(_fromUtf8("scansTimerVLayout"))
        
        self.scansLabel = QtWidgets.QLabel(self.frame_11)
        self.stdSizePolicyMinimum(self.scansLabel)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.scansLabel.setFont(font)
        self.scansLabel.setObjectName(_fromUtf8("scansLabel"))
        self.scansLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "scans:", None))
        self.scansTimerVLayout.addWidget(self.scansLabel)
        
        self.timerLabel = QtWidgets.QLabel(self.frame_11)
        self.stdSizePolicyMinimum(self.timerLabel)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.timerLabel.setFont(font)
        self.timerLabel.setObjectName(_fromUtf8("timerLabel"))
        self.timerLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "timer:", None))
        self.scansTimerVLayout.addWidget(self.timerLabel)
        # end: scans and timer labels
        self.obsParsGLayout.addLayout(self.scansTimerVLayout, 0, 1, 1, 1)
        
        # start: scans and timer values column
        self.scansTimerValueVLayout = QtWidgets.QVBoxLayout()
        self.scansTimerValueVLayout.setObjectName(_fromUtf8("scansTimerValueVLayout"))
        
        self.lcd_cycles = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lcd_cycles.setFont(font)
        self.lcd_cycles.setObjectName(_fromUtf8("lcd_cycles"))
        self.lcd_cycles.setText(QtWidgets.QApplication.translate(
                                                     "Observatory", "-1", None))
        self.scansTimerValueVLayout.addWidget(self.lcd_cycles)
        
        self.obs_time = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.obs_time.setFont(font)
        self.obs_time.setObjectName(_fromUtf8("obs_time"))
        self.obs_time.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.scansTimerValueVLayout.addWidget(self.obs_time)
        # end: scans and time values column
        self.obsParsGLayout.addLayout(self.scansTimerValueVLayout, 0, 2, 1, 1)
        
        # start: total time row
        self.totalTHLayout = QtWidgets.QHBoxLayout()
        self.totalTHLayout.setObjectName(_fromUtf8("totalTHLayout"))
        
        self.totalTLabel = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.totalTLabel.setFont(font)
        self.totalTLabel.setObjectName(_fromUtf8("totalTLabel"))
        self.totalTLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "Ttotal", None))
        self.totalTHLayout.addWidget(self.totalTLabel)
        
        self.pos_interval = QtWidgets.QDoubleSpinBox(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pos_interval.setFont(font)
        self.pos_interval.setMinimum(1.0)
        self.pos_interval.setMaximum(120.0)
        self.pos_interval.setObjectName(_fromUtf8("pos_interval"))
        self.totalTHLayout.addWidget(self.pos_interval)
        
        self.minutesLabel = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.minutesLabel.setFont(font)
        self.minutesLabel.setObjectName(_fromUtf8("minutesLabel"))
        self.minutesLabel.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "min", None))
        self.totalTHLayout.addWidget(self.minutesLabel)
        # end: total time row
        self.obsParsGLayout.addLayout(self.totalTHLayout, 1, 0, 1, 3)
                
        # start: observing modes column
        self.obsModeVLayout = QtWidgets.QVBoxLayout()
        self.obsModeVLayout.setObjectName(_fromUtf8("obsModeVLayout"))
        
        self.nod_bg = QtWidgets.QButtonGroup(Observatory)
        self.nod_bg.setObjectName(_fromUtf8("nod_bg"))
        
        self.sr_nodding = QtWidgets.QCheckBox(self.frame_11)
        self.sr_nodding.setToolTip("Beam switching or 'chopping'")
        self.sr_nodding.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.sr_nodding.setFont(font)
        self.sr_nodding.setCheckable(True)
        self.sr_nodding.setObjectName(_fromUtf8("sr_nodding"))
        self.sr_nodding.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Feed Xing", None))
        self.nod_bg.addButton(self.sr_nodding)
        self.obsModeVLayout.addWidget(self.sr_nodding)
        
        self.pos_switch = QtWidgets.QCheckBox(self.frame_11)
        self.pos_switch.setToolTip("Position switching or 'nodding'")
        self.pos_switch.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pos_switch.setFont(font)
        self.pos_switch.setCheckable(True)
        self.pos_switch.setChecked(True)
        self.pos_switch.setObjectName(_fromUtf8("pos_switch"))
        self.pos_switch.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Antenna Nod", None))
        self.obsModeVLayout.addWidget(self.pos_switch)
        
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        
        self.onsourceFeedLabel = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.onsourceFeedLabel.setFont(font)
        self.onsourceFeedLabel.setObjectName(_fromUtf8("onsourceFeedLabel"))
        self.onsourceFeedLabel.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Onsource Feed", None))
        self.horizontalLayout_4.addWidget(self.onsourceFeedLabel)
        
        self.obsModeVLayout.addLayout(self.horizontalLayout_4)
        
        self.beam_switch = QtWidgets.QCheckBox(self.frame_11)
        self.beam_switch.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.beam_switch.setFont(font)
        self.beam_switch.setCheckable(True)
        self.beam_switch.setObjectName(_fromUtf8("beam_switch"))
        self.beam_switch.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Beam switch", None))
        self.obsModeVLayout.addWidget(self.beam_switch)
        # end: observing modes column
        self.obsParsGLayout.addLayout(self.obsModeVLayout, 2, 0, 1, 3)
        # end: observing parameters block
    
           
    def setupUi(self, Observatory):
        """
        initialize the GUI
        """
        self.name = Observatory.name
        # configure the main window
        Observatory.setObjectName(_fromUtf8("Observatory"))
        Observatory.setEnabled(True)
        Observatory.resize(1260, 733)
        self.stdSizePolicyExpanding(Observatory)
        Observatory.setMinimumSize(QtCore.QSize(0, 0))
        Observatory.setMaximumSize(QtCore.QSize(1305, 733))
        stdPalette(Observatory)        
        Observatory.setMouseTracking(False)
        Observatory.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(
        "../../../../../../../../../../../../../../../../../../../../../galaxy_png.png")),
         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Observatory.setWindowIcon(icon)
        Observatory.setAutoFillBackground(True)
        Observatory.setAnimated(False)
        Observatory.setWindowTitle(QtWidgets.QApplication.translate(
                      "Observatory", "DSS43 K-Band Observatory Software", None))
        
        # define the central widget
        self.centralwidget = QtWidgets.QWidget(Observatory)
        self.stdSizePolicyExpanding(self.centralwidget)  
        stdPalette(self.centralwidget)        
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        # initialize tooltips
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        # tabbed page setup
        self.Ctrl_Tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.Ctrl_Tabs.setEnabled(True)
        self.stdSizePolicyMinimum(self.Ctrl_Tabs)
        self.Ctrl_Tabs.setMinimumSize(QtCore.QSize(1100, 500))
        self.Ctrl_Tabs.setMaximumSize(QtCore.QSize(1240, 663))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PT Sans"))
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.Ctrl_Tabs.setFont(font)
        self.Ctrl_Tabs.setMouseTracking(False)
        self.Ctrl_Tabs.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Ctrl_Tabs.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.Ctrl_Tabs.setAcceptDrops(False)
        self.Ctrl_Tabs.setAutoFillBackground(False)
        self.Ctrl_Tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.Ctrl_Tabs.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.Ctrl_Tabs.setElideMode(QtCore.Qt.ElideNone)
        self.Ctrl_Tabs.setTabsClosable(False)
        self.Ctrl_Tabs.setMovable(True)
        self.Ctrl_Tabs.setObjectName(_fromUtf8("Ctrl_Tabs"))
        
        # info bar across window bottom
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        timeStatusLayout = QtWidgets.QHBoxLayout()
        timeStatusLayout.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridLayout.addLayout(timeStatusLayout, 3, 0, 1, 1)
        
        self.statusBarHLayout = QtWidgets.QHBoxLayout()
        self.statusBarHLayout.setSpacing(0)
        self.statusBarHLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.statusBarHLayout.setObjectName(_fromUtf8("statusBarHLayout"))
        self.statusBarHLayout.addWidget(self.Ctrl_Tabs)
        
        # --------------------------- status report ----------------------------
        self.gridLayout.addLayout(self.statusBarHLayout, 0, 0, 2, 1)
        self.status = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.status.setFont(font)
        self.status.setObjectName(_fromUtf8("status"))
        self.status.setText(QtWidgets.QApplication.translate("Observatory",
           "Status: ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",
           None))
        self.gridLayout.addWidget(self.status, 2, 0, 1, 1)
        Observatory.setCentralWidget(self.centralwidget)
        
        # --------------------- current status --------------------------------
        # project
        self.projectLabel = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.projectLabel)
        self.projectLabel.setObjectName(_fromUtf8("projectLabel"))
        self.projectLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Project:", None))
        timeStatusLayout.addWidget(self.projectLabel)
        
        self.projectText = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.projectText)
        self.projectText.setObjectName(_fromUtf8("projectText"))
        self.projectText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", Observatory.project, None))
        timeStatusLayout.addWidget(self.projectText)
        
        # activity
        self.activityLabel = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.activityLabel)
        self.activityLabel.setObjectName(_fromUtf8("activityLabel"))
        self.activityLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Activity:", None))
        timeStatusLayout.addWidget(self.activityLabel)
        
        self.activityText = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.activityText)
        self.activityText.setObjectName(_fromUtf8("activityText"))
        self.activityText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", Observatory.activity, None))
        timeStatusLayout.addWidget(self.activityText)
        
        #hardware context
        self.contextLabel = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.contextLabel)
        self.contextLabel.setObjectName(_fromUtf8("contextLabel"))
        self.contextLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Context:", None))
        timeStatusLayout.addWidget(self.contextLabel)
        
        self.contextText = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.contextText)
        self.contextText.setObjectName(_fromUtf8("contextText"))
        self.contextText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", Observatory.context, None))
        timeStatusLayout.addWidget(self.contextText)
        
        # times
        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.label_time)
        self.label_time.setObjectName(_fromUtf8("label_time"))
        self.label_time.setText(QtWidgets.QApplication.translate("Observatory",
         """<html>
              <body>
                <p align=\"right\">
                  <span style=\" font-weight:600;\">
                    Time
                  </span>
                </p>
              </body>
            </html>""", None))
        timeStatusLayout.addWidget(self.label_time)
        
        self.lcd_time = QtWidgets.QLCDNumber(self.centralwidget)
        self.stdSizePolicyPreferred(self.lcd_time)
        self.lcd_time.setMouseTracking(False)
        self.lcd_time.setAutoFillBackground(True)
        self.lcd_time.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lcd_time.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_time.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_time.setNumDigits(10)
        self.lcd_time.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_time.setObjectName(_fromUtf8("lcd_time"))
        timeStatusLayout.addWidget(self.lcd_time)
        
        self.label_time_3 = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.label_time_3)
        self.label_time_3.setObjectName(_fromUtf8("label_time_3"))
        timeStatusLayout.addWidget(self.label_time_3)
        
        self.lcd_time_3 = QtWidgets.QLCDNumber(self.centralwidget)
        self.stdSizePolicyPreferred(self.lcd_time_3)
        self.lcd_time_3.setMouseTracking(False)
        self.lcd_time_3.setAutoFillBackground(True)
        self.lcd_time_3.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lcd_time_3.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_time_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_time_3.setNumDigits(10)
        self.lcd_time_3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_time_3.setObjectName(_fromUtf8("lcd_time_3"))
        self.label_time_3.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'Ubuntu\'; font-size:11pt;
                             font-weight:600; font-style:normal;\">
                <p align=\"right\" style=\" margin-top:12px; margin-bottom:12px;
                                            margin-left:0px; margin-right:0px;
                                          -qt-block-indent:0; text-indent:0px;\">
                   <span style=\" font-family:\'Sans\'; font-size:10pt;\">
                     UTC
                   </span>
                 </p>
               </body>
             </html>""", None))
        timeStatusLayout.addWidget(self.lcd_time_3)
        
        self.label_time_4 = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyPreferred(self.label_time_4)
        self.label_time_4.setObjectName(_fromUtf8("label_time_4"))
        self.label_time_4.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'Sans\'; font-size:10pt;
                             font-weight:600; font-style:normal;\">
                <p align=\"right\" style=\" margin-top:12px; margin-bottom:12px;
                                            margin-left:0px; margin-right:0px;
                                         -qt-block-indent:0; text-indent:0px;\">
                  LST
                </p>
              </body>
            </html>""", None))
        timeStatusLayout.addWidget(self.label_time_4)
        
        self.lcd_LST = QtWidgets.QLCDNumber(self.centralwidget)
        self.stdSizePolicyPreferred(self.lcd_LST)
        self.lcd_LST.setMouseTracking(False)
        self.lcd_LST.setAutoFillBackground(True)
        self.lcd_LST.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lcd_LST.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_LST.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_LST.setNumDigits(10)
        self.lcd_LST.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_LST.setObjectName(_fromUtf8("lcd_LST"))
        #self.lcd_LST.setText(QtWidgets.QApplication.translate(
        #                                  "Observatory", Observatory.LST, None))
        timeStatusLayout.addWidget(self.lcd_LST)
        
        self.label_doy = QtWidgets.QLabel(self.centralwidget)
        self.stdSizePolicyMinimumPreferred(self.label_doy)
        self.label_doy.setObjectName(_fromUtf8("label_doy"))
        self.label_doy.setText(QtWidgets.QApplication.translate("Observatory",
         """<html>
              <body>
                <p align=\"right\">
                  DOY(utc)
                </p>
              </body>
            </html>""", None))
        timeStatusLayout.addWidget(self.label_doy)

        self.lcd_doy = QtWidgets.QLCDNumber(self.centralwidget)
        self.stdSizePolicyPreferred(self.lcd_doy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lcd_doy.setFont(font)
        self.lcd_doy.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lcd_doy.setAutoFillBackground(True)
        self.lcd_doy.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_doy.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_doy.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_doy.setProperty("value", 0.0)
        self.lcd_doy.setObjectName(_fromUtf8("lcd_doy"))
        timeStatusLayout.addWidget(self.lcd_doy)
        
        self.lcd_year = QtWidgets.QLCDNumber(self.centralwidget)
        self.stdSizePolicyPreferred(self.lcd_year)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lcd_year.setFont(font)
        self.lcd_year.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lcd_year.setAutoFillBackground(True)
        self.lcd_year.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcd_year.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_year.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_year.setProperty("value", 0.0)
        self.lcd_year.setObjectName(_fromUtf8("lcd_year"))
        timeStatusLayout.addWidget(self.lcd_year)
        
        # page for Observations tab ############################################
        self.ObsSummary = QtWidgets.QWidget()
        self.ObsSummary.setObjectName(_fromUtf8("ObsSummary"))
        
        self.gridLayout_27 = QtWidgets.QGridLayout(self.ObsSummary)
        self.gridLayout_27.setObjectName(_fromUtf8("gridLayout_27"))
        
        self.gridLayout_28 = QtWidgets.QGridLayout()
        self.gridLayout_28.setObjectName(_fromUtf8("gridLayout_28"))
        
        self.frame_5 = QtWidgets.QFrame(self.ObsSummary)
        self.stdSizePolicyExpanding(self.frame_5)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 0))
        stdPalette(self.frame_5)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.gridLayout_30 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_30.setObjectName(_fromUtf8("gridLayout_30"))
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem, 0, 3, 1, 1)
        
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName(_fromUtf8("gridLayout_16"))
        
        self.frame_6 = QtWidgets.QFrame(self.frame_5)
        self.stdSizePolicyMinimum(self.frame_6)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_44.setObjectName(_fromUtf8("horizontalLayout_44"))
        
        self.label_chns_4 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.frame_6)
        self.label_chns_4.setMaximumSize(QtCore.QSize(87, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_chns_4.setFont(font)
        self.label_chns_4.setMouseTracking(True)
        self.label_chns_4.setObjectName(_fromUtf8("label_chns_4"))
        self.label_chns_4.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
            <body style=\" font-family:\'PT Sans\'; font-size:8pt;
                           font-weight:400; font-style:normal;\">
              <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; 
                          margin-right:0px; -qt-block-indent:0;
                          text-indent:0px;\">
               <span style=\" font-family:\'Sans\';\">
                 SAO64K
               </span>
              </p>
            </body>
          </html>""", None))
        self.horizontalLayout_44.addWidget(self.label_chns_4)
        
        self.IF_label = {}
        for num in [1,2,3,4]:
          self.IF_label[num] = QtWidgets.QLabel(self.frame_6)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.IF_label[num].setFont(font)
          self.IF_label[num].setObjectName(_fromUtf8("IF_label_"+str(num)))
          self.IF_label[num].setText(QtWidgets.QApplication.translate(
                                                 "Observatory", str(num), None))
          self.horizontalLayout_44.addWidget(self.IF_label[num])
        self.gridLayout_6.addLayout(self.horizontalLayout_44, 0, 0, 1, 1)
        
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_43.setObjectName(_fromUtf8("horizontalLayout_43"))
        
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        
        self.label_chns_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_chns_3)
        self.label_chns_3.setMaximumSize(QtCore.QSize(87, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_chns_3.setFont(font)
        self.label_chns_3.setMouseTracking(True)
        self.label_chns_3.setObjectName(_fromUtf8("label_chns_3"))
        self.label_chns_3.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:11pt; 
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\'; font-size:8pt;\">
                    Channels
                  </span>
                </p>
              </body>
            </html>""", None))
        self.verticalLayout_11.addWidget(self.label_chns_3)
        
        self.label_bw_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_bw_3)
        self.label_bw_3.setMaximumSize(QtCore.QSize(87, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_bw_3.setFont(font)
        self.label_bw_3.setMouseTracking(True)
        self.label_bw_3.setObjectName(_fromUtf8("label_bw_3"))
        self.label_bw_3.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:8pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\';\">
                    BW(MHz)
                  </span>
                </p>
              </body>
            </html>""", None))        
        self.verticalLayout_11.addWidget(self.label_bw_3)
        
        self.label_cf_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_cf_3)
        self.label_cf_3.setMaximumSize(QtCore.QSize(87, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_cf_3.setFont(font)
        self.label_cf_3.setMouseTracking(True)
        self.label_cf_3.setObjectName(_fromUtf8("label_cf_3"))
        self.label_cf_3.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:8pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\';\">
                    CF(MHz)
                  </span>
                </p>
              </body>
            </html>""", None))
        self.verticalLayout_11.addWidget(self.label_cf_3)
        
        self.label_res_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_res_3)
        self.label_res_3.setMaximumSize(QtCore.QSize(87, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_res_3.setFont(font)
        self.label_res_3.setMouseTracking(True)
        self.label_res_3.setObjectName(_fromUtf8("label_res_3"))
        self.label_res_3.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:8pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\';\">
                    Res(kHz)
                  </span>
                </p>
              </body>
            </html>""", None))
        self.verticalLayout_11.addWidget(self.label_res_3)
        
        self.label_oflw_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_oflw_3)
        self.label_oflw_3.setMaximumSize(QtCore.QSize(92, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_oflw_3.setFont(font)
        self.label_oflw_3.setMouseTracking(True)
        self.label_oflw_3.setObjectName(_fromUtf8("label_oflw_3"))
        self.label_oflw_3.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:8pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\';\">
                    Overflw
                  </span>
                </p>
              </body>
            </html>""", None))
        self.verticalLayout_11.addWidget(self.label_oflw_3)
        
        self.label_int_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_int_3)
        self.label_int_3.setMaximumSize(QtCore.QSize(92, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_int_3.setFont(font)
        self.label_int_3.setMouseTracking(True)
        self.label_int_3.setObjectName(_fromUtf8("label_int_3"))
        self.label_int_3.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:11pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\'; font-size:8pt;\">
                    Intg time
                  </span>
                </p>
              </body>
            </html>""", None))
        self.verticalLayout_11.addWidget(self.label_int_3)
        
        self.horizontalLayout_43.addLayout(self.verticalLayout_11)
        
        self.SAOparsVerticalLayout = {}
        self.saochan = {}
        self.saobw = {}
        self.saocf = {}
        self.saoreso = {}
        self.saoof = {}
        self.saoit = {}
        for num in [1, 2, 3, 4]:
          self.SAOparsVerticalLayout[num] = QtWidgets.QVBoxLayout()
          self.SAOparsVerticalLayout[num].setObjectName(
                                    _fromUtf8("SAOparsVerticalLayout"+str(num)))
          
          
          self.saochan[num] = QtWidgets.QLCDNumber(self.frame_6)
          self.stdSizePolicyPreferred(self.saochan[num])
          self.saochan[num].setMaximumSize(QtCore.QSize(64, 17))
          font = QtGui.QFont()
          font.setPointSize(5)
          self.saochan[num].setFont(font)
          self.saochan[num].setFrameShadow(QtWidgets.QFrame.Plain)
          self.saochan[num].setSegmentStyle(QtWidgets.QLCDNumber.Flat)
          self.saochan[num].setObjectName(_fromUtf8("saochan"+str(num)))
          self.SAOparsVerticalLayout[num].addWidget(self.saochan[num])
        
          self.saobw[num] = QtWidgets.QLCDNumber(self.frame_6)
          self.stdSizePolicyPreferred(self.saobw[num])
          self.saobw[num].setMaximumSize(QtCore.QSize(64, 17))
          font = QtGui.QFont()
          font.setPointSize(5)
          self.saobw[num].setFont(font)
          self.saobw[num].setFrameShadow(QtWidgets.QFrame.Plain)
          #self.sao1bw.setNumDigits(8) #
          self.saobw[num].setSegmentStyle(QtWidgets.QLCDNumber.Flat)
          self.saobw[num].setObjectName(_fromUtf8("saobw"+str(num)))
          self.SAOparsVerticalLayout[num].addWidget(self.saobw[num])
        
          self.saocf[num] = QtWidgets.QLCDNumber(self.frame_6)
          self.stdSizePolicyPreferred(self.saocf[num])
          self.saocf[num].setMaximumSize(QtCore.QSize(64, 17))
          font = QtGui.QFont()
          font.setPointSize(5)
          self.saocf[num].setFont(font)
          self.saocf[num].setFrameShadow(QtWidgets.QFrame.Plain)
          self.saocf[num].setSegmentStyle(QtWidgets.QLCDNumber.Flat)
          self.saocf[num].setObjectName(_fromUtf8("saocf"+str(num)))
          self.SAOparsVerticalLayout[num].addWidget(self.saocf[num])
        
          self.saoreso[num] = QtWidgets.QLCDNumber(self.frame_6)
          self.stdSizePolicyPreferred(self.saoreso[num])
          self.saoreso[num].setMaximumSize(QtCore.QSize(64, 17))
          font = QtGui.QFont()
          font.setPointSize(5)
          self.saoreso[num].setFont(font)
          self.saoreso[num].setFrameShadow(QtWidgets.QFrame.Plain)
          self.saoreso[num].setSegmentStyle(QtWidgets.QLCDNumber.Flat)
          self.saoreso[num].setObjectName(_fromUtf8("saoreso"+str(num)))
          self.SAOparsVerticalLayout[num].addWidget(self.saoreso[num])
        
          self.saoof[num] = QtWidgets.QLCDNumber(self.frame_6)
          self.stdSizePolicyPreferred(self.saoof[num])
          self.saoof[num].setMaximumSize(QtCore.QSize(64, 17))
          font = QtGui.QFont()
          font.setPointSize(5)
          self.saoof[num].setFont(font)
          self.saoof[num].setFrameShadow(QtWidgets.QFrame.Plain)
          self.saoof[num].setSegmentStyle(QtWidgets.QLCDNumber.Flat)
          self.saoof[num].setObjectName(_fromUtf8("saoof"+str(num)))
          self.SAOparsVerticalLayout[num].addWidget(self.saoof[num])
        
          self.saoit[num] = QtWidgets.QLCDNumber(self.frame_6)
          self.stdSizePolicyPreferred(self.saoit[num])
          self.saoit[num].setMaximumSize(QtCore.QSize(64, 17))
          font = QtGui.QFont()
          font.setPointSize(5)
          self.saoit[num].setFont(font)
          self.saoit[num].setFrameShadow(QtWidgets.QFrame.Plain)
          self.saoit[num].setSegmentStyle(QtWidgets.QLCDNumber.Flat)
          self.saoit[num].setObjectName(_fromUtf8("saoit"+str(num)))
          self.SAOparsVerticalLayout[num].addWidget(self.saoit[num])
          
          self.horizontalLayout_43.addLayout(self.SAOparsVerticalLayout[num])
        
        self.gridLayout_6.addLayout(self.horizontalLayout_43, 1, 0, 1, 1)
        
        self.gridLayout_16.addWidget(self.frame_6, 1, 0, 1, 1)
        
        # source list and data dir frame
        self.sourceListDataDirFrame = QtWidgets.QFrame(self.frame_5)
        self.stdSizePolicyMinimum(self.sourceListDataDirFrame)
        self.sourceListDataDirFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sourceListDataDirFrame.setFrameShadow(QtWidgets.QFrame.Raised) 
        self.sourceListDataDirFrame.setObjectName(_fromUtf8("frame"))
        
        # source list layout ---------------------------------------------------
        self.sourceListLayout = QtWidgets.QGridLayout(self.sourceListDataDirFrame)
        self.sourceListLayout.setObjectName(_fromUtf8("gridLayout_63"))
        #        source list label
        self.sourceListLabel = QtWidgets.QLabel(self.sourceListDataDirFrame)
        self.stdSizePolicyExpanding(self.sourceListLabel)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.sourceListLabel.setFont(font)
        self.sourceListLabel.setObjectName(_fromUtf8("label_89"))
        self.sourceListLabel.setText(QtWidgets.QApplication.translate(
                                           "Observatory", "Source List ", None))
        self.sourceListLayout.addWidget(self.sourceListLabel, 0, 0, 1, 1)
        #        source list widget
        self.source_que = QtWidgets.QListWidget(self.sourceListDataDirFrame)
        self.stdSizePolicyMinimum(self.source_que)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.source_que.setFont(font)
        self.source_que.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.source_que.setObjectName(_fromUtf8("source_que"))
        self.source_que.setToolTip(
                         "Left double-click to select source for observation.\n"
                         + "Drag and drop to BS sources que.")
        self.sourceListLayout.addWidget(self.source_que, 1, 0, 1, 1)
        #        empty frame and layout
        self.sourceListEmptyFrame = QtWidgets.QFrame(self.sourceListDataDirFrame)
        self.sourceListEmptyFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sourceListEmptyFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sourceListEmptyFrame.setObjectName(_fromUtf8("frame_19"))
        self.sourceListEmptyLayout = QtWidgets.QGridLayout(self.sourceListEmptyFrame)
        self.sourceListEmptyLayout.setObjectName(_fromUtf8("gridLayout_45"))
        spacerItem1 = QtWidgets.QSpacerItem(130, 20,
                                            QtWidgets.QSizePolicy.Fixed, 
                                            QtWidgets.QSizePolicy.Minimum)
        self.sourceListEmptyLayout.addItem(spacerItem1, 0, 0, 1, 1)
        
        self.sourceListLayout.addWidget(self.sourceListEmptyFrame, 1, 1, 1, 1)
        #        TextLabel and Data Dir layout
        self.textLabelDataDirHLayout = QtWidgets.QHBoxLayout()
        self.textLabelDataDirHLayout.setObjectName(_fromUtf8("horizontalLayout_46"))
        #                TextLabel
        self.sourceListTextLabel = QtWidgets.QLabel(self.sourceListDataDirFrame)
        self.stdSizePolicyExpanding(self.sourceListTextLabel)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.sourceListTextLabel.setFont(font)
        self.sourceListTextLabel.setObjectName(_fromUtf8("label_62"))
        self.sourceListTextLabel.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "TextLabel", None))
        self.textLabelDataDirHLayout.addWidget(self.sourceListTextLabel)
        self.sourceListLayout.addLayout(self.textLabelDataDirHLayout, 2, 0, 1, 1)
        #                Data Dir
        self.label_47 = QtWidgets.QLabel(self.sourceListDataDirFrame)
        self.stdSizePolicyExpanding(self.label_47)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_47.setFont(font)
        self.label_47.setObjectName(_fromUtf8("label_47"))
        self.label_47.setText(QtWidgets.QApplication.translate(
                                      "Observatory", "Current Data Dir:", None))
        self.textLabelDataDirHLayout.addWidget(self.label_47)
        
        self.gridLayout_16.addWidget(self.sourceListDataDirFrame, 2, 0, 1, 1)
        # end of source list and data dir frame --------------------------------
        
        self.frame_3 = QtWidgets.QFrame(self.frame_5)
        self.stdSizePolicyMinimum(self.frame_3)

        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        
        # Tsys recording layout
        #    top row
        self.gridLayout_20 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_20.setObjectName(_fromUtf8("gridLayout_20"))
        
        self.label_95 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_95.setFont(font)
        self.label_95.setObjectName(_fromUtf8("label_95"))
        self.label_95.setText(QtWidgets.QApplication.translate(
                                                     "Observatory", "IF", None))
        self.gridLayout_20.addWidget(self.label_95, 0, 0, 1, 1)
        
        self.label_112 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_112.setFont(font)
        self.label_112.setObjectName(_fromUtf8("label_112"))
        self.label_112.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Position", None))
        self.gridLayout_20.addWidget(self.label_112, 0, 1, 1, 1)
        
        self.label_115 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_115.setFont(font)
        self.label_115.setObjectName(_fromUtf8("label_115"))
        self.label_115.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Tsys", None))
        self.gridLayout_20.addWidget(self.label_115, 0, 4, 1, 1)
        
        self.label_96 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_96.setFont(font)
        self.label_96.setObjectName(_fromUtf8("label_96"))
        self.label_96.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "Rec", None))
        self.gridLayout_20.addWidget(self.label_96, 0, 5, 1, 1)
        
        #    IF 1 row
        self.IFLabel = {}
        self.combo = {}
        self.tsys = {}
        self.k_led = {}
        for num in [1,2,3,4]:
          self.IFLabel[num] = QtWidgets.QLabel(self.frame_3)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.IFLabel[num].setFont(font)
          self.IFLabel[num].setObjectName(_fromUtf8("IFLabel"+str(num)))
          self.IFLabel[num].setText(QtWidgets.QApplication.translate(
                                                 "Observatory", str(num), None))
          self.gridLayout_20.addWidget(self.IFLabel[num], num, 0, 1, 1)
        
          self.combo[num] = QtWidgets.QComboBox(self.frame_3)
          self.stdSizePolicyMinimumExpanding(self.combo[num])
          font = QtGui.QFont()
          font.setPointSize(6)
          self.combo[num].setFont(font)
          self.combo[num].setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
          self.combo[num].setObjectName(_fromUtf8("combo"+str(num)))
          self.gridLayout_20.addWidget(self.combo[num], num, 1, 1, 1)
        
          self.tsys[num] = QtWidgets.QLabel(self.frame_3)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.tsys[num].setFont(font)
          self.tsys[num].setObjectName(_fromUtf8("tsys"+str(num)))
          self.tsys[num].setText(QtWidgets.QApplication.translate(
                                              "Observatory", "TextLabel", None))
          self.gridLayout_20.addWidget(self.tsys[num], num, 4, 1, 1)
        
          self.k_led[num] = KLed(self.frame_3)
          self.k_led[num].setChecked(not self.k_led[num].isChecked())
          self.k_led[num].setObjectName(_fromUtf8("k_led"+str(num)))
          self.gridLayout_20.addWidget(self.k_led[num], num, 5, 1, 1)
        
        self.gridLayout_16.addWidget(self.frame_3, 0, 0, 1, 1)
        
        self.gridLayout_30.addLayout(self.gridLayout_16, 0, 1, 1, 1)
        
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName(_fromUtf8("gridLayout_17"))
        
        self.frame_11 = QtWidgets.QFrame(self.frame_5)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName(_fromUtf8("frame_11"))
        
        # self.observing_parameters_block(Observatory)
        self.obs_pars = ObsParsFrame(Observatory)
        self.gridLayout_17.addWidget(self.obs_pars, 3, 0, 1, 1)
        """
        # start: observing parameters block
        self.obsParsGLayout = QtWidgets.QGridLayout(self.frame_11)
        self.obsParsGLayout.setObjectName(_fromUtf8("obsParsGLayout"))
        
        # start: cycles and time/scan layout
        
        self.cyclesTimePerScanGridLayout = QtWidgets.QGridLayout()
        self.cyclesTimePerScanGridLayout.setObjectName(_fromUtf8("cyclesTimePerScanGridLayout"))
        #    label row
        self.cyclesLabel = QtWidgets.QLabel(self.frame_11)
        self.cyclesLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cyclesLabel.setFont(font)
        self.cyclesLabel.setObjectName(_fromUtf8("cyclesLabel"))
        self.cyclesLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "cycles", None))
        self.cyclesTimePerScanGridLayout.addWidget(self.cyclesLabel, 0, 0, 1, 1)
        
        self.timePerScanLabel = QtWidgets.QLabel(self.frame_11)
        self.timePerScanLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.timePerScanLabel.setFont(font)
        self.timePerScanLabel.setObjectName(_fromUtf8("timePerScanLabel"))
        self.timePerScanLabel.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "time/scan(s):", None))
        self.cyclesTimePerScanGridLayout.addWidget(self.timePerScanLabel, 0, 1, 1, 1)
        # spinbox row
        self.cycles = QtWidgets.QSpinBox(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cycles.setFont(font)
        self.cycles.setMinimum(1)
        self.cycles.setMaximum(99)
        self.cycles.setObjectName(_fromUtf8("cycles"))
        #self.cycles.valueChanged.connect() <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.cyclesTimePerScanGridLayout.addWidget(self.cycles, 1, 0, 1, 1)
        
        self.tperscan = QtWidgets.QSpinBox(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tperscan.setFont(font)
        self.tperscan.setMinimum(10)
        self.tperscan.setMaximum(99999)
        self.tperscan.setObjectName(_fromUtf8("tperscan"))
        self.cyclesTimePerScanGridLayout.addWidget(self.tperscan, 1, 1, 1, 1)
        # end: cycles and time/scan layout
        self.obsParsGLayout.addLayout(self.cyclesTimePerScanGridLayout, 0, 0, 1, 1)
        
        # start: scans and timer labels
        self.scansTimerVLayout = QtWidgets.QVBoxLayout()
        self.scansTimerVLayout.setObjectName(_fromUtf8("scansTimerVLayout"))
        
        self.scansLabel = QtWidgets.QLabel(self.frame_11)
        self.stdSizePolicyMinimum(self.scansLabel)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.scansLabel.setFont(font)
        self.scansLabel.setObjectName(_fromUtf8("scansLabel"))
        self.scansLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "scans:", None))
        self.scansTimerVLayout.addWidget(self.scansLabel)
        
        self.timerLabel = QtWidgets.QLabel(self.frame_11)
        self.stdSizePolicyMinimum(self.timerLabel)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.timerLabel.setFont(font)
        self.timerLabel.setObjectName(_fromUtf8("timerLabel"))
        self.timerLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "timer:", None))
        self.scansTimerVLayout.addWidget(self.timerLabel)
        # end: scans and timer labels
        self.obsParsGLayout.addLayout(self.scansTimerVLayout, 0, 1, 1, 1)
        
        # start: scans and timer values column
        self.scansTimerValueVLayout = QtWidgets.QVBoxLayout()
        self.scansTimerValueVLayout.setObjectName(_fromUtf8("scansTimerValueVLayout"))
        
        self.lcd_cycles = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lcd_cycles.setFont(font)
        self.lcd_cycles.setObjectName(_fromUtf8("lcd_cycles"))
        self.lcd_cycles.setText(QtWidgets.QApplication.translate(
                                                     "Observatory", "-1", None))
        self.scansTimerValueVLayout.addWidget(self.lcd_cycles)
        
        self.obs_time = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.obs_time.setFont(font)
        self.obs_time.setObjectName(_fromUtf8("obs_time"))
        self.obs_time.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.scansTimerValueVLayout.addWidget(self.obs_time)
        # end: scans and time values column
        self.obsParsGLayout.addLayout(self.scansTimerValueVLayout, 0, 2, 1, 1)
        
        # start: total time row
        self.totalTHLayout = QtWidgets.QHBoxLayout()
        self.totalTHLayout.setObjectName(_fromUtf8("totalTHLayout"))
        
        self.totalTLabel = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.totalTLabel.setFont(font)
        self.totalTLabel.setObjectName(_fromUtf8("totalTLabel"))
        self.totalTLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "Ttotal", None))
        self.totalTHLayout.addWidget(self.totalTLabel)
        
        self.pos_interval = QtWidgets.QDoubleSpinBox(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pos_interval.setFont(font)
        self.pos_interval.setMinimum(1.0)
        self.pos_interval.setMaximum(120.0)
        self.pos_interval.setObjectName(_fromUtf8("pos_interval"))
        self.totalTHLayout.addWidget(self.pos_interval)
        
        self.minutesLabel = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.minutesLabel.setFont(font)
        self.minutesLabel.setObjectName(_fromUtf8("minutesLabel"))
        self.minutesLabel.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "min", None))
        self.totalTHLayout.addWidget(self.minutesLabel)
        # end: total time row
        self.obsParsGLayout.addLayout(self.totalTHLayout, 1, 0, 1, 3)
                
        # start: observing modes column
        self.obsModeVLayout = QtWidgets.QVBoxLayout()
        self.obsModeVLayout.setObjectName(_fromUtf8("obsModeVLayout"))
        
        self.nod_bg = QtWidgets.QButtonGroup(Observatory)
        self.nod_bg.setObjectName(_fromUtf8("nod_bg"))
        
        self.sr_nodding = QtWidgets.QCheckBox(self.frame_11)
        self.sr_nodding.setToolTip("Beam switching or 'chopping'")
        self.sr_nodding.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.sr_nodding.setFont(font)
        self.sr_nodding.setCheckable(True)
        self.sr_nodding.setObjectName(_fromUtf8("sr_nodding"))
        self.sr_nodding.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Feed Xing", None))
        self.nod_bg.addButton(self.sr_nodding)
        self.obsModeVLayout.addWidget(self.sr_nodding)
        
        self.pos_switch = QtWidgets.QCheckBox(self.frame_11)
        self.pos_switch.setToolTip("Position switching or 'nodding'")
        self.pos_switch.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pos_switch.setFont(font)
        self.pos_switch.setCheckable(True)
        self.pos_switch.setChecked(True)
        self.pos_switch.setObjectName(_fromUtf8("pos_switch"))
        self.pos_switch.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Antenna Nod", None))
        self.obsModeVLayout.addWidget(self.pos_switch)
        
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        
        self.onsourceFeedLabel = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.onsourceFeedLabel.setFont(font)
        self.onsourceFeedLabel.setObjectName(_fromUtf8("onsourceFeedLabel"))
        self.onsourceFeedLabel.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Onsource Feed", None))
        self.horizontalLayout_4.addWidget(self.onsourceFeedLabel)
        
        self.obsModeVLayout.addLayout(self.horizontalLayout_4)
        
        self.beam_switch = QtWidgets.QCheckBox(self.frame_11)
        self.beam_switch.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.beam_switch.setFont(font)
        self.beam_switch.setCheckable(True)
        self.beam_switch.setObjectName(_fromUtf8("beam_switch"))
        self.beam_switch.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Beam switch", None))
        self.obsModeVLayout.addWidget(self.beam_switch)
        # end: observing modes column
        self.obsParsGLayout.addLayout(self.obsModeVLayout, 2, 0, 1, 3)
        # end: observing parameters block
        """
        
        #self.gridLayout_17.addWidget(self.frame_11, 3, 0, 1, 1)
        self.frame_12 = QtWidgets.QFrame(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName(_fromUtf8("frame_12"))
        
        self.gridLayout_66 = QtWidgets.QGridLayout(self.frame_12)
        self.gridLayout_66.setObjectName(_fromUtf8("gridLayout_66"))
        
        # antenna status
        self.antStatLabel = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.antStatLabel.setFont(font)
        self.antStatLabel.setObjectName(_fromUtf8("label_79"))
        self.antStatLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Ant Stat", None))
        self.gridLayout_66.addWidget(self.antStatLabel, 0, 0, 1, 1)
        
        self.ant_sts = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.ant_sts.setFont(font)
        self.ant_sts.setObjectName(_fromUtf8("ant_sts"))
        self.ant_sts.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "None", None))
        self.gridLayout_66.addWidget(self.ant_sts, 0, 1, 1, 1)
        
        # predicted azimuth
        self.predAzLabel = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.predAzLabel.setFont(font)
        self.predAzLabel.setObjectName(_fromUtf8("label_97"))
        self.predAzLabel.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "Pr Az(deg)", None))
        self.gridLayout_66.addWidget(self.predAzLabel, 1, 0, 1, 1)
        
        self.az_mon = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.az_mon.setFont(font)
        self.az_mon.setObjectName(_fromUtf8("az_mon"))
        self.az_mon.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "0.0", None))
        self.gridLayout_66.addWidget(self.az_mon, 1, 1, 1, 1)
        
        # Predicted elevation
        self.predElevLabel = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.predElevLabel.setFont(font)
        self.predElevLabel.setObjectName(_fromUtf8("label_234"))
        self.predElevLabel.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "Pr El(deg)", None))
        self.gridLayout_66.addWidget(self.predElevLabel, 2, 0, 1, 1)
        
        self.el_mon = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.el_mon.setFont(font)
        self.el_mon.setObjectName(_fromUtf8("el_mon"))
        self.el_mon.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "0.0", None))
        self.gridLayout_66.addWidget(self.el_mon, 2, 1, 1, 1)
        
        # Antenna wrap
        self.antWrapLabel = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.antWrapLabel.setFont(font)
        self.antWrapLabel.setObjectName(_fromUtf8("label_240"))
        self.antWrapLabel.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Wrap", None))
        self.gridLayout_66.addWidget(self.antWrapLabel, 3, 0, 1, 1)
        
        self.wrap = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.wrap.setFont(font)
        self.wrap.setObjectName(_fromUtf8("wrap"))
        self.wrap.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "wrap", None))
        self.gridLayout_66.addWidget(self.wrap, 3, 1, 1, 1)
        
        # El Offset
        self.elOffsetLabel = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.elOffsetLabel.setFont(font)
        self.elOffsetLabel.setObjectName(_fromUtf8("label_15"))
        self.elOffsetLabel.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Offset El(deg)", None))
        self.gridLayout_66.addWidget(self.elOffsetLabel, 4, 0, 1, 1)
        
        self.el_offset = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.el_offset.setFont(font)
        self.el_offset.setObjectName(_fromUtf8("el_offset"))
        self.el_offset.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "0.0", None))
        self.gridLayout_66.addWidget(self.el_offset, 4, 1, 1, 1)
        
        # xEl offset
        self.label_16 = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_16.setText(QtWidgets.QApplication.translate(
                                        "Observatory", "Offset xEl(deg)", None))
        self.gridLayout_66.addWidget(self.label_16, 5, 0, 1, 1)
        
        self.xel_offset = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.xel_offset.setFont(font)
        self.xel_offset.setObjectName(_fromUtf8("xel_offset"))
        self.xel_offset.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "0.0", None))
        self.gridLayout_66.addWidget(self.xel_offset, 5, 1, 1, 1)
        
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
          QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_66.addItem(spacerItem2, 8, 0, 1, 1)
        
        self.gridLayout_17.addWidget(self.frame_12, 1, 0, 1, 1)
        
        self.frame_15 = QtWidgets.QFrame(self.frame_5)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName(_fromUtf8("frame_15"))
        self.gridLayout_17.addWidget(self.frame_15, 6, 0, 1, 1)
        
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_du = QtWidgets.QLabel(self.frame_5)
        self.stdSizePolicyPreferred(self.label_du)
        self.label_du.setMaximumSize(QtCore.QSize(61, 26))
        self.label_du.setObjectName(_fromUtf8("label_du"))
        self.label_du.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:11pt; 
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\'; font-size:8pt;\">
                    Disk Usage
                  </span>
                </p>
              </body>
            </html>""", None))
        self.horizontalLayout_9.addWidget(self.label_du)
        
        self.progressBar_1 = QtWidgets.QProgressBar(self.frame_5)
        self.stdSizePolicyPreferred(self.progressBar_1)
        self.progressBar_1.setMinimumSize(QtCore.QSize(0, 0))
        self.progressBar_1.setMaximumSize(QtCore.QSize(108, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progressBar_1.setFont(font)
        self.progressBar_1.setMaximum(100)
        self.progressBar_1.setProperty("value", 1)
        self.progressBar_1.setObjectName(_fromUtf8("progressBar_1"))
        self.horizontalLayout_9.addWidget(self.progressBar_1)
        self.gridLayout_17.addLayout(self.horizontalLayout_9, 9, 0, 1, 1)
        
        self.frame_2 = QtWidgets.QFrame(self.frame_5)
        self.stdSizePolicyExpanding(self.frame_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        
        # source information box
        self.gridLayout_21 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_21.setObjectName(_fromUtf8("gridLayout_21"))
        
        # obervation code
        self.obsCodeLabel = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.obsCodeLabel.setFont(font)
        self.obsCodeLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.obsCodeLabel.setObjectName(_fromUtf8("obsCodeLabel"))
        self.obsCodeLabel.setText(QtWidgets.QApplication.translate(
                                     "Observatory", "Observation code: ", None))
        self.gridLayout_21.addWidget(self.obsCodeLabel, 0, 0, 1, 1)
        
        self.obs_code = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.obs_code.setFont(font)
        self.obs_code.setObjectName(_fromUtf8("obs_code"))
        self.obs_code.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.gridLayout_21.addWidget(self.obs_code, 0, 3, 1, 1)
        
        # source name
        self.source_name_label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.source_name_label.setFont(font)
        self.source_name_label.setObjectName(_fromUtf8("source_name_label"))
        self.source_name_label.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Source:", "none"))
        self.gridLayout_21.addWidget(self.source_name_label, 1, 0, 1, 1)
        
        self.source_name = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.source_name.setFont(font)
        self.source_name.setObjectName(_fromUtf8("source_name_label"))
        self.gridLayout_21.addWidget(self.source_name, 1, 3, 1, 1)
        self.source_name.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "none", None))
        # right ascension 2000
        self.ra2000_label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ra2000_label.setFont(font)
        self.ra2000_label.setObjectName(_fromUtf8("ra2000_label"))
        self.ra2000_label.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "RA(J2000):", None))
        self.gridLayout_21.addWidget(self.ra2000_label, 2, 0, 1, 1)
        
        self.ra_sf = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ra_sf.setFont(font)
        self.ra_sf.setObjectName(_fromUtf8("ra_sf"))
        self.ra_sf.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.gridLayout_21.addWidget(self.ra_sf, 2, 3, 1, 1)
        
        # declination 2000
        self.dec2000_label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dec2000_label.setFont(font)
        self.dec2000_label.setObjectName(_fromUtf8("dec2000_label"))
        self.dec2000_label.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "DEC(J2000):", None))
        self.gridLayout_21.addWidget(self.dec2000_label, 3, 0, 1, 1)
        
        self.dec_sf = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dec_sf.setFont(font)
        self.dec_sf.setObjectName(_fromUtf8("dec_sf"))
        self.dec_sf.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.gridLayout_21.addWidget(self.dec_sf, 3, 3, 1, 1)
        
        # azimuth
        self.azLabel = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.azLabel.setFont(font)
        self.azLabel.setObjectName(_fromUtf8("azLabel"))
        self.azLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Az(deg):", None))
        self.gridLayout_21.addWidget(self.azLabel, 4, 0, 1, 1)
        
        self.az_sf = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.az_sf.setFont(font)
        self.az_sf.setObjectName(_fromUtf8("az_sf"))
        self.az_sf.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.gridLayout_21.addWidget(self.az_sf, 4, 3, 1, 1)
        
        # elevation
        self.el_label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.el_label.setFont(font)
        self.el_label.setObjectName(_fromUtf8("el_label"))
        self.el_label.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "El(deg):", None))
        self.gridLayout_21.addWidget(self.el_label, 5, 0, 1, 1)
        
        self.el_sf = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.el_sf.setFont(font)
        self.el_sf.setObjectName(_fromUtf8("el_sf"))
        self.el_sf.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.gridLayout_21.addWidget(self.el_sf, 5, 3, 1, 1)
        
        spacerItem3 = QtWidgets.QSpacerItem(40, 20,
                 QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_21.addItem(spacerItem3, 9, 1, 1, 1)
        
        self.source_vel_cb = QtWidgets.QComboBox(self.frame_2)
        self.source_vel_cb.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.source_vel_cb.setFont(font)
        self.source_vel_cb.setObjectName(_fromUtf8("source_vel_cb"))
        self.source_vel_cb.addItem(_fromUtf8(""))
        self.source_vel_cb.addItem(_fromUtf8(""))
        self.source_vel_cb.addItem(_fromUtf8(""))
        self.source_vel_cb.addItem(_fromUtf8(""))
        self.source_vel_cb.setItemText(0, QtWidgets.QApplication.translate(
                                             "Observatory", "R_HC(km/s)", None))
        self.source_vel_cb.setItemText(1, QtWidgets.QApplication.translate(
                                            "Observatory", "R_LSR(km/s)", None))
        self.source_vel_cb.setItemText(2, QtWidgets.QApplication.translate(
                                             "Observatory", "O_HC(km/s)", None))
        self.source_vel_cb.setItemText(3, QtWidgets.QApplication.translate(
                                            "Observatory", "O_LSR(km/s)", None))
        self.source_vel_cb.setCurrentIndex(3)
        self.gridLayout_21.addWidget(self.source_vel_cb, 9, 0, 1, 1)
        
        self.obsFreqLabel = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.obsFreqLabel.setFont(font)
        self.obsFreqLabel.setObjectName(_fromUtf8("obsFreqLabel"))
        self.obsFreqLabel.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Obs Freq(mhz)", None))
        self.gridLayout_21.addWidget(self.obsFreqLabel, 7, 0, 1, 1)
        
        self.restFreqLabel = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.restFreqLabel.setFont(font)
        self.restFreqLabel.setObjectName(_fromUtf8("restFreqLabel"))
        self.restFreqLabel.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Rest Freq(khz)", None))
        self.gridLayout_21.addWidget(self.restFreqLabel, 8, 0, 1, 1)
        
        self.src_obs = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.src_obs.setFont(font)
        self.src_obs.setObjectName(_fromUtf8("src_obs"))
        self.src_obs.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.gridLayout_21.addWidget(self.src_obs, 7, 3, 1, 1)
        
        self.rst = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.rst.setFont(font)
        self.rst.setObjectName(_fromUtf8("rst"))
        self.rst.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.gridLayout_21.addWidget(self.rst, 8, 3, 1, 1)
        
        self.vsys = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.vsys.setFont(font)
        self.vsys.setObjectName(_fromUtf8("vsys"))
        self.vsys.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "0.0", None))
        self.gridLayout_21.addWidget(self.vsys, 9, 3, 1, 1)
        # end source info box
        
        self.gridLayout_17.addWidget(self.frame_2, 0, 0, 1, 1)
        
        # start: Start and Close button row
        self.startCloseHLayout = QtWidgets.QHBoxLayout()
        self.startCloseHLayout.setObjectName(_fromUtf8("startCloseHLayout"))
        
        # start: Start Observing
        self.start_obs = QtWidgets.QPushButton(self.frame_5)
        self.start_obs.setEnabled(True)
        self.stdSizePolicyExpanding(self.start_obs)
        self.start_obs.setMaximumSize(QtCore.QSize(100, 50))
        startPalette(self.start_obs)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(True)
        font.setWeight(75)
        self.start_obs.setFont(font)
        self.start_obs.setCheckable(True)
        self.start_obs.setAutoExclusive(False)
        self.start_obs.setObjectName(_fromUtf8("start_obs"))
        self.start_obs.setText(QtWidgets.QApplication.translate(
                                        "Observatory", "Start Observing", None))
        # end: Start Observing
        self.startCloseHLayout.addWidget(self.start_obs)
        
        # start: close APC
        self.close_apc = QtWidgets.QPushButton(self.frame_5)
        closePalette(self.close_apc)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(True)
        font.setWeight(75)
        self.close_apc.setFont(font)
        self.close_apc.setObjectName(_fromUtf8("close_apc"))
        self.startCloseHLayout.addWidget(self.close_apc)
        # end: close APC
        self.gridLayout_17.addLayout(self.startCloseHLayout, 5, 0, 1, 1)
        # end: Start and Close button row  
             
        self.gridLayout_30.addLayout(self.gridLayout_17, 0, 4, 1, 1)
        
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"))
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName(_fromUtf8("horizontalLayout_27"))
        
        self.bsOfstSRposFrame = QtWidgets.QFrame(self.frame_5)
        self.bsOfstSRposFrame.setEnabled(True)
        self.bsOfstSRposFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bsOfstSRposFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bsOfstSRposFrame.setObjectName(_fromUtf8("frame_4"))
        
        self.gridLayout_14 = QtWidgets.QGridLayout(self.bsOfstSRposFrame)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        
        # programmed offsets
        
        self.progOffsHorLayout = QtWidgets.QHBoxLayout()
        self.progOffsHorLayout.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.progOffsLayout = QtWidgets.QGridLayout()
        self.progOffsLayout.setObjectName(_fromUtf8("gridLayout_60"))
        
        self.xel_prog_offsets = QtWidgets.QDoubleSpinBox(self.bsOfstSRposFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.xel_prog_offsets.setFont(font)
        self.xel_prog_offsets.setDecimals(2)
        self.xel_prog_offsets.setMinimum(-99.0)
        self.xel_prog_offsets.setMaximum(99.0)
        self.xel_prog_offsets.setSingleStep(0.01)
        self.xel_prog_offsets.setObjectName(_fromUtf8("xel_prog_offsets"))
        self.progOffsLayout.addWidget(self.xel_prog_offsets, 2, 1, 1, 1)
        
        self.xElLabel = QtWidgets.QLabel(self.bsOfstSRposFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.xElLabel.setFont(font)
        self.xElLabel.setObjectName(_fromUtf8("xElLabel"))
        self.xElLabel.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "xEl(mdeg)", None))
        self.progOffsLayout.addWidget(self.xElLabel, 1, 0, 2, 1)
        
        self.set_offsets = QtWidgets.QPushButton(self.bsOfstSRposFrame)
        self.set_offsets.setEnabled(True)
        offsetPalette(self.set_offsets)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.set_offsets.setFont(font)
        self.set_offsets.setObjectName(_fromUtf8("set_offsets"))
        self.set_offsets.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "set", None)) 
        self.progOffsLayout.addWidget(self.set_offsets, 2, 3, 1, 1)
        
        spacerItem4 = QtWidgets.QSpacerItem(40, 20,
                 QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.progOffsLayout.addItem(spacerItem4, 0, 2, 1, 1)
        self.label_225 = QtWidgets.QLabel(self.bsOfstSRposFrame)
        self.label_225.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_225.setFont(font)
        self.label_225.setObjectName(_fromUtf8("label_225"))
        self.label_225.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "El(mdeg)", None))
        self.progOffsLayout.addWidget(self.label_225, 0, 0, 1, 1)
        
        self.BSoffsetLabel = QtWidgets.QLabel(self.bsOfstSRposFrame)
        self.BSoffsetLabel.setEnabled(False)
        self.BSoffsetLabel.setObjectName(_fromUtf8("label_91"))
        self.BSoffsetLabel.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "BS Offsets", None))        
        self.progOffsLayout.addWidget(self.BSoffsetLabel, 0, 3, 1, 1)
        
        self.el_prog_offsets = QtWidgets.QDoubleSpinBox(self.bsOfstSRposFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.el_prog_offsets.setFont(font)
        self.el_prog_offsets.setDecimals(2)
        self.el_prog_offsets.setMinimum(-999.0)
        self.el_prog_offsets.setMaximum(999.99)
        self.el_prog_offsets.setSingleStep(0.01)
        self.el_prog_offsets.setObjectName(_fromUtf8("el_prog_offsets"))
        self.progOffsLayout.addWidget(self.el_prog_offsets, 0, 1, 1, 1)
        
        self.progOffsHorLayout.addLayout(self.progOffsLayout)
        
        self.horizontalLayout_16.addLayout(self.progOffsHorLayout)
        
        self.gridLayout_33 = QtWidgets.QGridLayout()
        self.gridLayout_33.setObjectName(_fromUtf8("gridLayout_33"))
        
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName(_fromUtf8("horizontalLayout_28"))
        
        self.kled_12 = KLed(self.bsOfstSRposFrame)
        self.kled_12.setChecked(not self.kled_12.isChecked())
        self.kled_12.setObjectName(_fromUtf8("kled_12"))
        self.horizontalLayout_28.addWidget(self.kled_12)
        
        self.kled_17 = KLed(self.bsOfstSRposFrame)
        self.kled_17.setObjectName(_fromUtf8("kled_17"))
        self.horizontalLayout_28.addWidget(self.kled_17)
        
        self.kled_14 = KLed(self.bsOfstSRposFrame)
        self.kled_14.setChecked(not self.kled_14.isChecked())
        self.kled_14.setObjectName(_fromUtf8("kled_14"))
        
        self.horizontalLayout_28.addWidget(self.kled_14)
        self.gridLayout_33.addLayout(self.horizontalLayout_28, 2, 1, 1, 1)
        
        self.SRposLabel = QtWidgets.QLabel(self.bsOfstSRposFrame)
        self.SRposLabel.setObjectName(_fromUtf8("SRposLabel"))
        self.SRposLabel.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "SR Pos", None))
        self.gridLayout_33.addWidget(self.SRposLabel, 0, 1, 1, 1)
        
        self.horizontalLayout_16.addLayout(self.gridLayout_33)
        self.gridLayout_14.addLayout(self.horizontalLayout_16, 2, 0, 1, 1)
        
        self.horizontalLayout_27.addWidget(self.bsOfstSRposFrame)
        self.gridLayout_18.addLayout(self.horizontalLayout_27, 1, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20,
                 QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_18.addItem(spacerItem5, 0, 1, 1, 1)
        
        self.modeTabWidget = QtWidgets.QTabWidget(self.frame_5)
        tabPalette(self.modeTabWidget)
        #palette = self.tabPalette()
        #self.modeTabWidget.setPalette(palette)
        self.modeTabWidget.setObjectName(_fromUtf8("tabWidget"))
        
        self.modeTab = QtWidgets.QWidget()
        self.modeTab.setObjectName(_fromUtf8("Mode"))
        
        self.gridLayout_36 = QtWidgets.QGridLayout(self.modeTab)
        self.gridLayout_36.setObjectName(_fromUtf8("gridLayout_36"))
        
        self.frame_7 = QtWidgets.QFrame(self.modeTab)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName(_fromUtf8("frame_7"))
        
        self.gridLayout_24 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_24.setObjectName(_fromUtf8("gridLayout_24"))
        
        self.FEstatusLayout = QtWidgets.QVBoxLayout()
        self.FEstatusLayout.setObjectName(_fromUtf8("verticalLayout_2"))
        
        self.label_6 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_6.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Front End", None))
        self.FEstatusLayout.addWidget(self.label_6)
        
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName(_fromUtf8("horizontalLayout_30"))
        
        self.label_9 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_9.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "Feed 1", None))
        self.horizontalLayout_30.addWidget(self.label_9)
        
        self.label_8 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_8.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "Feed 2", None))
        self.horizontalLayout_30.addWidget(self.label_8)
        
        # Front End Status Box
        self.FEstatusLayout.addLayout(self.horizontalLayout_30)
        # feed crossover
        self.checkFeeds = QtWidgets.QCheckBox(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkFeeds.setFont(font)
        self.checkFeeds.setObjectName(_fromUtf8("checkFeeds"))
        self.checkFeeds.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Feeds Crossed", None))
        self.FEstatusLayout.addWidget(self.checkFeeds)
        
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.checkAmp1 = QtWidgets.QCheckBox(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkAmp1.setFont(font)
        self.checkAmp1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkAmp1.setChecked(True)
        self.checkAmp1.setObjectName(_fromUtf8("checkAmp1"))
        self.checkAmp1.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Amp1,2 Bias", None))
        self.horizontalLayout_8.addWidget(self.checkAmp1)
        self.checkAmp2 = QtWidgets.QCheckBox(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkAmp2.setFont(font)
        self.checkAmp2.setChecked(True)
        self.checkAmp2.setObjectName(_fromUtf8("checkAmp2"))
        self.checkAmp2.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Amp3,4 Bias", None))
        self.horizontalLayout_8.addWidget(self.checkAmp2)
        self.FEstatusLayout.addLayout(self.horizontalLayout_8)
        
        # Sky/Load Switch Layout
        self.skyLoadLayout = QtWidgets.QHBoxLayout()
        self.skyLoadLayout.setObjectName(_fromUtf8("skyLoadLayout"))
        
        self.SwitchSkyLoad = {}
        for num in [1,2]:
          self.SwitchSkyLoad[num] = QtWidgets.QComboBox(self.frame_7)
          self.stdSizePolicyMinimum(self.SwitchSkyLoad[num])
          font = QtGui.QFont()
          font.setPointSize(8)
          self.SwitchSkyLoad[num].setFont(font)
          self.SwitchSkyLoad[num].setObjectName(
                                            _fromUtf8("SwitchSkyLoad"+str(num)))
          self.SwitchSkyLoad[num].addItem(_fromUtf8(""))
          self.SwitchSkyLoad[num].addItem(_fromUtf8(""))
          self.SwitchSkyLoad[num].setItemText(0,
                   QtWidgets.QApplication.translate("Observatory", "Sky", None))
          self.SwitchSkyLoad[num].setItemText(1,
                  QtWidgets.QApplication.translate("Observatory", "Load", None))
          self.skyLoadLayout.addWidget(self.SwitchSkyLoad[num])
                
        self.FEstatusLayout.addLayout(self.skyLoadLayout)
        # end Sky/Load Switch Layout
        
        self.gridLayout_24.addLayout(self.FEstatusLayout, 0, 0, 1, 1)
        
        self.gridLayout_36.addWidget(self.frame_7, 0, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.verticalLayout_23 = QtWidgets.QVBoxLayout()
        self.verticalLayout_23.setObjectName(_fromUtf8("verticalLayout_23"))
        
        self.pwrMtrsLabel = QtWidgets.QLabel(self.modeTab)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pwrMtrsLabel.setFont(font)
        self.pwrMtrsLabel.setObjectName(_fromUtf8("pwrMtrsLabel"))
        self.pwrMtrsLabel.setText(QtWidgets.QApplication.translate(
                                           "Observatory", "Power Meters", None))
        self.verticalLayout_23.addWidget(self.pwrMtrsLabel)
        
        self.labelPM = {}
        for num in [1,2,3,4]:
          self.labelPM[num] = QtWidgets.QLabel(self.modeTab)
          palette = self.pmLabelPalette()
          self.labelPM[num].setPalette(palette)
          font = QtGui.QFont()
          font.setPointSize(9)
          self.labelPM[num].setFont(font)
          self.labelPM[num].setAutoFillBackground(True)
          self.labelPM[num].setFrameShape(QtWidgets.QFrame.WinPanel)
          self.labelPM[num].setFrameShadow(QtWidgets.QFrame.Sunken)
          self.labelPM[num].setAlignment(QtCore.Qt.AlignCenter)
          self.labelPM[num].setObjectName(_fromUtf8("labelPM"+str(num)))
          self.labelPM[num].setText(QtWidgets.QApplication.translate(
                                 "Observatory", "PM"+str(num)+" reading", None))
          self.verticalLayout_23.addWidget(self.labelPM[num])

        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName(_fromUtf8("horizontalLayout_31"))
        
        self.WradioButton = QtWidgets.QRadioButton(self.modeTab)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.WradioButton.setFont(font)
        self.WradioButton.setChecked(True)
        self.WradioButton.setAutoExclusive(True)
        self.WradioButton.setObjectName(_fromUtf8("WradioButton"))
        self.horizontalLayout_31.addWidget(self.WradioButton)
        
        self.dBmradioButton = QtWidgets.QRadioButton(self.modeTab)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.dBmradioButton.setFont(font)
        self.dBmradioButton.setChecked(False)
        self.dBmradioButton.setAutoExclusive(True)
        self.dBmradioButton.setObjectName(_fromUtf8("dBmradioButton"))
        self.horizontalLayout_31.addWidget(self.dBmradioButton)
        
        self.verticalLayout_23.addLayout(self.horizontalLayout_31)
        self.gridLayout_7.addLayout(self.verticalLayout_23, 0, 0, 1, 1)
        
        # Attenuation Box
        self.attenVLayout = QtWidgets.QVBoxLayout()
        self.attenVLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.attenuationLabel = QtWidgets.QLabel(self.modeTab)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.attenuationLabel.setFont(font)
        self.attenuationLabel.setObjectName(_fromUtf8("attenuationLabel"))
        self.attenuationLabel.setText(QtWidgets.QApplication.translate(
                                        "Observatory", "Attenuation(dB)", None))
        self.attenVLayout.addWidget(self.attenuationLabel)
        
        self.set_atten = QtWidgets.QPushButton(self.modeTab)
        self.set_atten.setObjectName(_fromUtf8("set_atten"))
        self.set_atten.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Set Atten", None))
        self.attenVLayout.addWidget(self.set_atten)
        
        self.atten = {}
        for num in [1,2,3,4]:
          self.atten[num] = QtWidgets.QDoubleSpinBox(self.modeTab)
          self.atten[num].setMaximum(15.0)
          self.atten[num].setObjectName(_fromUtf8("atten"+str(num)))
          self.attenVLayout.addWidget(self.atten[num])
        self.gridLayout_7.addLayout(self.attenVLayout, 0, 1, 1, 1)
        
        self.gridLayout_36.addLayout(self.gridLayout_7, 2, 0, 1, 1)
        self.frame_13 = QtWidgets.QFrame(self.modeTab)
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName(_fromUtf8("frame_13"))
        
        self.gridLayout_32 = QtWidgets.QGridLayout(self.frame_13)
        self.gridLayout_32.setObjectName(_fromUtf8("gridLayout_32"))
        
        self.label_7 = QtWidgets.QLabel(self.frame_13)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_7.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Downconverter", None))
        self.gridLayout_32.addWidget(self.label_7, 0, 0, 1, 1)
        
        # band select
        self.SwitchBand = QtWidgets.QComboBox(self.frame_13)
        self.stdSizePolicyMinimum(self.SwitchBand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SwitchBand.setFont(font)
        self.SwitchBand.setObjectName(_fromUtf8("SwitchBand"))
        self.SwitchBand.addItem(_fromUtf8(""))
        self.SwitchBand.setItemText(0, QtWidgets.QApplication.translate(
                                               "Observatory", "17-19GHz", None))
        self.SwitchBand.addItem(_fromUtf8(""))
        self.SwitchBand.setItemText(1, QtWidgets.QApplication.translate(
                                               "Observatory", "19-21GHz", None))
        self.SwitchBand.addItem(_fromUtf8(""))
        self.SwitchBand.setItemText(2, QtWidgets.QApplication.translate(
                                               "Observatory", "21-23GHz", None))
        self.SwitchBand.addItem(_fromUtf8(""))
        self.SwitchBand.setItemText(3, QtWidgets.QApplication.translate(
                                               "Observatory", "23-25GHz", None))
        self.SwitchBand.addItem(_fromUtf8(""))
        self.SwitchBand.setItemText(4, QtWidgets.QApplication.translate(
                                               "Observatory", "25-27GHz", None))
        self.SwitchBand.setCurrentIndex(2)
        self.gridLayout_32.addWidget(self.SwitchBand, 1, 0, 1, 1)
        
        # polarization select
        self.LCselectHLayout = QtWidgets.QHBoxLayout()
        self.LCselectHLayout.setObjectName(_fromUtf8("horizontalLayout_41"))
        self.SwitchLin = {}
        for num in [1,2]:
          self.SwitchLin[num] = QtWidgets.QComboBox(self.frame_13)
          self.stdSizePolicyMinimum(self.SwitchLin[num])
          font = QtGui.QFont()
          font.setPointSize(8)
          self.SwitchLin[num].setFont(font)
          self.SwitchLin[num].setObjectName(_fromUtf8("SwitchLin"+str(num)))
          self.SwitchLin[num].addItem(_fromUtf8(""))
          self.SwitchLin[num].addItem(_fromUtf8(""))
          self.SwitchLin[num].setItemText(0, QtWidgets.QApplication.translate(
                                                 "Observatory", "linear", None))
          self.SwitchLin[num].setItemText(1, QtWidgets.QApplication.translate(
                                               "Observatory", "circular", None))
          self.SwitchLin[num].setCurrentIndex(0)
          self.LCselectHLayout.addWidget(self.SwitchLin[num])
        self.gridLayout_32.addLayout(self.LCselectHLayout, 3, 0, 1, 1)
        
        # UL/IQ select
        self.ULIQselectHLayout = QtWidgets.QHBoxLayout()
        self.ULIQselectHLayout.setObjectName(_fromUtf8("horizontalLayout_42"))
        self.SwitchULIQ = {}
        for num in [1,2]:
          self.SwitchULIQ[num] = QtWidgets.QComboBox(self.frame_13)
          self.stdSizePolicyMinimum(self.SwitchULIQ[num])
          font = QtGui.QFont()
          font.setPointSize(8)
          self.SwitchULIQ[num].setFont(font)
          self.SwitchULIQ[num].setObjectName(_fromUtf8("Switch1ULIQ"))
          self.SwitchULIQ[num].addItem(_fromUtf8(""))
          self.SwitchULIQ[num].addItem(_fromUtf8(""))
          self.SwitchULIQ[num].setItemText(0, QtWidgets.QApplication.translate(
                                                     "Observatory", "UL", None))
          self.SwitchULIQ[num].setItemText(1, QtWidgets.QApplication.translate(
                                                     "Observatory", "IQ", None))
          self.SwitchULIQ[num].setCurrentIndex(0)
          self.ULIQselectHLayout.addWidget(self.SwitchULIQ[num])
        self.gridLayout_32.addLayout(self.ULIQselectHLayout, 2, 0, 1, 1)
        
        # Y-factor
        self.yfactor = QtWidgets.QPushButton(self.frame_13)
        self.yfactor.setCheckable(True)
        self.yfactor.setObjectName(_fromUtf8("yfactor"))
        self.yfactor.setText(QtWidgets.QApplication.translate(
                                                "Observatory", "YFactor", None))
        self.gridLayout_32.addWidget(self.yfactor, 4, 0, 1, 1)
        
        self.gridLayout_36.addWidget(self.frame_13, 1, 0, 1, 1)
        self.modeTabWidget.addTab(self.modeTab, _fromUtf8(""))
        
        self.Boresight = QtWidgets.QWidget()
        self.Boresight.setObjectName(_fromUtf8("Boresight"))
        self.gridLayout_40 = QtWidgets.QGridLayout(self.Boresight)
        
        self.gridLayout_40.setObjectName(_fromUtf8("gridLayout_40"))
        
        self.gridLayout_35 = QtWidgets.QGridLayout()
        self.gridLayout_35.setObjectName(_fromUtf8("gridLayout_35"))
        
        self.label_30 = QtWidgets.QLabel(self.Boresight)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_30.setFont(font)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.label_30.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Boresight", None))
        self.gridLayout_35.addWidget(self.label_30, 0, 0, 1, 1)
        
        self.bs_source_que = QtWidgets.QListWidget(self.Boresight)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.bs_source_que.setFont(font)
        self.bs_source_que.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.bs_source_que.setObjectName(_fromUtf8("bs_source_que"))
        self.gridLayout_35.addWidget(self.bs_source_que, 1, 1, 1, 1)
        
        self.label_20 = QtWidgets.QLabel(self.Boresight)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_20.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "BS sources", None))
        self.gridLayout_35.addWidget(self.label_20, 0, 1, 1, 1)
        
        self.frame_10 = QtWidgets.QFrame(self.Boresight)
        self.stdSizePolicyExpanding(self.frame_10)
        self.frame_10.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_10.setMaximumSize(QtCore.QSize(361, 161))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_10.setFont(font)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName(_fromUtf8("frame_10"))
        self.gridLayout_13 = QtWidgets.QGridLayout(self.frame_10)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_33.setObjectName(_fromUtf8("horizontalLayout_33"))
        
        self.label_11 = QtWidgets.QLabel(self.frame_10)
        self.stdSizePolicyFixed(self.label_11)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_11.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Pts.", None))
        self.horizontalLayout_33.addWidget(self.label_11)
        
        self.bs_points = QtWidgets.QLineEdit(self.frame_10)
        self.bs_points.setEnabled(False)
        self.bs_points.setObjectName(_fromUtf8("bs_points"))
        self.horizontalLayout_33.addWidget(self.bs_points)
        
        self.verticalLayout_4.addLayout(self.horizontalLayout_33)
        
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_34.setObjectName(_fromUtf8("horizontalLayout_34"))
        
        self.label_24 = QtWidgets.QLabel(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_24.setFont(font)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.horizontalLayout_34.addWidget(self.label_24)
        self.bs_repeats = QtWidgets.QLineEdit(self.frame_10)
        self.bs_repeats.setEnabled(False)
        self.bs_repeats.setObjectName(_fromUtf8("bs_repeats"))
        self.horizontalLayout_34.addWidget(self.bs_repeats)
        self.verticalLayout_4.addLayout(self.horizontalLayout_34)
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setObjectName(_fromUtf8("horizontalLayout_35"))
        self.label_31 = QtWidgets.QLabel(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_31.setFont(font)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.horizontalLayout_35.addWidget(self.label_31)
        self.beamsize = QtWidgets.QLineEdit(self.frame_10)
        self.beamsize.setEnabled(False)
        self.beamsize.setObjectName(_fromUtf8("beamsize"))
        self.horizontalLayout_35.addWidget(self.beamsize)
        self.verticalLayout_4.addLayout(self.horizontalLayout_35)
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setObjectName(_fromUtf8("horizontalLayout_36"))
        self.label_25 = QtWidgets.QLabel(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_25.setFont(font)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.horizontalLayout_36.addWidget(self.label_25)
        self.bs_rate = QtWidgets.QDoubleSpinBox(self.frame_10)
        self.bs_rate.setDecimals(1)
        self.bs_rate.setMinimum(1.0)
        self.bs_rate.setMaximum(20.0)
        self.bs_rate.setProperty("value", 2.0)
        self.bs_rate.setObjectName(_fromUtf8("bs_rate"))
        self.horizontalLayout_36.addWidget(self.bs_rate)
        self.verticalLayout_4.addLayout(self.horizontalLayout_36)
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName(_fromUtf8("horizontalLayout_37"))
        self.label_32 = QtWidgets.QLabel(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_32.setFont(font)
        self.label_32.setObjectName(_fromUtf8("label_32"))
        self.horizontalLayout_37.addWidget(self.label_32)
        self.bs_combo_box = QtWidgets.QComboBox(self.frame_10)
        self.bs_combo_box.setObjectName(_fromUtf8("bs_combo_box"))
        self.bs_combo_box.addItem(_fromUtf8(""))
        self.bs_combo_box.addItem(_fromUtf8(""))
        self.horizontalLayout_37.addWidget(self.bs_combo_box)
        self.verticalLayout_4.addLayout(self.horizontalLayout_37)
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setObjectName(_fromUtf8("horizontalLayout_38"))
        
        self.kled = KLed(self.frame_10)
        self.kled.setChecked(not self.kled.isChecked())
        self.kled.setObjectName(_fromUtf8("kled"))
        self.horizontalLayout_38.addWidget(self.kled)
        
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_38.addItem(spacerItem6)
        self.calc_bs_results = QtWidgets.QPushButton(self.frame_10)
        #palette = self.
        #self.calc_bs_results.setPalette(palette)
        bsPalette(self.calc_bs_results)
        self.calc_bs_results.setCheckable(True)
        self.calc_bs_results.setAutoExclusive(True)
        self.calc_bs_results.setObjectName(_fromUtf8("calc_bs_results"))
        self.horizontalLayout_38.addWidget(self.calc_bs_results)
        self.verticalLayout_4.addLayout(self.horizontalLayout_38)
        self.gridLayout_13.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.gridLayout_35.addWidget(self.frame_10, 1, 0, 1, 1)
        
        # boresight plot
        self.bore_mpl = QtWidgets.QWidget(self.Boresight)
        self.stdSizePolicyExpanding(self.bore_mpl)
        self.bore_mpl.setMinimumSize(QtCore.QSize(0, 0))
        self.bore_mpl.setObjectName(_fromUtf8("bore_mpl"))
        self.bore_fig = Figure()
        self.bore_canvas = FigureCanvas(self.bore_fig)
        self.bore_axes = self.bore_fig.add_subplot(111)
        self.bore_axes.grid(color='grey', linestyle='--', linewidth=0.5)
        self.bore_axes.set_title("Boresight", fontsize=8)
        self.bore_VBL = QtWidgets.QVBoxLayout(self.bore_mpl)
        self.bore_VBL.addWidget(self.bore_canvas)
        self.bore_NTB = NavigationToolbar(self.bore_canvas, self.bore_mpl)
        self.bore_VBL.addWidget(self.bore_NTB)
        self.gridLayout_35.addWidget(self.bore_mpl, 3, 0, 1, 2)
        
        self.slew_to_source = QtWidgets.QPushButton(self.Boresight)
        self.slew_to_source.setToolTip('Send source to antenna and track')
        #palette = self.bs2Palette()
        #self.slew_to_source.setPalette(palette)
        bs2Palette(self.slew_to_source)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.slew_to_source.setFont(font)
        self.slew_to_source.setCheckable(True)
        self.slew_to_source.setObjectName(_fromUtf8("slew_to_source"))
        self.slew_to_source.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "slew to source", None))
        self.gridLayout_35.addWidget(self.slew_to_source, 2, 0, 1, 1)
        
        self.gridLayout_40.addLayout(self.gridLayout_35, 0, 0, 1, 1)
        
        self.modeTabWidget.addTab(self.Boresight, _fromUtf8(""))
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridLayout_38 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_38.setObjectName(_fromUtf8("gridLayout_38"))
        
        self.frame_16 = QtWidgets.QFrame(self.tab_3)
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName(_fromUtf8("frame_16"))
        
        self.gridLayout_44 = QtWidgets.QGridLayout(self.frame_16)
        self.gridLayout_44.setObjectName(_fromUtf8("gridLayout_44"))
        
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName(_fromUtf8("verticalLayout_17"))
        
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName(_fromUtf8("verticalLayout_19"))
        
        # tipcurve plot
        self.tipping_mpl = QtWidgets.QWidget(self.frame_16)
        self.stdSizePolicyExpanding(self.tipping_mpl)
        self.tipping_mpl.setMinimumSize(QtCore.QSize(0, 0))
        self.tipping_mpl.setMaximumSize(QtCore.QSize(300, 200))
        self.tipping_mpl.setObjectName(_fromUtf8("tipping_mpl"))
        self.tipping_fig = Figure()
        self.tipping_canvas = FigureCanvas(self.tipping_fig)
        self.tipping_axes = self.tipping_fig.add_subplot(111)
        self.tipping_axes.grid(color='grey', linestyle='--', linewidth=0.5)
        self.tipping_axes.set_title("Tsys vs Elevation", fontsize=8)
        self.tipping_VBL = QtWidgets.QVBoxLayout(self.tipping_mpl)
        self.tipping_VBL.addWidget(self.tipping_canvas)
        self.tipping_NTB = NavigationToolbar(self.tipping_canvas, self.tipping_mpl)
        self.tipping_VBL.addWidget(self.tipping_NTB)  
        self.verticalLayout_19.addWidget(self.tipping_mpl)
        
        # tipcurve button
        self.tipping_PB = QtWidgets.QPushButton(self.frame_16)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tipping_PB.setFont(font)
        self.tipping_PB.setCheckable(True)
        self.tipping_PB.setObjectName(_fromUtf8("tipping"))
        self.tipping_PB.setText(QtWidgets.QApplication.translate(
                                                "Observatory", "Tipping", None))
        self.verticalLayout_19.addWidget(self.tipping_PB)
        
        self.verticalLayout_17.addLayout(self.verticalLayout_19)
        
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName(_fromUtf8("verticalLayout_20"))
        
        # beam map
        self.beammap_mpl = QtWidgets.QWidget(self.frame_16)
        self.stdSizePolicyExpanding(self.beammap_mpl)
        self.beammap_mpl.setMinimumSize(QtCore.QSize(0, 0))
        self.beammap_mpl.setMaximumSize(QtCore.QSize(300, 200))
        self.beammap_mpl.setObjectName(_fromUtf8("beammap_mpl"))
        self.beammap_fig = Figure()
        self.beammap_canvas = FigureCanvas(self.beammap_fig)
        self.beammap_axes = self.beammap_fig.add_subplot(111, projection="polar")
        self.beammap_axes.grid(color='grey', linestyle='--', linewidth=0.5)
        self.beammap_axes.set_title("Beam Scan Plot", fontsize=8)
        self.beammap_axes.set_theta_zero_location('N')
        self.beammap_axes.invert_yaxis()
        self.beammap_axes.set_theta_direction(-1)
        self.beammap_VLB = QtWidgets.QVBoxLayout(self.beammap_mpl)
        self.beammap_VLB.addWidget(self.beammap_canvas)
        self.verticalLayout_20.addWidget(self.beammap_mpl)
        
        # beam map pushbutton
        self.beammap_PB = QtWidgets.QPushButton(self.frame_16)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.beammap_PB.setFont(font)
        self.beammap_PB.setCheckable(True)
        self.beammap_PB.setObjectName(_fromUtf8("beammap"))
        self.beammap_PB.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Beam Map", None))
        self.verticalLayout_20.addWidget(self.beammap_PB)
        
        self.verticalLayout_17.addLayout(self.verticalLayout_20)
        
        self.gridLayout_44.addLayout(self.verticalLayout_17, 0, 0, 1, 1)
        
        self.gridLayout_38.addWidget(self.frame_16, 0, 0, 1, 1)
        
        self.modeTabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.gridLayout_18.addWidget(self.modeTabWidget, 0, 0, 1, 1)
        
        self.gridLayout_30.addLayout(self.gridLayout_18, 0, 2, 1, 1)
        
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName(_fromUtf8("gridLayout_19"))
        
        # system temperature plot
        self.tsys_widget = QtWidgets.QWidget(self.frame_5)
        self.stdSizePolicyExpanding( self.tsys_widget)
        self.tsys_widget.setMinimumSize(QtCore.QSize(289, 191))
        self.tsys_widget.setMaximumSize(QtCore.QSize(1000, 1000))
        self.tsys_widget.setObjectName(_fromUtf8("tsys_widget"))
        self.tsys_fig = Figure()
        self.tsys_canvas = FigureCanvas(self.tsys_fig)
        self.tsys_axes = self.tsys_fig.add_subplot(111)
        self.tsys_axes.set_title("Tsys vs Time", fontsize=8)
        self.tsys_axes.set_ylabel ('Tsys(K)', fontsize = 'smaller')
        self.tsys_axes.set_xlabel ('Time (sec)', fontsize = 'smaller')
        self.tsys_axes.tick_params(axis='both', which='major', labelsize=8)
        self.tsys_axes.set_title("W vs Time", fontsize=8)
        self.tsys_axes.set_ylabel ('ND(W)', fontsize = 'smaller')
        self.tsys_canvas.draw()
        self.tsys_VBL = QtWidgets.QVBoxLayout(self.tsys_widget)
        self.tsys_VBL.addWidget(self.tsys_canvas)
        self.tsys_NTB = NavigationToolbar(self.tsys_canvas, self.tsys_widget)
        self.tsys_VBL.addWidget(self.tsys_NTB)
        self.gridLayout_19.addWidget(self.tsys_widget, 1, 0, 1, 1)
        
        spacerItem7 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding, 
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_19.addItem(spacerItem7, 3, 0, 1, 1)
        
        # source location on Observations page
        self.source_mpl = QtWidgets.QWidget(self.frame_5)
        self.source_mpl.setToolTip('Antenna direction')
        self.stdSizePolicyExpanding(self.source_mpl)
        self.source_mpl.setMinimumSize(QtCore.QSize(289, 191))
        self.source_mpl.setMaximumSize(QtCore.QSize(1000, 1000))
        self.source_mpl.setObjectName(_fromUtf8("source_mpl"))
        self.source_fig = Figure()
        self.source_canvas = FigureCanvas(self.source_fig)
        self.source_axes = self.source_fig.add_subplot(111, projection="polar")
        self.source_axes.set_theta_direction(-1)
        self.source_axes.set_theta_zero_location('N')
        self.source_axes.set_ylim(0,90)
        self.source_axes.invert_yaxis()
        self.source_axes.set_thetagrids(numpy.arange(0, 360, 20))
        self.source_axes.grid(color='grey', linestyle='--', linewidth=0.5)
        self.source_axes.set_title("Antenna Az-El Plot", fontsize=8)
        self.azel_mark, = self.source_axes.plot(0, 90,
                             marker='o', color='red')
        self.source_VBL = QtWidgets.QVBoxLayout(self.source_mpl)
        self.source_VBL.addWidget(self.source_canvas)
        self.source_NTB = NavigationToolbar(self.source_canvas, self.source_mpl)
        self.source_VBL.addWidget(self.source_NTB)
        self.gridLayout_19.addWidget(self.source_mpl, 0, 0, 1, 1)
        
        self.gridLayout_30.addLayout(self.gridLayout_19, 0, 0, 1, 1)
        
        self.gridLayout_28.addWidget(self.frame_5, 0, 0, 1, 1)
        
        self.gridLayout_27.addLayout(self.gridLayout_28, 0, 0, 1, 1)
        
        self.Ctrl_Tabs.addTab(self.ObsSummary, _fromUtf8(""))
        self.Ctrl_Tabs.setTabText(self.Ctrl_Tabs.indexOf(self.ObsSummary),
                                  QtWidgets.QApplication.translate(
                                           "Observatory", "Observations", None))
        # end of Observations page
        
        # page for the Catalogues tab ##########################################
        self.Sources = QtWidgets.QWidget()
        self.Sources.setObjectName(_fromUtf8("Sources"))
        
        # right side of the page
        self.CatalogTabLayout = QtWidgets.QGridLayout(self.Sources)
        self.CatalogTabLayout.setObjectName(_fromUtf8("gridLayout_15"))
        
        # tracker widgets
        self.modeTabWidget_2 = QtWidgets.QTabWidget(self.Sources)
        self.modeTabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        
        self.gridLayout_37 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_37.setObjectName(_fromUtf8("gridLayout_37"))
        
        # elevation vs time plot
        self.EltimeSource = QtWidgets.QWidget(self.tab)
        self.stdSizePolicyMinimum(self.EltimeSource)
        self.EltimeSource.setMinimumSize(QtCore.QSize(175, 175))
        self.EltimeSource.setMaximumSize(QtCore.QSize(275, 275))
        self.EltimeSource.setObjectName(_fromUtf8("EltimeSource"))
        self.ElTime_fig = Figure()
        self.ElTime_canvas = FigureCanvas(self.ElTime_fig)
        self.ElTime_axes = self.ElTime_fig.add_subplot(111)
        self.ElTime_axes.grid(color='grey', linestyle='--', linewidth=0.5)
        self.ElTime_axes.set_title("Elevation-Time", fontsize=8)
        self.ElTime_axes.tick_params(axis='both', which='major', labelsize=6)
        self.vbl9 = QtWidgets.QVBoxLayout(self.EltimeSource)
        self.vbl9.addWidget(self.ElTime_canvas)
        self.ntb9 = NavigationToolbar(self.ElTime_canvas, self.EltimeSource)
        self.vbl9.addWidget(self.ntb9)
        self.gridLayout_37.addWidget(self.EltimeSource, 0, 0, 1, 1)
        
        self.frame_14 = QtWidgets.QFrame(self.tab)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName(_fromUtf8("frame_14"))
        
        self.gridLayout_34 = QtWidgets.QGridLayout(self.frame_14)
        self.gridLayout_34.setObjectName(_fromUtf8("gridLayout_34"))
        
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        
        self.label_66 = QtWidgets.QLabel(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_66.setFont(font)
        self.label_66.setObjectName(_fromUtf8("label_66"))
        self.label_66.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Source Info", None))
        self.gridLayout_9.addWidget(self.label_66, 0, 0, 1, 1)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        
        self.sourceInfo = QtWidgets.QPlainTextEdit(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.sourceInfo.setFont(font)
        self.sourceInfo.setReadOnly(True)
        self.sourceInfo.setObjectName(_fromUtf8("sourceInfo"))
        self.sourceInfo.setPlainText(QtWidgets.QApplication.translate(
                                      "Observatory", "source_unselected", None))
        self.verticalLayout_14.addWidget(self.sourceInfo)
        
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setObjectName(_fromUtf8("horizontalLayout_39"))
        self.verticalLayout_14.addLayout(self.horizontalLayout_39)
        
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.verticalLayout_14.addWidget(self.dateTimeEdit)
        
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setObjectName(_fromUtf8("horizontalLayout_47"))
        
        # pick source
        self.pick_source = QtWidgets.QPushButton(self.frame_14)
        self.pick_source.setToolTip('Add to Source List on Observations tab')
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pick_source.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("reverse.png")),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pick_source.setIcon(icon1)
        self.pick_source.setIconSize(QtCore.QSize(20, 20))
        self.pick_source.setCheckable(False)
        self.pick_source.setChecked(False)
        self.pick_source.setAutoExclusive(False)
        self.pick_source.setAutoDefault(False)
        self.pick_source.setDefault(False)
        self.pick_source.setFlat(False)
        self.pick_source.setObjectName(_fromUtf8("pick_source"))
        self.pick_source.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Pick Source", None))
        self.horizontalLayout_47.addWidget(self.pick_source)
        
        self.find_nearest = QtWidgets.QPushButton(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.find_nearest.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(
        _fromUtf8("../../../../../../../../../../../../../../../../../../../../../home/asoni/.designer/backup/png/play.png")),
         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(
        _fromUtf8("../../../../../../../../../../../../../../../../../../../../../home/asoni/.designer/backup/png/pause.png")),
         QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.find_nearest.setIcon(icon2)
        self.find_nearest.setIconSize(QtCore.QSize(20, 20))
        self.find_nearest.setCheckable(False)
        self.find_nearest.setChecked(False)
        self.find_nearest.setAutoExclusive(False)
        self.find_nearest.setAutoDefault(False)
        self.find_nearest.setDefault(False)
        self.find_nearest.setFlat(False)
        self.find_nearest.setObjectName(_fromUtf8("find_nearest"))
        self.find_nearest.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "nearest BS", None))
        self.horizontalLayout_47.addWidget(self.find_nearest)
        self.verticalLayout_14.addLayout(self.horizontalLayout_47)
        
        self.horizontalLayout_40 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_40.setObjectName(_fromUtf8("horizontalLayout_40"))
        self.verticalLayout_14.addLayout(self.horizontalLayout_40)
        
        self.skymapSelectLayout = QtWidgets.QGridLayout()
        self.skymapSelectLayout.setObjectName(_fromUtf8("gridLayout_22"))
        
        self.checkDisplaySelect = {}
        for category in Observatory.categories:
          index = Observatory.categories.index(category)
          self.checkDisplaySelect[index] = QtWidgets.QCheckBox(self.frame_14)
          palette = QtGui.QPalette()
          palette.setColor(QtGui.QPalette.Text, QtGui.QColor(
                                          Observatory.styles[category]['fill']))
          self.checkDisplaySelect[index].setPalette(palette)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.checkDisplaySelect[index].setFont(font)
          self.checkDisplaySelect[index].setObjectName(_fromUtf8(category))
          self.checkDisplaySelect[index].setText(
                QtWidgets.QApplication.translate("Observatory", category, None))
          label = QtWidgets.QApplication.translate("Observatory",
                                  Observatory.styles[category]['display'], None)
          self.checkDisplaySelect[index].setText(label)
          self.skymapSelectLayout.addWidget(self.checkDisplaySelect[index],
                                            index, 0, 1, 1)
          
        self.cb_tel = QtWidgets.QCheckBox(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cb_tel.setFont(font)
        self.cb_tel.setObjectName(_fromUtf8("cb_tel"))
        self.cb_tel.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Telescope", None))
        self.skymapSelectLayout.addWidget(self.cb_tel, 0, 1, 1, 1)
        
        self.cb_sun = QtWidgets.QCheckBox(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cb_sun.setFont(font)
        self.cb_sun.setObjectName(_fromUtf8("cb_sun"))
        self.cb_sun.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "Sun", None))
        self.skymapSelectLayout.addWidget(self.cb_sun, 1, 1, 1, 1)
           
        self.cb_moon = QtWidgets.QCheckBox(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cb_moon.setFont(font)
        self.cb_moon.setObjectName(_fromUtf8("cb_moon"))
        self.cb_moon.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Moon", None))
        self.skymapSelectLayout.addWidget(self.cb_moon, 2, 1, 1, 1)

        self.cb_op = QtWidgets.QCheckBox(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cb_op.setFont(font)
        self.cb_op.setObjectName(_fromUtf8("cb_op"))
        self.cb_op.setText(QtWidgets.QApplication.translate(
                                           "Observatory", "Current Source", None))
        self.skymapSelectLayout.addWidget(self.cb_op, 3, 1, 1, 1)
        
        self.cb_pl = QtWidgets.QCheckBox(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cb_pl.setFont(font)
        self.cb_pl.setObjectName(_fromUtf8("cb_pl"))
        self.cb_pl.setText(QtWidgets.QApplication.translate(
                                                "Observatory", "Planets", None))
        self.skymapSelectLayout.addWidget(self.cb_pl, 4, 1, 1, 1)
        
        self.cb_lab = QtWidgets.QCheckBox(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cb_lab.setFont(font)
        self.cb_lab.setObjectName(_fromUtf8("cb_lab"))
        self.cb_lab.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "Labels", None))
        self.skymapSelectLayout.addWidget(self.cb_lab, 5, 1, 1, 1)
        
        self.cb_gp = QtWidgets.QCheckBox(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cb_gp.setFont(font)
        self.cb_gp.setObjectName(_fromUtf8("cb_gp"))
        self.cb_gp.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Galactic Plane", None))
        self.skymapSelectLayout.addWidget(self.cb_gp, 6, 1, 1, 1)
        # end of plot display categories check boxes
        
        self.load_catalogue = QtWidgets.QPushButton(self.frame_14)
        self.load_catalogue.setEnabled(True)
        self.load_catalogue.setObjectName(_fromUtf8("load_catalogue"))
        self.load_catalogue.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Load Catalogue", None))
        self.skymapSelectLayout.addWidget(self.load_catalogue, 10, 0, 1, 2)
        
        self.Source_label = QtWidgets.QLabel(self.frame_14)
        self.Source_label.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Source_label.setFont(font)
        self.Source_label.setObjectName(_fromUtf8("Source_label"))
        self.Source_label.setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "Source", None))
        self.skymapSelectLayout.addWidget(self.Source_label, 11, 0, 1, 2)
        
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_48.setObjectName(_fromUtf8("horizontalLayout_48"))
        
        self.Dec_edit = QtWidgets.QLineEdit(self.frame_14)
        self.Dec_edit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Dec_edit.setFont(font)
        self.Dec_edit.setObjectName(_fromUtf8("Dec_edit"))
        self.horizontalLayout_48.addWidget(self.Dec_edit)
        self.skymapSelectLayout.addLayout(self.horizontalLayout_48, 12, 0, 1, 2)
        
        self.RA_label = QtWidgets.QLabel(self.frame_14)
        self.RA_label.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RA_label.setFont(font)
        self.RA_label.setObjectName(_fromUtf8("RA_label"))
        self.RA_label.setText(QtWidgets.QApplication.translate(
                                                     "Observatory", "RA", None))
        self.horizontalLayout_48.addWidget(self.RA_label)
        
        self.RA_edit = QtWidgets.QLineEdit(self.frame_14)
        self.RA_edit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RA_edit.setFont(font)
        self.RA_edit.setObjectName(_fromUtf8("RA_edit"))
        self.horizontalLayout_48.addWidget(self.RA_edit)
        
        self.Dec_label = QtWidgets.QLabel(self.frame_14)
        self.Dec_label.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Dec_label.setFont(font)
        self.Dec_label.setObjectName(_fromUtf8("Dec_label"))
        self.Dec_label.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "Dec", None))
        self.horizontalLayout_48.addWidget(self.Dec_label)
        
        self.verticalLayout_14.addLayout(self.skymapSelectLayout)
        
        self.gridLayout_9.addLayout(self.verticalLayout_14, 1, 0, 1, 1)
        self.gridLayout_34.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.gridLayout_37.addWidget(self.frame_14, 0, 1, 2, 1)
        
        self.AzTime = QtWidgets.QWidget(self.tab)
        self.stdSizePolicyMinimum(self.AzTime)
        self.AzTime.setMinimumSize(QtCore.QSize(175, 175))
        self.AzTime.setMaximumSize(QtCore.QSize(275, 275))
        self.AzTime.setObjectName(_fromUtf8("AzTime"))
        #self.canvas10.spectrum_Aztime(self.ui)
        self.AzTime_fig = Figure()
        self.AzTime_canvas = FigureCanvas(self.AzTime_fig)
        self.AzTime_axes = self.AzTime_fig.add_subplot(111)
        self.AzTime_axes.grid(color='grey', linestyle='--', linewidth=0.5)
        self.AzTime_axes.set_title("Azimuth-Time", fontsize=8)
        self.AzTime_axes.tick_params(axis='both', which='major', labelsize=6)
        
        self.AzTime_VBL = QtWidgets.QVBoxLayout(self.AzTime)
        self.AzTime_VBL.addWidget(self.AzTime_canvas)
        self.AzTime_NTB = NavigationToolbar(self.AzTime_canvas, self.AzTime)
        self.AzTime_VBL.addWidget(self.AzTime_NTB)

        self.gridLayout_37.addWidget(self.AzTime, 1, 0, 1, 1)
        
        self.modeTabWidget_2.addTab(self.tab, _fromUtf8(""))
        
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
                
        self.modeTabWidget_2.addTab(self.tab_2, _fromUtf8(""))
        self.modeTabWidget_2.setTabText(self.modeTabWidget_2.indexOf(self.tab_2),
            QtWidgets.QApplication.translate("Observatory",
                                             "AntennaTracker", None))
        self.CatalogTabLayout.addWidget(self.modeTabWidget_2, 0, 1, 1, 1)
        
        # left side of the page: sky map
        self.skymap_mpl = QtWidgets.QWidget(self.Sources)
        self.skymap_mpl.setToolTip(
            'Left click: select for Source Info\nRight click: show source name')
        self.stdSizePolicyExpanding(self.skymap_mpl)
        self.skymap_mpl.setMinimumSize(QtCore.QSize(300, 300))
        self.skymap_mpl.setMaximumSize(QtCore.QSize(600, 600))
        self.skymap_mpl.setObjectName(_fromUtf8("skymap_mpl"))
        self.skymap_fig = Figure()
        self.skymap_canvas = FigureCanvas(self.skymap_fig)
        self.skymap_axes = self.skymap_fig.add_subplot(111)
        self.skymap_axes.set_xlim(0, 360)
        self.skymap_axes.set_ylim(0, 90)
        self.skymap_axes.grid(True)
        self.skymap_VBL = QtWidgets.QVBoxLayout(self.skymap_mpl)
        self.skymap_NTB = NavigationToolbar(self.skymap_canvas, self.skymap_mpl)
        self.skymap_VBL.addWidget(self.skymap_canvas)
        self.skymap_VBL.addWidget(self.skymap_NTB)       
        self.CatalogTabLayout.addWidget(self.skymap_mpl, 0, 0, 1, 1)
        
        self.Ctrl_Tabs.addTab(self.Sources, _fromUtf8(""))
        self.Ctrl_Tabs.setTabText(self.Ctrl_Tabs.indexOf(self.Sources),
                                  QtWidgets.QApplication.translate(
                                             "Observatory", "Catalogues", None))
        # end of Catalogues page
        
        # page for the Spectra 4Ghz-128K tab ==================================
        self.roach1_ctrls = QtWidgets.QWidget()
        self.stdSizePolicyExpanding(self.roach1_ctrls)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.roach1_ctrls.setFont(font)
        self.roach1_ctrls.setObjectName(_fromUtf8("roach1_ctrls"))
        self.gridLayout_3 = QtWidgets.QGridLayout(self.roach1_ctrls)
        
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.spectra_mpl = QtWidgets.QWidget(self.roach1_ctrls)
        self.stdSizePolicyExpanding(self.spectra_mpl)
        self.spectra_mpl.setMinimumSize(QtCore.QSize(913, 530))
        self.spectra_mpl.setMaximumSize(QtCore.QSize(1050, 530))
        self.spectra_mpl.setBaseSize(QtCore.QSize(1050, 530))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.spectra_mpl.setFont(font)
        self.spectra_mpl.setObjectName(_fromUtf8("spectra_mpl"))
        
        self.spectra_fig = Figure()
        self.canvas1 = FigureCanvas(self.spectra_fig)
        #self.canvas1.spectrum_roach(self.ui)
        self.axes1 = self.spectra_fig.add_subplot(221)
        self.axes2 = self.spectra_fig.add_subplot(222)
        self.axes3 = self.spectra_fig.add_subplot(223)
        self.axes4 = self.spectra_fig.add_subplot(224)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)    
        textstr1 = 'SAO64K-1'    
        textstr2 = 'SAO64K-2'    
        textstr3 = 'SAO64K-3'    
        textstr4 = 'SAO64K-4'    
        self.axes1.text(0.05, 0.95, textstr1, transform=self.axes1.transAxes,
                        fontsize=10,verticalalignment='top', bbox=props)
        self.axes2.text(0.05, 0.95, textstr2, transform=self.axes2.transAxes,
                        fontsize=10,verticalalignment='top', bbox=props)
        self.axes3.text(0.05, 0.95, textstr3, transform=self.axes3.transAxes,
                        fontsize=10,verticalalignment='top', bbox=props)
        self.axes4.text(0.05, 0.95, textstr4, transform=self.axes4.transAxes,
                        fontsize=10,verticalalignment='top', bbox=props)
        
        self.vbl1 = QtWidgets.QVBoxLayout(self.spectra_mpl)
        self.ntb1 = NavigationToolbar(self.canvas1, self.spectra_mpl)
        self.vbl1.addWidget(self.canvas1)
        self.vbl1.addWidget(self.ntb1)
        
        
        self.gridLayout_3.addWidget(self.spectra_mpl, 0, 0, 1, 1)
        
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        
        self.pushButton_rec_flg = QtWidgets.QPushButton(self.roach1_ctrls)
        self.pushButton_rec_flg.setEnabled(True)
        self.stdSizePolicyPreferred(self.pushButton_rec_flg)
        self.pushButton_rec_flg.setMaximumSize(QtCore.QSize(130, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_rec_flg.setFont(font)
        self.pushButton_rec_flg.setAutoFillBackground(False)
        self.pushButton_rec_flg.setCheckable(True)
        self.pushButton_rec_flg.setObjectName(_fromUtf8("pushButton_rec_flg"))
        self.horizontalLayout_13.addWidget(self.pushButton_rec_flg)
        self.verticalLayout_5.addLayout(self.horizontalLayout_13)
        
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        
        self.label_4 = QtWidgets.QLabel(self.roach1_ctrls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(56, 18))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_4.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                 \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:11pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0; text-indent:0px;\">
                  <span style=\" font-family:\'Sans\'; font-size:10pt;
                                 font-weight:600;\">
                    Source
                  </span>
                </p>
              </body>
            </html>""", None))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        
        self.roachInput1 = QtWidgets.QLineEdit(self.roach1_ctrls)
        self.stdSizePolicyPreferred(self.roachInput1)
        self.roachInput1.setMaximumSize(QtCore.QSize(144, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.roachInput1.setFont(font)
        self.roachInput1.setObjectName(_fromUtf8("roachInput1"))
        self.gridLayout_2.addWidget(self.roachInput1, 0, 1, 1, 1)
        
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lcd_counts = QtWidgets.QLCDNumber(self.roach1_ctrls)
        self.lcd_counts.setObjectName(_fromUtf8("lcd_counts"))
        self.gridLayout_4.addWidget(self.lcd_counts, 1, 0, 1, 1)
        
        self.reset_spec_counter = QtWidgets.QPushButton(self.roach1_ctrls)
        self.reset_spec_counter.setEnabled(False)
        self.reset_spec_counter.setAutoExclusive(True)
        self.reset_spec_counter.setObjectName(_fromUtf8("reset_spec_counter"))
        self.reset_spec_counter.setText(QtWidgets.QApplication.translate(
                                                  "Observatory", "reset", None))
        self.gridLayout_4.addWidget(self.reset_spec_counter, 0, 0, 1, 1)
        
        self.verticalLayout_5.addLayout(self.gridLayout_4)
        self.roach1_led = KLed(self.roach1_ctrls)
        self.roach1_led.setObjectName(_fromUtf8("roach1_led"))
        self.verticalLayout_5.addWidget(self.roach1_led)
        
        self.roach2_led = KLed(self.roach1_ctrls)
        self.roach2_led.setObjectName(_fromUtf8("roach2_led"))
        self.verticalLayout_5.addWidget(self.roach2_led)
        
        self.roach3_led = KLed(self.roach1_ctrls)
        self.roach3_led.setObjectName(_fromUtf8("roach3_led"))
        self.verticalLayout_5.addWidget(self.roach3_led)
        
        self.roach4_led = KLed(self.roach1_ctrls)
        self.roach4_led.setObjectName(_fromUtf8("roach4_led"))
        self.verticalLayout_5.addWidget(self.roach4_led)
        
        spacerItem8 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem8)
        
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        
        self.verticalLayout_5.addLayout(self.gridLayout_8)
        
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.verticalLayout_5.addLayout(self.gridLayout_12)
        
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        
        self.label_17 = QtWidgets.QLabel(self.roach1_ctrls)
        self.stdSizePolicyPreferred(self.label_17)
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setMinimumSize(QtCore.QSize(0, 0))
        self.label_17.setMaximumSize(QtCore.QSize(100, 17))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_17.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:11pt;
                             font-weight:400; font-style:normal;\">\
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-size:10pt; font-weight:600;\">
                    X-Scale
                  </span>
                </p>
              </body>
            </html>""", None))
        self.gridLayout_5.addWidget(self.label_17, 0, 0, 1, 1)
        
        self.label_18 = QtWidgets.QLabel(self.roach1_ctrls)
        self.stdSizePolicyPreferred(self.label_18)
        self.label_18.setMinimumSize(QtCore.QSize(0, 0))
        self.label_18.setMaximumSize(QtCore.QSize(101, 17))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_18.setText(QtWidgets.QApplication.translate("Observatory",
         """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                  \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:11pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-size:10pt; font-weight:600;\">
                    Y-Scale
                  </span>
                </p>
              </body>
            </html>""", None))
        self.gridLayout_5.addWidget(self.label_18, 0, 1, 1, 1)
        
        self.R1Y = QtWidgets.QComboBox(self.roach1_ctrls)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.R1Y.setFont(font)
        self.R1Y.setObjectName(_fromUtf8("R1Y"))
        self.R1Y.addItem(_fromUtf8(""))
        self.R1Y.setItemText(0, QtWidgets.QApplication.translate(
                                               "Observatory", "RegValue", None))
        self.R1Y.addItem(_fromUtf8(""))
        self.R1Y.setItemText(1, QtWidgets.QApplication.translate(
                                                "Observatory", "SkyTemp", None))
        self.R1Y.addItem(_fromUtf8(""))
        self.R1Y.setItemText(2, QtWidgets.QApplication.translate(
                                                    "Observatory", "dBm", None))
        self.gridLayout_5.addWidget(self.R1Y, 1, 1, 1, 1)
        
        self.R1X = QtWidgets.QComboBox(self.roach1_ctrls)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.R1X.setFont(font)
        self.R1X.setObjectName(_fromUtf8("R1X"))
        self.R1X.addItem(_fromUtf8(""))
        self.R1X.setItemText(0, QtWidgets.QApplication.translate(
                                               "Observatory", "Channels", None))
        self.R1X.addItem(_fromUtf8(""))
        self.R1X.setItemText(1, QtWidgets.QApplication.translate(
                                                 "Observatory", "BBFreq", None))
        self.R1X.addItem(_fromUtf8(""))
        self.R1X.setItemText(2, QtWidgets.QApplication.translate(
                                                "Observatory", "SkyFreq", None))
        self.R1X.addItem(_fromUtf8(""))        
        self.R1X.setItemText(3, QtWidgets.QApplication.translate(
                                                "Observatory", "LSRVelo", None))
        self.gridLayout_5.addWidget(self.R1X, 1, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_5)
        
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.SDFITShorizontalLayout = QtWidgets.QHBoxLayout()
        self.SDFITShorizontalLayout.setObjectName(_fromUtf8("horizontalLayout_11"))
        
        self.sdfits = QtWidgets.QCheckBox(self.roach1_ctrls)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.sdfits.setFont(font)
        self.sdfits.setChecked(True)
        self.sdfits.setObjectName(_fromUtf8("sdfits"))
        self.sdfits .setText(QtWidgets.QApplication.translate(
                                                 "Observatory", "sdfits", None))
        self.SDFITShorizontalLayout.addWidget(self.sdfits)
        
        self.saveButton = QtWidgets.QPushButton(self.roach1_ctrls)
        self.stdSizePolicyPreferred(self.saveButton)
        self.saveButton.setMaximumSize(QtCore.QSize(128, 24))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.saveButton.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Save Figure", None))
        self.SDFITShorizontalLayout.addWidget(self.saveButton)
        
        self.verticalLayout_12.addLayout(self.SDFITShorizontalLayout)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        
        self.label_recsince = QtWidgets.QLabel(self.roach1_ctrls)
        self.stdSizePolicyPreferred(self.label_recsince)
        self.label_recsince.setMaximumSize(QtCore.QSize(105, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_recsince.setFont(font)
        self.label_recsince.setObjectName(_fromUtf8("label_recsince"))
        self.horizontalLayout_14.addWidget(self.label_recsince)
        
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.roach1_ctrls)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.horizontalLayout_14.addWidget(self.doubleSpinBox)
        
        self.verticalLayout_12.addLayout(self.horizontalLayout_14)
        
        self.verticalLayout_5.addLayout(self.verticalLayout_12)
        self.gridLayout_3.addLayout(self.verticalLayout_5, 0, 1, 3, 1)
        
        self.Ctrl_Tabs.addTab(self.roach1_ctrls, _fromUtf8(""))
        self.Ctrl_Tabs.setTabText(self.Ctrl_Tabs.indexOf(self.roach1_ctrls),
                                  QtWidgets.QApplication.translate(
                                      "Observatory", "Spectra 4Ghz-128K", None))
                                      
        # page for the System Status
        self.RfPath = QtWidgets.QWidget()
        self.RfPath.setObjectName(_fromUtf8("RfPath"))
        
        self.gridLayout_41 = QtWidgets.QGridLayout(self.RfPath)
        self.gridLayout_41.setObjectName(_fromUtf8("gridLayout_41"))
        
        self.gridLayout_25 = QtWidgets.QGridLayout()
        self.gridLayout_25.setObjectName(_fromUtf8("gridLayout_25"))
        
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName(_fromUtf8("verticalLayout_18"))
        
        self.minical_mpl = QtWidgets.QWidget(self.RfPath)
        self.stdSizePolicyExpanding(self.minical_mpl)
        self.minical_mpl.setMinimumSize(QtCore.QSize(450, 250))
        self.minical_mpl.setMaximumSize(QtCore.QSize(800, 800))
        self.minical_mpl.setObjectName(_fromUtf8("minical_mpl"))
        self.minical_fig = Figure()
        self.minical_canvas = FigureCanvas(self.minical_fig)
        self.minical_axes = {}
        for num in [1,2,3,4]:
          self.minical_axes[num] = self.minical_fig.add_subplot(220+num)
          self.minical_axes[num].set_xlabel("Power (W)")
          self.minical_axes[num].set_ylabel("Temperature (K)")
          self.minical_axes[num].legend(loc='lower right')
          self.minical_axes[num].grid(True)
        self.minical_VLB = QtWidgets.QVBoxLayout(self.minical_mpl)
        self.minical_VLB.addWidget(self.minical_canvas)
        self.minical_NTB = NavigationToolbar(self.minical_canvas, self.minical_mpl)
        self.minical_VLB.addWidget(self.minical_NTB)
        self.verticalLayout_18.addWidget(self.minical_mpl)
        
        self.horizontalLayout_51 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_51.setObjectName(_fromUtf8("horizontalLayout_51"))
        
        spacerItem9 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_51.addItem(spacerItem9)
        
        self.verticalLayout_18.addLayout(self.horizontalLayout_51)
        
        self.gridLayout_25.addLayout(self.verticalLayout_18, 0, 0, 1, 1)
        
        self.gridLayout_43 = QtWidgets.QGridLayout()
        self.gridLayout_43.setObjectName(_fromUtf8("gridLayout_43"))
        
        self.gridLayout_23 = QtWidgets.QGridLayout()
        self.gridLayout_23.setObjectName(_fromUtf8("gridLayout_23"))
        
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName(_fromUtf8("horizontalLayout_26"))
        
        self.frame_9 = QtWidgets.QFrame(self.RfPath)
        
        self.stdSizePolicyExpanding(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.frame_9.setFont(font)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName(_fromUtf8("frame_9"))
        
        self.gridLayout_11 = QtWidgets.QGridLayout(self.frame_9)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        
        self.noiseLevelSpinBox = QtWidgets.QDoubleSpinBox(self.frame_9)
        self.noiseLevelSpinBox.setEnabled(False)
        self.noiseLevelSpinBox.setMaximum(350.0)
        self.noiseLevelSpinBox.setSingleStep(5.0)
        self.noiseLevelSpinBox.setProperty("value", 50.0)
        self.noiseLevelSpinBox.setObjectName(_fromUtf8("noiseLevelSpinBox"))
        self.horizontalLayout_17.addWidget(self.noiseLevelSpinBox)
        
        self.NDtempLabel = QtWidgets.QLabel(self.frame_9)
        self.NDtempLabel.setObjectName(_fromUtf8("NDtempLabel"))
        self.horizontalLayout_17.addWidget(self.NDtempLabel)
        
        self.verticalLayout_9.addLayout(self.horizontalLayout_17)
        
        self.checkNoise = QtWidgets.QCheckBox(self.frame_9)
        self.checkNoise.setObjectName(_fromUtf8("checkNoise"))
        self.verticalLayout_9.addWidget(self.checkNoise)
        
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.nd_mod_pb = QtWidgets.QPushButton(self.frame_9)
        self.nd_mod_pb.setCheckable(True)
        self.nd_mod_pb.setObjectName(_fromUtf8("nd_mod_pb"))
        self.horizontalLayout_5.addWidget(self.nd_mod_pb)
        
        self.label_19 = QtWidgets.QLabel(self.frame_9)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.label_19.setText(QtWidgets.QApplication.translate("Observatory",
                                                       "ND mod rate(Hz)", None))
        self.horizontalLayout_5.addWidget(self.label_19)
        
        self.ndmod = QtWidgets.QSpinBox(self.frame_9)
        self.ndmod.setEnabled(False)
        self.ndmod.setMinimum(1)
        self.ndmod.setMaximum(6)
        self.ndmod.setSingleStep(1)
        self.ndmod.setProperty("value", 4)
        self.ndmod.setObjectName(_fromUtf8("ndmod"))
        self.horizontalLayout_5.addWidget(self.ndmod)
        
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.gridLayout_11.addLayout(self.verticalLayout_9, 1, 1, 1, 1)
        
        self.label_27 = QtWidgets.QLabel(self.frame_9)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.label_27.setText(QtWidgets.QApplication.translate(
                                 "Observatory", "Noise Diode Modulation", None))
        self.gridLayout_11.addWidget(self.label_27, 0, 1, 1, 1)
        
        spacerItem10 = QtWidgets.QSpacerItem(40, 20,
                                             QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem10, 1, 2, 1, 1)
        
        self.horizontalLayout_26.addWidget(self.frame_9)
        self.verticalLayout_13.addLayout(self.horizontalLayout_26)
        
        spacerItem11 = QtWidgets.QSpacerItem(40, 20,
                                             QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_13.addItem(spacerItem11)
        
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        
        self.phaseCalcheckBox = QtWidgets.QCheckBox(self.RfPath)
        self.phaseCalcheckBox.setObjectName(_fromUtf8("phaseCalcheckBox"))
        self.phaseCalcheckBox.setText(
             QtWidgets.QApplication.translate("Observatory", "Phase Cal", None))
        self.horizontalLayout_6.addWidget(self.phaseCalcheckBox)
        
        self.RadioButton1MHz = QtWidgets.QRadioButton(self.RfPath)
        self.RadioButton1MHz.setChecked(True)
        self.RadioButton1MHz.setObjectName(_fromUtf8("RadioButton1MHz"))
        self.RadioButton1MHz.setText(
                 QtWidgets.QApplication.translate("Observatory", "1 MHz", None))
        self.horizontalLayout_6.addWidget(self.RadioButton1MHz)
        
        self.RadioButton5MHz = QtWidgets.QRadioButton(self.RfPath)
        self.RadioButton5MHz.setObjectName(_fromUtf8("RadioButton5MHz"))
        self.RadioButton5MHz.setText(
                 QtWidgets.QApplication.translate("Observatory", "5 MHz", None))
        self.horizontalLayout_6.addWidget(self.RadioButton5MHz)
        
        self.verticalLayout_13.addLayout(self.horizontalLayout_6)
        
        self.frame_8 = QtWidgets.QFrame(self.RfPath)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName(_fromUtf8("frame_8"))
        
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_25.setObjectName(_fromUtf8("horizontalLayout_25"))
        
        self.verticalLayout_24 = QtWidgets.QVBoxLayout()
        self.verticalLayout_24.setObjectName(_fromUtf8("verticalLayout_24"))
        
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        
        self.label_46 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_46.setFont(font)
        self.label_46.setObjectName(_fromUtf8("label_46"))
        self.label_46.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Temp", None))
        self.horizontalLayout_19.addWidget(self.label_46)
        
        self.temp = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.temp.setFont(font)
        self.temp.setObjectName(_fromUtf8("temp"))
        self.temp.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.horizontalLayout_19.addWidget(self.temp)
        
        self.verticalLayout_24.addLayout(self.horizontalLayout_19)
        
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        
        self.label_45 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_45.setFont(font)
        self.label_45.setObjectName(_fromUtf8("label_45"))
        self.label_45.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Pressure", None))
        self.horizontalLayout_12.addWidget(self.label_45)
        
        self.pressure = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pressure.setFont(font)
        self.pressure.setObjectName(_fromUtf8("pressure"))
        self.pressure.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.horizontalLayout_12.addWidget(self.pressure)
        
        self.verticalLayout_24.addLayout(self.horizontalLayout_12)
        
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName(_fromUtf8("horizontalLayout_22"))
        
        self.label_43 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_43.setFont(font)
        self.label_43.setObjectName(_fromUtf8("label_43"))
        self.label_43.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Humidity", None))
        self.horizontalLayout_22.addWidget(self.label_43)
        
        self.humidity = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.humidity.setFont(font)
        self.humidity.setObjectName(_fromUtf8("humidity"))
        self.humidity.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.horizontalLayout_22.addWidget(self.humidity)
        
        self.verticalLayout_24.addLayout(self.horizontalLayout_22)
        
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName(_fromUtf8("horizontalLayout_23"))
        
        self.label_53 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_53.setFont(font)
        self.label_53.setObjectName(_fromUtf8("label_53"))
        self.label_53.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "Wind speed", None))
        self.horizontalLayout_23.addWidget(self.label_53)
        
        self.windspeed = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.windspeed.setFont(font)
        self.windspeed.setObjectName(_fromUtf8("windspeed"))
        self.windspeed.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.horizontalLayout_23.addWidget(self.windspeed)
        
        self.verticalLayout_24.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName(_fromUtf8("horizontalLayout_24"))
        
        self.label_57 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_57.setFont(font)
        self.label_57.setObjectName(_fromUtf8("label_57"))
        self.label_57.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Wind direction", None))
        self.horizontalLayout_24.addWidget(self.label_57)
        
        self.winddir = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.winddir.setFont(font)
        self.winddir.setObjectName(_fromUtf8("winddir"))
        self.winddir.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.horizontalLayout_24.addWidget(self.winddir)
        
        self.verticalLayout_24.addLayout(self.horizontalLayout_24)
        
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_49.setObjectName(_fromUtf8("horizontalLayout_49"))
        
        self.label_64 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_64.setFont(font)
        self.label_64.setObjectName(_fromUtf8("label_64"))
        self.label_64.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Precipitation", None))
        self.horizontalLayout_49.addWidget(self.label_64)
        
        self.precip = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.precip.setFont(font)
        self.precip.setObjectName(_fromUtf8("precip"))
        self.precip.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.horizontalLayout_49.addWidget(self.precip)
        
        self.verticalLayout_24.addLayout(self.horizontalLayout_49)
        
        self.horizontalLayout_25.addLayout(self.verticalLayout_24)
        
        self.frame_18 = QtWidgets.QFrame(self.frame_8)
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName(_fromUtf8("frame_18"))
        self.horizontalLayout_25.addWidget(self.frame_18)
        
        self.verticalLayout_13.addWidget(self.frame_8)
        self.gridLayout_23.addLayout(self.verticalLayout_13, 3, 0, 1, 1)
        
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        
        self.label_21 = QtWidgets.QLabel(self.RfPath)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.label_21.setText(QtWidgets.QApplication.translate(
                                        "Observatory", "Frontend status", None))
        self.horizontalLayout_7.addWidget(self.label_21)
         
        spacerItem12 = QtWidgets.QSpacerItem(40, 20,
                                             QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem12)
        
        self.gridLayout_23.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
        
        self.gridLayout_29 = QtWidgets.QGridLayout()
        self.gridLayout_29.setObjectName(_fromUtf8("gridLayout_29"))
        
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        
        self.label70K = QtWidgets.QLabel(self.RfPath)
        self.label70K.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|
                                   QtCore.Qt.AlignVCenter)
        self.label70K.setObjectName(_fromUtf8("label70K"))
        self.label70K.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "70 K stage", None))
        self.horizontalLayout_15.addWidget(self.label70K)
        
        self.lcd70K = QtWidgets.QLCDNumber(self.RfPath)
        self.lcd70K.setEnabled(True)
        palette = self.palette70K()
        self.lcd70K.setPalette(palette)
        self.lcd70K.setAutoFillBackground(True)
        self.lcd70K.setObjectName(_fromUtf8("lcd70K"))
        self.lcd70K.setProperty("value", 0.0)
        self.horizontalLayout_15.addWidget(self.lcd70K)
        
        self.lcd12K = QtWidgets.QLCDNumber(self.RfPath)
        self.lcd12K.setEnabled(True)
        palette = self.palette12K()
        self.lcd12K.setPalette(palette)
        self.lcd12K.setAutoFillBackground(True)
        self.lcd12K.setObjectName(_fromUtf8("lcd12K"))
        self.lcd12K.setProperty("value", 0.0)
        self.horizontalLayout_15.addWidget(self.lcd12K)
        
        self.label12K = QtWidgets.QLabel(self.RfPath)
        self.label12K.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|
                                   QtCore.Qt.AlignVCenter)
        self.label12K.setObjectName(_fromUtf8("label12K"))
        self.label12K.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "12 K stage", None))
        self.horizontalLayout_15.addWidget(self.label12K)
        
        self.gridLayout_29.addLayout(self.horizontalLayout_15, 1, 0, 1, 1)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        
        self.lcdLoad1 = QtWidgets.QLCDNumber(self.RfPath)
        self.lcdLoad1.setEnabled(True)
        palette = self.load1Palette()
        self.lcdLoad1.setPalette(palette)
        self.lcdLoad1.setAutoFillBackground(True)
        self.lcdLoad1.setProperty("value", 0.0)
        self.lcdLoad1.setObjectName(_fromUtf8("lcdLoad1"))
        self.horizontalLayout_2.addWidget(self.lcdLoad1)
        
        self.lcdLoad2 = QtWidgets.QLCDNumber(self.RfPath)
        self.lcdLoad2.setEnabled(True)
        palette = self.load2Palette()
        self.lcdLoad2.setPalette(palette)
        self.lcdLoad2.setAutoFillBackground(True)
        self.lcdLoad2.setObjectName(_fromUtf8("lcdLoad2"))
        self.lcdLoad2.setProperty("value", 0.0)

        self.horizontalLayout_2.addWidget(self.lcdLoad2)
        self.gridLayout_29.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_23.addLayout(self.gridLayout_29, 2, 0, 1, 1)
        self.gridLayout_43.addLayout(self.gridLayout_23, 0, 0, 1, 2)
        
        self.minical = QtWidgets.QPushButton(self.RfPath)
        self.minical.setEnabled(True)
        self.minical.setCheckable(True)
        self.minical.setObjectName(_fromUtf8("minical"))
        self.minical.setText(QtWidgets.QApplication.translate(
                                                "Observatory", "Minical", None))
        self.gridLayout_43.addWidget(self.minical, 1, 0, 1, 1)
        
        self.frame_17 = QtWidgets.QFrame(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.frame_17.setFont(font)
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName(_fromUtf8("frame_17"))
        self.gridLayout_42 = QtWidgets.QGridLayout(self.frame_17)
        self.gridLayout_42.setObjectName(_fromUtf8("gridLayout_42"))
        self.g2 = QtWidgets.QLabel(self.frame_17)
        self.g2.setObjectName(_fromUtf8("g2"))
        self.gridLayout_42.addWidget(self.g2, 2, 5, 1, 1)
        self.ft4 = QtWidgets.QLabel(self.frame_17)
        self.ft4.setObjectName(_fromUtf8("ft4"))
        self.gridLayout_42.addWidget(self.ft4, 4, 3, 1, 1)
        self.label_38 = QtWidgets.QLabel(self.frame_17)
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.gridLayout_42.addWidget(self.label_38, 2, 0, 1, 1)
        self.label_34 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_34.setFont(font)
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.gridLayout_42.addWidget(self.label_34, 0, 3, 1, 1)
        self.g1 = QtWidgets.QLabel(self.frame_17)
        self.g1.setObjectName(_fromUtf8("g1"))
        self.gridLayout_42.addWidget(self.g1, 1, 5, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_35.setFont(font)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.gridLayout_42.addWidget(self.label_35, 0, 0, 1, 1)
        self.at2 = QtWidgets.QLabel(self.frame_17)
        self.at2.setObjectName(_fromUtf8("at2"))
        self.gridLayout_42.addWidget(self.at2, 2, 2, 1, 1)
        self.at4 = QtWidgets.QLabel(self.frame_17)
        self.at4.setObjectName(_fromUtf8("at4"))
        self.gridLayout_42.addWidget(self.at4, 4, 2, 1, 1)
        self.ft2 = QtWidgets.QLabel(self.frame_17)
        self.ft2.setObjectName(_fromUtf8("ft2"))
        self.gridLayout_42.addWidget(self.ft2, 2, 3, 1, 1)
        self.label_36 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_36.setFont(font)
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.gridLayout_42.addWidget(self.label_36, 0, 5, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.frame_17)
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.gridLayout_42.addWidget(self.label_37, 1, 0, 1, 1)
        self.adt1 = QtWidgets.QLabel(self.frame_17)
        self.adt1.setObjectName(_fromUtf8("adt1"))
        self.gridLayout_42.addWidget(self.adt1, 1, 4, 1, 1)
        self.adt2 = QtWidgets.QLabel(self.frame_17)
        self.adt2.setObjectName(_fromUtf8("adt2"))
        self.gridLayout_42.addWidget(self.adt2, 2, 4, 1, 1)
        self.ft1 = QtWidgets.QLabel(self.frame_17)
        self.ft1.setObjectName(_fromUtf8("ft1"))
        self.gridLayout_42.addWidget(self.ft1, 1, 3, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.frame_17)
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.gridLayout_42.addWidget(self.label_39, 3, 0, 1, 1)
        self.label_65 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_65.setFont(font)
        self.label_65.setObjectName(_fromUtf8("label_65"))
        self.gridLayout_42.addWidget(self.label_65, 0, 4, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_33.setFont(font)
        self.label_33.setObjectName(_fromUtf8("label_33"))
        self.gridLayout_42.addWidget(self.label_33, 0, 2, 1, 1)
        self.g4 = QtWidgets.QLabel(self.frame_17)
        self.g4.setObjectName(_fromUtf8("g4"))
        self.gridLayout_42.addWidget(self.g4, 4, 5, 1, 1)
        self.ft3 = QtWidgets.QLabel(self.frame_17)
        self.ft3.setObjectName(_fromUtf8("ft3"))
        self.gridLayout_42.addWidget(self.ft3, 3, 3, 1, 1)
        self.adt3 = QtWidgets.QLabel(self.frame_17)
        self.adt3.setObjectName(_fromUtf8("adt3"))
        self.gridLayout_42.addWidget(self.adt3, 3, 4, 1, 1)
        self.at1 = QtWidgets.QLabel(self.frame_17)
        self.at1.setObjectName(_fromUtf8("at1"))
        self.gridLayout_42.addWidget(self.at1, 1, 2, 1, 1)
        self.at3 = QtWidgets.QLabel(self.frame_17)
        self.at3.setObjectName(_fromUtf8("at3"))
        self.gridLayout_42.addWidget(self.at3, 3, 2, 1, 1)
        self.g3 = QtWidgets.QLabel(self.frame_17)
        self.g3.setObjectName(_fromUtf8("g3"))
        self.gridLayout_42.addWidget(self.g3, 3, 5, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.frame_17)
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.gridLayout_42.addWidget(self.label_40, 4, 0, 1, 1)
        self.adt4 = QtWidgets.QLabel(self.frame_17)
        self.adt4.setObjectName(_fromUtf8("adt4"))
        self.gridLayout_42.addWidget(self.adt4, 4, 4, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_42.setFont(font)
        self.label_42.setObjectName(_fromUtf8("label_42"))
        self.gridLayout_42.addWidget(self.label_42, 0, 1, 1, 1)
        self.rms1 = QtWidgets.QLabel(self.frame_17)
        self.rms1.setObjectName(_fromUtf8("rms1"))
        self.gridLayout_42.addWidget(self.rms1, 1, 1, 1, 1)
        self.rms2 = QtWidgets.QLabel(self.frame_17)
        self.rms2.setObjectName(_fromUtf8("rms2"))
        self.gridLayout_42.addWidget(self.rms2, 2, 1, 1, 1)
        self.rms3 = QtWidgets.QLabel(self.frame_17)
        self.rms3.setObjectName(_fromUtf8("rms3"))
        self.gridLayout_42.addWidget(self.rms3, 3, 1, 1, 1)
        self.rms4 = QtWidgets.QLabel(self.frame_17)
        self.rms4.setObjectName(_fromUtf8("rms4"))
        self.gridLayout_42.addWidget(self.rms4, 4, 1, 1, 1)
        self.gridLayout_43.addWidget(self.frame_17, 3, 0, 1, 2)
        self.label_22 = QtWidgets.QLabel(self.RfPath)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout_43.addWidget(self.label_22, 2, 0, 1, 1)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.SGFreqSpinBox = QtWidgets.QDoubleSpinBox(self.RfPath)
        self.SGFreqSpinBox.setEnabled(True)
        self.SGFreqSpinBox.setDecimals(5)
        self.SGFreqSpinBox.setMinimum(20000.0)
        self.SGFreqSpinBox.setMaximum(26000.0)
        self.SGFreqSpinBox.setSingleStep(1e-06)
        self.SGFreqSpinBox.setProperty("value", 20000.0)
        self.SGFreqSpinBox.setObjectName(_fromUtf8("SGFreqSpinBox"))
        self.horizontalLayout_18.addWidget(self.SGFreqSpinBox)
        self.SGAmpSpinBox = QtWidgets.QDoubleSpinBox(self.RfPath)
        self.SGAmpSpinBox.setEnabled(True)
        self.SGAmpSpinBox.setMinimum(-100.0)
        self.SGAmpSpinBox.setMaximum(-5.0)
        self.SGAmpSpinBox.setProperty("value", -50.0)
        self.SGAmpSpinBox.setObjectName(_fromUtf8("SGAmpSpinBox"))
        self.horizontalLayout_18.addWidget(self.SGAmpSpinBox)
        self.gridLayout_43.addLayout(self.horizontalLayout_18, 6, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelSGFrq = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelSGFrq.setFont(font)
        self.labelSGFrq.setObjectName(_fromUtf8("labelSGFrq"))
        self.horizontalLayout.addWidget(self.labelSGFrq)
        self.labelSGAmp = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelSGAmp.setFont(font)
        self.labelSGAmp.setObjectName(_fromUtf8("labelSGAmp"))
        self.horizontalLayout.addWidget(self.labelSGAmp)
        self.gridLayout_43.addLayout(self.horizontalLayout, 5, 1, 1, 1)
        self.SGRFButton = QtWidgets.QPushButton(self.RfPath)
        self.SGRFButton.setEnabled(True)
        self.SGRFButton.setCheckable(True)
        self.SGRFButton.setObjectName(_fromUtf8("SGRFButton"))
        self.gridLayout_43.addWidget(self.SGRFButton, 6, 0, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.RfPath)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout_43.addWidget(self.label_26, 5, 0, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_41.setFont(font)
        self.label_41.setObjectName(_fromUtf8("label_41"))
        self.gridLayout_43.addWidget(self.label_41, 1, 1, 1, 1)
        
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName(_fromUtf8("horizontalLayout_21"))
        
        #
        self.last_tsys1 = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.last_tsys1.setFont(font)
        self.last_tsys1.setObjectName(_fromUtf8("last_tsys1"))
        self.horizontalLayout_21.addWidget(self.last_tsys1)
        
        self.last_tsys2 = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.last_tsys2.setFont(font)
        self.last_tsys2.setObjectName(_fromUtf8("last_tsys2"))
        self.horizontalLayout_21.addWidget(self.last_tsys2)
        self.last_tsys3 = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.last_tsys3.setFont(font)
        self.last_tsys3.setObjectName(_fromUtf8("last_tsys3"))
        self.horizontalLayout_21.addWidget(self.last_tsys3)
        self.last_tsys4 = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.last_tsys4.setFont(font)
        self.last_tsys4.setObjectName(_fromUtf8("last_tsys4"))
        self.horizontalLayout_21.addWidget(self.last_tsys4)
        self.gridLayout_43.addLayout(self.horizontalLayout_21, 2, 1, 1, 1)
        self.gridLayout_25.addLayout(self.gridLayout_43, 0, 1, 1, 1)
        self.gridLayout_41.addLayout(self.gridLayout_25, 0, 0, 1, 1)
        self.Ctrl_Tabs.addTab(self.RfPath, _fromUtf8(""))
        self.Ctrl_Tabs.setTabText(self.Ctrl_Tabs.indexOf(self.RfPath),
                                  QtWidgets.QApplication.translate(
                                          "Observatory", "System Status", None))

        # ------------------------ Analytics (empty) ---------------------------
        self.analytics_ctrls = QtWidgets.QWidget()
        self.stdSizePolicyExpanding(self.analytics_ctrls)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.analytics_ctrls.setFont(font)
        self.analytics_ctrls.setObjectName(_fromUtf8("analytics_ctrls"))
        self.gridLayout_10 = QtWidgets.QGridLayout(self.analytics_ctrls)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.Ctrl_Tabs.addTab(self.analytics_ctrls, _fromUtf8(""))
        self.Ctrl_Tabs.setTabText(self.Ctrl_Tabs.indexOf(self.analytics_ctrls),
                       QtWidgets.QApplication.translate(
                                        "Observatory", "Analytical Plot", None))
       
        # ------------------------- menubar -------------------------------
        self.menubar = QtWidgets.QMenuBar(Observatory)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1260, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle(QtWidgets.QApplication.translate(
                                                   "Observatory", "File", None))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        
        self.menuConfig = QtWidgets.QMenu(self.menubar)
        self.menuConfig.setTitle(QtWidgets.QApplication.translate(
                                                 "Observatory", "Config", None))
        self.menuConfig.setObjectName(_fromUtf8("menuConfig"))
        
        self.menuROACH1 = QtWidgets.QMenu(self.menuConfig)
        self.menuROACH1.setTitle(QtWidgets.QApplication.translate(
                                                  "Observatory", "ROACH", None))
        self.menuROACH1.setObjectName(_fromUtf8("menuROACH1"))
        
        self.menuCalibration = QtWidgets.QMenu(self.menuROACH1)
        self.menuCalibration.setObjectName(_fromUtf8("menuCalibration"))
        
        self.menuConfigure_ROACH = QtWidgets.QMenu(self.menuROACH1)
        self.menuConfigure_ROACH.setObjectName(_fromUtf8("menuConfigure_ROACH"))
        self.menuWBDC = QtWidgets.QMenu(self.menuConfig)
        self.menuWBDC.setObjectName(_fromUtf8("menuWBDC"))
        self.menuRFI_Analysis = QtWidgets.QMenu(self.menuConfig)
        self.menuRFI_Analysis.setObjectName(_fromUtf8("menuRFI_Analysis"))
        self.menuPlot = QtWidgets.QMenu(self.menubar)
        self.menuPlot.setObjectName(_fromUtf8("menuPlot"))
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        Observatory.setMenuBar(self.menubar)
        self.actionSelect_Spectrometer = QtWidgets.QAction(Observatory)
        self.actionSelect_Spectrometer.setObjectName(_fromUtf8("actionSelect_Spectrometer"))
        self.actionSelect_Firmware = QtWidgets.QAction(Observatory)
        self.actionSelect_Firmware.setObjectName(_fromUtf8("actionSelect_Firmware"))
        self.actionPop_out_Plot2 = QtWidgets.QAction(Observatory)
        self.actionPop_out_Plot2.setObjectName(_fromUtf8("actionPop_out_Plot2"))
        self.actionVelocity_Plot = QtWidgets.QAction(Observatory)
        self.actionVelocity_Plot.setObjectName(_fromUtf8("actionVelocity_Plot"))
        self.actionFrequency_Plot = QtWidgets.QAction(Observatory)
        self.actionFrequency_Plot.setObjectName(_fromUtf8("actionFrequency_Plot"))
        self.actionChannel_Plot = QtWidgets.QAction(Observatory)
        self.actionChannel_Plot.setObjectName(_fromUtf8("actionChannel_Plot"))
        self.actionOffset_Adjustments = QtWidgets.QAction(Observatory)
        self.actionOffset_Adjustments.setObjectName(_fromUtf8("actionOffset_Adjustments"))
        self.actionInput_naming = QtWidgets.QAction(Observatory)
        self.actionInput_naming.setObjectName(_fromUtf8("actionInput_naming"))
        self.actionProcess_Data_Quotient_Plots = QtWidgets.QAction(Observatory)
        self.actionProcess_Data_Quotient_Plots.setObjectName(_fromUtf8("actionProcess_Data_Quotient_Plots"))
        self.actionProcess_data_average_plots = QtWidgets.QAction(Observatory)
        self.actionProcess_data_average_plots.setObjectName(_fromUtf8("actionProcess_data_average_plots"))
        self.actionProcess_data_time_plots = QtWidgets.QAction(Observatory)
        self.actionProcess_data_time_plots.setObjectName(_fromUtf8("actionProcess_data_time_plots"))
        self.actionNoise_Integration_test = QtWidgets.QAction(Observatory)
        self.actionNoise_Integration_test.setObjectName(_fromUtf8("actionNoise_Integration_test"))
        self.actionTIme_domain_plots = QtWidgets.QAction(Observatory)
        self.actionTIme_domain_plots.setObjectName(_fromUtf8("actionTIme_domain_plots"))
        self.actionVelocity_Plots = QtWidgets.QAction(Observatory)
        self.actionVelocity_Plots.setObjectName(_fromUtf8("actionVelocity_Plots"))
        self.actionChannel_Plots = QtWidgets.QAction(Observatory)
        self.actionChannel_Plots.setObjectName(_fromUtf8("actionChannel_Plots"))
        self.actionLoad_Firmware = QtWidgets.QAction(Observatory)
        self.actionLoad_Firmware.setObjectName(_fromUtf8("actionLoad_Firmware"))
        self.actionReset_Spectrometer1 = QtWidgets.QAction(Observatory)
        self.actionReset_Spectrometer1.setObjectName(_fromUtf8("actionReset_Spectrometer1"))
        self.actionLoad_Firmware2 = QtWidgets.QAction(Observatory)
        self.actionLoad_Firmware2.setObjectName(_fromUtf8("actionLoad_Firmware2"))
        self.actionReset_Spectrometer2 = QtWidgets.QAction(Observatory)
        self.actionReset_Spectrometer2.setObjectName(
                                         _fromUtf8("actionReset_Spectrometer2"))
        self.actionOpen_Logfile_location = QtWidgets.QAction(Observatory)
        self.actionOpen_Logfile_location.setObjectName(
                                       _fromUtf8("actionOpen_Logfile_location"))
        self.actionOpen_Datafile_location = QtWidgets.QAction(Observatory)
        self.actionOpen_Datafile_location.setObjectName(
                                      _fromUtf8("actionOpen_Datafile_location"))
        
        self.actionCalibrate_ADC = QtWidgets.QAction(Observatory)
        self.actionCalibrate_ADC.setObjectName(_fromUtf8("actionCalibrate_ADC"))
        self.actionCalibrate_ADC.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Calibrate ADC", None))
        self.menuCalibration.addAction(self.actionCalibrate_ADC)
        
        self.actionCalibrate_ADC2 = QtWidgets.QAction(Observatory)
        self.actionCalibrate_ADC2.setObjectName(_fromUtf8("actionCalibrate_ADC2"))
        self.actionCalibrate_ADC2.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Calibrate ADC2", None))
        
        self.actionCalibrate_ADC3 = QtWidgets.QAction(Observatory)
        self.actionCalibrate_ADC3.setObjectName(_fromUtf8("actionCalibrate_ADC3"))
        self.actionCalibrate_ADC3.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Calibrate ADC3", None))
        
        self.actionCalibrate_ADC4 = QtWidgets.QAction(Observatory)
        self.actionCalibrate_ADC4.setObjectName(_fromUtf8("actionCalibrate_ADC4"))
        self.actionCalibrate_ADC4.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Calibrate ADC4", None))
    
    #def start_observing_actions(self):                                 
        self.start_obs.toggled.connect(self.xel_prog_offsets.setDisabled)
        self.start_obs.toggled.connect(self.el_prog_offsets.setDisabled)
        self.start_obs.toggled.connect(self.calc_bs_results.setDisabled)
        self.start_obs.toggled.connect(self.tipping_PB.setDisabled)
        self.start_obs.toggled.connect(self.set_offsets.setDisabled)
        self.start_obs.toggled.connect(self.slew_to_source.setDisabled)
        self.start_obs.toggled.connect(self.SwitchSkyLoad[1].setDisabled)
        self.start_obs.toggled.connect(self.SwitchSkyLoad[2].setDisabled)
        self.start_obs.toggled.connect(self.SwitchBand.setDisabled)
        self.start_obs.toggled.connect(self.SwitchULIQ[1].setDisabled)
        self.start_obs.toggled.connect(self.SwitchULIQ[2].setDisabled)
        self.start_obs.toggled.connect(self.SwitchLin[1].setDisabled)
        self.start_obs.toggled.connect(self.SwitchLin[2].setDisabled)
        self.start_obs.toggled.connect(self.yfactor.setDisabled)
        self.start_obs.toggled.connect(self.dBmradioButton.setDisabled)
        self.start_obs.toggled.connect(self.checkFeeds.setDisabled)
        self.start_obs.toggled.connect(self.checkAmp1.setDisabled)
        self.start_obs.toggled.connect(self.checkAmp2.setDisabled)

        
        self.actionLoad_data_file_to_simulate = QtWidgets.QAction(Observatory)
        self.actionLoad_data_file_to_simulate.setObjectName(_fromUtf8(
                                            "actionLoad_data_file_to_simulate"))
        self.actionLoad_data_1 = QtWidgets.QAction(Observatory)
        self.actionLoad_data_1.setObjectName(_fromUtf8("actionLoad_data_1"))
        self.actionLoad_data_2 = QtWidgets.QAction(Observatory)
        self.actionLoad_data_2.setObjectName(_fromUtf8("actionLoad_data_2"))
        self.actionLoad_Dir = QtWidgets.QAction(Observatory)
        self.actionLoad_Dir.setObjectName(_fromUtf8("actionLoad_Dir"))
        self.actionStart_time = QtWidgets.QAction(Observatory)
        self.actionStart_time.setObjectName(_fromUtf8("actionStart_time"))
        self.actionStop_time = QtWidgets.QAction(Observatory)
        self.actionStop_time.setObjectName(_fromUtf8("actionStop_time"))
        self.actionFrames_per_sec = QtWidgets.QAction(Observatory)
        self.actionFrames_per_sec.setObjectName(_fromUtf8("actionFrames_per_sec"))
        self.actionWBDC = QtWidgets.QAction(Observatory)
        self.actionWBDC.setObjectName(_fromUtf8("actionWBDC"))
        self.actionROACH1 = QtWidgets.QAction(Observatory)
        self.actionROACH1.setObjectName(_fromUtf8("actionROACH1"))
        self.actionROACH2 = QtWidgets.QAction(Observatory)
        self.actionROACH2.setObjectName(_fromUtf8("actionROACH2"))
        self.actionROACH3 = QtWidgets.QAction(Observatory)
        self.actionROACH3.setObjectName(_fromUtf8("actionROACH3"))
        self.actionAnalitical_Plot = QtWidgets.QAction(Observatory)
        self.actionAnalitical_Plot.setObjectName(_fromUtf8("actionAnalitical_Plot"))
        self.actionROACH4 = QtWidgets.QAction(Observatory)
        self.actionROACH4.setObjectName(_fromUtf8("actionROACH4"))
        self.actionWBDC_Edit = QtWidgets.QAction(Observatory)
        self.actionWBDC_Edit.setCheckable(True)
        self.actionWBDC_Edit.setEnabled(False)
        self.actionWBDC_Edit.setObjectName(_fromUtf8("actionWBDC_Edit"))
        
        self.actionQuit = QtWidgets.QAction(Observatory)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionQuit.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Quit", None))
        self.menuFile.addAction(self.actionQuit)

        self.actionSet_Lof_Dir = QtWidgets.QAction(Observatory)
        self.actionSet_Lof_Dir.setObjectName(_fromUtf8("actionSet_Lof_Dir"))
        self.actionSet_Data_Dir = QtWidgets.QAction(Observatory)
        self.actionSet_Data_Dir.setObjectName(_fromUtf8("actionSet_Data_Dir"))
        self.actionEdit = QtWidgets.QAction(Observatory)
        self.actionEdit.setObjectName(_fromUtf8("actionEdit"))
        self.actionBitstream400 = QtWidgets.QAction(Observatory)
        self.actionBitstream400.setObjectName(_fromUtf8("actionBitstream400"))
        self.actionBitstream_2 = QtWidgets.QAction(Observatory)
        self.actionBitstream_2.setObjectName(_fromUtf8("actionBitstream_2"))
        self.actionBitstream_3 = QtWidgets.QAction(Observatory)
        self.actionBitstream_3.setObjectName(_fromUtf8("actionBitstream_3"))
        self.actionBitstream_4 = QtWidgets.QAction(Observatory)
        self.actionBitstream_4.setObjectName(_fromUtf8("actionBitstream_4"))
        self.actionBitstream800 = QtWidgets.QAction(Observatory)
        self.actionBitstream800.setObjectName(_fromUtf8("actionBitstream800"))
        self.actionBitstream900 = QtWidgets.QAction(Observatory)
        self.actionBitstream900.setObjectName(_fromUtf8("actionBitstream900"))
        self.actionBitstream1000 = QtWidgets.QAction(Observatory)
        self.actionBitstream1000.setObjectName(_fromUtf8("actionBitstream1000"))
        self.actionSet_Data_Directory = QtWidgets.QAction(Observatory)
        self.actionSet_Data_Directory.setObjectName(_fromUtf8("actionSet_Data_Directory"))
        self.actionSet_integration_time = QtWidgets.QAction(Observatory)
        self.actionSet_integration_time.setObjectName(_fromUtf8("actionSet_integration_time"))
        self.actionReboot_ROACH1 = QtWidgets.QAction(Observatory)
        self.actionReboot_ROACH1.setObjectName(_fromUtf8("actionReboot_ROACH1"))
        self.actionSet_Integration_time_2 = QtWidgets.QAction(Observatory)
        self.actionSet_Integration_time_2.setObjectName(_fromUtf8("actionSet_Integration_time_2"))
        self.actionSet_digital_gain = QtWidgets.QAction(Observatory)
        self.actionSet_digital_gain.setObjectName(_fromUtf8("actionSet_digital_gain"))
        self.actionRun_ROACH = QtWidgets.QAction(Observatory)
        self.actionRun_ROACH.setObjectName(_fromUtf8("actionRun_ROACH"))
        self.actionStop_ROACH = QtWidgets.QAction(Observatory)
        self.actionStop_ROACH.setObjectName(_fromUtf8("actionStop_ROACH"))
        self.action400 = QtWidgets.QAction(Observatory)
        self.action400.setObjectName(_fromUtf8("action400"))
        self.action400_2 = QtWidgets.QAction(Observatory)
        self.action400_2.setObjectName(_fromUtf8("action400_2"))
        self.actionInitialise_WBDC = QtWidgets.QAction(Observatory)
        self.actionInitialise_WBDC.setObjectName(_fromUtf8("actionInitialise_WBDC"))
        self.actionInitialise_Attenuators = QtWidgets.QAction(Observatory)
        self.actionInitialise_Attenuators.setObjectName(_fromUtf8("actionInitialise_Attenuators"))
        self.actionCalibrate_Attenuators = QtWidgets.QAction(Observatory)
        self.actionCalibrate_Attenuators.setObjectName(_fromUtf8("actionCalibrate_Attenuators"))
        
        self.actionWBDC_Low_Level_status = QtWidgets.QAction(Observatory)
        self.actionWBDC_Low_Level_status.setObjectName(_fromUtf8("actionWBDC_Low_Level_status"))
        self.actionWBDC_Low_Level_status.setText(QtWidgets.QApplication.translate(
                                  "Observatory", "WBDC low level status", None))
        
        self.actionQuotient_Plots = QtWidgets.QAction(Observatory)
        self.actionQuotient_Plots.setObjectName(_fromUtf8("actionQuotient_Plots"))
        self.actionVelocity_Plots_2 = QtWidgets.QAction(Observatory)
        self.actionVelocity_Plots_2.setObjectName(_fromUtf8("actionVelocity_Plots_2"))
        self.actionTime_Domain_Plots = QtWidgets.QAction(Observatory)
        self.actionTime_Domain_Plots.setObjectName(_fromUtf8("actionTime_Domain_Plots"))
        
        self.Show_harmonics_scale = QtWidgets.QAction(Observatory)
        self.Show_harmonics_scale.setObjectName(_fromUtf8("Show_harmonics_scale"))
        self.Show_harmonics_scale.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Show Harmonics", None))
        self.menuRFI_Analysis.addAction(self.Show_harmonics_scale)
        
        self.Set_LO_Freq = QtWidgets.QAction(Observatory)
        self.Set_LO_Freq.setObjectName(_fromUtf8("Set_LO_Freq"))
        self.Set_LO_Freq .setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Set LO Freq", None))
        self.menuRFI_Analysis.addAction(self.Set_LO_Freq)
        
        self.actionSky_Frequency = QtWidgets.QAction(Observatory)
        self.actionSky_Frequency.setObjectName(_fromUtf8("actionSky_Frequency"))
        self.actionSet_Reference_Frequency = QtWidgets.QAction(Observatory)
        self.actionSet_Reference_Frequency.setObjectName(_fromUtf8("actionSet_Reference_Frequency"))
        self.actionAveraged_Plots = QtWidgets.QAction(Observatory)
        self.actionAveraged_Plots.setObjectName(_fromUtf8("actionAveraged_Plots"))
        
        self.actionConfigEdit = QtWidgets.QAction(Observatory)
        self.actionConfigEdit.setObjectName(_fromUtf8("actionConfigEdit"))
        self.actionConfigEdit.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Edit", None))
        self.menuConfig.addAction(self.actionConfigEdit)
        
        # the following is not part of anything
        self.actionStart_Observing = QtWidgets.QAction(Observatory)
        self.actionStart_Observing.setObjectName(_fromUtf8("actionStart_Observing"))
        self.actionStart_Observing.setText(QtWidgets.QApplication.translate(
                                        "Observatory", "Start Observing", None))
        
        # this is not part of anything
        self.actionStop_Observing = QtWidgets.QAction(Observatory)
        self.actionStop_Observing.setObjectName(_fromUtf8("actionStop_Observing"))
        self.actionStop_Observing.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Stop Observing", None))

        self.actionStow_Antenna = QtWidgets.QAction(Observatory)
        self.actionStow_Antenna.setObjectName(_fromUtf8("actionStow_Antenna"))
        self.actionStow_Antenna.setText(QtWidgets.QApplication.translate(
                                           "Observatory", "Stow Antenna", None))
        self.menuFile.addAction(self.actionStow_Antenna)
        
        self.actionPAN = QtWidgets.QAction(Observatory)
        self.actionPAN.setObjectName(_fromUtf8("actionPAN"))
        self.actionPAN.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "PAN", None))
        self.menuTools.addAction(self.actionPAN)
        
        self.ProgramROACH = QtWidgets.QAction(Observatory)
        self.ProgramROACH.setObjectName(_fromUtf8("ProgramROACH"))
        self.ProgramROACH.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Program ROACH", None))
        self.menuROACH1.addAction(self.ProgramROACH)
        
        self.actionInitialise_ADC = QtWidgets.QAction(Observatory)
        self.actionInitialise_ADC.setObjectName(_fromUtf8("actionInitialise_ADC"))
        self.actionInitialise_ADC.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Initialise ADC", None))
        self.menuCalibration.addAction(self.actionInitialise_ADC)
        
        self.actionSet_ADC_Gain = QtWidgets.QAction(Observatory)
        self.actionSet_ADC_Gain.setObjectName(_fromUtf8("actionSet_ADC_Gain"))
        self.actionSet_ADC_Gain.setText(QtWidgets.QApplication.translate(
                                           "Observatory", "Set ADC Gain", None))
        self.menuCalibration.addAction(self.actionSet_ADC_Gain)
        
        self.actionSet_FFT_shift = QtWidgets.QAction(Observatory)
        self.actionSet_FFT_shift.setObjectName(_fromUtf8("actionSet_FFT_shift"))
        self.actionAbout = QtWidgets.QAction(Observatory)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAP_TRK = QtWidgets.QAction(Observatory)
        self.actionAP_TRK.setObjectName(_fromUtf8("actionAP_TRK"))
        self.actionAP_STOP = QtWidgets.QAction(Observatory)
        self.actionAP_STOP.setObjectName(_fromUtf8("actionAP_STOP"))
        
        self.actionRun_Snap_Block = QtWidgets.QAction(Observatory)
        self.actionRun_Snap_Block.setObjectName(_fromUtf8("actionRun_Snap_Block"))
        self.actionRun_Snap_Block.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Run Snap Block", None))        
        self.menuROACH1.addAction(self.actionRun_Snap_Block)
        
        self.actionClose_APC = QtWidgets.QAction(Observatory)
        self.actionClose_APC.setObjectName(_fromUtf8("actionClose_APC"))
        self.menuFile.addAction(self.actionSet_Lof_Dir)
        self.menuFile.addAction(self.actionSet_Data_Dir)
        self.menuFile.addAction(self.actionAP_TRK)
        self.menuFile.addAction(self.actionAP_STOP)
        self.menuFile.addAction(self.actionClose_APC)
        
        self.menuConfigure_ROACH.addAction(self.actionRun_ROACH)
        self.menuConfigure_ROACH.addAction(self.actionStop_ROACH)
        self.menuConfigure_ROACH.addAction(self.actionSet_Integration_time_2)
        self.menuConfigure_ROACH.addAction(self.actionSet_digital_gain)
        self.menuConfigure_ROACH.addAction(self.actionSet_FFT_shift)
        self.menuROACH1.addAction(self.menuConfigure_ROACH.menuAction())
        self.menuROACH1.addAction(self.menuCalibration.menuAction())
        self.menuROACH1.addAction(self.actionReboot_ROACH1)
        self.menuWBDC.addAction(self.actionInitialise_WBDC)
        self.menuWBDC.addAction(self.actionInitialise_Attenuators)
        self.menuWBDC.addAction(self.actionCalibrate_Attenuators)
        self.menuWBDC.addAction(self.actionWBDC_Low_Level_status)
        self.menuConfig.addAction(self.menuROACH1.menuAction())
        self.menuConfig.addAction(self.menuWBDC.menuAction())
        self.menuConfig.addAction(self.menuRFI_Analysis.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Observatory)
        self.Ctrl_Tabs.setCurrentIndex(0)
        for num in [2,3,4]:
          self.combo[num].setCurrentIndex(-1)
        #self.combo3.setCurrentIndex(-1)
        #self.combo4.setCurrentIndex(-1)
        #self.combo2.setCurrentIndex(-1)
        self.modeTabWidget.setCurrentIndex(1)
        self.modeTabWidget_2.setCurrentIndex(0)
        
        self.calc_bs_results.toggled.connect(self.kled.toggle)
        
        
        self.calc_bs_results.toggled.connect(self.start_obs.setDisabled)
        
        QtCore.QMetaObject.connectSlotsByName(Observatory)

    def retranslateUi(self, Observatory):
        

        self.close_apc.setText(QtWidgets.QApplication.translate("Observatory", "close APC", None))
        self.WradioButton.setText(QtWidgets.QApplication.translate("Observatory", "W", None))
        self.dBmradioButton.setText(QtWidgets.QApplication.translate("Observatory", "dBm", None))
        self.modeTabWidget.setTabText(self.modeTabWidget.indexOf(self.modeTab), QtWidgets.QApplication.translate("Observatory", "Mode", None))
        self.bs_points.setText(QtWidgets.QApplication.translate("Observatory", "9", None))
        self.label_24.setText(QtWidgets.QApplication.translate("Observatory", "Iterations", None))
        self.bs_repeats.setText(QtWidgets.QApplication.translate("Observatory", "1", None))
        self.label_31.setText(QtWidgets.QApplication.translate("Observatory", "steps (mdeg)", None))
        self.beamsize.setText(QtWidgets.QApplication.translate("Observatory", "4.502", None))
        self.label_25.setText(QtWidgets.QApplication.translate("Observatory", "sec/step", None))
        self.label_32.setText(QtWidgets.QApplication.translate("Observatory", "BS Type", None))
        self.bs_combo_box.setItemText(0, QtWidgets.QApplication.translate("Observatory", "point", None))
        self.bs_combo_box.setItemText(1, QtWidgets.QApplication.translate("Observatory", "conscan", None))
        self.calc_bs_results.setText(QtWidgets.QApplication.translate("Observatory", "Calculate", None))
        self.modeTabWidget.setTabText(self.modeTabWidget.indexOf(self.Boresight), QtWidgets.QApplication.translate("Observatory", "Boresight", None))
        self.modeTabWidget.setTabText(self.modeTabWidget.indexOf(self.tab_3), QtWidgets.QApplication.translate("Observatory", "Tip/Map", None))
        
        self.modeTabWidget_2.setTabText(self.modeTabWidget_2.indexOf(self.tab), QtWidgets.QApplication.translate("Observatory", "SourceTracker", None))
        
        self.pushButton_rec_flg.setText(QtWidgets.QApplication.translate("Observatory", "Record Data", None))
        self.roachInput1.setText(QtWidgets.QApplication.translate("Observatory", "Input1", None))
         
        self.label_recsince.setText(QtWidgets.QApplication.translate("Observatory", "Rec time(min)", None))
        
        
        self.NDtempLabel.setText(QtWidgets.QApplication.translate("Observatory", "K", None))
        self.checkNoise.setText(QtWidgets.QApplication.translate("Observatory", "Noise Diode", None))
        self.nd_mod_pb.setText(QtWidgets.QApplication.translate("Observatory", "ND mod", None))
        self.g2.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        self.ft4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.label_38.setText(QtWidgets.QApplication.translate("Observatory", "2", None))
        self.label_34.setText(QtWidgets.QApplication.translate("Observatory", "FPGAclk(MHz)", None))
        self.g1.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        self.label_35.setText(QtWidgets.QApplication.translate("Observatory", "Roach", None))
        self.at2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.at4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.ft2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.label_36.setText(QtWidgets.QApplication.translate("Observatory", "Gain(dBm)", None))
        self.label_37.setText(QtWidgets.QApplication.translate("Observatory", "1", None))
        self.adt1.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.adt2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.ft1.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.label_39.setText(QtWidgets.QApplication.translate("Observatory", "3", None))
        self.label_65.setText(QtWidgets.QApplication.translate("Observatory", "ADC T(C)", None))
        self.label_33.setText(QtWidgets.QApplication.translate("Observatory", "Amb T(C)", None))
        self.g4.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        self.ft3.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.adt3.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.at1.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.at3.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.g3.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        self.label_40.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        self.adt4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.label_42.setText(QtWidgets.QApplication.translate("Observatory", "RMS", None))
        self.rms1.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.rms2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.rms3.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.rms4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.label_22.setText(QtWidgets.QApplication.translate("Observatory", "ROACH monitor", None))
        self.labelSGFrq.setText(QtWidgets.QApplication.translate("Observatory", "Frequency(MHz)", None))
        self.labelSGAmp.setText(QtWidgets.QApplication.translate("Observatory", "Amplitude(dBm)", None))
        self.SGRFButton.setText(QtWidgets.QApplication.translate("Observatory", "RF ON", None))
        self.label_26.setText(QtWidgets.QApplication.translate("Observatory", "FE Signal Inject", None))
        self.label_41.setText(QtWidgets.QApplication.translate("Observatory", "Last minical Tsys", None))
        self.last_tsys1.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.last_tsys2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.last_tsys3.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.last_tsys4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        
        
        
        self.menuCalibration.setTitle(QtWidgets.QApplication.translate("Observatory", "Calibration", None))
        self.menuConfigure_ROACH.setTitle(QtWidgets.QApplication.translate("Observatory", "Configure ROACH", None))
        self.menuWBDC.setTitle(QtWidgets.QApplication.translate("Observatory", "WBDC", None))
        self.menuRFI_Analysis.setTitle(QtWidgets.QApplication.translate("Observatory", "RFI Analysis", None))
        self.menuPlot.setTitle(QtWidgets.QApplication.translate("Observatory", "Plot", None))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("Observatory", "Help", None))
        self.menuTools.setTitle(QtWidgets.QApplication.translate("Observatory", "Tools", None))
        self.actionSelect_Spectrometer.setText(QtWidgets.QApplication.translate("Observatory", "Select Spectrometer", None))
        self.actionSelect_Firmware.setText(QtWidgets.QApplication.translate("Observatory", "Select Firmware", None))
        self.actionPop_out_Plot2.setText(QtWidgets.QApplication.translate("Observatory", "pop out Plot2", None))
        self.actionVelocity_Plot.setText(QtWidgets.QApplication.translate("Observatory", "Velocity Plot", None))
        self.actionFrequency_Plot.setText(QtWidgets.QApplication.translate("Observatory", "Baseband Frequency", None))
        self.actionChannel_Plot.setText(QtWidgets.QApplication.translate("Observatory", "Channel Plot", None))
        self.actionOffset_Adjustments.setText(QtWidgets.QApplication.translate("Observatory", "Offset Adjustments", None))
        self.actionInput_naming.setText(QtWidgets.QApplication.translate("Observatory", "Input naming", None))
        self.actionProcess_Data_Quotient_Plots.setText(QtWidgets.QApplication.translate("Observatory", "Process Quotient Plots", None))
        self.actionProcess_data_average_plots.setText(QtWidgets.QApplication.translate("Observatory", "Process Averaged Plots", None))
        self.actionProcess_data_time_plots.setText(QtWidgets.QApplication.translate("Observatory", "Process Time Plots", None))
        self.actionNoise_Integration_test.setText(QtWidgets.QApplication.translate("Observatory", "Noise Integration test", None))
        self.actionTIme_domain_plots.setText(QtWidgets.QApplication.translate("Observatory", "Time domain", None))
        self.actionVelocity_Plots.setText(QtWidgets.QApplication.translate("Observatory", "LSR Velocity", None))
        self.actionChannel_Plots.setText(QtWidgets.QApplication.translate("Observatory", "Channel Numbers", None))
        self.actionLoad_Firmware.setText(QtWidgets.QApplication.translate("Observatory", "Load Spectro1", None))
        self.actionReset_Spectrometer1.setText(QtWidgets.QApplication.translate("Observatory", "Spectro1", None))
        self.actionLoad_Firmware2.setText(QtWidgets.QApplication.translate("Observatory", "LoadSpectro2", None))
        self.actionReset_Spectrometer2.setText(QtWidgets.QApplication.translate("Observatory", "Reset Spectro2", None))
        self.actionOpen_Logfile_location.setText(QtWidgets.QApplication.translate("Observatory", "Open Log Dir", None))
        self.actionOpen_Datafile_location.setText(QtWidgets.QApplication.translate("Observatory", "Open Data Dir", None))
        
        
        
        self.actionLoad_data_file_to_simulate.setText(QtWidgets.QApplication.translate("Observatory", "Load data file to simulate", None))
        self.actionLoad_data_1.setText(QtWidgets.QApplication.translate("Observatory", "Load data 1", None))
        self.actionLoad_data_2.setText(QtWidgets.QApplication.translate("Observatory", "Load data 2", None))
        self.actionLoad_Dir.setText(QtWidgets.QApplication.translate("Observatory", "Load Dir", None))
        self.actionStart_time.setText(QtWidgets.QApplication.translate("Observatory", "Start time", None))
        self.actionStop_time.setText(QtWidgets.QApplication.translate("Observatory", "Stop time", None))
        self.actionFrames_per_sec.setText(QtWidgets.QApplication.translate("Observatory", "Frames per sec", None))
        self.actionWBDC.setText(QtWidgets.QApplication.translate("Observatory", "WBDC", None))
        self.actionROACH1.setText(QtWidgets.QApplication.translate("Observatory", "ROACH1", None))
        self.actionROACH2.setText(QtWidgets.QApplication.translate("Observatory", "ROACH2", None))
        self.actionROACH3.setText(QtWidgets.QApplication.translate("Observatory", "ROACH3", None))
        self.actionAnalitical_Plot.setText(QtWidgets.QApplication.translate("Observatory", "Analytical Plot", None))
        self.actionROACH4.setText(QtWidgets.QApplication.translate("Observatory", "ROACH4", None))
        self.actionWBDC_Edit.setText(QtWidgets.QApplication.translate("Observatory", "WBDC Edit", None))
        self.actionSet_Lof_Dir.setText(QtWidgets.QApplication.translate("Observatory", "Set Log Dir", None))
        self.actionSet_Data_Dir.setText(QtWidgets.QApplication.translate("Observatory", "Set Data Dir", None))
        self.actionEdit.setText(QtWidgets.QApplication.translate("Observatory", "Edit", None))
        self.actionBitstream400.setText(QtWidgets.QApplication.translate("Observatory", "400Mhz_iadc_2x", None))
        self.actionBitstream_2.setText(QtWidgets.QApplication.translate("Observatory", "Bitstream 2", None))
        self.actionBitstream_3.setText(QtWidgets.QApplication.translate("Observatory", "Bitstream 3", None))
        self.actionBitstream_4.setText(QtWidgets.QApplication.translate("Observatory", "Bitstream 4", None))
        self.actionBitstream800.setText(QtWidgets.QApplication.translate("Observatory", "800Mhz_iadc_1x", None))
        self.actionBitstream900.setText(QtWidgets.QApplication.translate("Observatory", "900MHz_katcp_1x", None))
        self.actionBitstream1000.setText(QtWidgets.QApplication.translate("Observatory", "1GHz_katcp_1x", None))
        self.actionSet_Data_Directory.setText(QtWidgets.QApplication.translate("Observatory", "Set Data Directory", None))
        self.actionSet_integration_time.setText(QtWidgets.QApplication.translate("Observatory", "Set integration time", None))
        self.actionReboot_ROACH1.setText(QtWidgets.QApplication.translate("Observatory", "Reboot ROACH", None))
        self.actionSet_Integration_time_2.setText(QtWidgets.QApplication.translate("Observatory", "Set Integration time", None))
        self.actionSet_digital_gain.setText(QtWidgets.QApplication.translate("Observatory", "Set digital gain", None))
        self.actionRun_ROACH.setText(QtWidgets.QApplication.translate("Observatory", "Run ROACH", None))
        self.actionStop_ROACH.setText(QtWidgets.QApplication.translate("Observatory", "Stop ROACH", None))
        self.action400.setText(QtWidgets.QApplication.translate("Observatory", "400MHz", None))
        self.action400_2.setText(QtWidgets.QApplication.translate("Observatory", "800MHz", None))
        self.actionInitialise_WBDC.setText(QtWidgets.QApplication.translate("Observatory", "Initialise WBDC", None))
        self.actionInitialise_Attenuators.setText(QtWidgets.QApplication.translate("Observatory", "Initialise Attenuators", None))
        self.actionCalibrate_Attenuators.setText(QtWidgets.QApplication.translate("Observatory", "Calibrate Attenuators", None))
        self.actionQuotient_Plots.setText(QtWidgets.QApplication.translate("Observatory", "Quotient Plots", None))
        self.actionVelocity_Plots_2.setText(QtWidgets.QApplication.translate("Observatory", "Velocity Plots", None))
        self.actionTime_Domain_Plots.setText(QtWidgets.QApplication.translate("Observatory", "Time Domain Plots", None))

       
        self.actionSky_Frequency.setText(QtWidgets.QApplication.translate("Observatory", "Sky Frequency", None))
        self.actionSet_Reference_Frequency.setText(QtWidgets.QApplication.translate("Observatory", "Set Reference Frequency", None))
        self.actionAveraged_Plots.setText(QtWidgets.QApplication.translate("Observatory", "Averaged Plots", None))
        self.actionSet_FFT_shift.setText(QtWidgets.QApplication.translate("Observatory", "Set FFT shift", None))
        self.actionAbout.setText(QtWidgets.QApplication.translate("Observatory", "About", None))
        self.actionAP_TRK.setText(QtWidgets.QApplication.translate("Observatory", "AP TRK", None))
        self.actionAP_STOP.setText(QtWidgets.QApplication.translate("Observatory", "AP STOP", None))

        self.actionClose_APC.setText(QtWidgets.QApplication.translate("Observatory", "close APC", None))

from LED.LedIndicatorWidget import LedIndicator as KLed
