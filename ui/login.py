# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\login.ui'
#
# Created: Tue Dec 23 00:43:30 2014
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

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName(_fromUtf8("LoginDialog"))
        LoginDialog.resize(240, 120)
        LoginDialog.setMinimumSize(QtCore.QSize(240, 120))
        self.verticalLayout = QtGui.QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.usernameLabel = QtGui.QLabel(LoginDialog)
        self.usernameLabel.setObjectName(_fromUtf8("usernameLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.usernameLabel)
        self.usernameLine = QtGui.QLineEdit(LoginDialog)
        self.usernameLine.setObjectName(_fromUtf8("usernameLine"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.usernameLine)
        self.passwordLabel = QtGui.QLabel(LoginDialog)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLine = QtGui.QLineEdit(LoginDialog)
        self.passwordLine.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLine.setObjectName(_fromUtf8("passwordLine"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.passwordLine)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 19, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.loginButton = QtGui.QPushButton(LoginDialog)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.horizontalLayout.addWidget(self.loginButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(_translate("LoginDialog", "Авторизация", None))
        self.usernameLabel.setText(_translate("LoginDialog", "Пользователь:", None))
        self.usernameLine.setPlaceholderText(_translate("LoginDialog", "Email или телефон", None))
        self.passwordLabel.setText(_translate("LoginDialog", "Пароль:", None))
        self.passwordLine.setPlaceholderText(_translate("LoginDialog", "Пароль", None))
        self.loginButton.setText(_translate("LoginDialog", "Войти", None))

