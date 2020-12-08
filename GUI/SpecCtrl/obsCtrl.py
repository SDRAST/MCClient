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
import time

logger = logging.getLogger(__name__)

mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

import Astronomy as A
from Radio_Astronomy.bands import band_to_frequency, frequency_to_band
from Astronomy.Ephem.serializable_body import SerializableBody
SerializableBody.register_with_Pyro5()
import DatesTimes as DT

from support.asyncio.pyro import async_method, CallbackReceiver
from support.lists import unique
#from support.pyro.async_callback import async_callback

from roach_control import Ui_Observatory
from sky_map import PlotSkymap

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
    #self.logger.debug('finished: got result from %s', who)
    if who == "get_tsys":
      self.parent.handle_tsys(msg)
    elif who == "tsys_calibration":
      self.parent.handle_minical(msg)
    elif who == "start_spec_scans":
      self.parent.handle_spectra(msg)

obsmodes = ["TLPW", "BMSW", "PSSW", "BPSW"]
obstypes = ["LINE", "CONT", "PULS"]

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
    self.band = 'K'
    self.freq = band_to_frequency(self.band)
    
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
    self.start_UI()
    self.ui.projectionInd.button[0].setChecked(True)
    self.logger.debug("__init__: finished")
  
  def start_UI(self, polar_sky=False):
    """
    start the display
    """
    self.ui.setupUi(self, polar_sky=polar_sky)
    self.get_mode()
    self.__connect()
    
    self.ui.projectText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", self.project, None))
    self.ui.activityText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", self.activity, None))
    self.ui.contextText.setText(QtWidgets.QApplication.translate(
                                 "Observatory", self.context, None))
    
    # start the timers
    self.PM_timer = QtCore.QTimer()
    self.ant_timer = QtCore.QTimer()
    self.time_timer = QtCore.QTimer()
    self.PM_timer.start(1000)
    self.ant_timer.start(10000)
    self.time_timer.start(1000)
    self.time_timer.timeout.connect(self.__lcdtimedUpdates)
    self.PM_timer.timeout.connect(self.__PMupdates)
    self.ant_timer.timeout.connect(self.__antennaUpdates)
    
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
           
    self.get_signals()
    self.get_weather()
    self.get_ADC_inputs()
    self.get_ADC_clock()
    self.get_ADC_temps()
    self.get_amb_temps()
    self.get_gains()
    self.get_firmware_pars()
  
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
    Actions for widgets with signals
    
    Connections to signals/slots for GUI made here.
    """
    # "Files, Quit"
    self.ui.actionQuit.triggered.connect(self.exit_clean)

    # "Pick Source" (add source to source list)
    self.ui.pick_source.clicked.connect(self.source_select)
    
    # select new target from source list
    self.ui.source_que.itemDoubleClicked.connect(self.observe_source)
    
    # slew to new target
    self.ui.slew_to_source.clicked.connect(self.point)
    
    # start observing
    self.ui.start_obs.clicked.connect(self.start_observing)
    
    # observing modes
    self.ui.obs_pars.mode_select.buttonGroup.buttonClicked.connect(
                                                                  self.set_mode)    
    # minical
    self.ui.minical.clicked.connect(self.minical)
    
    # scans combobox
    self.ui.obs_pars.numScans.value.valueChanged.connect(self.set_scans)
    
    # cycles
    self.ui.obs_pars.num_cycles.value.valueChanged.connect(self.set_cycles)
    
    # attenuators
    self.ui.set_atten.clicked.connect(self.set_atten)

    # Sources skymap projection
    self.ui.projectionInd.buttonGroup.buttonClicked.connect(self.set_projection)
    
    # Control Load
    self.ui.SwitchSkyLoad[1].currentIndexChanged.connect(self.set_load)
    self.ui.SwitchSkyLoad[2].currentIndexChanged.connect(self.set_load)
    
    # Noise diode
    self.ui.checkNoise.stateChanged.connect(self.set_ND)
    
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
      self.roachnames = self.centralServer.get_roach_names()
      self.roachnames.sort()
    except Exception as details:
      self.logger.warning(
                   "connect_to_server: could not connect to given Pyro uri %s\n"
                          + "skipping WBDC control connection because\n"
                          + "%s", pyro_uri, str(details))
      self.centralServer = None
      self.roachnames = ['SAO64K-1', 'SAO64K-2', 'SAO64K-3', 'SAO64K-4']
    self.logger.info("__init__: connected to %s for control", str(pyro_uri))
    
  def display_spectra(self, response):
    self.logger.debug("display_spectra: 'response' is type %s", type(response))
    signals = response['table'][0]
    data = NP.array(response['table'][1:])
    #self.logger.debug("display_spectra: 'data' is type %s", type(data))
    self.logger.debug("display_spectra: freqs: %s", data[:,0][:10])
    self.logger.debug("display_spectra: col 1 data: %s...%s",
                      data[:,1][:10], data[:,1][-10:])
    self.logger.debug("display_spectra: col 2 data: %s...%s",
                      data[:,2][:10], data[:,2][-10:])
    self.logger.debug("display_spectra: col 3 data: %s...%s",
                      data[:,3][:10], data[:,3][-10:])
    self.logger.debug("display_spectra: col 4 data: %s...%s",
                      data[:,4][:10], data[:,4][-10:])
    for roach in self.roachnames:
      num = self.roachnames.index(roach) + 1
      self.ui.spectraAxes[num].plot(data[:,0], data[:,num])
    self.ui.spectraCanvas.draw()
    self.logger.debug("display_spectra: done")
  
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
    
    The response is via a callback which refers the result to `handle_tsys`.
    """ 
    self.centralServer.get_tsys(timestamp=True,
                             callback=self.cb_receiver)
    
  def __antennaUpdates(self):
    """
    update antenna angles
    
    The requestde angles are::
      "AzimuthAngle",            "ElevationAngle",
      "AzimuthPredictedAngle",   "ElevationPredictedAngle",
      "ElevationPositionOffset", "CrossElevationPositionOffset"
    """
    self.logger.debug("__antennaUpdates: entered at %s", DT.logtime()) 
    now = datetime.datetime.now()
    az_obs, el_obs, az_pred, el_pred, xel_ofst, el_ofst = \
                                         self.centralServer.get_antenna_angles()
    self.logger.debug(
       "__antennaUpdates: antenna angles at %s are %s, %s, %s, %s, %s, %s",
       now, az_obs, el_obs, az_pred, el_pred, xel_ofst, el_ofst)
                                         
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
                                      "Observatory", ("%6.3f" % xel_ofst), None))
    # beamswitch indicator
    self.logger.debug
    if el_ofst == 14 and xel_ofst == 31:
      # only works for DSS-43
      self.logger.debug("__antennaUpdates: (%) source in off beam", DT.logtime())
      self.ui.obs_pars.sigBeamInd.button[0].setChecked(False)
      self.ui.obs_pars.sigBeamInd.button[1].setChecked(True)
    else:
      self.logger.debug("__antennaUpdates: (%s) source in on beam", DT.logtime())
      self.ui.obs_pars.sigBeamInd.button[0].setChecked(True)
      self.ui.obs_pars.sigBeamInd.button[1].setChecked(False)
    
    # history plot for elevation
    self.ui.ElTime_axes.plot_date(date2num(now), el_obs, '.', color="black")
    self.ui.ElTime_fig.autofmt_xdate()
    self.ui.ElTime_canvas.draw()
    
    # history plot for azimuth
    self.ui.AzTime_axes.plot_date(date2num(now), az_obs, '.', color="black")
    self.ui.AzTime_fig.autofmt_xdate()
    self.ui.AzTime_canvas.draw()

    # plot az-el on Observations page
    self.ui.azel_mark.set_data(az_obs*NP.pi/180, el_obs)
    self.ui.source_canvas.draw()

    # weather
    self.get_weather()
    
    # --------------------- connect() slots (actions) -------------------------

  def source_select(self):
    #If source window contains a text, activate select source option and
    # when pressed select source for observation
    self.logger.debug("source_select: called")
    self.ui.source_name.setText(self.ui.skymap_axes.source_name)
    self.ui.ra_sf.setText(str(ephem.hours(self.skymap.source_info_ra)))
    self.ui.dec_sf.setText(str(ephem.degrees(self.skymap.source_info_dec)))
    self.selected_source_list = []
    try:
      self.selected_source_list.append(self.ui.skymap_axes.source_name)
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
    time.sleep(0.1) # give the command time to be processed
    self.__antennaUpdates()
  
  def start_observing(self):
    """
    start scans
    
    Notes
    =====
    Arguments passed:
    
    Args
    ----
      n_scans (int)    - number of scans
      n_spectra (int)  - number of records (spectra) per scan
      int_time (float) - seconds per record
      log_n_avg (int)  - log-base-2 of number of channels to average
      mid_chan (int)   - middle channel of averaged channels to display
    """
    self.logger.debug("start_observing: in mode %s", self.mode)
    if  self.mode[4:] == "PSSW" or self.mode[4:] == "BPSW":
      n_cycles = self.ui.obs_pars.num_cycles.value.value()
      n_scans = 2*n_cycles
      self.ui.obs_pars.numScans.value.setValue(n_scans)
    else:
      n_scans = self.ui.obs_pars.numScans.value.value()
    n_spectra = self.ui.obs_pars.recsPerScan.value.value()
    int_time = self.ui.obs_pars.secsPerRec.value.value()
    self.logger.debug("start_observing: %d scans of %d records of %f sec",
                      n_scans, n_spectra, int_time)
    self.centralServer.start_spec_scans(n_scans=n_scans, n_spectra=n_spectra,
                                        int_time=int_time,
                                        log_n_avg=6, mid_chan=None,
                                        callback=self.cb_receiver)
  
  def set_mode(self, *args):
    """
    0 - unchecked
    1 - some of the children are checked
    2 - checked
    """
    self.logger.debug("set_mode: args = %s", args)
    btn = args[0]
    self.mode = obstypes[0]+btn.text()
    self.set_scan_cycle_status()
    self.logger.debug("set_mode: mode is %s", self.mode)
  
  def set_scan_cycle_status(self):
    """
    enable/disable scan and cycle boxes according to mode.
    """
    self.centralServer.set_obsmode(self.mode)
    if self.mode[4:] == "PSSW" or self.mode[4:] == "BPSW":
      self.ui.obs_pars.numScans.value.setEnabled(False)
      self.ui.obs_pars.numScans.title.setEnabled(False)
      self.ui.obs_pars.num_cycles.value.setEnabled(True)
      self.ui.obs_pars.num_cycles.title.setEnabled(True)
    else:
      self.ui.obs_pars.numScans.value.setEnabled(True)
      self.ui.obs_pars.numScans.title.setEnabled(True)
      self.ui.obs_pars.num_cycles.value.setEnabled(False)
      self.ui.obs_pars.num_cycles.title.setEnabled(False)
  
  def minical(self):
    self.centralServer.tsys_calibration(callback=self.cb_receiver)
  
  def set_scans(self, *args):
    self.logger.debug("set_scans: args = %s", args)
    self.num_scans = args[0]
    
  def set_cycles(self, *args):
    self.logger.debug("set_cycles: args = %s", args)
    self.num_cycles = args[0]
    self.num_scans = 2*self.num_cycles
    self.ui.obs_pars.numScans.value.setValue(self.num_scans)
  
  def set_atten(self, *args):
    self.logger.debug("set_atten: args = %s", args)
    for num in [1,2,3,4]:
      atten = self.ui.atten[num].value()
      self.logger.debug("set_atten: %s has %s dB", num, atten)
  
  def set_projection(self, *args):
    self.logger.debug("set_projection: args = %s", args)
    btn = args[0]
    projection = btn.text()
    self.logger.debug("set_projection: projection = %s", projection)
    # save the checked categories
    cat_state = {}
    for category in self.categories:
      index = self.categories.index(category)
      cat_state[index] = self.ui.checkDisplaySelect[index].isChecked()
    cat_state["tel"] = self.ui.cb_tel.isChecked()
    cat_state["sun"] = self.ui.cb_sun.isChecked()
    cat_state["moon"] = self.ui.cb_moon.isChecked()
    cat_state["pl"] = self.ui.cb_pl.isChecked()
    # change the projection
    if projection == "polar":
      self.start_UI(polar_sky=True)
      self.ui.projectionInd.button[1].setChecked(True)
    else:
      self.start_UI(polar_sky=False)
      self.ui.projectionInd.button[0].setChecked(True)
    # return to "Catalogues" tab
    self.ui.Ctrl_Tabs.setCurrentIndex(1) 
    # restore the checked categories
    for category in self.categories:
      index = self.categories.index(category)
      if cat_state[index]:
        self.ui.checkDisplaySelect[index].setChecked(True)
      else:
        self.ui.checkDisplaySelect[index].setChecked(False)
    if cat_state["tel"]:
      self.ui.cb_tel.setChecked(True)
    else:
      self.ui.cb_tel.setChecked(False)
    if cat_state["sun"]:
      self.ui.cb_sun.setChecked(True)
    else:
      self.ui.cb_sun.setChecked(False)
    if cat_state["moon"]:
      self.ui.cb_moon.setChecked(True)
    else:
      self.ui.cb_moon.setChecked(False)
    if cat_state["pl"]:
      self.ui.cb_pl.setChecked(True)
    else:
      self.ui.cb_pl.setChecked(False)
  
  def set_load(self, *args, **kwargs):
      states = ["sky", "load"]
      state_index = args[0]
      sender = self.sender()
      self.logger.debug("set_load: sender = %s", sender)
      sender_name = sender.objectName()
      self.logger.debug("set_load: sender = %s", sender_name)
      feed = "F"+sender_name[-1]
      self.centralServer.set_feed(feed, states[state_index])
  
  def set_ND(self, *args, **kwargs):
      self.logger.debug("set_load: args = %s", args)
      if self.ui.checkNoise.isChecked() == "True":
        self.centralServer.set_ND("on")
      else:
        self.centralServer.set_ND("off")
        
      
  # --------------------------- server calls ----------------------------------
    
  def get_mode(self):
    self.mode = self.centralServer.get_obsmode()
    self.logger.debug("get_mode: mode is %s", self.mode)
    index = obsmodes.index(self.mode[4:])
    self.ui.obs_pars.mode_select.button[index].setChecked(True)
    self.set_scan_cycle_status()
    
  def get_frontend_temperatures(self):
    # physical temperatures
    fe_temps = self.centralServer.get_frontend_temps()
    self.logger.debug("get_frontend_temperatures: front end temperatures: %s",
                      fe_temps)
    self.ui.lcd70K.setProperty("value", fe_temps['70K'])
    self.ui.lcd12K.setProperty("value", fe_temps['12K'])
    self.ui.lcdLoad1.setProperty("value", fe_temps['load1'])
    self.ui.lcdLoad2.setProperty("value", fe_temps['load2'])
  
  def get_signals(self):
    """
    get and display signal names
    """
    self.signals = self.centralServer.get_signals()
    self.logger.debug("get_signals: %s", self.signals)
    # extract bands from signals
    band_centers = unique([int(signal[3:5]) for signal in self.signals])
    self.logger.debug("get_signals: bands: %s", band_centers)
    if len(band_centers) == 1:
      self.band_freq = band_centers[0]
      self.band = frequency_to_band(self.band_freq)
    else:
      self.logger.error("get_signals: need (only) one band from: %s", 
                        band_centers)
      raise RuntimeError("server must provide a valid band")
    # extract polarizations from signals
    pols = unique([signal[2] for signal in self.signals])
    self.logger.debug("get_signals: pols: %s", pols)
    # extract IF modes from signals
    IFs = unique([signal[5] for signal in self.signals])
    self.logger.debug("get_signals: IFs: %s", IFs)
    # make list of IF mode options
    IFoptions = []
    if 'L' in IFs or 'U' in IFs:
      IFoptions += ["L", "U"]
    if 'I' in IFs or 'Q' in IFs:
      IFoptions += ['I', 'Q']
    self.signal_options = []
    # add band, pol, and IF options for each feed
    for feed in ['F1', 'F2']:
      for pol in pols:
        for IF in IFoptions:
          self.signal_options.append(feed+pol+str(self.band_freq)+IF)
    self.logger.debug("get_signals: options: %s", self.signal_options)
    # add all the options to the combo box dropdown
    for num in [1,2,3,4]:
      for IFopt in self.signal_options:
        IFind = self.signal_options.index(IFopt)
        self.ui.RFselCombo[num].addItem(_fromUtf8(""))
        self.ui.RFselCombo[num].setItemText(IFind,
                   QtWidgets.QApplication.translate("Observatory", IFopt[:3], None))
      self.ui.RFselCombo[num].setCurrentIndex(2*(num-1))
  
  def get_weather(self):
    self.logger.debug("get_weather: entered")
    self.temperature, self.pressure, self.windspeed, self.winddirection, \
                                self.humidity = self.centralServer.get_weather()
    self.logger.debug("get_weather: temperature=%s, pressure=%s, windspeed=%s,"
                      " wind direction=%s, humidity=%s", self.temperature,
                        self.pressure, self.windspeed, self.winddirection,
                        self.humidity)
    self.ui.temp.setText(QtWidgets.QApplication.translate(
                                    "Observatory", str(self.temperature), None))
    self.ui.pressure.setText(QtWidgets.QApplication.translate(
                                       "Observatory", str(self.pressure), None))
    self.ui.humidity.setText(QtWidgets.QApplication.translate(
                                       "Observatory", str(self.humidity), None))
    self.ui.windspeed.setText(QtWidgets.QApplication.translate(
                                      "Observatory", str(self.windspeed), None))
    self.ui.winddir.setText(QtWidgets.QApplication.translate(
                                  "Observatory", str(self.winddirection), None))
  
  def get_ADC_inputs(self):
    response = self.centralServer.get_adc_inputs()
    self.logger.debug("get_ADC_inputs: got %s", response)
    for idx in list(range(4)):
      num = idx+1
      roach = self.roachnames[idx]
      rms = response[roach]['sample std']
      self.ui.rms[num].setText(QtWidgets.QApplication.translate(
                                          "Observatory", ("%5.1f" % rms), None))
  
  def get_ADC_clock(self):
    response = self.centralServer.get_sample_clock()
    self.logger.debug("get_ADC_clock: got %s", response)
    for idx in list(range(4)):
      num = idx+1
      roach = self.roachnames[idx]
      clk = response[roach]
      self.ui.ft[num].setText(QtWidgets.QApplication.translate(
                                                  "Observatory",str(clk), None))
  
  def get_ADC_temps(self):
    """
    """
    response = self.centralServer.get_adc_temps()
    self.logger.debug("get_ADC_temps: got %s", response)
    for idx in list(range(4)):
      num = idx+1
      roach = self.roachnames[idx]
      adc_temp = response[roach]
      self.ui.adt[num].setText(QtWidgets.QApplication.translate(
                                     "Observatory", ("%5.1f" % adc_temp), None))
                                     
  def get_amb_temps(self):
    """
    """
    response = self.centralServer.get_amb_temps()
    self.logger.debug("get_amb_temps: got %s", response)
    for idx in list(range(4)):
      num = idx+1
      roach = self.roachnames[idx]
      amb_temp = response[roach]
      self.ui.at[num].setText(QtWidgets.QApplication.translate(
                                     "Observatory", ("%5.1f" % amb_temp), None))
  
  def get_gains(self):
    """
    """
    response = self.centralServer.get_gains()
    self.logger.debug("get_gains: got %s", response)
    for idx in list(range(4)):
      num = idx+1
      roach = self.roachnames[idx]
      gain = response[roach]
      self.ui.g[num].setText(QtWidgets.QApplication.translate(
                                     "Observatory", ("%5.1f" % gain), None))
  
  def get_firmware_pars(self):
    """
    """
    fw_pars = self.centralServer.get_firmware_pars()
    self.logger.debug("get_firmware_pars: got %s", fw_pars)
    for idx in list(range(4)):
      num = idx+1
      roach = self.roachnames[idx]
      self.ui.saochan[num].setProperty("value", fw_pars[roach]['nchans'])
      self.ui.saobw[num].setProperty("value", fw_pars[roach]['bandwidth'])
      res = round(1000.*fw_pars[roach]['bandwidth']/fw_pars[roach]['nchans'],2)
      self.ui.saoreso[num].setProperty("value", res)
    
  # -------------------------- async callbacks -------------------------------
  #@async_callback
  #def handle_sources(self, *args):
  #  self.logger.debug("handle_sources: got %s", args)
  
  #@async_callback
  def handle_tsys(self, response):
    #self.logger.debug("handle_tsys: got %s", response)
    pmtime, tsys, readings = response
    for num in [1,2,3,4]:
      self.ui.tsys[num].setText('%4.2f' % (tsys[num-1]))
      pwr_text = '%8.3e' % (readings[num-1])
      self.ui.labelPM[num].setText(pwr_text)
      self.ui.RFpower[num].setText(QtWidgets.QApplication.translate(
                                              "Observatory", pwr_text, None))
      self.tsys_list[num].append(tsys[num-1])
    self.date_list.append(datestr2num(pmtime))
    self.ui.tsys_axes.cla()
    for num in [1,2,3,4]:
      self.ui.tsys_axes.plot_date(self.date_list[-3600:], 
                                  self.tsys_list[num][-3600:], 
                                  "-", label=self.signals[num-1][:3]) # "PM"+str(num))
    self.ui.tsys_axes.legend()
    self.ui.tsys_axes.grid(True)
    self.ui.tsys_fig.autofmt_xdate()
    self.ui.tsys_canvas.draw()
  
  def handle_ordered(self, *args, **kwargs):
    """
    process ordered list of source categories
    """
    self.logger.debug("handle_ordered: got: %s, %s", args, kwargs)
  
  def handle_minical(self, *args, **kwargs):
    """
    process results of Tsys calibration
    """
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
        self.ui.minical_axes[PM_num].grid(True)
      self.ui.minical_canvas.update()
      self.ui.minical_canvas.draw()
  
  def handle_spectra(self, *args, **kwargs):
    """
    process spectrometer data acquisition messages
    """
    #self.logger.debug("handle_spectra: got: %s, %s", args, kwargs)
    response = args[0]
    #self.logger.debug("handle_spectra: response: %s", response)
    if "left" in response:
      scans_left = response["left"]
    elif "table" in response:
      scan = response["scan"]
      self.ui.obs_pars.scan.value.setText(str(scan))
      record = response["record"]
      self.ui.obs_pars.record.value.setText(str(record))
      #spectra = response["table"]
      self.display_spectra(response)
      self.logger.debug("handle_spectra: scan %d record %d done", scan, record)
    elif "type" in response and response["type"] == "saved":
      scan = response["scan"]
      self.ui.obs_pars.scan.value.setText(str(scan))
      record = response["record"]
      self.ui.obs_pars.record.value.setText(str(record))
      self.logger.debug("handle_spectra: saved scan %s, record %s",
                        scan, record)
  
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
