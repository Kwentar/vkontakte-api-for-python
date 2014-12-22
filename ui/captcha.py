# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\captcha.ui'
#
# Created: Mon Dec 22 22:40:30 2014
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

class Ui_CaptchaDialog(object):
    def setupUi(self, CaptchaDialog):
        CaptchaDialog.setObjectName(_fromUtf8("CaptchaDialog"))
        CaptchaDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        CaptchaDialog.resize(240, 160)
        CaptchaDialog.setMinimumSize(QtCore.QSize(240, 160))
        self.verticalLayout = QtGui.QVBoxLayout(CaptchaDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.widget = QtGui.QWidget(CaptchaDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(150, 100))
        self.widget.setBaseSize(QtCore.QSize(0, 0))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.captchaLabel = QtGui.QLabel(self.widget)
        self.captchaLabel.setGeometry(QtCore.QRect(10, 10, 130, 50))
        self.captchaLabel.setObjectName(_fromUtf8("captchaLabel"))
        self.captchaLine = QtGui.QLineEdit(self.widget)
        self.captchaLine.setGeometry(QtCore.QRect(10, 70, 130, 20))
        self.captchaLine.setObjectName(_fromUtf8("captchaLine"))
        self.horizontalLayout_2.addWidget(self.widget)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.sendButton = QtGui.QPushButton(CaptchaDialog)
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.horizontalLayout.addWidget(self.sendButton)
        self.cancelButton = QtGui.QPushButton(CaptchaDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CaptchaDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CaptchaDialog.reject)
        QtCore.QObject.connect(self.sendButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CaptchaDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(CaptchaDialog)

    def retranslateUi(self, CaptchaDialog):
        CaptchaDialog.setWindowTitle(_translate("CaptchaDialog", "Капча", None))
        self.captchaLabel.setText(_translate("CaptchaDialog", "Image", None))
        self.sendButton.setText(_translate("CaptchaDialog", "Отправить", None))
        self.cancelButton.setText(_translate("CaptchaDialog", "Отмена", None))

