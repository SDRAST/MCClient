# -*- coding: utf-8 -*-
import ephem
import logging

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
from miscPalette import pmLabelPalette, palette70K, palette12K
from miscPalette import load2Palette, load1Palette

from obs_pars import ObsParsFrame, MultiHChecks

logger = logging.getLogger(__name__)
rad2deg= 180/numpy.pi

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def makeSkyMapAxes(parent, fig, polar=False, title="title", azticks=None,
                     top="N", fontsize=8):
  """
  return class for Cartesian or polar Axes for horizon coordinate system
  
  Args:
    fig (Figure): to which the axes belong
    polar (bool): True for a polar plot
    title (str):  plot title
    azticks(int): separation before azimuth ticks (default 45 deg)
  """
  if polar:
    from matplotlib.projections.polar import PolarAxes
    class SkyMapAxes(PolarAxes):
      """
      Azimuth is the polar angle.
      Elevation is the co-radius 90 at pol, 0 at circumference.
      """
      def __init__(self, parent, fig, polar=False, title="title", azticks=None,
                     top="N", fontsize=8):
        self.logger = logging.getLogger(logger.name+".SkyMapAxes")
        self.parent = parent
        self.polar = True
        PolarAxes.__init__(self, fig, [0.05, 0.05, 0.95, 0.95])
        self.format_axes(title=title, azticks=azticks,
                         top=top, fontsize=fontsize)
        fig.add_axes(self)
        self.logger.debug("__init__: initialized for polar projection")
      
      def format_axes(self, title="title", azticks=None,
                     top="N", fontsize=8):
        """
        """
        self.grid(color='grey', linestyle='--', linewidth=0.5)
        self.set_title(title, fontsize=fontsize)
        self.set_theta_zero_location(top)
        self.invert_yaxis()
        self.set_theta_direction(-1)
        if azticks:
          self.set_thetagrids(numpy.arange(0, 360, azticks))
        self.set_ylim(90,0)        
        
      def plot(self, az, el, marker='.', markersize=None, color=None, alpha=None,
               linestyle=None, ls=None, picker=None):
        """
        converts azimuth in degrees to radians
        """
        if type(az) == list:
          az = numpy.array(az)
        az = az*numpy.pi/180
        if ls:
          linestyle=ls
        lines = super(SkyMapAxes, self).plot(az, el,
                                     marker=marker, markersize=markersize,
                                     linestyle=linestyle, color=color,
                                     alpha=alpha, picker=picker)
        return lines
        
      def picker(self, *args):
        """
        """
        self.logger.debug("picker: called with: %s", args)
        event = args[0]
        thisline = event.artist
        self.logger.debug("picker: this line: %s", thisline)
        self.source_pick_az = thisline.get_xdata()[0]*rad2deg
        self.source_pick_alt = thisline.get_ydata()[0]
        self.logger.debug("picker: az/el = %s/%s", 
                          self.source_pick_az, self.source_pick_alt)
        for key, value in list(self.parent.parent.skymap.source_dict.items()):
          azimuth = value[2]*rad2deg
          self.logger.debug("picker: matching az %s for %s with az=%s",
                            self.source_pick_az, key, azimuth)
          if round(numpy.float64(self.source_pick_az), 6) == \
             round(numpy.float64(repr(azimuth)), 6): 
            self.logger.debug("picker: match found for object %s", key)
            self.source_name = key
            self.parent.parent.skymap.source_info_ra = value[0]
            self.parent.parent.skymap.source_info_dec = value[1]
            self.parent.parent.skymap.source_info_az = value[2]
            self.parent.parent.skymap.source_info_alt = value[3]
            self.parent.parent.skymap.source_info_flux = value[4]
            self.parent.parent.skymap.source_info_vsys = value[5]
          else:
            pass
        #self.annotation = self.parent.skymap_axes.annotate(
        self.annotation = self.annotate(
                           self.source_name,
                           xy = ((self.source_pick_az), (self.source_pick_alt)),
                           xytext = (-20, 20), textcoords = 'offset points',
                           ha = 'right', va = 'bottom',
                           bbox = dict(boxstyle = 'round,pad=0.5',
                           fc = 'yellow', alpha = 0.5),
                           arrowprops = dict(arrowstyle = '->',
                           connectionstyle = 'arc3,rad=0'))
        # by default, disable the annotation visibility
        self.annotation.set_visible(True)
        self.parent.skymap_canvas.draw()
        self.annotation.set_visible(False)
    return SkyMapAxes(parent, fig, polar=polar, title=title, azticks=azticks,
                      top=top, fontsize=fontsize)
  else: # not polar
    from matplotlib.axes import Axes
    class SkyMapAxes(Axes):
      """
      Azimuth is the X-axis.
      Elevation is the Y-axis.
      """
      def __init__(self, parent, fig, polar=False, title="title", azticks=None,
                     top="N", fontsize=8):
        self.logger = logging.getLogger(logger.name+".SkyMapAxes")
        self.parent = parent
        self.polar = False
        Axes.__init__(self, fig, [0.05, 0.05, 0.95, 0.95])
        self.format_axes(title=title, azticks=azticks,
                         top=top, fontsize=fontsize)
        fig.add_axes(self)
        self.logger.debug("__init__: initialized for rectangular projection")

      def format_axes(self, title="title", azticks=None,
                     top="N", fontsize=8):
        """
        """
        self.set_xlim(0, 360)
        self.set_ylim(0, 90)
        self.grid(True)
        
      def plot(self, az, el, marker='.', markersize=None, color=None, alpha=None,
               linestyle=None, ls=None, picker=None):
        """
        plot source(s) in degree units
        """
        if ls:
          linestyle=ls
        lines = super(SkyMapAxes, self).plot(az, el,
                                     marker=marker, markersize=markersize,
                                     linestyle=linestyle, color=color,
                                     alpha=alpha, picker=picker)
        return lines
        
      def picker(self, *args):
        """
        """
        self.logger.debug("picker: called with: %s", args)
        event = args[0]
        thisline = event.artist
        self.logger.debug("picker: this line: %s", thisline)
        self.source_pick_az = thisline.get_xdata()[0]
        self.source_pick_alt = thisline.get_ydata()[0]
        self.logger.debug("picker: az/el = %s/%s", 
                      self.source_pick_az, self.source_pick_alt)
        for key, value in list(self.parent.parent.skymap.source_dict.items()):
          self.logger.debug("source_pick: matching az %s",
                            self.source_pick_az)
          azimuth = ephem.hours(value[2])*rad2deg
          self.logger.debug("source_pick: ... az %s", repr(azimuth))
          if round(numpy.float64(self.source_pick_az), 6) == \
             round(numpy.float64(repr(azimuth)), 6): 
            self.logger.debug("source_pick: match found for object %s", key)
            self.source_name = key
            self.parent.parent.skymap.source_info_ra = value[0]
            self.parent.parent.skymap.source_info_dec = value[1]
            self.parent.parent.skymap.source_info_az = value[2]
            self.parent.parent.skymap.source_info_alt = value[3]
            self.parent.parent.skymap.source_info_flux = value[4]
            self.parent.parent.skymap.source_info_vsys = value[5]
          else:
            pass
        #self.annotation = self.parent.skymap_axes.annotate(
        self.annotation = self.annotate(
                           self.source_name,
                           xy = ((self.source_pick_az), (self.source_pick_alt)),
                           xytext = (-20, 20), textcoords = 'offset points',
                           ha = 'right', va = 'bottom',
                           bbox = dict(boxstyle = 'round,pad=0.5',
                           fc = 'yellow', alpha = 0.5),
                           arrowprops = dict(arrowstyle = '->',
                           connectionstyle = 'arc3,rad=0'))
        # by default, disable the annotation visibility
        self.annotation.set_visible(True)
        self.parent.skymap_canvas.draw()
        self.annotation.set_visible(False)
    return SkyMapAxes(parent, fig, polar=polar, title=title, azticks=azticks,
                      top=top, fontsize=fontsize)

class AboutDialog(QtWidgets.QDialog):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("About M&C GUI")
        self.layout = QtWidgets.QVBoxLayout()
        
        proglabel = QtWidgets.QLabel()
        proglabel.setText("Observatory Monitor and Control")
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PT Sans"))
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        proglabel.setFont(font)
        proglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(proglabel)
        
        # logos
        dsnralogo = QtGui.QPixmap("./DSNra.png").scaledToHeight(194)
        dsnralabel = QtWidgets.QLabel()
        dsnralabel.setPixmap(dsnralogo)
        dsnralabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(dsnralabel)
        
        logosLayout = QtWidgets.QHBoxLayout()
        
        citlogo = QtGui.QPixmap("./caltech.png").scaledToHeight(194)
        citlabel = QtWidgets.QLabel()
        citlabel.setPixmap(citlogo)
        logosLayout.addWidget(citlabel)
        
        nyuadlogo = QtGui.QPixmap("./nyu-ad.png").scaledToHeight(194)
        nyuadlabel = QtWidgets.QLabel()
        nyuadlabel.setPixmap(nyuadlogo)
        logosLayout.addWidget(nyuadlabel)
        
        saologo = QtGui.QPixmap("./HSCfA.jpg")
        saolabel = QtWidgets.QLabel()
        saolabel.setPixmap(saologo)
        logosLayout.addWidget(saolabel)
        
        self.layout.addLayout(logosLayout)
        
        # buttons to close dialog
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
class Ui_Observatory(object):
    """
    Notes
    =====
    
    """
    def show_about(self):
        about = AboutDialog()
        if about.exec_():
            print("Success!")
        else:
            print("Cancel!")     
               
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

    def HTMLformat(self, text):
         return """<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"
                                \"http://www.w3.org/TR/REC-html40/strict.dtd\">
            <html>
              <body style=\" font-family:\'PT Sans\'; font-size:8pt;
                             font-weight:400; font-style:normal;\">
                <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;
                            margin-right:0px; -qt-block-indent:0;
                            text-indent:0px;\">
                  <span style=\" font-family:\'Sans\';\">""" +\
                    text +\
               """</span>
                </p>
              </body>
            </html>"""            
    
    def setupUi(self, Observatory, polar_sky=False):
        """
        initialize the GUI
        """
        self.name = Observatory.name
        self.parent = Observatory
        # configure the main window
        Observatory.setObjectName(_fromUtf8("Observatory"))
        Observatory.setEnabled(True)
        Observatory.resize(1260, 800)
        self.stdSizePolicyExpanding(Observatory)
        Observatory.setMinimumSize(QtCore.QSize(0, 0))
        Observatory.setMaximumSize(QtCore.QSize(1260, 900))
        stdPalette(Observatory)        
        Observatory.setMouseTracking(False)
        Observatory.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("galaxy.png")),
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
        self.Ctrl_Tabs.setMaximumSize(QtCore.QSize(1240, 700))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PT Sans"))
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        
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
        palette = self.status.palette()
        brush = QtGui.QBrush(QtGui.QColor(255, 120, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.status.setPalette(palette)
        self.status.setObjectName(_fromUtf8("status"))
        self.status.setText(QtWidgets.QApplication.translate("Observatory",
           "Status: welcome to the Telescope Monitor and Control interface",
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
        
        self.observTabFrame = QtWidgets.QFrame(self.ObsSummary)
        self.stdSizePolicyExpanding(self.observTabFrame)
        self.observTabFrame.setMinimumSize(QtCore.QSize(0, 0))
        stdPalette(self.observTabFrame)
        palette = self.observTabFrame.palette()
        brush = QtGui.QBrush(QtGui.QColor(100, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.observTabFrame.setPalette(palette)
        self.observTabFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.observTabFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.observTabFrame.setObjectName(_fromUtf8("observTabFrame"))
        self.gridLayout_30 = QtWidgets.QGridLayout(self.observTabFrame)
        self.gridLayout_30.setObjectName(_fromUtf8("gridLayout_30"))
        
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem, 0, 3, 1, 1)
        
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName(_fromUtf8("gridLayout_16"))
        
        self.frame_6 = QtWidgets.QFrame(self.observTabFrame)
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
        
        # firmware parameters labels
        self.fwParsLabelVLayout = QtWidgets.QVBoxLayout()
        self.fwParsLabelVLayout.setObjectName(_fromUtf8("fwParsLabelVLayout"))
        
        self.specChansLabel = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.specChansLabel)
        self.specChansLabel.setMaximumSize(QtCore.QSize(87, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.specChansLabel.setFont(font)
        self.specChansLabel.setMouseTracking(True)
        self.specChansLabel.setObjectName(_fromUtf8("specChansLabel"))
        self.specChansLabel.setText(QtWidgets.QApplication.translate(
                              "Observatory", self.HTMLformat("Channels"), None))
        self.fwParsLabelVLayout.addWidget(self.specChansLabel)
        
        self.bwLabel = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.bwLabel)
        self.bwLabel.setMaximumSize(QtCore.QSize(87, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.bwLabel.setFont(font)
        self.bwLabel.setMouseTracking(True)
        self.bwLabel.setObjectName(_fromUtf8("bwLabel"))
        self.bwLabel.setText(QtWidgets.QApplication.translate(
                             "Observatory", self.HTMLformat("BW(MHz))"), None)) 
        self.fwParsLabelVLayout.addWidget(self.bwLabel)
        
        self.label_cf_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_cf_3)
        self.label_cf_3.setMaximumSize(QtCore.QSize(87, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_cf_3.setFont(font)
        self.label_cf_3.setMouseTracking(True)
        self.label_cf_3.setObjectName(_fromUtf8("label_cf_3"))
        self.label_cf_3.setText(QtWidgets.QApplication.translate(
                               "Observatory", self.HTMLformat("CF(MHz)"), None))
        self.fwParsLabelVLayout.addWidget(self.label_cf_3)
        
        self.label_res_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_res_3)
        self.label_res_3.setMaximumSize(QtCore.QSize(87, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_res_3.setFont(font)
        self.label_res_3.setMouseTracking(True)
        self.label_res_3.setObjectName(_fromUtf8("label_res_3"))
        self.label_res_3.setText(QtWidgets.QApplication.translate(
                              "Observatory", self.HTMLformat("Res(kHz)"), None))
        self.fwParsLabelVLayout.addWidget(self.label_res_3)
        
        self.label_oflw_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_oflw_3)
        self.label_oflw_3.setMaximumSize(QtCore.QSize(92, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_oflw_3.setFont(font)
        self.label_oflw_3.setMouseTracking(True)
        self.label_oflw_3.setObjectName(_fromUtf8("label_oflw_3"))
        self.label_oflw_3.setText(QtWidgets.QApplication.translate(
                               "Observatory", self.HTMLformat("Overflw"), None))
        self.fwParsLabelVLayout.addWidget(self.label_oflw_3)
        
        self.label_int_3 = QtWidgets.QLabel(self.frame_6)
        self.stdSizePolicyPreferred(self.label_int_3)
        self.label_int_3.setMaximumSize(QtCore.QSize(92, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_int_3.setFont(font)
        self.label_int_3.setMouseTracking(True)
        self.label_int_3.setObjectName(_fromUtf8("label_int_3"))
        self.label_int_3.setText(QtWidgets.QApplication.translate(
                             "Observatory", self.HTMLformat("Accum's"), None))
        self.fwParsLabelVLayout.addWidget(self.label_int_3)
        
        self.horizontalLayout_43.addLayout(self.fwParsLabelVLayout)
        
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
        self.sourceListDataDirFrame = QtWidgets.QFrame(self.observTabFrame)
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
        
        self.frame_3 = QtWidgets.QFrame(self.observTabFrame)
        self.stdSizePolicyMinimum(self.frame_3)

        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        
        # Tsys recording layout
        #    top row
        self.TsysRecGridLayout = QtWidgets.QGridLayout(self.frame_3)
        self.TsysRecGridLayout.setObjectName(_fromUtf8("TsysRecGridLayout"))
        
        self.feRFnumLabel = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.feRFnumLabel.setFont(font)
        self.feRFnumLabel.setObjectName(_fromUtf8("feRFnumLabel"))
        self.feRFnumLabel.setText(QtWidgets.QApplication.translate(
                                                     "Observatory", "RF", None))
        self.TsysRecGridLayout.addWidget(self.feRFnumLabel, 0, 0, 1, 1)
        
        self.feRFsrcLabel = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.feRFsrcLabel.setFont(font)
        self.feRFsrcLabel.setObjectName(_fromUtf8("feRFsrcLabel"))
        self.feRFsrcLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Source", None))
        self.TsysRecGridLayout.addWidget(self.feRFsrcLabel, 0, 1, 1, 1)
        
        self.fePwrLabel = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.fePwrLabel.setFont(font)
        self.fePwrLabel.setObjectName(_fromUtf8("fePwrLabel"))
        self.fePwrLabel.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Power", None))
        self.TsysRecGridLayout.addWidget(self.fePwrLabel, 0, 3, 1, 1)
        
        self.feTsysLabel = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.feTsysLabel.setFont(font)
        self.feTsysLabel.setObjectName(_fromUtf8("feTsysLabel"))
        self.feTsysLabel.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Tsys", None))
        self.TsysRecGridLayout.addWidget(self.feTsysLabel, 0, 4, 1, 1)
        
        self.label_96 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_96.setFont(font)
        self.label_96.setObjectName(_fromUtf8("label_96"))
        self.label_96.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "Rec", None))
        self.TsysRecGridLayout.addWidget(self.label_96, 0, 5, 1, 1)
        
        #    IF rows
        self.RFLabel = {}
        self.RFselCombo = {}
        self.RFpower = {}
        self.tsys = {}
        self.k_led = {}
        for num in [1,2,3,4]:
          # RF number
          self.RFLabel[num] = QtWidgets.QLabel(self.frame_3)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.RFLabel[num].setFont(font)
          self.RFLabel[num].setObjectName(_fromUtf8("RFLabel"+str(num)))
          self.RFLabel[num].setText(QtWidgets.QApplication.translate(
                                                 "Observatory", str(num), None))
          self.TsysRecGridLayout.addWidget(self.RFLabel[num], num, 0, 1, 1)
          # FE channel select
          self.RFselCombo[num] = QtWidgets.QComboBox(self.frame_3)
          self.stdSizePolicyMinimumExpanding(self.RFselCombo[num])
          font = QtGui.QFont()
          font.setPointSize(6)
          self.RFselCombo[num].setFont(font)
          self.RFselCombo[num].setSizeAdjustPolicy(
                                           QtWidgets.QComboBox.AdjustToContents)
          self.RFselCombo[num].setObjectName(_fromUtf8("combo"+str(num)))
          self.TsysRecGridLayout.addWidget(self.RFselCombo[num], num, 1, 1, 1)
          if num in [2,3,4]:
            self.RFselCombo[num].setCurrentIndex(-1)

          # power
          self.RFpower[num] = QtWidgets.QLabel(self.frame_3)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.RFpower[num].setFont(font)
          self.RFpower[num].setObjectName(_fromUtf8("tsys"+str(num)))
          self.RFpower[num].setText(QtWidgets.QApplication.translate(
                                              "Observatory", "TextLabel", None))
          self.TsysRecGridLayout.addWidget(self.RFpower[num], num, 3, 1, 1)
          # system temperature
          self.tsys[num] = QtWidgets.QLabel(self.frame_3)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.tsys[num].setFont(font)
          self.tsys[num].setObjectName(_fromUtf8("tsys"+str(num)))
          self.tsys[num].setText(QtWidgets.QApplication.translate(
                                              "Observatory", "TextLabel", None))
          self.TsysRecGridLayout.addWidget(self.tsys[num], num, 4, 1, 1)
          # record on/off LED
          self.k_led[num] = KLed(self.frame_3)
          self.k_led[num].setChecked(not self.k_led[num].isChecked())
          self.k_led[num].setObjectName(_fromUtf8("k_led"+str(num)))
          self.TsysRecGridLayout.addWidget(self.k_led[num], num, 5, 1, 1)
        
        self.gridLayout_16.addWidget(self.frame_3, 0, 0, 1, 1)
        
        self.gridLayout_30.addLayout(self.gridLayout_16, 0, 1, 1, 1)
        
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName(_fromUtf8("gridLayout_17"))
        
        self.frame_11 = QtWidgets.QFrame(self.observTabFrame)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName(_fromUtf8("frame_11"))
        
        self.obs_pars = ObsParsFrame(Observatory)
        self.gridLayout_17.addWidget(self.obs_pars, 3, 0, 1, 1)
        
        self.frame_12 = QtWidgets.QFrame(self.observTabFrame)
        self.stdSizePolicyExpanding(self.frame_12)
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
        self.antStatLabel.setObjectName(_fromUtf8("antStatLabel"))
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
                                         "Observatory", "Offset El(mdeg)", None))
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
                                        "Observatory", "Offset xEl(mdeg)", None))
        self.gridLayout_66.addWidget(self.label_16, 5, 0, 1, 1)
        
        self.xel_offset = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.xel_offset.setFont(font)
        self.xel_offset.setObjectName(_fromUtf8("xel_offset"))
        self.xel_offset.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "0.0", None))
        self.gridLayout_66.addWidget(self.xel_offset, 5, 1, 1, 1)
                
        self.gridLayout_17.addWidget(self.frame_12, 1, 0, 1, 1)
        
        self.frame_15 = QtWidgets.QFrame(self.observTabFrame)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName(_fromUtf8("frame_15"))
        self.gridLayout_17.addWidget(self.frame_15, 6, 0, 1, 1)
        
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_du = QtWidgets.QLabel(self.observTabFrame)
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
        
        self.progressBar_1 = QtWidgets.QProgressBar(self.observTabFrame)
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
        
        self.frame_2 = QtWidgets.QFrame(self.observTabFrame)
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
        self.start_obs = QtWidgets.QPushButton(self.observTabFrame)
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
        self.close_apc = QtWidgets.QPushButton(self.observTabFrame)
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
        
        self.bsOfstSRposFrame = QtWidgets.QFrame(self.observTabFrame)
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
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BSoffsetLabel.setFont(font)
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
        
        self.focusLedHLayout = QtWidgets.QHBoxLayout()
        self.focusLedHLayout.setObjectName(_fromUtf8("focusLedHLayout"))
        
        self.leftFocusLED = KLed(self.bsOfstSRposFrame)
        self.leftFocusLED.setChecked(False)
        self.leftFocusLED.setObjectName(_fromUtf8("leftFocusLED"))
        self.focusLedHLayout.addWidget(self.leftFocusLED)
        
        self.cntrFocusLED = KLed(self.bsOfstSRposFrame)
        self.cntrFocusLED.setChecked(True)
        self.cntrFocusLED.setObjectName(_fromUtf8("cntrFocusLED"))
        self.focusLedHLayout.addWidget(self.cntrFocusLED)
        
        self.rghtFocusLED = KLed(self.bsOfstSRposFrame)
        self.rghtFocusLED.setChecked(False)
        self.rghtFocusLED.setObjectName(_fromUtf8("rghtFocusLED"))
        self.focusLedHLayout.addWidget(self.rghtFocusLED)
        
        self.gridLayout_33.addLayout(self.focusLedHLayout, 2, 1, 1, 1)
        
        self.SRposLabel = QtWidgets.QLabel(self.bsOfstSRposFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SRposLabel.setFont(font)
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
        
        self.modeTabWidget = QtWidgets.QTabWidget(self.observTabFrame)
        tabPalette(self.modeTabWidget)
        self.modeTabWidget.setObjectName(_fromUtf8("tabWidget"))
        
        self.modeTab = QtWidgets.QWidget()
        self.modeTab.setObjectName(_fromUtf8("Mode"))
         
        self.boresightTab = QtWidgets.QWidget()
        self.boresightTab.setObjectName(_fromUtf8("Boresight"))
        self.boreTabGridLayout = QtWidgets.QGridLayout()
        self.boreTabGridLayout.setObjectName(_fromUtf8("boreTabGridLayout"))
        self.boreParsGridLayout = QtWidgets.QGridLayout(self.boresightTab)
        self.boreParsGridLayout.addLayout(self.boreTabGridLayout, 0, 0, 1, 1)
        self.boreParsGridLayout.setObjectName(_fromUtf8("gridLayout_40"))
        
        self.tipMapTab = QtWidgets.QWidget()
        self.tipMapTab.setObjectName(_fromUtf8("tab_3"))
        self.gridLayout_38 = QtWidgets.QGridLayout(self.tipMapTab)
        self.gridLayout_38.setObjectName(_fromUtf8("gridLayout_38"))
        self.frame_16 = QtWidgets.QFrame(self.tipMapTab)
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName(_fromUtf8("frame_16"))
        
        self.modeTabWidget.addTab(self.modeTab, _fromUtf8(""))
        self.modeTabWidget.setTabText(self.modeTabWidget.indexOf(self.modeTab),
                  QtWidgets.QApplication.translate("Observatory", "Mode", None))
                  
        self.modeTabWidget.addTab(self.boresightTab, _fromUtf8(""))
        self.modeTabWidget.setTabText(
                                  self.modeTabWidget.indexOf(self.boresightTab),
             QtWidgets.QApplication.translate("Observatory", "Boresight", None))
        
        self.modeTabWidget.addTab(self.tipMapTab, _fromUtf8(""))
        self.gridLayout_18.addWidget(self.modeTabWidget, 0, 0, 1, 1)
        self.modeTabWidget.setTabText(self.modeTabWidget.indexOf(self.tipMapTab),
               QtWidgets.QApplication.translate("Observatory", "Tip/Map", None))
        
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
          palette = pmLabelPalette()
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
        
        
        
        self.label_30 = QtWidgets.QLabel(self.boresightTab)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_30.setFont(font)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.label_30.setText(QtWidgets.QApplication.translate(
                                              "Observatory", "Boresight", None))
        self.boreTabGridLayout.addWidget(self.label_30, 0, 0, 1, 1)
        
        self.bs_source_que = QtWidgets.QListWidget(self.boresightTab)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.bs_source_que.setFont(font)
        self.bs_source_que.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.bs_source_que.setObjectName(_fromUtf8("bs_source_que"))
        self.bs_source_que.setToolTip("Drag sources here from Source List")
        self.boreTabGridLayout.addWidget(self.bs_source_que, 1, 1, 1, 1)
        
        self.label_20 = QtWidgets.QLabel(self.boresightTab)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_20.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "BS sources", None))
        self.boreTabGridLayout.addWidget(self.label_20, 0, 1, 1, 1)
        
        self.frame_10 = QtWidgets.QFrame(self.boresightTab)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                                 self.label_24.sizePolicy().hasHeightForWidth())
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                                    QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                                 self.label_31.sizePolicy().hasHeightForWidth())
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                                    QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                                 self.label_25.sizePolicy().hasHeightForWidth())
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                                 self.label_32.sizePolicy().hasHeightForWidth())
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
        
        spacerItem6 = QtWidgets.QSpacerItem(20, 40,
                 QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_38.addItem(spacerItem6)
        self.calc_bs_results = QtWidgets.QPushButton(self.frame_10)
        bsPalette(self.calc_bs_results)
        self.calc_bs_results.setCheckable(True)
        self.calc_bs_results.setAutoExclusive(True)
        self.calc_bs_results.setObjectName(_fromUtf8("calc_bs_results"))
        self.horizontalLayout_38.addWidget(self.calc_bs_results)
        self.verticalLayout_4.addLayout(self.horizontalLayout_38)
        self.gridLayout_13.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.boreTabGridLayout.addWidget(self.frame_10, 1, 0, 1, 1)
        
        # boresight plot
        self.bore_mpl = QtWidgets.QWidget(self.boresightTab)
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
        self.boreTabGridLayout.addWidget(self.bore_mpl, 3, 0, 1, 2)
        
        self.slew_to_source = QtWidgets.QPushButton(self.boresightTab)
        self.slew_to_source.setToolTip('Send source to antenna and track')
        bs2Palette(self.slew_to_source)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.slew_to_source.setFont(font)
        self.slew_to_source.setCheckable(True)
        self.slew_to_source.setObjectName(_fromUtf8("slew_to_source"))
        self.slew_to_source.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "slew to source", None))
        self.boreTabGridLayout.addWidget(self.slew_to_source, 2, 0, 1, 1)
        
        
        
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
        self.beammap_axes = makeSkyMapAxes(self, self.beammap_fig, 
                                      polar=True,
                                      title="Beam Scan Plot", azticks=45)
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
        
        
        self.gridLayout_30.addLayout(self.gridLayout_18, 0, 2, 1, 1)
        
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName(_fromUtf8("gridLayout_19"))
        
        # system temperature plot
        self.tsys_widget = QtWidgets.QWidget(self.observTabFrame)
        self.stdSizePolicyExpanding( self.tsys_widget)
        self.tsys_widget.setMinimumSize(QtCore.QSize(289, 191))
        self.tsys_widget.setMaximumSize(QtCore.QSize(1000, 1000))
        self.tsys_widget.setObjectName(_fromUtf8("tsys_widget"))
        self.tsys_fig = Figure()
        self.tsys_canvas = FigureCanvas(self.tsys_fig)
        self.tsys_canvas.setToolTip("Front end system\ntemperature (K)")
        self.tsys_axes = self.tsys_fig.add_subplot(111)
        self.tsys_axes.set_title("Tsys vs Time", fontsize=8) # not showing
        self.tsys_axes.set_ylabel ('Tsys(K)', fontsize = 'smaller') # not show
        self.tsys_axes.set_xlabel ('Time (sec)', fontsize = 'smaller') # no show
        self.tsys_axes.tick_params(axis='both', which='major', labelsize=8)
        self.tsys_axes.set_title("W vs Time", fontsize=8) # not showing
        self.tsys_axes.set_ylabel ('ND(W)', fontsize = 'smaller') # not showing
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
        self.source_mpl = QtWidgets.QWidget(self.observTabFrame)
        self.source_mpl.setToolTip('Antenna direction')
        self.stdSizePolicyExpanding(self.source_mpl)
        self.source_mpl.setMinimumSize(QtCore.QSize(289, 191))
        self.source_mpl.setMaximumSize(QtCore.QSize(1000, 1000))
        self.source_mpl.setObjectName(_fromUtf8("source_mpl"))
        self.source_fig = Figure()
        self.source_canvas = FigureCanvas(self.source_fig)
        self.source_axes =  makeSkyMapAxes(self, self.source_fig, 
                                      polar=True,
                                      title="Antenna Az-El", azticks=45)
        logger.debug("setupUi: 'source_axes' is %s", self.source_axes)
        self.azel_mark, = self.source_axes.plot(0, 90, marker='o', color='red')
        self.source_VBL = QtWidgets.QVBoxLayout(self.source_mpl)
        self.source_VBL.addWidget(self.source_canvas)
        self.source_NTB = NavigationToolbar(self.source_canvas, self.source_mpl)
        self.source_VBL.addWidget(self.source_NTB)
        self.gridLayout_19.addWidget(self.source_mpl, 0, 0, 1, 1)
        
        self.gridLayout_30.addLayout(self.gridLayout_19, 0, 0, 1, 1)
        
        self.gridLayout_28.addWidget(self.observTabFrame, 0, 0, 1, 1)
        
        self.gridLayout_27.addLayout(self.gridLayout_28, 0, 0, 1, 1)
        
        self.Ctrl_Tabs.addTab(self.ObsSummary, _fromUtf8(""))
        self.Ctrl_Tabs.setTabText(self.Ctrl_Tabs.indexOf(self.ObsSummary),
                                  QtWidgets.QApplication.translate(
                                           "Observatory", "Observations", None))
        # end of Observations page
        
        # page for the Catalogues tab ##########################################
        
        self.Sources = QtWidgets.QWidget()
        self.Sources.name = "Sources"
        self.Sources.setObjectName(_fromUtf8("Sources"))
        palette = self.Sources.palette()
        brush = QtGui.QBrush(QtGui.QColor(100, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.Sources.setPalette(palette)
        
        # right side of the page
        self.CatalogTabLayout = QtWidgets.QGridLayout(self.Sources)
        self.CatalogTabLayout.setObjectName(_fromUtf8("gridLayout_15"))
        
        # tracker widgets
        self.modeTabWidget_2 = QtWidgets.QTabWidget(self.Sources)
        self.modeTabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        
        # source tracker tab
        self.srcTrackTab = QtWidgets.QWidget()
        self.srcTrackTab.setObjectName(_fromUtf8("srcTrackTab"))
        
        self.srcTrackGLayout = QtWidgets.QGridLayout(self.srcTrackTab)
        self.srcTrackGLayout.setObjectName(_fromUtf8("srcTrackGLayout"))
        
        # elevation vs time plot
        self.EltimeSource = QtWidgets.QWidget(self.srcTrackTab)
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
        self.srcTrackGLayout.addWidget(self.EltimeSource, 0, 0, 1, 1)
        
        self.frame_14 = QtWidgets.QFrame(self.srcTrackTab)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName(_fromUtf8("frame_14"))
        
        self.gridLayout_34 = QtWidgets.QGridLayout(self.frame_14)
        self.gridLayout_34.setObjectName(_fromUtf8("gridLayout_34"))
        
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        
        # source info block on Catalogues page (right column)
        #    label
        self.sourceInfoLabel = QtWidgets.QLabel(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.sourceInfoLabel.setFont(font)
        self.sourceInfoLabel.setObjectName(_fromUtf8("sourceInfoLabel"))
        self.sourceInfoLabel.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Source Info", None))
        self.gridLayout_9.addWidget(self.sourceInfoLabel, 0, 0, 1, 1)
        
        self.srcCatgCatlVLayout = QtWidgets.QVBoxLayout()
        self.srcCatgCatlVLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.srcCatgCatlVLayout.setObjectName(_fromUtf8("srcCatgCatlVLayout"))
        #    text window
        self.sourceInfo = QtWidgets.QPlainTextEdit(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.sourceInfo.setFont(font)
        self.sourceInfo.setReadOnly(True)
        self.sourceInfo.setObjectName(_fromUtf8("sourceInfo"))
        self.sourceInfo.setPlainText(QtWidgets.QApplication.translate(
                                      "Observatory", "source_unselected", None))
        self.srcCatgCatlVLayout.addWidget(self.sourceInfo)
        
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setObjectName(_fromUtf8("horizontalLayout_39"))
        self.srcCatgCatlVLayout.addLayout(self.horizontalLayout_39)
        
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.frame_14)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.srcCatgCatlVLayout.addWidget(self.dateTimeEdit)
        
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setObjectName(_fromUtf8("horizontalLayout_47"))
        
        # pick source
        self.pick_source = QtWidgets.QPushButton(self.frame_14)
        self.pick_source.setToolTip('Add to Source List on Observations tab')
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pick_source.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("back.png")),
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
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("play.png")),
                                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("pause.png")),
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
        self.srcCatgCatlVLayout.addLayout(self.horizontalLayout_47)
        
        self.horizontalLayout_40 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_40.setObjectName(_fromUtf8("horizontalLayout_40"))
        self.srcCatgCatlVLayout.addLayout(self.horizontalLayout_40)
        
        # sky map select
        self.skymapSelectLayout = QtWidgets.QGridLayout()
        self.skymapSelectLayout.setObjectName(_fromUtf8("gridLayout_22"))
        #           category and source select
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
        #           end of plot display categories check boxes
        
        #           source from other catalog section
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
        
        self.sourceRaDecHLayout = QtWidgets.QHBoxLayout()
        self.sourceRaDecHLayout.setObjectName(_fromUtf8("sourceRaDecHLayout"))
        
        self.Dec_edit = QtWidgets.QLineEdit(self.frame_14)
        self.Dec_edit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Dec_edit.setFont(font)
        self.Dec_edit.setObjectName(_fromUtf8("Dec_edit"))
        self.sourceRaDecHLayout.addWidget(self.Dec_edit)
        self.skymapSelectLayout.addLayout(self.sourceRaDecHLayout, 12, 0, 1, 2)
        
        self.RA_label = QtWidgets.QLabel(self.frame_14)
        self.RA_label.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RA_label.setFont(font)
        self.RA_label.setObjectName(_fromUtf8("RA_label"))
        self.RA_label.setText(QtWidgets.QApplication.translate(
                                                     "Observatory", "RA", None))
        self.sourceRaDecHLayout.addWidget(self.RA_label)
        
        self.RA_edit = QtWidgets.QLineEdit(self.frame_14)
        self.RA_edit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RA_edit.setFont(font)
        self.RA_edit.setObjectName(_fromUtf8("RA_edit"))
        self.sourceRaDecHLayout.addWidget(self.RA_edit)
        
        self.Dec_label = QtWidgets.QLabel(self.frame_14)
        self.Dec_label.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Dec_label.setFont(font)
        self.Dec_label.setObjectName(_fromUtf8("Dec_label"))
        self.Dec_label.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "Dec", None))
        self.sourceRaDecHLayout.addWidget(self.Dec_label)
        
        self.srcCatgCatlVLayout.addLayout(self.skymapSelectLayout)
        # end right column
        
        self.gridLayout_9.addLayout(self.srcCatgCatlVLayout, 1, 0, 1, 1)
        self.gridLayout_34.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.srcTrackGLayout.addWidget(self.frame_14, 0, 1, 2, 1)
        
        self.AzTime = QtWidgets.QWidget(self.srcTrackTab)
        self.stdSizePolicyMinimum(self.AzTime)
        self.AzTime.setMinimumSize(QtCore.QSize(175, 175))
        self.AzTime.setMaximumSize(QtCore.QSize(275, 275))
        self.AzTime.setObjectName(_fromUtf8("AzTime"))
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

        self.srcTrackGLayout.addWidget(self.AzTime, 1, 0, 1, 1)
        # end source tracker layout
        
        self.modeTabWidget_2.addTab(self.srcTrackTab, _fromUtf8(""))
        self.modeTabWidget_2.setTabText(
                                 self.modeTabWidget_2.indexOf(self.srcTrackTab),
         QtWidgets.QApplication.translate("Observatory", "SourceTracker", None))
        # end of source tracker tab
        
        # antenna tracker tab
        #     this is an empty tab
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
                
        self.modeTabWidget_2.addTab(self.tab_2, _fromUtf8(""))
        self.modeTabWidget_2.setTabText(self.modeTabWidget_2.indexOf(self.tab_2),
            QtWidgets.QApplication.translate("Observatory",
                                             "AntennaTracker", None))
        self.CatalogTabLayout.addWidget(self.modeTabWidget_2, 0, 1, 1, 1)
        # end of tab widget
        
        # left side of the page: sky map
        self.skymap_mpl = QtWidgets.QWidget(self.Sources)
        palette = self.skymap_mpl.palette()
        brush = QtGui.QBrush(QtGui.QColor(100, 255, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.skymap_mpl.setPalette(palette)
        self.skymap_mpl.setToolTip(
            'Left click: select for Source Info\nRight click: show source name')
        self.stdSizePolicyExpanding(self.skymap_mpl)
        self.skymap_mpl.setMinimumSize(QtCore.QSize(300, 300))
        self.skymap_mpl.setMaximumSize(QtCore.QSize(600, 600))
        self.skymap_mpl.setObjectName(_fromUtf8("skymap_mpl"))
        self.skymap_fig = Figure()
        self.skymap_canvas = FigureCanvas(self.skymap_fig)
        self.skymap_axes = makeSkyMapAxes(self, self.skymap_fig, 
                                      polar=polar_sky,
                                      title="Source Selection", azticks=20)
        self.skymap_VBL = QtWidgets.QVBoxLayout(self.skymap_mpl)
        self.skymap_NTB = NavigationToolbar(self.skymap_canvas, self.skymap_mpl)
        self.skymap_VBL.addWidget(self.skymap_canvas)
        self.skymap_VBL.addWidget(self.skymap_NTB)       
        self.CatalogTabLayout.addWidget(self.skymap_mpl, 0, 0, 1, 1)
        self.projectionInd = MultiHChecks(self.Sources, "projectionInd",
                                    number=2,
                                    enabled=[True, True],
                                    checkable=[True, True],
                                    label=["cartesian", "polar"],
                        tooltip=["rectangular XY grid", "polar grid"])
        self.CatalogTabLayout.addWidget(self.projectionInd, 1, 0, 1, 1)
        
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
        self.spectraCanvas = FigureCanvas(self.spectra_fig)
        self.spectraAxes = {}
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)    
        for roach in Observatory.roachnames:
          number = Observatory.roachnames.index(roach) + 1
          self.spectraAxes[number] = self.spectra_fig.add_subplot(220+number)
          self.spectraAxes[number].text(0.05, 0.95, roach, fontsize=10,
                                verticalalignment='top', bbox=props)
          self.spectraAxes[number].grid(True)
        self.spectraVBL = QtWidgets.QVBoxLayout(self.spectra_mpl)
        self.spectraNavTB = NavigationToolbar(self.spectraCanvas, self.spectra_mpl)
        self.spectraVBL.addWidget(self.spectraCanvas)
        self.spectraVBL.addWidget(self.spectraNavTB)
        
        
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
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
        palette = self.RfPath.palette()
        brush = QtGui.QBrush(QtGui.QColor(100, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.RfPath.setPalette(palette)
        
        self.sysStatPageGLayout = QtWidgets.QGridLayout(self.RfPath)
        self.sysStatPageGLayout.setObjectName(_fromUtf8("sysStatPageGLayout"))
        
        # minical plots
        self.minicalPlotVLayout = QtWidgets.QVBoxLayout()
        self.minicalPlotVLayout.setObjectName(_fromUtf8("minicalPlotVLayout"))
        self.minical_mpl = QtWidgets.QWidget(self.RfPath)
        palette = self.minical_mpl.palette()
        brush = QtGui.QBrush(QtGui.QColor(255, 150, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.minical_mpl.setPalette(palette)
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
        self.minicalPlotVLayout.addWidget(self.minical_mpl)
        
        self.sysStatPageGLayout.addLayout(self.minicalPlotVLayout, 0, 0, 1, 1)
        
        # status info column
        self.gridLayout_43 = QtWidgets.QGridLayout()
        self.gridLayout_43.setObjectName(_fromUtf8("gridLayout_43"))
        
        self.gridLayout_23 = QtWidgets.QGridLayout()
        self.gridLayout_23.setObjectName(_fromUtf8("gridLayout_23"))
                
        self.FEstatusLabel = QtWidgets.QLabel(self.RfPath)
        self.FEstatusLabel.setObjectName(_fromUtf8("FEstatusLabel"))
        self.FEstatusLabel.setText(QtWidgets.QApplication.translate(
                                        "Observatory", "Frontend status", None))
        self.gridLayout_23.addWidget(self.FEstatusLabel, 1, 0, 1, 1)

        self.NDweatherVLayout = QtWidgets.QVBoxLayout()
        self.NDweatherVLayout.setObjectName(_fromUtf8("NDweatherVLayout"))
        
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName(_fromUtf8("horizontalLayout_26"))
        
        # noise diode modulation frame
        self.NDmodFRame = QtWidgets.QFrame(self.RfPath)
        palette = self.NDmodFRame.palette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.NDmodFRame.setPalette(palette)
        
        self.stdSizePolicyExpanding(self.NDmodFRame)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.NDmodFRame.setFont(font)
        self.NDmodFRame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.NDmodFRame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.NDmodFRame.setObjectName(_fromUtf8("NDmodFRame"))
        
        self.gridLayout_11 = QtWidgets.QGridLayout(self.NDmodFRame)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        
        self.noiseLevelSpinBox = QtWidgets.QDoubleSpinBox(self.NDmodFRame)
        self.noiseLevelSpinBox.setEnabled(False)
        self.noiseLevelSpinBox.setMaximum(350.0)
        self.noiseLevelSpinBox.setSingleStep(5.0)
        self.noiseLevelSpinBox.setProperty("value", 50.0)
        self.noiseLevelSpinBox.setObjectName(_fromUtf8("noiseLevelSpinBox"))
        self.horizontalLayout_17.addWidget(self.noiseLevelSpinBox)
        
        self.NDtempLabel = QtWidgets.QLabel(self.NDmodFRame)
        self.NDtempLabel.setObjectName(_fromUtf8("NDtempLabel"))
        self.horizontalLayout_17.addWidget(self.NDtempLabel)
        
        self.verticalLayout_9.addLayout(self.horizontalLayout_17)
        
        self.checkNoise = QtWidgets.QCheckBox(self.NDmodFRame)
        self.checkNoise.setObjectName(_fromUtf8("checkNoise"))
        self.checkNoise.setText(QtWidgets.QApplication.translate(
                                            "Observatory", "Noise Diode", None))
        self.verticalLayout_9.addWidget(self.checkNoise)
        
        self.NDmodHLayout = QtWidgets.QHBoxLayout()
        self.NDmodHLayout.setObjectName(_fromUtf8("NDmodHLayout"))
        self.nd_mod_pb = QtWidgets.QPushButton(self.NDmodFRame)
        self.nd_mod_pb.setCheckable(True)
        self.nd_mod_pb.setObjectName(_fromUtf8("nd_mod_pb"))
        self.NDmodHLayout.addWidget(self.nd_mod_pb)
        
        self.NDmodRateLabel = QtWidgets.QLabel(self.NDmodFRame)
        self.NDmodRateLabel.setObjectName(_fromUtf8("NDmodRateLabel"))
        self.NDmodRateLabel.setText(QtWidgets.QApplication.translate("Observatory",
                                                       "ND mod rate(Hz)", None))
        self.NDmodHLayout.addWidget(self.NDmodRateLabel)
        
        self.ndmod = QtWidgets.QSpinBox(self.NDmodFRame)
        self.ndmod.setEnabled(False)
        self.ndmod.setMinimum(1)
        self.ndmod.setMaximum(6)
        self.ndmod.setSingleStep(1)
        self.ndmod.setProperty("value", 4)
        self.ndmod.setObjectName(_fromUtf8("ndmod"))
        self.NDmodHLayout.addWidget(self.ndmod)
        
        self.verticalLayout_9.addLayout(self.NDmodHLayout)
        self.gridLayout_11.addLayout(self.verticalLayout_9, 1, 1, 1, 1)
        
        self.label_27 = QtWidgets.QLabel(self.NDmodFRame)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.label_27.setText(QtWidgets.QApplication.translate(
                                 "Observatory", "Noise Diode Modulation", None))
        self.gridLayout_11.addWidget(self.label_27, 0, 1, 1, 1)
        
        #spacerItem10 = QtWidgets.QSpacerItem(40, 20,
        #                                     QtWidgets.QSizePolicy.Expanding,
        #                                     QtWidgets.QSizePolicy.Minimum)
        #self.gridLayout_11.addItem(spacerItem10, 1, 2, 1, 1)
        
        self.horizontalLayout_26.addWidget(self.NDmodFRame)
        self.NDweatherVLayout.addLayout(self.horizontalLayout_26)
        # end ND mod frame
                
        # phase cal layout
        self.phaseCalHLayout = QtWidgets.QHBoxLayout()
        self.phaseCalHLayout.setObjectName(_fromUtf8("phaseCalHLayout"))
        
        self.phaseCalcheckBox = QtWidgets.QCheckBox(self.RfPath)
        self.phaseCalcheckBox.setObjectName(_fromUtf8("phaseCalcheckBox"))
        self.phaseCalcheckBox.setText(
             QtWidgets.QApplication.translate("Observatory", "Phase Cal", None))
        self.phaseCalHLayout.addWidget(self.phaseCalcheckBox)
        
        self.RadioButton1MHz = QtWidgets.QRadioButton(self.RfPath)
        self.RadioButton1MHz.setChecked(True)
        self.RadioButton1MHz.setObjectName(_fromUtf8("RadioButton1MHz"))
        self.RadioButton1MHz.setText(
                 QtWidgets.QApplication.translate("Observatory", "1 MHz", None))
        self.phaseCalHLayout.addWidget(self.RadioButton1MHz)
        
        self.RadioButton5MHz = QtWidgets.QRadioButton(self.RfPath)
        self.RadioButton5MHz.setObjectName(_fromUtf8("RadioButton5MHz"))
        self.RadioButton5MHz.setText(
                 QtWidgets.QApplication.translate("Observatory", "5 MHz", None))
        self.phaseCalHLayout.addWidget(self.RadioButton5MHz)
        
        self.NDweatherVLayout.addLayout(self.phaseCalHLayout)
        # end phase cal layout
        
        # weather frame
        self.weatherFrame = QtWidgets.QFrame(self.RfPath)
        self.weatherFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.weatherFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.weatherFrame.setObjectName(_fromUtf8("weatherFrame"))
        
        self.weatherHLayout = QtWidgets.QHBoxLayout(self.weatherFrame)
        self.weatherHLayout.setObjectName(_fromUtf8("weatherHLayout"))
        
        self.weatherParsVLayout = QtWidgets.QVBoxLayout()
        self.weatherParsVLayout.setObjectName(_fromUtf8("weatherParsVLayout"))
        
        # temperature
        self.tempHLayout = QtWidgets.QHBoxLayout()
        self.tempHLayout.setObjectName(_fromUtf8("tempHLayout"))
        
        self.tempLabel = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tempLabel.setFont(font)
        self.tempLabel.setObjectName(_fromUtf8("tempLabel"))
        self.tempLabel.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", "Temp", None))
        self.tempHLayout.addWidget(self.tempLabel)
        
        self.temp = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.temp.setFont(font)
        self.temp.setObjectName(_fromUtf8("temp"))
        self.temp.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.tempHLayout.addWidget(self.temp)
        self.weatherParsVLayout.addLayout(self.tempHLayout)
        
        # pressure
        self.pressureHLayout = QtWidgets.QHBoxLayout()
        self.pressureHLayout.setObjectName(_fromUtf8("pressureHLayout"))
        
        self.pressureLabel = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pressureLabel.setFont(font)
        self.pressureLabel.setObjectName(_fromUtf8("pressureLabel"))
        self.pressureLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Pressure", None))
        self.pressureHLayout.addWidget(self.pressureLabel)
        
        self.pressure = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pressure.setFont(font)
        self.pressure.setObjectName(_fromUtf8("pressure"))
        self.pressure.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.pressureHLayout.addWidget(self.pressure)
        self.weatherParsVLayout.addLayout(self.pressureHLayout)
        
        # humidity
        self.humidityHLayout = QtWidgets.QHBoxLayout()
        self.humidityHLayout.setObjectName(_fromUtf8("humidityHLayout"))
        
        self.humidityLabel = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.humidityLabel.setFont(font)
        self.humidityLabel.setObjectName(_fromUtf8("humidityLabel"))
        self.humidityLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Humidity", None))
        self.humidityHLayout.addWidget(self.humidityLabel)
        
        self.humidity = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.humidity.setFont(font)
        self.humidity.setObjectName(_fromUtf8("humidity"))
        self.humidity.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.humidityHLayout.addWidget(self.humidity)
        self.weatherParsVLayout.addLayout(self.humidityHLayout)
        
        # windspeed
        self.windspeedHLayout = QtWidgets.QHBoxLayout()
        self.windspeedHLayout.setObjectName(_fromUtf8("windspeedHLayout"))
        
        self.windspeedLabel = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.windspeedLabel.setFont(font)
        self.windspeedLabel.setObjectName(_fromUtf8("windspeedLabel"))
        self.windspeedLabel.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "Wind speed", None))
        self.windspeedHLayout.addWidget(self.windspeedLabel)
        
        self.windspeed = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.windspeed.setFont(font)
        self.windspeed.setObjectName(_fromUtf8("windspeed"))
        self.windspeed.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.windspeedHLayout.addWidget(self.windspeed)
        self.weatherParsVLayout.addLayout(self.windspeedHLayout)
        
        # wind direction
        self.windDirHLayout = QtWidgets.QHBoxLayout()
        self.windDirHLayout.setObjectName(_fromUtf8("windDirHLayout"))
        
        self.windDirLabel = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.windDirLabel.setFont(font)
        self.windDirLabel.setObjectName(_fromUtf8("windDirLabel"))
        self.windDirLabel.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Wind direction", None))
        self.windDirHLayout.addWidget(self.windDirLabel)
        
        self.winddir = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.winddir.setFont(font)
        self.winddir.setObjectName(_fromUtf8("winddir"))
        self.winddir.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.windDirHLayout.addWidget(self.winddir)
        self.weatherParsVLayout.addLayout(self.windDirHLayout)
        
        # precipitation
        self.precipHLayout = QtWidgets.QHBoxLayout()
        self.precipHLayout.setObjectName(_fromUtf8("precipHLayout"))
        
        self.precipLabel = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.precipLabel.setFont(font)
        self.precipLabel.setObjectName(_fromUtf8("precipLabel"))
        self.precipLabel.setText(QtWidgets.QApplication.translate(
                                          "Observatory", "Precipitation", None))
        self.precipHLayout.addWidget(self.precipLabel)
        
        self.precip = QtWidgets.QLabel(self.weatherFrame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.precip.setFont(font)
        self.precip.setObjectName(_fromUtf8("precip"))
        self.precip.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
        self.precipHLayout.addWidget(self.precip)
        self.weatherParsVLayout.addLayout(self.precipHLayout)
        # end precip
        
        self.weatherHLayout.addLayout(self.weatherParsVLayout)
        
        self.emptyWeatherFrame = QtWidgets.QFrame(self.weatherFrame)
        self.emptyWeatherFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.emptyWeatherFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.emptyWeatherFrame.setObjectName(_fromUtf8("emptyWeatherFrame"))
        self.weatherHLayout.addWidget(self.emptyWeatherFrame)
        
        self.NDweatherVLayout.addWidget(self.weatherFrame)
        self.gridLayout_23.addLayout(self.NDweatherVLayout, 3, 0, 1, 1)
        # end weather frame
        
        # front end temperatures layout
        self.feTempGLayout = QtWidgets.QGridLayout()
        self.feTempGLayout.setObjectName(_fromUtf8("feTempGLayout"))
        
        # load temps
        self.loadTempHLayout = QtWidgets.QHBoxLayout()
        self.loadTempHLayout.setObjectName(_fromUtf8("loadTempHLayout"))
        
        self.load1tempLabel = QtWidgets.QLabel(self.RfPath)
        self.load1tempLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|
                                   QtCore.Qt.AlignVCenter)
        self.load1tempLabel.setObjectName(_fromUtf8("load1tempLabel"))
        self.load1tempLabel.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "load 1", None))
        self.loadTempHLayout.addWidget(self.load1tempLabel)
        
        self.lcdLoad1 = QtWidgets.QLCDNumber(self.RfPath)
        self.lcdLoad1.setEnabled(True)
        palette = load1Palette()
        self.lcdLoad1.setPalette(palette)
        self.lcdLoad1.setAutoFillBackground(True)
        self.lcdLoad1.setProperty("value", 0.0)
        self.lcdLoad1.setObjectName(_fromUtf8("lcdLoad1"))
        self.loadTempHLayout.addWidget(self.lcdLoad1)
        
        self.lcdLoad2 = QtWidgets.QLCDNumber(self.RfPath)
        self.lcdLoad2.setEnabled(True)
        palette = load2Palette()
        self.lcdLoad2.setPalette(palette)
        self.lcdLoad2.setAutoFillBackground(True)
        self.lcdLoad2.setObjectName(_fromUtf8("lcdLoad2"))
        self.lcdLoad2.setProperty("value", 0.0)
        self.loadTempHLayout.addWidget(self.lcdLoad2)
        
        self.load2tempLabel = QtWidgets.QLabel(self.RfPath)
        self.load2tempLabel.setAlignment(
                                     QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|
                                   QtCore.Qt.AlignVCenter)
        self.load2tempLabel.setObjectName(_fromUtf8("load2tempLabel"))
        self.load2tempLabel.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "load 2", None))
        self.loadTempHLayout.addWidget(self.load2tempLabel)
        self.feTempGLayout.addLayout(self.loadTempHLayout, 0, 0, 1, 1)
        # end load temps
        
        # cryotemps
        self.cryTempHLayout = QtWidgets.QHBoxLayout()
        self.cryTempHLayout.setObjectName(_fromUtf8("cryTempHLayout"))
        
        self.label70K = QtWidgets.QLabel(self.RfPath)
        self.label70K.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|
                                   QtCore.Qt.AlignVCenter)
        self.label70K.setObjectName(_fromUtf8("label70K"))
        self.label70K.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "70 K stage", None))
        self.cryTempHLayout.addWidget(self.label70K)
        
        self.lcd70K = QtWidgets.QLCDNumber(self.RfPath)
        self.lcd70K.setEnabled(True)
        palette = palette70K()
        self.lcd70K.setPalette(palette)
        self.lcd70K.setAutoFillBackground(True)
        self.lcd70K.setObjectName(_fromUtf8("lcd70K"))
        self.lcd70K.setProperty("value", 0.0)
        self.cryTempHLayout.addWidget(self.lcd70K)
        
        self.lcd12K = QtWidgets.QLCDNumber(self.RfPath)
        self.lcd12K.setEnabled(True)
        palette = palette12K()
        self.lcd12K.setPalette(palette)
        self.lcd12K.setAutoFillBackground(True)
        self.lcd12K.setObjectName(_fromUtf8("lcd12K"))
        self.lcd12K.setProperty("value", 0.0)
        self.cryTempHLayout.addWidget(self.lcd12K)
        
        self.label12K = QtWidgets.QLabel(self.RfPath)
        self.label12K.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|
                                   QtCore.Qt.AlignVCenter)
        self.label12K.setObjectName(_fromUtf8("label12K"))
        self.label12K.setText(QtWidgets.QApplication.translate(
                                             "Observatory", "12 K stage", None))
        self.cryTempHLayout.addWidget(self.label12K)
        self.feTempGLayout.addLayout(self.cryTempHLayout, 1, 0, 1, 1)
        # end cry temps
        
        self.gridLayout_23.addLayout(self.feTempGLayout, 2, 0, 1, 1)
        
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
        
        self.label_35 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_35.setFont(font)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.label_35.setText(QtWidgets.QApplication.translate(
                                                  "Observatory", "Roach", None))
        self.gridLayout_42.addWidget(self.label_35, 0, 0, 1, 1)
        
        self.label_36 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_36.setFont(font)
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.gridLayout_42.addWidget(self.label_36, 0, 5, 1, 1)
        
        self.label_38 = QtWidgets.QLabel(self.frame_17)
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.label_38.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "2", None))
        self.gridLayout_42.addWidget(self.label_38, 2, 0, 1, 1)
        
        self.label_39 = QtWidgets.QLabel(self.frame_17)
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.label_39.setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "3", None))
        self.gridLayout_42.addWidget(self.label_39, 3, 0, 1, 1)
        
        self.label_42 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_42.setFont(font)
        self.label_42.setObjectName(_fromUtf8("label_42"))
        self.label_42.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "RMS", None))
        self.gridLayout_42.addWidget(self.label_42, 0, 1, 1, 1)
        
        self.RFTambLabel = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RFTambLabel.setFont(font)
        self.RFTambLabel.setObjectName(_fromUtf8("RFTambLabel"))
        self.RFTambLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "Amb T(C)", None)) 
        self.gridLayout_42.addWidget(self.RFTambLabel, 0, 2, 1, 1)
        
        self.FPGAclkLabel = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FPGAclkLabel.setFont(font)
        self.FPGAclkLabel.setObjectName(_fromUtf8("FPGAclkLabel"))
        self.FPGAclkLabel.setText(QtWidgets.QApplication.translate(
                                           "Observatory", "FPGAclk(MHz)", None))
        self.gridLayout_42.addWidget(self.FPGAclkLabel, 0, 3, 1, 1)
        
        self.ADCTambLabel = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ADCTambLabel.setFont(font)
        self.ADCTambLabel.setObjectName(_fromUtf8("ADCTambLabel"))
        self.ADCTambLabel.setText(QtWidgets.QApplication.translate(
                                               "Observatory", "ADC T(C)", None))
        self.gridLayout_42.addWidget(self.ADCTambLabel, 0, 4, 1, 1)
        
        self.roachNum = {}
        self.rms = {}
        self.at = {}
        self.ft = {}
        self.adt = {}
        self.g = {}
        for num in [1,2,3,4]:
          self.roachNum[num] = QtWidgets.QLabel(self.frame_17)
          self.roachNum[num].setObjectName(_fromUtf8("roachNum"+str(num)))
          self.roachNum[num].setText(QtWidgets.QApplication.translate(
                                                 "Observatory", str(num), None))
          self.gridLayout_42.addWidget(self.roachNum[num], num, 0, 1, 1)
          self.rms[num] = QtWidgets.QLabel(self.frame_17)
          self.rms[num].setObjectName(_fromUtf8("rms"+str(num)))
          self.rms[num].setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
          self.gridLayout_42.addWidget(self.rms[num], num, 1, 1, 1)
          self.at[num] = QtWidgets.QLabel(self.frame_17)
          self.at[num].setObjectName(_fromUtf8("at"+str(num)))
          self.at[num].setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
          self.gridLayout_42.addWidget(self.at[num], num, 2, 1, 1)
          self.ft[num] = QtWidgets.QLabel(self.frame_17)
          self.ft[num].setObjectName(_fromUtf8("ft"+str(num)))
          self.ft[num].setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
          self.gridLayout_42.addWidget(self.ft[num], num, 3, 1, 1)
          self.adt[num] = QtWidgets.QLabel(self.frame_17)
          self.adt[num].setObjectName(_fromUtf8("adt"+str(num)))
          self.adt[num].setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
          self.gridLayout_42.addWidget(self.adt[num], num, 4, 1, 1)
          self.g[num] = QtWidgets.QLabel(self.frame_17)
          self.g[num].setObjectName(_fromUtf8("g"+str(num)))
          self.g[num].setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
          self.gridLayout_42.addWidget(self.g[num], num, 5, 1, 1)

        self.label_40 = QtWidgets.QLabel(self.frame_17)
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.gridLayout_42.addWidget(self.label_40, 4, 0, 1, 1)
        self.gridLayout_43.addWidget(self.frame_17, 3, 0, 1, 2)
        self.label_22 = QtWidgets.QLabel(self.RfPath)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout_43.addWidget(self.label_22, 2, 0, 1, 1)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.labelSGFrq = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelSGFrq.setFont(font)
        self.labelSGFrq.setObjectName(_fromUtf8("labelSGFrq"))
        self.labelSGFrq.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Frequency(MHz)", None))
        self.horizontalLayout.addWidget(self.labelSGFrq)
        
        self.RFsigInjLabel = QtWidgets.QLabel(self.RfPath)
        self.RFsigInjLabel.setObjectName(_fromUtf8("RFsigInjLabel"))
        self.RFsigInjLabel.setText(QtWidgets.QApplication.translate(
                                       "Observatory", "FE Signal Inject", None))
        self.gridLayout_43.addWidget(self.RFsigInjLabel, 5, 0, 1, 1)
        
        self.labelSGAmp = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelSGAmp.setFont(font)
        self.labelSGAmp.setObjectName(_fromUtf8("labelSGAmp"))
        self.labelSGAmp.setText(QtWidgets.QApplication.translate(
                                         "Observatory", "Amplitude(dBm)", None))
        self.horizontalLayout.addWidget(self.labelSGAmp)
        self.gridLayout_43.addLayout(self.horizontalLayout, 5, 1, 1, 1)
        
        self.SGRFButton = QtWidgets.QPushButton(self.RfPath)
        self.SGRFButton.setEnabled(True)
        self.SGRFButton.setCheckable(True)
        self.SGRFButton.setObjectName(_fromUtf8("SGRFButton"))
        self.SGRFButton.setText(QtWidgets.QApplication.translate(
                                                  "Observatory", "RF ON", None))
        self.SGRFButton.setDisabled(True)
        self.gridLayout_43.addWidget(self.SGRFButton, 6, 0, 1, 1)
        
        self.freqAmpSpinBoxHLayout = QtWidgets.QHBoxLayout()
        self.freqAmpSpinBoxHLayout.setObjectName(_fromUtf8(
                                                       "freqAmpSpinBoxHLayout"))
        self.SGFreqSpinBox = QtWidgets.QDoubleSpinBox(self.RfPath)
        self.SGFreqSpinBox.setEnabled(True)
        self.SGFreqSpinBox.setDecimals(5)
        self.SGFreqSpinBox.setMinimum(20000.0)
        self.SGFreqSpinBox.setMaximum(26000.0)
        self.SGFreqSpinBox.setSingleStep(1e-06)
        self.SGFreqSpinBox.setProperty("value", 20000.0)
        self.SGFreqSpinBox.setObjectName(_fromUtf8("SGFreqSpinBox"))
        self.SGFreqSpinBox.setDisabled(True)
        self.freqAmpSpinBoxHLayout.addWidget(self.SGFreqSpinBox)
        self.SGAmpSpinBox = QtWidgets.QDoubleSpinBox(self.RfPath)
        self.SGAmpSpinBox.setEnabled(True)
        self.SGAmpSpinBox.setMinimum(-100.0)
        self.SGAmpSpinBox.setMaximum(-5.0)
        self.SGAmpSpinBox.setProperty("value", -50.0)
        self.SGAmpSpinBox.setObjectName(_fromUtf8("SGAmpSpinBox"))
        self.SGAmpSpinBox.setDisabled(True)
        self.freqAmpSpinBoxHLayout.addWidget(self.SGAmpSpinBox)
        self.gridLayout_43.addLayout(self.freqAmpSpinBoxHLayout, 6, 1, 1, 1)
        
        self.label_41 = QtWidgets.QLabel(self.RfPath)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_41.setFont(font)
        self.label_41.setObjectName(_fromUtf8("label_41"))
        self.gridLayout_43.addWidget(self.label_41, 1, 1, 1, 1)
        
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName(_fromUtf8("horizontalLayout_21"))
        self.last_tsys = {}
        for num in [1,2,3,4]:
          self.last_tsys[num] = QtWidgets.QLabel(self.RfPath)
          font = QtGui.QFont()
          font.setPointSize(8)
          self.last_tsys[num].setFont(font)
          self.last_tsys[num].setObjectName(_fromUtf8("last_tsys"+str(num)))
          self.last_tsys[num].setText(QtWidgets.QApplication.translate(
                                                      "Observatory", "0", None))
          self.horizontalLayout_21.addWidget(self.last_tsys[num])
        self.gridLayout_43.addLayout(self.horizontalLayout_21, 2, 1, 1, 1)
        self.sysStatPageGLayout.addLayout(self.gridLayout_43, 0, 1, 1, 1)
        
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
        self.actionInitialise_Attenuators.setObjectName(
                                      _fromUtf8("actionInitialise_Attenuators"))
        self.actionCalibrate_Attenuators = QtWidgets.QAction(Observatory)
        self.actionCalibrate_Attenuators.setObjectName(
                                       _fromUtf8("actionCalibrate_Attenuators"))
        
        self.actionWBDC_Low_Level_status = QtWidgets.QAction(Observatory)
        self.actionWBDC_Low_Level_status.setObjectName(_fromUtf8(
                                                 "actionWBDC_Low_Level_status"))
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
        self.actionSet_Reference_Frequency.setObjectName(
                                     _fromUtf8("actionSet_Reference_Frequency"))
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
        self.actionAbout.setText(QtWidgets.QApplication.translate(
                                                  "Observatory", "About", None))
        self.actionAbout.triggered.connect(self.show_about)
        
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
        self.modeTabWidget.setCurrentIndex(1)
        self.modeTabWidget_2.setCurrentIndex(0)
        
        self.calc_bs_results.toggled.connect(self.kled.toggle)
        
        
        self.calc_bs_results.toggled.connect(self.start_obs.setDisabled)
        
        QtCore.QMetaObject.connectSlotsByName(Observatory)

    def retranslateUi(self, Observatory):
        

        self.close_apc.setText(QtWidgets.QApplication.translate("Observatory", "close APC", None))
        self.WradioButton.setText(QtWidgets.QApplication.translate("Observatory", "W", None))
        self.dBmradioButton.setText(QtWidgets.QApplication.translate("Observatory", "dBm", None))
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
        
        
        self.pushButton_rec_flg.setText(QtWidgets.QApplication.translate("Observatory", "Record Data", None))
        self.roachInput1.setText(QtWidgets.QApplication.translate("Observatory", "Input1", None))
         
        self.label_recsince.setText(QtWidgets.QApplication.translate("Observatory", "Rec time(min)", None))
        
        
        self.NDtempLabel.setText(QtWidgets.QApplication.translate("Observatory", "K", None))
        self.nd_mod_pb.setText(QtWidgets.QApplication.translate("Observatory", "ND mod", None))
        #self.g2.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        #self.ft4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.at2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.at4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.ft2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.label_36.setText(QtWidgets.QApplication.translate("Observatory", "Gain(dBm)", None))
        #self.adt2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.at3.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.g3.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        self.label_40.setText(QtWidgets.QApplication.translate("Observatory", "4", None))
        #self.adt4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.rms2.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.rms3.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        #self.rms4.setText(QtWidgets.QApplication.translate("Observatory", "0", None))
        self.label_22.setText(QtWidgets.QApplication.translate("Observatory", "ROACH monitor", None))
        self.label_41.setText(QtWidgets.QApplication.translate("Observatory", "Last minical Tsys", None))
        
        
        
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
        self.actionAP_TRK.setText(QtWidgets.QApplication.translate("Observatory", "AP TRK", None))
        self.actionAP_STOP.setText(QtWidgets.QApplication.translate("Observatory", "AP STOP", None))

        self.actionClose_APC.setText(QtWidgets.QApplication.translate("Observatory", "close APC", None))

from LED.LedIndicatorWidget import LedIndicator as KLed
