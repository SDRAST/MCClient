import logging
from PyQt5 import QtWidgets
import sys

mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()
mylogger.setLevel(logging.DEBUG)

from obsCtrl import observatoryGUI

app = QtWidgets.QApplication(sys.argv)
GUI = observatoryGUI()
GUI.show()
sys.exit(app.exec_())
