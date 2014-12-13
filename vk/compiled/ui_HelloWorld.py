# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Code\vkontakte\vk\sources\HelloWorld.ui'
#
# Created: Sat Dec 13 02:55:25 2014
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_HelloWorld(object):
    def setupUi(self, HelloWorld):
        HelloWorld.setObjectName(_fromUtf8("HelloWorld"))
        HelloWorld.resize(300, 150)
        HelloWorld.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.horizontalLayout = QtGui.QHBoxLayout(HelloWorld)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(HelloWorld)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(HelloWorld)
        QtCore.QMetaObject.connectSlotsByName(HelloWorld)

    def retranslateUi(self, HelloWorld):
        HelloWorld.setWindowTitle(_translate("HelloWorld", "Привет мир", None))
        self.label.setText(_translate("HelloWorld", "Привет, мир!", None))

