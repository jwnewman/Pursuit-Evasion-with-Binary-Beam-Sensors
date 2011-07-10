# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showsimulation.ui'
#
# Created: Fri Jul 08 20:36:01 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(807, 584)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 681, 541))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(700, 10, 91, 91))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.turnButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.turnButton.setObjectName(_fromUtf8("turnButton"))
        self.verticalLayout.addWidget(self.turnButton)
        self.clearButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.verticalLayout.addWidget(self.clearButton)
        self.exitButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        self.verticalLayout.addWidget(self.exitButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 807, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.turnButton.setText(QtGui.QApplication.translate("MainWindow", "Advance turn", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

