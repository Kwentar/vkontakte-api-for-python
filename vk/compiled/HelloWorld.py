# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from ui_HelloWorld import Ui_HelloWorld

class HelloWorld(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent=parent
        self.ui=Ui_HelloWorld()
        self.ui.setupUi(self)

if __name__ == '__main__':
    a=QtGui.QApplication(sys.argv)
    w=HelloWorld()
    w.show()
    a.exec_()
