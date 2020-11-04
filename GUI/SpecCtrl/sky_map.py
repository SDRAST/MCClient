#TODO-
# to clean up this code; perform unit test.
import ephem
import datetime
import logging

from matplotlib import rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.transforms import offset_copy
import numpy

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from Plotter import PlotDef
from Radio_Astronomy.bands import band_to_frequency
from Radio_Astronomy.radio_flux import get_planet_flux

rad2deg= 180/numpy.pi
rad2hr = 13/numpy.pi
"""
from matplotlib.projections import PolarAxes, register_projection
from matplotlib.transforms import Affine2D, Bbox, IdentityTransform
"""
debug = 0
logger = logging.getLogger(__name__)
"""
import numpy as np
import  mpl_toolkits.axisartist.angle_helper as angle_helper
from matplotlib.projections import PolarAxes, HammerAxes, MollweideAxes, AitoffAxes, LambertAxes
from matplotlib.transforms import Affine2D
from mpl_toolkits.axisartist import SubplotHost
from mpl_toolkits.axisartist import GridHelperCurveLinear
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
"""
#import Astronomy.Ephem as Aeph
"""
Observatory info
"""
cdscc = ephem.Observer()
cdscc.long, cdscc.lat, cdscc.elevation = '148.980057138', '-35.403983527', 688.867

#No refraction correction
cdscc.pressure = 0
cdscc.epoch = ephem.J2000
cdscc.date = datetime.datetime.utcnow()
marker = {}
sun = ephem.Sun();          marker[sun] = "$\u2609$"
mercury = ephem.Mercury() ; marker[mercury] = "$\u263F$"
venus = ephem.Venus();      marker[venus] = "$\u2640$"
moon = ephem.Moon();        marker[moon] = "$\u263D$"
mars = ephem.Mars();        marker[mars] = "$\u2642$"
jove = ephem.Jupiter();     marker[jove] = "$\u2609$"


#class PlotSkymap(PlotDef):
class PlotSkymap(object):
    """
    class for source selection sky map
    """
    # signals when categories are updated
    masers = pyqtSignal(bool)
    calibrators = pyqtSignal(bool)
    def __init__(self, main, ui, server, band):        # removed logfile
        """
        initialize the sky map
        
        
        """
        mylogger = logging.getLogger(logger.name+".PlotSkymap")
        mylogger.debug("__init__: entered")
        self.logger = mylogger
        self.main = main
        self.ui = ui
        self.server = server
        self.band = band
        self.freq = band_to_frequency(self.band)
        # default (placeholder) annotation
        self.annotation = 'xxx'
        
        self.timer5= QtCore.QTimer()
        self.timer5.start(1000)
        
        self.plot_definitions() # initialize sky map
        
        # since we don't plan on removing these mouse event connections we don't
        # need to save their ISm
        self.ui.skymap_canvas.mpl_connect('pick_event', self.source_pick)
        self.ui.skymap_canvas.mpl_connect('button_press_event', self.onclick)
        
        #self.ui.cb_srcs.clicked.connect(self.current_pos)
        #self.ui.cb_cal.clicked.connect(self.current_pos)
        #self.ui.cb_km.clicked.connect(self.current_pos)
        self.ui.cb_tel.clicked.connect(self.current_pos) # antenna
        self.ui.cb_pl.clicked.connect(self.current_pos) # planets
        self.ui.cb_moon.clicked.connect(self.current_pos) # moon
        self.ui.cb_sun.clicked.connect(self.current_pos) # sun
        #self.ui.cb_gp.clicked.connect(self.current_pos)

        self.ui.load_catalogue.clicked.connect(self.load_catalogue)
        self.ui.find_nearest.clicked.connect(self.find_nearest_bore)

        self.timer5.timeout.connect(self.__timerfunction)
                
        self.logger.debug("__init__: finished")

    def __call__(self, mouse_event):
        ax = mouse_event.inaxes
        if not ax:
            return
        line = ax.get_lines()[0]
        contained, infos = line.contains(mouse_event)
        if not contained:                                # eventually exited
            for annotation in list(self.annotations.values()):
                annotation.set_visible(False)
        else:
            xdata, ydata = line.get_data()
            ind = infos['ind'][0]
            annotation = self.annotations[xdata[ind], ydata[ind]]
            if not annotation.get_visible():             # is entered
                annotation.set_visible(True)
        ax.figure.canvas.update()

    def plot_definitions(self):
        """
        initialize az/el plot
        """
        self.ui.skymap_axes.grid(True)
        # draw elevation limit lines in appropriate units
        low_limit_x_axis_plt = numpy.arange(0, 360, 1)
          
        low_limit_y_axis_plt = numpy.zeros(360)
        high_limit_y_axis_plt = numpy.zeros(360)
        low_limit_y_axis_plt[:] = 6
        high_limit_y_axis_plt[:] = 80
        self.ui.skymap_axes.set_xlabel('AZ (deg)')
        self.ui.skymap_axes.set_ylabel('EL (deg)')
        self.ui.skymap_axes.set_xlim(0,360)
        self.ui.skymap_axes.set_ylim(-1,91)
        self.ui.skymap_axes.plot(low_limit_x_axis_plt, low_limit_y_axis_plt,
                                color='red', ls ='--')
        self.ui.skymap_axes.plot(low_limit_x_axis_plt, high_limit_y_axis_plt,
                                color='red', ls ='--')
        self.ui.skymap_canvas.draw()

    def current_pos(self):
        """
        plot all the currently checked categories
        """
        self.plot_current()
        self.refresh_plot()
            
    def plot_current(self):
        """
        Notes
        =====
        why not put this code in ``current_pos``?
        
        Why ``QDateTime.currentDateTimeUtc`` instead of ``datetime.now``?
        
        ``source_dict`` values are lists of [ra, dec, az, alt].
        """
        #cdscc.date = datetime.datetime.utcnow()
        utc_now_qt = QtCore.QDateTime.currentDateTimeUtc()
        self.ui.dateTimeEdit.setDateTime(utc_now_qt)
        utc_now_py = utc_now_qt.toPyDateTime()
        # self.logger.debug("plot_current: called at %s", utc_now_py)

        self.ui.skymap_axes.cla() # clear plot
        self.source_dict = {}     # clear dict of all plotted sources
        plot_categories = []
        for category in self.main.categories:
          index = self.main.categories.index(category)
          if self.ui.checkDisplaySelect[index].isChecked():
            plot_categories.append(category)
          else:
            if category in plot_categories:
              plot_categories.remove(category)
        #self.logger.debug("plot_current: categories: %s", plot_categories)
        self.plot_Calcurrent(utc_now_py, categories=plot_categories)
        #if self.ui.cb_srcs.isChecked():
        #    self.plot_6dfcurrent(utc_now_py)
        #elif self.ui.cb_km.isChecked():
        #    self.plot_km(utc_now_py)
        if self.ui.cb_tel.isChecked():         # telescope
            self.calculate_telescope_pos()
        if self.ui.cb_sun.isChecked():         # sun
            self.calculate_sun(utc_now_py)
        if self.ui.cb_moon.isChecked():        # moon
            self.calculate_moon(utc_now_py)
        if self.ui.cb_pl.isChecked():          # planets
            self.calculate_planets(utc_now_py)
        self.plot_definitions()
        
    def calculate_telescope_pos(self):
        """
        plot the telescope direction
        """
        # plot the telescope position in Az-El
        tel_az = float(self.ui.az_mon.text())
        tel_el = float(self.ui.el_mon.text())
        #self.logger.debug("calculate_telescope_pos: el, az = %s, %s",
        #                  tel_el, tel_az)
        self.ui.skymap_axes.plot(tel_az, tel_el, "+", color="red",
                                 markersize=16)

    def calculate_sun(self, date):
        """
        plot the position of the Sun
        """
        cdscc.date = date
        sun.compute(cdscc)            
        #self.logger.debug("calculate_sun: el, az = %6.1f, %6.1f",
        #                  sun.az*rad2deg, sun.alt*rad2deg)
        self.ui.skymap_axes.plot(sun.az*rad2deg, sun.alt*rad2deg,
                                marker=marker[sun], color="yellow",
                                markersize=16, picker=5)
        # add to dict of all plotted sources
        self.source_dict[sun.name] = [sun.ra, sun.dec, sun.az, sun.alt]
        
    def calculate_moon(self, date):
        """
        plot the position of the moon
        """
        cdscc.date = date
        moon.compute(cdscc)            
        #self.logger.debug("calculate_moon: el, az = %6.1f, %6.1f",
        #                  moon.az*rad2deg, moon.alt*rad2deg)
        self.ui.skymap_axes.plot(moon.az*rad2deg, moon.alt*rad2deg,
                                marker=marker[moon], color="orange",
                                markersize=15, picker=5)
        # add to dict of all plotted sources
        self.source_dict[moon.name] = [moon.ra, moon.dec, moon.az, moon.alt]

    def calculate_planets(self, date):
        cdscc.date = date
        
        jove.compute(cdscc)
        flux = get_planet_flux('Jupiter', self.freq, datetime.datetime.now())
        self.ui.skymap_axes.plot(jove.az*rad2deg, jove.alt*rad2deg, 
                                marker=marker[jove], color="brown",
                                markersize=flux+3, picker=5)
        self.source_dict[jove.name] = [jove.ra, jove.dec, jove.az, jove.alt,
                                       flux, 0.0]
                                       
        mars.compute(cdscc)
        flux = get_planet_flux('Mars', self.freq, datetime.datetime.now())
        self.ui.skymap_axes.plot(mars.az*rad2deg, mars.alt*rad2deg,
                                marker=marker[mars], color="red",
                                markersize=flux+3, picker=5)
        self.source_dict[mars.name] = [mars.ra, mars.dec, mars.az, mars.alt,
                                       flux, 0.0
                                       ]
        venus.compute(cdscc)
        flux = get_planet_flux('Venus', self.freq, datetime.datetime.now())
        self.ui.skymap_axes.plot(venus.az*rad2deg, venus.alt*rad2deg,
                                marker=marker[venus], color="orange",
                                markersize=flux+3, picker=5)
        self.source_dict[venus.name] = [venus.ra, venus.dec, venus.az, venus.alt,
                                        flux, 0.0]
                                        
        #self.mercury.compute(cdscc)
        #self.saturn.compute(cdscc)
        #self.uranus.compute(cdscc)

    def plot_Calcurrent(self, utc_now_py, categories=None):
        """
        plot the calibrators
        
        A ``SerializableBody`` returned by ``CentralServer`` method ``get_sources()``
        initially has the following attributes: ``_ra``, ``_dec``, ``name``, 
        ``info``, and ``observer_info``.  After ``compute()`` has been called 
        it also has ``az`` and ``alt``, and other ``ephem.Body}`` attributes.
        """
        #self.plot_calibrators = True
        #self.calibrators.emit(self.plot_calibrators)
        #self.emit(QtCore.SIGNAL("calibrators"), self.plot_calibrators)
        cdscc.date = utc_now_py
        if categories:
          #self.logger.debug("plot_Calcurrent: requesting %s", categories)
          sources = self.main.get_sources_data(
                                self.main.project, filter_categories=categories)
        else:
          return
        #self.logger.debug("plot_Calcurrent: %d sources returned", len(sources))
        for item in sources:
          #self.logger.debug("plot_Calcurrent: processing %s", sources[item].info['key'])
          source = sources[item]
          source.compute(cdscc)
          if source.alt > 0:
            self.ui.skymap_axes.plot(source.az*rad2deg, source.alt*rad2deg,
                                   marker='o', color=source.info['fill'],
                                   markersize=source.info['r'],
                                   alpha=source.info['opacity'], picker=5)
            self.source_dict[source.name] = [source.ra, source.dec,
                                             source.az, source.alt,
                                             float(source.info['flux'][self.band]),
                                             source.info['velocity']]

    def source_pick(self, event1):
        """
        Right click- gets Info of the source
        Left click- selects source
        scroll- finds nearest source
        """
        # Merge dictinaries for whatever sources ticked in the GUI
        thisline = None
        thisline = event1.artist
#        thisline.update
#        if thisline is not None and not hasattr(event1, 'already_picked'):
        self.logger.debug("source_pick: this line: %s", thisline)
        #When Plotting in Az-El
        self.source_pick_az = thisline.get_xdata()[0]
        self.source_pick_alt = thisline.get_ydata()[0]
        #self.logger.debug("source_pick: az/el = %s/%s", 
        #                  self.source_pick_az, self.source_pick_alt)
        n = 0
        m = 0
        for key, value in list(self.source_dict.items()):
            #self.logger.debug("source_pick: matching az %s",
            #                  self.source_pick_az)
            #self.logger.debug("source_pick: ... az %s",
            #                  repr(ephem.hours(value[2])*rad2deg))
            if round(numpy.float64(self.source_pick_az), 6) == \
               round(numpy.float64(repr(ephem.hours(value[2])*rad2deg)), 6): 
                self.logger.debug("source_pick: match found for object %s", key)
                self.source_name = key
                self.source_info_ra = value[0]
                self.source_info_dec = value[1]
                self.source_info_az = value[2]
                self.source_info_alt = value[3]
                self.source_info_vsys = value[5]
            else:
                pass
            #n = n +1
        #m = m+1
        self.annotation = self.ui.skymap_axes.annotate(self.source_name,
                           xy = ((self.source_pick_az), (self.source_pick_alt)),
                           xytext = (-20, 20), textcoords = 'offset points',
                           ha = 'right', va = 'bottom',
                           bbox = dict(boxstyle = 'round,pad=0.5',
                           fc = 'yellow', alpha = 0.5),
                           arrowprops = dict(arrowstyle = '->',
                           connectionstyle = 'arc3,rad=0'))
        # by default, disable the annotation visibility
        self.annotation.set_visible(True)
        self.ui.skymap_canvas.draw()
        self.annotation.set_visible(False)

    def onclick(self, event):
        self.logger.debug("onclick: click detected")
        try:
            if event.button==1:
                self.logger.debug('onclick: left click- Source selected')
                self.ui.sourceInfo.clear()
                self.ui.sourceInfo.insertPlainText(self.source_name+"\n")
                self.ui.sourceInfo.insertPlainText("RA: "+str(self.source_info_ra)+"\n")
                self.ui.sourceInfo.insertPlainText("DEC: "+str(self.source_info_dec)+"\n")
                self.ui.sourceInfo.insertPlainText("Az: "+str(self.source_info_az)+"\n")
                self.ui.sourceInfo.insertPlainText("El: "+str(self.source_info_alt)+"\n")
                self.ui.sourceInfo.insertPlainText("Vsys: "+str(self.source_info_vsys)+"\n")

            elif event.button==3:
                self.logger.debug('onclick: right click- Source info presented')
                self.ui.sourceInfo.clear()
                self.ui.sourceInfo.insertPlainText(self.source_name_label+"\n")
                self.ui.sourceInfo.insertPlainText("RA: "+str(self.source_info_ra)+"\n")
                self.ui.sourceInfo.insertPlainText("DEC: "+str(self.source_info_dec)+"\n")
                self.ui.sourceInfo.insertPlainText("Az: "+str(self.source_info_az)+"\n")
                self.ui.sourceInfo.insertPlainText("El: "+str(self.source_info_alt)+"\n")
                self.ui.sourceInfo.insertPlainText("Vsys: "+str(self.source_info_vsys)+"\n")
            else:
                self.logger.warning("onclick: button not recognised")
        except:
            self.logger.error("onclick: error occured when getting source info")
            
    def refresh_plot(self):
        self.ui.skymap_canvas.update()
        self.ui.skymap_canvas.draw()
                
    def run(self):
        """
        Sources-
        Observer, Sun, Moon, Planets,
        TODO:
            Plot feed position on sky
        """
        self.plot_definitions()
        self.__timerfunction()

    def __timerfunction(self):
        """
        Azimuth and elevation are updated every second using timer5
        
        no longer needed because they now come from the server
        """
        cdscc.date = datetime.datetime.utcnow()
        #self.ui.label_LST.setText(str(cdscc.sidereal_time()))
        
        self.current_pos()

                                
#---------------------------------- salt --------------------------------------

    def get_6dfsource_info(self, cat_file):
        cat = open(cat_file, 'r')
        source_6df = {}
        n = 0
        for line in cat:
            li=line.strip()
            if not li.startswith("#"):
                source_info = line.rstrip().split()
                src_nm = source_info[0]
                src_ra_dec = source_info[1]
                src_dec_dec = source_info[2]
                src_ra = ephem.hours(src_ra_dec)
                src_dec = ephem.degrees(src_dec_dec)
                src_flux = 0
                src_velo = source_info[3]
                source_6df[src_nm] = ([src_ra, src_dec, src_flux, src_velo])
                n=n+1
        return source_6df

    def get_calibrator_info(self):
        cat_file = '/home/ops/workspace/current_workspace/ok_cals.list'
        cat = open(cat_file, 'r')
        source_cal = {}
        #self.source_name = {}
        n = 0
        for line in cat:
            li=line.strip()
            if not li.startswith("#"):
                source_cal_info = line.rstrip().split()
                try:
                    cal_src_nm = source_cal_info[0]
                    cal_src_ra = source_cal_info[1:4]
                    cal_src_dec = source_cal_info[4:7]
                    cal_src_K_flux = source_cal_info[-2]
                    cal_src_ra =  (':'.join(cal_src_ra))
                    cal_src_dec =  (':'.join(cal_src_dec))
                    src_velo = 0
                    source_cal[cal_src_nm] = ([cal_src_ra, cal_src_dec,
                                               cal_src_K_flux, src_velo])
                    n=n+1
                except:
                    pass
        return source_cal

    def get_masersource_info(self):
        cat_file = '/home/ops/workspace/current_workspace/sources/maser.txt'
        cat = open(cat_file, 'r')
        self.source = {}
        n = 0
        for line in cat:
            li=line.strip()
            if not li.startswith("#"):
                source_info = line.rstrip().split()
                src_nm = source_info[0]
                src_ra = source_info[-9:-6]
                src_dec = source_info[-6:-3]
                src_ra = ephem.hours((':'.join(src_ra)))
                src_dec = ephem.degrees((':'.join(src_dec)))
                src_flux = 0
                src_velo = source_info[-3]
                self.source[src_nm] = ([src_ra, src_dec, src_flux, src_velo])
                n=n+1
        return self.source

    def calculate_source_positions(self, source, date):
        """
        calculate the horizon coordinates for a source
        
        returns a dict with source info
        """
        cdscc.date = date
        source_dict = {}
        rc('grid', color='#316931', linewidth=1, linestyle='-')
        rc('xtick', labelsize=10)
        rc('ytick', labelsize=10)
        for key, value in source.items():
            #Compute the Az-Alt from RA-DEC for CDSCC
            source = ephem.FixedBody()
            source._ra = value[0]   #source_ra
            source._dec = value[1]  #source_dec
            source._epoch = ephem.J2000
            source_flux = value[2]
            source_velo = value[3]
            source.compute(cdscc)
            #Create a new 6df dictionary
            source_dict[key] = ([source.ra, source.dec, source.az, source.alt,
                                 source_flux, source_velo])
        return source_dict
            
    def plot_sources(self, n, source_dict, color, alpha):
        self.line8, = self.ui.skymap_canvas.plot(0,0)
        self.line9, = self.ui.skymap_canvas.plot(0,0)
        if n == 0:
            # Plot the calibrator sources
            for key, value in list(source_dict.items()):
                name = key
                ra = (value[0])
                dec = (value[1])
                az = (value[2])
                alt = (value[3])
                flux = (value[4])
                # TODO- Flux can be chosen for wither L, S, C, X, K, W;
                #  default K for TAMS
                self.line8, = self.ui.skymap_canvas.plot(az, alt, "o", color=color,
                                    picker=5, markersize = float(flux), alpha=1)
        else:
            # Plot the target sources
            for key, value in list(source_dict.items())[:n]:
                name = key
                ra = (value[0])
                dec = (value[1])
                az = (value[2])
                alt = (value[3])
                #Plot RA-DEC
                #???
                #Plot Az-El
                self.line9, = self.ui.skymap_canvas.plot(az, alt, "*", color=color,
                                          picker=5, markersize = 8, alpha=alpha)
        self.ui.skymap_canvas.legend([self.line8, self.line9],
                                  ["calibrators", "TAMS sources"],
                                  prop={'size':8})

    def load_catalogue(self):
        cdscc.date = datetime.datetime.utcnow()
        utc_now_qt = QtCore.QDateTime.currentDateTimeUtc()
        utc_now_py = utc_now_qt.toPyDateTime()
        new_cat = str(QtWidgets.QFileDialog.getOpenFileName(None,
                                                 'Select File', './', "*.list"))
        cat_file = new_cat
        cat = open(cat_file, 'r')
        source_cal = {}
        n = 0
        for line in cat:
            li=line.strip()
            if not li.startswith("#"):
                source_cal_info = line.rstrip().split()
                self.logger.debug("load_catalogue: source info: %s",
                                  source_cal_info)
                cal_src_nm = source_cal_info[0]
                cal_src_ra = source_cal_info[1]
                cal_src_dec = source_cal_info[2]
                cal_src_K_flux = 0
                cal_src_ra =  (':'.join(cal_src_ra))
                cal_src_dec =  (':'.join(cal_src_dec))
                cal_src_velo = 0
                source_cal[cal_src_nm] = ([cal_src_ra, cal_src_dec,
                                           cal_src_K_flux, cal_src_velo])
                n=n+1
        self.plot_sources(0, 
                         self.calculate_source_positions(source_cal, utc_now_py),
                          'blue', 1)
        self.source_dict = dict(list(self.calculate_source_positions(source_cal,
                                                           utc_now_py).items()))


    def plot_6dfcurrent(self, utc_now_py):
        """
        plot the sources in the catalogues
        """
        file1 = '/home/ops/workspace/current_workspace/sources/TargetList_Priority1.txt'
        file2 = '/home/ops/workspace/current_workspace/sources/PartialObs.txt'
        file3 = '/home/ops/workspace/current_workspace/sources/DoneObs.txt'
        file4 = '/home/ops/workspace/current_workspace/sources/TargetList_Priority4.txt'
        self.plot_6dfsrcs = True
        #self.emit(QtCore.SIGNAL("calibrators"), self.plot_6dfsrcs)
        self.calibrators.emit(self.plot_6dfsrcs)
        
        # plot each of the source catalogues
        self.plot_sources(400, self.calculate_source_positions(
                        self.get_6dfsource_info(file1), utc_now_py), 'green', 1)
        self.plot_sources(400, self.calculate_source_positions(
                        self.get_6dfsource_info(file2), utc_now_py), 'red', 0.5)
        self.plot_sources(400, self.calculate_source_positions(
                      self.get_6dfsource_info(file3), utc_now_py), 'black', 0.3)
        self.plot_sources(400, self.calculate_source_positions(
                     self.get_6dfsource_info(file4), utc_now_py), 'orange', 0.2)

        self.source_dict1 = dict(list(self.calculate_source_positions(
                           self.get_6dfsource_info(file1), utc_now_py).items()))
        self.source_dict2 = dict(list(self.calculate_source_positions(
                           self.get_6dfsource_info(file2), utc_now_py).items()))
        self.source_dict3 = dict(list(self.calculate_source_positions(
                           self.get_6dfsource_info(file3), utc_now_py).items()))
        self.source_dict4 = dict(list(self.calculate_source_positions(
                           self.get_6dfsource_info(file4), utc_now_py).items()))
        self.source_dict = dict(list(self.source_dict1.items())
                              + list(self.source_dict2.items())
                              + list(self.source_dict3.items())
                              + list(self.source_dict4.items()))
        
    def plot_km(self, utc_now_py):
        """
        plot known masers
        """
        self.plot_masers = True
#            self.ui.skymap_canvas.cla()
        self.masers.emit(self.plot_masers)
        self.plot_sources(100, self.calculate_source_positions(
                          self.get_masersource_info(), utc_now_py), 'yellow', 1)
        self.source_dict = dict(list(self.calculate_source_positions(
                              self.get_masersource_info(), utc_now_py).items()))

    def test(self, event1):
        if debug: print("Debug1")

    #Scroll refreshes the plot...
    #  to be used for peak search function(not implemented)
    def scroll(self, event):
        """Record mouse scrolling...to be used for ??? function(not implemented)"""
        self.refresh = True
        try:
            self.refresh_plot()
        except: pass

    def fwd_time(self):
        if debug: print("Method: Sources being forwarded in time")
        pass

    def find_nearest(self):
        self.logger.debug(
                        "find_nearest: Method: Find nearest object on the plot;"
                             " forward on key press N go back with key press B")
        #Find nearest object to the telescope on the plot
        #Not implemented
        pass


    def find_nearest_bore(self):
        """
        get current viewport dimensions in normalised device coordinates.
        This is used to re-normalise the data so that tne nearest point
        as viewed on the screen is selected.
        Method::
        
          1. Pick a source.
          2. Get source coordinates in RA-DEC.
          3. Define max angular distance of 15 degrees to search the calibrators
             within.
          4. Search the calibrators within max angular distance.
          5. If no candidates found step the angular distance by 15 degrees and
             search again.
          6. If unsuitable candidates are found, step the angular distance by
             15 degrees on key press N, go back to the previous source 
             on key press B.

        """
        self.logger.debug("find_nearest_bore: Method: Find nearest boresight on"
                   " the plot; forward on key press C go back with key press V")
        import math
        nearest_bs = []
        x1 = self.source_pick_az #source RA
        y1 = self.source_pick_alt #source DEC
        if debug: print(x1, y1)
        angular_incrx = numpy.deg2rad(360./1000.)
        angular_incry = numpy.deg2rad(90./1000.)

        n = 0
        m = 0
        xmax = x1
        ymax = y1 
        xmin = x1
        ymin = y1
        
        while(True):
          if debug: print(n, xmin, xmax)
          for key, value in list(self.source_dict.items()):
              if  (xmin < value[2] < xmax) and  (ymin < value[3] < ymax):
                  x2 = round(numpy.float64(repr(ephem.hours(value[2]))), 6)
                  y2 = round(numpy.float64(repr(ephem.degrees(value[3]))), 6)
                  if key == self.source_name:
                    if debug: print('Debug1')
                    continue
                  else:
                    if debug: print('nearest boresight found %s, within %i iterations'%(key, n))
                    if debug: print(len(nearest_bs))
                    self.annotation = self.ui.skymap_axes.annotate(key,
                              xy = ((x2), (y2)),
                              xytext = (-20, 20),
                              textcoords = 'offset points',
                              ha = 'right', va = 'bottom',
                              bbox = dict(boxstyle = 'round,pad=0.5',
                                          fc = 'pink', alpha = 0.5),
                              arrowprops = dict(arrowstyle = '->',
                                                connectionstyle = 'arc3,rad=0'))
                    # by default, disable the annotation visibility
                    self.annotation.set_visible(True)
                    self.canvas8.draw()
                    self.annotation.set_visible(False)
                    return
              else:
                pass
          xmax = xmax + angular_incrx
          ymax = ymax + angular_incry
          xmin = xmin - angular_incrx
          ymin = ymin - angular_incry
          n = n +1

    def offset(self,ax, x, y):
        return offset_copy(ax.transData, x=x, y=y, units='dots')

    def distance(self, x1, x2, y1, y2):
        """
        return the distance between two points
        """
        return

