"""
for classes RoachMPL (FigureCanvas), PlotDef(ThreadInit), Canvas3Plots(PlotDef)

The logic of this module escapes me. 

``PlotDef`` starts a thread and has methods to define ``canvas`` attributes. 
Each canvas is a ``RoachMPL`` instance.  ``RoachMPL`` has methods for defining
the details of these canvases, typically one method for each canvas. The only
thing common to all ``RoachMPL`` instances is a ``Figure`` attribute.  A
``FigureCanvas`` attribute is also defined but only used in the 
``spectrum_roach()`` method.  All the other methods initialize their own
``FigureCanvas`` instances.
"""
import h5py
import logging
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets
import time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import threaded
ThreadInit = threaded.ThreadInit
logger = logging.getLogger(__name__)

class RoachMPL(FigureCanvas):
    """
    Class initiates matplotlib and defines matplotlib axis properties::
    
      axes1 belongs to canvas   and is used by spectrum_roach()
      axes2    ''   '' canvas           ''        ''
      axes3    ''   '' canvas           ''        ''
      axes4    ''   '' canvas           ''        '', and also spectrum_SRsource()
      axes5    ''   '' canvas5          ''     spectrum_tsys()
      axes6    ''   '' canvas6          ''     spectrum_bore()
      axes7    ''   '' canvas7          ''     spectrum_source()
      axes8    ''   '' canvas8          ''     spectrum_skymap()
      axes9    ''   '' canvas9          ''     spectrumElTime()
      axes10   ''   '' canvas10         ''     spectrumAztime()
      axes14   ''   '' canvas14         ''     spectrum_minical()
      axes15   ''   '' canvas15         ''     spectrum_yfactor()
      axes16   ''   '' canvas16         ''     tipping_plot()
      axes17   ''   '' canvas17         ''     beam_mapping_plot()
    
    canvas15 is not defined by PlotDef. 
    2x Matplotlib windows for 1020 MHz firmware 2 inputs per ROACH(interleaved)
        Working configuration
        -1000MHz, 900MHz(to be implemented) for 16k channels 
    4x Matplotlib windows for 400 MHz firmware 4 inputs per ROACH
        Working configuration
        -400 MHz, 450MHz(to be implemented) for 8k channels 
    """
    def __init__(self, parent=None):
        """
        Initiates matplotlib windows
        """
        self.logger = logging.getLogger(logger.name+".RoachMPL")
        self.fig = Figure()
        #self.fig.hold(False)
        self.canvas = FigureCanvas.__init__(self, self.fig)

    def spectrum_roach(self, ui):
        """
        Define initial plots for various configurations of the 
        hardware/firmware, this is to be controlled by the RF Map path tab
        """
        self.ui = ui
        #self.fig = Figure()
        #self.canvas = FigureCanvas.__init__(self, self.fig)
        self.axes1 = self.fig.add_subplot(221)
        self.axes2 = self.fig.add_subplot(222)
        self.axes3 = self.fig.add_subplot(223)
        self.axes4 = self.fig.add_subplot(224)
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

    def spectrum_tsys(self, ui):
        self.ui = ui
        self.canvas5 = FigureCanvas.__init__(self, self.fig)
        self.axes5 = self.fig.add_subplot(111)
        self.axes5.set_title("Tsys vs Time", fontsize=8)
        self.axes5.set_ylabel ('Tsys(K)', fontsize = 'smaller')
        self.axes5.set_xlabel ('Time (sec)', fontsize = 'smaller')
        self.axes5.tick_params(axis='both', which='major', labelsize=8)
        
    def spectrum_skymap(self, ui):
        """
        """
        self.logger.debug("spectrum_skymap: entered")
        self.ui = ui
        self.canvas8 = FigureCanvas.__init__(self, self.fig)
        self.curvelinear_test2(self.fig)

    def curvelinear_test2(self, fig):
        """
        polar projection, but in a rectangular box.
        """
        self.logger.debug("curvelinear_test2: entered")
        self.axes8 = self.fig.add_subplot(111)
        self.axes8.set_xlim(0, 360)
        self.axes8.set_ylim(0, 90)
        self.axes8.grid(True)

    def spectrum_source(self, ui):
        self.ui = ui
        self.canvas7 = FigureCanvas.__init__(self, self.fig)
        self.axes7 = self.fig.add_subplot(111, projection="polar")
        self.axes7.set_theta_direction(-1)
        self.axes7.set_theta_zero_location('N')
        self.axes7.invert_yaxis()
        self.axes7.set_thetagrids(numpy.arange(0, 360, 20))
        self.axes7.grid(color='grey', linestyle='--', linewidth=0.5)
        self.axes7.set_title("Antenna Az-El Plot", fontsize=8)

    def spectrum_minical(self, ui):
        self.ui = ui
        self.canvas14 = FigureCanvas.__init__(self, self.fig)
        self.axes14 = self.fig.add_subplot(221)
        self.axes14_2 = self.fig.add_subplot(222)
        self.axes14_3 = self.fig.add_subplot(223)
        self.axes14_4 = self.fig.add_subplot(224)
        self.axes14.set_xlabel("Power (W)")
        self.axes14.set_ylabel("Temperature (K)")
        self.axes14.legend(loc='lower right')  

    def spectrum_yfactor(self, ui):
        self.ui = ui
        self.canvas15 = FigureCanvas.__init__(self, self.fig)
        self.axes15 = self.fig.add_subplot(111)

    def spectrum_SRsource(self, ui):
        self.ui = ui
        self.canvas4 = FigureCanvas.__init__(self, self.fig)
        self.axes4 = self.fig.add_subplot(111, projection="polar", axisbg='#d5de9c')
        self.axes4.grid(color='grey', linestyle='--', linewidth=0.5)
        self.axes4.set_title("Subreflector-Source", fontsize=8)
        self.axes4.set_theta_zero_location('N')
        self.axes4.invert_yaxis()
        self.axes4.set_theta_direction(-1)

    def spectrum_bore(self, ui):
        self.ui = ui
        self.canvas6 = FigureCanvas.__init__(self, self.fig)
        self.axes6 = self.fig.add_subplot(111)
        self.axes6.grid(color='grey', linestyle='--', linewidth=0.5)
        self.axes6.set_title("Boresight", fontsize=8)
        
    def spectrum_ElTime(self, ui):
        """
        elevation vs time
        """
        self.ui = ui
        self.canvas9 = FigureCanvas.__init__(self, self.fig)
        self.axes9 = self.fig.add_subplot(111)
        self.axes9.grid(color='grey', linestyle='--', linewidth=0.5)
        self.axes9.set_title("Elevation-Time", fontsize=8)
        self.axes9.tick_params(axis='both', which='major', labelsize=8)

    def spectrum_Aztime(self, ui):
        """
        azimuth vs time
        """
        self.ui = ui
        self.canvas10 = FigureCanvas.__init__(self, self.fig)
        self.axes10 = self.fig.add_subplot(111)
        self.axes10.grid(color='grey', linestyle='--', linewidth=0.5)
        self.axes10.set_title("Azimuth-Time", fontsize=8)
        self.axes10.tick_params(axis='both', which='major', labelsize=8)

    def tipping_plot(self, ui):
        self.ui = ui
        self.canvas16 = FigureCanvas.__init__(self, self.fig)
        self.axes16 = self.fig.add_subplot(111)
        self.axes16.grid(color='grey', linestyle='--', linewidth=0.5)
        self.axes16.set_title("Tsys vs Elevation", fontsize=8)

    def beam_mapping_plot(self, ui):
        self.ui = ui
        self.canvas17 = FigureCanvas.__init__(self, self.fig)
        self.axes17 = self.fig.add_subplot(111, projection="polar")
        self.axes17.grid(color='grey', linestyle='--', linewidth=0.5)
        self.axes17.set_title("Beam Scan Plot", fontsize=8)
        self.axes17.set_theta_zero_location('N')
        self.axes17.invert_yaxis()
        self.axes17.set_theta_direction(-1)

class PlotDef(ThreadInit):
    """
    class to define all canvases to be used in the following RoachMPL classes::
      
      canvas1 child of ui.ROACH1mpl
      canvas3   ''  '' ui.PROCESSmpl
      canvas5   ''  '' ui.tsys_widget
      canvas6   ''  '' ui.bore_mpl
      canvas7   ''  '' ui.source_mpl
      canvas8   ''  '' ui.skymap_mpl
      canvas9   ''  '' ui.eltime
      canvas10  ''  '' ui.aztime
      canvas14  ''  '' ui.minical_mpl
      canvas16  ''  '' ui.tipping_mpl
      canvas17  ''  '' ui.beammap_mpl
      
    Notes
    =====
    The code is almost the same for most of these. Might be simpler to have one
    method with the parent as an argument.  Unless, of course, the methods need
    to be argument-free.
    
    Why are these "connectX" calls not part of the UI definition? For now they
    are in the Observatory_GUI class.
    
    The RoachMPL class has many methods that are specific to specific classes
    """
    def __init__(self, ui):
        mylogger = logging.getLogger(logger.name+".PlotDef")
        mylogger.debug("__init__: entered")
        ThreadInit.__init__(self, ui)
        
        self.logger = mylogger
        self.logger.debug("__init__: initializing")
        self.x_data =        numpy.zeros(32768, dtype=numpy.float64)
        self.logger.debug("__init__: created x_data")
        self.x_data_scaled = numpy.zeros(32768, dtype=numpy.float64) 
        self.logger.debug("__init__: created x_data_scaled")
        self.y_data =        numpy.zeros(32768, dtype=numpy.float64)
        self.logger.debug("__init__: created y_data")
        self.y_data_scaled = numpy.zeros(32768, dtype=numpy.float64)
        self.logger.debug("__init__: created y_data_scaled")
        self.logger.debug("__init__: finished")
        
    #instantiate a matplotlib widget for ROACH Spectrum Plotter
    def mpl_connect1(self):
        """
        initialise Matplotlib widget for canvas1&2- spectrometers
        """
        self.logger.debug("connecting canvas 1, 2: ROACHs")
        self.ROACH1mpl = self.ui.ROACH1mpl
        self.canvas1 = RoachMPL(self.ROACH1mpl)
        self.canvas1.spectrum_roach(self.ui)
        # create a vertical box layout widget
        self.vbl1 = QtWidgets.QVBoxLayout(self.ROACH1mpl)
        # instantiate the navigation toolbar
        self.ntb1 = NavigationToolbar(self.canvas1, self.ROACH1mpl)
        # pack these widget into the vertical box
        self.vbl1.addWidget(self.canvas1)
        self.vbl1.addWidget(self.ntb1)
        #mpl connect for mouse movements canvas 1
        #self.cid1 = self.canvas1.mpl_connect('button_press_event', self.onclick)
        #self.cid2 = self.canvas1.mpl_connect('scroll_event', self.scroll)

    #instantiate a matplotlib widget for Analytical Plotter
    def mpl_connect2(self):
        """initialise Matplotlib widget for canvas3"""
#        print "connecting canvas 3: Analytical"
        self.PROCESSmpl = self.ui.PROCESSmpl
        self.canvas3 = RoachMPL(self.PROCESSmpl)
        self.canvas3.spectrum_roach(self.ui)
        self.vbl3 = QtWidgets.QVBoxLayout(self.PROCESSmpl)
        # instantiate the navigation toolbar
        self.ntb3 = NavigationToolbar(self.canvas3, self.PROCESSmpl)
        # pack these widget into the vertical box
        self.vbl3.addWidget(self.canvas3)
        self.vbl3.addWidget(self.ntb3)
        self.qp = 0
        self.tdp = 0
        self.ftpp = 0
        self.load = 0
        self.play = 0
        #QtCore.QObject.connect(self.ui.PlotTypeCB, QtCore.SIGNAL("currentIndexChanged(int)"), self.data_emit3)

    def mpl_connect5(self):
        """initialise Matplotlib widget for canvas5: Tsys/PM"""
        self.mpltsys = self.ui.tsys_widget        
        self.canvas5 = RoachMPL(self.mpltsys)
        self.canvas5.spectrum_tsys(self.ui)
        self.vbl5 = QtWidgets.QVBoxLayout(self.mpltsys)
        self.vbl5.addWidget(self.canvas5)
        self.ntb5 = NavigationToolbar(self.canvas5, self.mpltsys)
        self.vbl5.addWidget(self.ntb5)
        self.logger.debug("mpl_connect5: done")
        
    def mpl_connect6(self):
        """initialise Matplotlib widget for canvas 6: Boresight"""
        self.bore_mpl = self.ui.bore_mpl
        self.canvas6 = RoachMPL(self.bore_mpl)
        self.canvas6.spectrum_bore(self.ui)
        self.vbl6 = QtWidgets.QVBoxLayout(self.bore_mpl)
        self.vbl6.addWidget(self.canvas6)
        self.ntb6 = NavigationToolbar(self.canvas6, self.bore_mpl)
        self.vbl6.addWidget(self.ntb6)
        
    def mpl_connect7(self):
        """initialise Matplotlib widget for canvas7"""
#        print "connecting canvas 7: Az-Source"
        self.source_mpl = self.ui.source_mpl
        self.canvas7 = RoachMPL(self.source_mpl)
        self.canvas7.spectrum_source(self.ui)
        self.vbl7 = QtWidgets.QVBoxLayout(self.source_mpl)
        self.vbl7.addWidget(self.canvas7)
        self.ntb7 = NavigationToolbar(self.canvas7, self.source_mpl)
        self.vbl7.addWidget(self.ntb7)
        
    def mpl_connect13(self):
        """initialise Matplotlib widget for canvas13- source tracking, azimuth vs time """
        self.source_mpl = self.ui.source_mpl
        self.canvas7 = RoachMPL(self.source_mpl)
        self.canvas7.spectrum_source(self.ui)
        self.vbl7 = QtWidgets.QVBoxLayout(self.source_mpl)
        self.vbl7.addWidget(self.canvas7)
        self.ntb7 = NavigationToolbar(self.canvas7, self.source_mpl)
        self.vbl7.addWidget(self.ntb7)

    def mpl_connect8(self):
        """
        initialise Matplotlib widget for canvas8- sky map/catalogues
        """
        self.logger.debug("mpl_connect8: Skymap")
        self.skymap_mpl = self.ui.skymap_mpl
        self.canvas8 = RoachMPL(self.skymap_mpl)
        self.canvas8.spectrum_skymap(self.ui)

        self.vbl8 = QtWidgets.QVBoxLayout(self.skymap_mpl)
        # instantiate the navigation toolbar
        self.ntb8 = NavigationToolbar(self.canvas8, self.skymap_mpl)
        # pack these widget into the vertical box
        self.vbl8.addWidget(self.canvas8)
        self.vbl8.addWidget(self.ntb8)
        self.logger.debug("mpl_connect8: done")

    def mpl_connect9(self):
        """
        initialise Matplotlib widget for canvas9
          source tracking, elevation vs time 
        """
        self.eltime = self.ui.EltimeSource        
        self.canvas9 = RoachMPL(self.eltime)
        self.canvas9.spectrum_ElTime(self.ui)
        self.vbl9 = QtWidgets.QVBoxLayout(self.eltime)
        self.vbl9.addWidget(self.canvas9)
        self.ntb9 = NavigationToolbar(self.canvas9, self.eltime)
        self.vbl9.addWidget(self.ntb9)
        self.logger.debug("mpl_connect9: done")

    def mpl_connect10(self):
        """initialise Matplotlib widget for canvas10- Antenna Az-El Plot"""
        self.aztime = self.ui.EltimeSource_3        
        self.canvas10 = RoachMPL(self.aztime)
        self.canvas10.spectrum_Aztime(self.ui)
        self.vbl10 = QtWidgets.QVBoxLayout(self.aztime)
        self.vbl10.addWidget(self.canvas10)
        self.ntb10 = NavigationToolbar(self.canvas10, self.aztime)
        self.vbl10.addWidget(self.ntb10)
        self.logger.debug("mpl_connect10: done")
 
    def mpl_connect14(self):
        """initialise Matplotlib widget for canvas14- minical"""
#        print "connecting canvas 7: Az-Source"
        self.minical_mpl = self.ui.minical_mpl
        self.canvas14 = RoachMPL(self.minical_mpl)
        self.canvas14.spectrum_minical(self.ui)
        self.vbl14 = QtWidgets.QVBoxLayout(self.minical_mpl)
        self.vbl14.addWidget(self.canvas14)
        self.ntb14 = NavigationToolbar(self.canvas14, self.minical_mpl)
        self.vbl14.addWidget(self.ntb14)

    def mpl_connect16(self):
        """initialise Matplotlib widget for canvas7"""
#        print "connecting canvas 7: Az-Source"
        self.tipping_mpl = self.ui.tipping_mpl
        self.canvas16 = RoachMPL(self.tipping_mpl)
        self.canvas16.tipping_plot(self.ui)
        self.vbl16 = QtWidgets.QVBoxLayout(self.tipping_mpl)
        self.vbl16.addWidget(self.canvas16)
        self.ntb16 = NavigationToolbar(self.canvas16, self.tipping_mpl)
        self.vbl16.addWidget(self.ntb16)

    def mpl_connect17(self):
        """initialise Matplotlib widget for canvas7"""
#        print "connecting canvas 7: Az-Source"
        self.beammap_mpl = self.ui.beammap_mpl
        self.canvas17 = RoachMPL(self.beammap_mpl)
        self.canvas17.beam_mapping_plot(self.ui)
        self.vbl17 = QtWidgets.QVBoxLayout(self.beammap_mpl)
        self.vbl17.addWidget(self.canvas17)
#        self.ntb17 = NavigationToolbar(self.canvas17, self.beammap_mpl)
#        self.vbl17.addWidget(self.ntb17)

class Canvas3Plots(PlotDef):
    """
    Collects and plots historical files for replay
    """
    def __init__(self, ui):
        PlotDef.__init__(self, ui)
        self.mpl_connect2()
        #self.data_emit3()
        self.Adata = numpy.zeros(32768, dtype=numpy.float64)
        self.Tdata = numpy.zeros(32768, dtype=numpy.float64)

    def run(self):
        """Run wither the Quotient Plots, TimeDomainPlots or History Plots"""
        if self.ui.PlotTypeCB.currentText() == "QuotientPlots":
            self.plot_analysis_plot()
        elif self.ui.PlotTypeCB.currentText() == "TimeDomainPlots":
            self.plot_timedomain_plot()
        else:
            self.datafn = str(self.ui.file_selected.text())
            self.select_history_plot()

    def select_history_plot(self):
        """Select files for plotting historical data"""
        try:
            chn1_dataspectraf = h5py.File(self.datafn, 'r')
        except:
            print("No datafiles loaded")
            pass
        while True:
            #Read Data from the file
            historic_dataI = chn1_dataspectraf['spectraCh1']
            print("Restarting Plotting")
            #historic_dataQ = chn1_dataspectraf['spectraCh2']
            for n in range (0, historic_dataI.shape[0]):
                if self.ui.play.isChecked():
                    fps = self.ui.fps.value()
                    time.sleep(1/fps)
                    #print max(historic_dataI[n]), min(historic_dataI[n])
                    count = self.canvas3.axes1.annotate(str(n), xy=(50, 50),
                              textcoords='offset points', va='top', ha='center')
                    self.canvas3.line1.set_ydata(historic_dataI[n])
                    self.canvas3.axes1.set_ylim(0, max_limit)
                    self.canvas3.update()
                    self.canvas3.draw()
                    self.canvas3.axes1.texts.remove(count)
                else:
                    break;
            break;
        #self.canvas3.axes1.clear()
        self.destroy()
                #yield True

    def sourceAdata(self, Adata):
        """Start thread when called upon"""
        self.history_flg = 0
        #print "Quotient values are", processed_data[1]
        self.Adata = Adata
        try:
            self.start()
        except ():
            self.destroy()
    
    def sourceTdata(self, timestamp, Tdata):
        """Start thread when called upon"""
        self.history_flg = 0
        #print "Quotient values are", processed_data[1]
        self.Tdata = Tdata
        self.timestamp = timestamp
        try:
            self.start()
        except ():
            self.destroy()

    def plot_timedomain_plot(self):
        """
        Plot time domain data from start to end channels
        """
        #self.canvas3.axes1.set_ylim(-1,1)
        self.start_chn = self.ui.st_chn.value()
        self.end_chn = self.ui.end_chn.value()
        self.scan_no = self.ui.scan_no.value()
        self.canvas3.axes1.set_xlabel ('Time (scans)', fontsize = 'smaller')
        self.canvas3.axes1.set_ylabel ('Arbitrary Power', fontsize = 'smaller')
        print(self.timestamp[self.start_chn:self.end_chn])
        print(self.Tdata[self.start_chn:self.end_chn])
        self.canvas3.line1.set_xdata(self.timestamp[self.start_chn:self.end_chn])
        self.canvas3.line1.set_ydata(self.Tdata[self.start_chn:self.end_chn])
        self.canvas3.update()

    def plot_analysis_plot(self):
        self.canvas3.axes1.set_ylim(-1,1)
        self.canvas3.line1.set_ydata(self.Adata)
        self.canvas3.update()

    def peak_search(self):
        """TODO: Include peak search functionality"""
        pass

    def destroy(self):
        if self.isRunning():
            self.abort = True
            #sys.stdout.flush()
            #self.canvas3.
            #self.mutex.lock()
            #self.cond.wakeOne()
