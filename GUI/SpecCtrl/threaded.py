'''
Created on Sep 28, 2012
@author: asoni
'''
from roach_control import Ui_Observatory
from PyQt5 import QtCore

import sys, os
import logging

logger = logging.getLogger(__name__)

class ThreadInit(QtCore.QThread):
    """
    A Qt thread class with common objects/parameters
    Also, defines Output log format such as highlighting, color etc. for logging
 into the GUI log window.
    Log window logs information about-
    1. krx43 controls (WBDC and frontend)
    2. ROACH information errors, warnings, data overflow etc.
    3. 
    """
    def __init__(self, ui, color=None):
        QtCore.QThread.__init__(self)
        self.logger = logging.getLogger(logger.name+".ThreadInit")
        self.ui = ui
        self.color = color
        self.logger.debug("__init__: finished")

    def write(self, msg):
        if self.color:
            tc = self.ui.viewLog.textColor()
            self.ui.viewLog.setTextColor(self.color)
        self.ui.viewLog.insertPlainText(msg)
        if self.color:
                self.ui.viewLog.setTextColor(tc)

