#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from gui.playing import Playing
from gui.downloading import Downloading

class CentralWidget(QtGui.QWidget):
    """ Main Widget for flvdown"""
        
    def __init__(self, nextep, parent=None):
        """ nothing special here"""
        super(CentralWidget, self).__init__()
        self.parent = parent
        self.nextep = nextep
        self.playing = Playing(self.nextep)

        self.downloading = Downloading(self.nextep, self.parent.list_site, parent=self)


        self.populate()
    def populate(self):
        """ define the main layout"""
        mainLayout = QtGui.QGridLayout(self)

        tab_widget = QtGui.QTabWidget()
        mainLayout.addWidget(tab_widget, 0, 0, 1, 2)

        tab_widget.addTab(self.playing, "Playing")
        tab_widget.addTab(self.downloading, "Downloading")

        tab_widget.setCurrentIndex(1)

        button_refresh = QtGui.QPushButton("Refresh")
        mainLayout.addWidget(button_refresh, 1, 0)
        self.connect(button_refresh, SIGNAL("clicked()"), self.parent.update)
                
        button_close = QtGui.QPushButton("Quit")
        mainLayout.addWidget(button_close, 1, 1)
        button_close.clicked.connect(self.parent.close)

        self.setLayout(mainLayout)

    def showMessage(self, title, message):
        """ tray icon notification """
        self.parent.trayIcon.showMessage(title, message)
