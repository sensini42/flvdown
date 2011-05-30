#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """

from PyQt4 import QtGui


class Settings(QtGui.QDialog):
    """ display playing list """

    def __init__(self, conf, parent=None):
        """ initialisation """
        super(Settings, self).__init__(parent)

        self.parent = parent

        ## pylint warning
        self.list_edit = []

        self.populate(conf)

    def populate(self, conf):
        """ create layout """
        
        mainLayout = QtGui.QGridLayout(self)

        i = 0
        for key in conf.keys():
            mainLayout.addWidget(QtGui.QLabel(key), i, 0)
            self.list_edit.append([key, QtGui.QLineEdit()])
            mainLayout.addWidget(self.list_edit[i][1], i, 1, 1, 1) 
            if key == 'password':
                self.list_edit[i][1].setEchoMode(2)
            self.list_edit[i][1].setText(conf[key])
            i += 1

        button_save = QtGui.QPushButton("Save config")
        button_save.clicked.connect(self.saveClicked)
        mainLayout.addWidget(button_save, i, 0)

        button_cancel = QtGui.QPushButton("Cancel")
        button_cancel.clicked.connect(self.reject)
        mainLayout.addWidget(button_cancel, i, 1)

    def saveClicked(self):
        """ save the config"""
        options = {} 
        for (key, line) in self.list_edit:
            options[key] = str(line.text())
        self.parent.updateOptions(options)
        super(Settings, self).accept()
  
