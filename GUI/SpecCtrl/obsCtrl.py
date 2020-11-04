"""
obsCtrl - a client-based version of ObervatoryCtrl

Notes
=====
If we want to take advantage of the CentralServer async methods then we need to
create a Pyro server class to handle the callbacks.
"""
import datetime
import ephem
import logging
import math
from matplotlib.dates import date2num, datestr2num
import numpy as NP
from PyQt5 import QtCore, QtGui, QtWidgets
import Pyro5
import Pyro5.api
import serpent
import sys

logger = logging.getLogger(__name__)

mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

import Astronomy as A
from Radio_Astronomy.bands import band_to_frequency
from Astronomy.Ephem.serializable_body import SerializableBody
SerializableBody.register_with_Pyro5()

from support.asyncio.pyro import async_method, CallbackReceiver
from support.pyro.async_callback import async_callback

from roach_control import Ui_Observatory
from sky_map import PlotSkymap

class CallbackHandler(CallbackReceiver):
  """
  subclass to provide mofified `finished()`
  """
  def __init__(self, parent):
    """
    initialize superclass
    """
    CallbackReceiver.__init__(self, parent=parent)
    self.parent = parent
    
  @Pyro5.api.expose
  @Pyro5.api.callback
  def finished(self, who, msg):
    """
    Method used by the remote server to return the data
    
    Parent must have a thread waiting to do queue.get()
    
    Because this runs in the server namespace, no logging is possible.
    """
    self.logger.debug('finished: got result from %s', who)
    if who == "get_tsys":
      self.parent.handle_tsys(msg)
    if who == "tsys_calibration":
      self.parent.handle_minical(msg)

obsmodes = ["TLPW", "BMSW", "PSSW", "BPSW"]

class observatoryGUI(QtWidgets.QMainWindow):
  """
  """
  def __init__(self, parent=None):
    QtWidgets.QMainWindow.__init__(self, parent)
    self.logger = logging.getLogger(logger.name+".observatoryGUI")
    self.name = "Observatory"
    self.setWindowTitle("Radio Observatory")
    
    # callback handler
    self.cb_receiver = CallbackHandler(parent=self)
    
    self.connect_to_server()
    
    # get current state of the server; this calls a normal method
    self.info = self.centralServer.report_info()
    self.logger.debug("__init__: from 'report_info' got %d info items: %s",
                      len(self.info), self.info.keys())
    self.project = self.info["project"]["name"]
    self.activity = self.centralServer.get_current_activity()
    self.context = self.centralServer.get_current_context()
    
    self.sources = self.get_sources_data() # not asynchronously this time
    self.logger.debug("__init__: sources data requested")
    
    # the following cannot be async since the `get_ordered` and `get_styles`
    #   depend on `get_sources_data` being completed.
    # get source categories for sky map
    self.categories = self.centralServer.get_ordered()
    self.logger.debug("__init__: ordered: %s", self.categories)
    self.styles = self.centralServer.get_styles()
    self.logger.debug("__init__: styles: %s", self.styles)
    
    self.ui = Ui_Observatory()
    self.ui.setupUi(self)
    self.band = 'K'
    self.freq = band_to_frequency(self.band)
    self.mode = self.get_mode()
    self.__connect()
    
    self.PM_timer = QtCore.QTimer()
    self.ant_timer = QtCore.QTimer()
    self.time_timer = QtCore.QTimer()
    self.PM_timer.start(1000)
    self.ant_timer.start(10000)
    self.time_timer.start(1000)
    
    self.ui.projectText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", self.project, None))
    self.ui.activityText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", self.activity, None))
    self.ui.contextText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", self.context, None))
    
    # update displayed source info
    self.source = self.info['point']['current_source']
    self.logger.debug("__init__: source: %s", self.source.__dict__)
    self.ui.source_name.setText(QtWidgets.QApplication.translate("Observatory",
                                                        self.source.name, None))
    ra = self.info['point']['current_source']._ra     # radians
    dec = self.info['point']['current_source']._dec   # radians
    rastr, decstr = A.format_angles(ra*12/math.pi, dec*180/math.pi)
    self.ui.ra_sf.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", rastr, None))
    self.ui.dec_sf.setText(QtWidgets.QApplication.translate(
                                                   "Observatory", decstr, None))
    vel = self.info['point']['current_source'].info['velocity']
    self.ui.vsys.setText(QtWidgets.QApplication.translate(
                                                    "Observatory", "0.0", None))
    
    # receiver state
    crossover = self.centralServer.get_crossover()
    crossover = False
    self.logger .debug("__init__: feed crossover is %s", crossover)
    if crossover:
      self.ui.checkFeeds.setChecked(True)
    else:
      self.ui.checkFeeds.setChecked(False)
      
    feed_states = self.centralServer.get_feed_states()
    feed_states =[False, False]
    self.logger .debug("__init__: feeds in load is %s", feed_states)
    for num in [1,2]:
      self.ui.SwitchSkyLoad[num].setCurrentIndex(feed_states[num-1])
    
    atten = {}
    for num in [1,2,3,4]:
      atten[num] = self.centralServer.get_atten(num)
      self.ui.atten[num].textFromValue(atten[num])
    self.logger.debug("__init__: attenuations: %s", atten)  
      
    polarizers = self.centralServer.get_polarizer_states()
    self.logger.debug("__init__:polarizers: %s", polarizers)
    for num in [1,2]:
      self.ui.SwitchLin[num].setCurrentIndex(polarizers[num-1])
      
    self.get_frontend_temperatures()
    
    # Tsys plot initialization
    self.date_list = []
    self.tsys_list = {1: [], 2: [], 3: [], 4:[]}
    
    # Catalogs / Sky map
    self.skymap = PlotSkymap(self, self.ui, self.centralServer, self.band)
    #sources = self.centralServer.get_sources_data("TAMS")
    #self.logger.debug("__init__: 10 from sources: %s", list(sources.keys())[:10])
    
    # Spectra plots
    response = self.centralServer.last_scan()
    self.logger.debug("__init__: last_scan response: %s", response.keys())
    data = NP.array(response['table'][1:])
    self.logger.debug("__init__: freqs: %s", data[:,0][:10])
    self.ui.axes1.plot(data[:,0], data[:,1])
    self.ui.axes2.plot(data[:,0], data[:,2])
    self.ui.axes3.plot(data[:,0], data[:,3])
    self.ui.axes4.plot(data[:,0], data[:,4])
        
    self.time_timer.timeout.connect(self.__lcdtimedUpdates)
    self.PM_timer.timeout.connect(self.__PMupdates)
    self.ant_timer.timeout.connect(self.__antennaUpdates)
    
    
    self.logger.debug("__init__: finished")
  
  def get_sources_data(self, when=None, filter_categories=[]):
    """
    normal or long running call to get sources
    
    Call this first with synchronous method to set up categories and styles
    """
    #self.logger.debug("get_sources_data: requesting %s", filter_categories)
    self.sources = self.centralServer.get_sources_data(
                          self.project, categories=filter_categories)
    #self.logger.debug("get_sources_data: got %d sources", len(self.sources))
    return self.sources
      
  def __connect(self):
    """
    Connections to signals/slots for GUI made here along with the timer 
    definition of 1 sec interval for GUI LCD updates.
    """
    self.ui.actionQuit.triggered.connect(self.exit_clean)

    # action for "Pick Source" button; add source to source list
    self.ui.pick_source.clicked.connect(self.source_select)
    # select new target from source list
    self.ui.source_que.itemDoubleClicked.connect(self.observe_source)
    # slew to new target
    self.ui.slew_to_source.clicked.connect(self.point)
    # start observing
    self.ui.start_obs.clicked.connect(self.start_observing)
    # observing modes
    for index in list(range(4)):
      self.ui.obs_pars.mode_select.button[index].stateChanged.connect(
                                                                  self.set_mode)
    # minical
    self.ui.minical.clicked.connect(self.minical)
    
  def connect_to_server(self, uri='PYRO:DSS-43@localhost:50015'):
    """
    """
    self.logger.info("connect_to_server: connecting to %s for control", str(uri))
    pyro_uri = Pyro5.api.URI(uri)
    self.logger.info("connect_to_server: control host is %s",
                     str(pyro_uri.host))
    try:
      self.centralServer = Pyro5.api.Proxy(pyro_uri)
      self.logger.info("__init__: connected to port %s for control",
                       str(pyro_uri.port))
    except Exception as details:
      self.logger.warning(
                   "connect_to_server: could not connect to given Pyro uri %s\n"
                          + "skipping WBDC control connection because\n"
                          + "%s", pyro_uri, str(details))
      self.centralServer = None
    self.logger.info("__init__: connected to %s for control", str(pyro_uri))
  
  #--------------------------timed actions ------------------------------------
  
  def __lcdtimedUpdates(self):
    """
    Timed updates every second
    """
    UT_txt, LST_txt = self.centralServer.server_time()
    
    nowutc = datetime.datetime.utcnow().timetuple()
    now = datetime.datetime.now()
    # Local time
    self.ui.lcd_time.display("%02d:%02d:%02d" % (now.hour, now.minute, now.second))
    # UTC time
    self.ui.lcd_time_3.display("%02d:%02d:%02d" % (nowutc.tm_hour, nowutc.tm_min,
                                             nowutc.tm_sec))
    self.ui.lcd_LST.display(LST_txt)
    # UTC day of year
    self.ui.lcd_doy.display("%s" % nowutc.tm_yday)
    # UT year
    self.ui.lcd_year.display("%s" % nowutc.tm_year)
    
    
  def __PMupdates(self):
    """
    Updates system temperatures
    """
    #pmtime, tsys, readings = 
    self.centralServer.get_tsys(timestamp=True,
                             callback=self.cb_receiver)
    
  def __antennaUpdates(self):
    """
    """
    # update antenna angles
    now = datetime.datetime.now()
    az_obs, el_obs, az_pred, el_pred, az_ofst, el_ofst = \
                                         self.centralServer.get_antenna_angles()
    self.logger.debug(
       "__antennaUpdates: antenna angles at %s are %s, %s, %s, %s, %s, %s",
       now, az_obs, el_obs, az_pred, el_pred, az_ofst, el_ofst)
                                         
    self.ui.az_sf.setText(QtWidgets.QApplication.translate(
                                       "Observatory", ("%5.1f" % az_obs), None))
    self.ui.el_sf.setText(QtWidgets.QApplication.translate(
                                       "Observatory", ("%5.1f" % el_obs), None))
    self.ui.az_mon.setText(QtWidgets.QApplication.translate(
                                      "Observatory", ("%5.1f" % az_pred), None))
    self.ui.el_mon.setText(QtWidgets.QApplication.translate(
                                      "Observatory", ("%5.1f" % el_pred), None))
    self.ui.el_offset.setText(QtWidgets.QApplication.translate(
                                      "Observatory", ("%6.3f" % el_ofst), None))
    self.ui.xel_offset.setText(QtWidgets.QApplication.translate(
                                      "Observatory", ("%6.3f" % az_ofst), None))
        
    # history plot for elevation
    self.ui.ElTime_axes.plot_date(date2num(now), el_obs, '.', color="black")
    self.ui.ElTime_fig.autofmt_xdate()
    self.ui.ElTime_canvas.draw()
    
    # history plot for azimuth
    self.ui.AzTime_axes.plot_date(date2num(now), az_obs, '.', color="black")
    self.ui.AzTime_fig.autofmt_xdate()
    self.ui.AzTime_canvas.draw()

    # plot az-el on Observations page
    #mark, = self.ui.source_axes.plot(az_obs, el_obs,
    #                         marker='o', color='red')
    self.ui.azel_mark.set_data(az_obs*NP.pi/180, el_obs)
    self.ui.source_canvas.draw()

    # --------------------- connect() slots (actions) -------------------------

  def source_select(self):
    #If source window contains a text, activate select source option and
    # when pressed select source for observation
    self.logger.debug("source_select: called")
    self.ui.source_name.setText(self.skymap.source_name)
    self.ui.ra_sf.setText(str(ephem.hours(self.skymap.source_info_ra)))
    self.ui.dec_sf.setText(str(ephem.degrees(self.skymap.source_info_dec)))
    self.selected_source_list = []
    try:
      self.selected_source_list.append(self.skymap.source_name)
      self.ui.source_que.addItems(self.selected_source_list)
    except:
      raise RuntimeWarning ("No source selected for observation!!!")
      pass

  def observe_source(self):
    """
    select this source from the source queue for observing
        
    This goes into the upper right box of the Observations page
    """
    selected_item =  self.ui.source_que.currentItem().text()
    self.logger.debug('observe_source: selected %s for observation',
                      selected_item)
    for key, value in self.skymap.source_dict.items():
      if key == selected_item:
        self.logger.debug("observe_source: %s has %s",
                          key, value)
        self.ui.obs_code.setText(str(key)) # ??????????????????
        self.ui.source_name.setText(str(key))
        self.ui.ra_sf.setText( str(ephem.hours(value[0])) )
        self.ui.dec_sf.setText(str(ephem.degrees(value[1])))
        self.ui.vsys.setText(str(value[5]))

  def point(self):
    """
    slew to new source
    """
    self.centralServer.point(self.ui.source_name.text())     
  
  def start_observing(self):
    """
    start scans
    """
    self.centralServer.start_spec_scans(self, n_scans=1, n_spectra=10, int_time=1,
                               log_n_avg=6, mid_chan=None)
  
  def set_mode(self, *args):
    """
    0 - unchecked
    1 - some of the children are checked
    2 - checked
    """
    self.logger.debug("set_mode: args = %s", args)
    for index in list(range(4)):
      if self.ui.obs_pars.mode_select.button[index].isChecked():
        self.mode = obsmodes[index]
        break
    self.logger.debug("set_mode: mode is %s", self.mode)
  
  def get_mode(self):
    self.mode = self.centralServer.get_obsmode()
    self.logger.debug("get_mode: mode is %s", self.mode)
    index = obsmodes.index(self.mode[4:])
    self.ui.obs_pars.mode_select.button[index].setChecked(True)
  
  def minical(self):
    self.centralServer.tsys_calibration(callback=self.cb_receiver)
    
  def get_frontend_temperatures(self):
    # physical temperatures
    fe_temps = self.centralServer.get_frontend_temps()
    self.logger.debug("handle_minical: front end temperatures: %s", fe_temps)
    self.ui.lcd70K.setProperty("value", fe_temps['70K'])
    self.ui.lcd12K.setProperty("value", fe_temps['12K'])
    self.ui.lcdLoad1.setProperty("value", fe_temps['load1'])
    self.ui.lcdLoad2.setProperty("value", fe_temps['load2'])
    
  # -------------------------- async callbacks -------------------------------
  #@async_callback
  #def handle_sources(self, *args):
  #  self.logger.debug("handle_sources: got %s", args)
  
  #@async_callback
  def handle_tsys(self, response):
    self.logger.debug("handle_tsys: got %s", response)
    pmtime, tsys, readings = response
    for num in [1,2,3,4]:
      self.ui.tsys[num].setText('%4.2f' % (tsys[num-1]))
      # I should really get the real PM readings from the server
      self.ui.labelPM[num].setText('%8.3e' % (readings[num-1]))
      self.tsys_list[num].append(tsys[num-1])
    self.date_list.append(datestr2num(pmtime))
    self.ui.tsys_axes.cla()
    for num in [1,2,3,4]:
      self.ui.tsys_axes.plot_date(self.date_list[-3600:], 
                                  self.tsys_list[num][-3600:], 
                                  "-", label="PM"+str(num))
    self.ui.tsys_axes.legend()
    self.ui.tsys_fig.autofmt_xdate()
    self.ui.tsys_canvas.draw()
  
  #@async_callback
  def handle_ordered(self, *args, **kwargs):
    self.logger.debug("handle_ordered: got: %s, %s", args, kwargs)
  
  def handle_minical(self, *args, **kwargs):
    self.logger.debug("handle_minical: got: %s, %s", args, kwargs)
    response = args[0]
    self.logger.debug("handle_minical: response: %s", response)
    if "status" in response:
      self.ui.status.setText("Status: %s" % response['status'])
    if "results" in response:
      results = response['results']
      targets = ['sky', 'sky+ND', 'load', 'load+ND']
      for PM_idx in list(range(4)):
        PM_num = PM_idx+1
        X = []; Y = []
        for data in targets:
          data_idx = targets.index(data)
          x = results[data][PM_idx]
          y = results['linear'][data_idx][PM_idx]
          X.append(x); Y.append(y)
          line, = self.ui.minical_axes[PM_num].plot(x, y, 'o', label=data)
        self.ui.minical_axes[PM_num].plot(X, Y, 'b-')
        self.ui.minical_axes[PM_num].legend()
      self.ui.minical_canvas.update()
      self.ui.minical_canvas.draw()
      
  # -----------------------------------
  
  def keyPressEvent(self, e):
    """Manage key events"""
    if e.key() == QtCore.Qt.Key_Escape:
      self.exit_clean()

  def exit_clean(self):
    """
    Stop all threads and exit cleanly
    """
    self.logger.debug("exit_clean: called")
    self.close()
    self.logger.debug("exit_clean: finished")                           
        
if __name__ == "__main__": 
  logging.basicConfig(level=logging.DEBUG)
  mylogger = logging.getLogger()
  mylogger.setLevel(logging.DEBUG)
  
  app = QtWidgets.QApplication(sys.argv)
  GUI = observatoryGUI()
  GUI.show()
  sys.exit(app.exec_())
