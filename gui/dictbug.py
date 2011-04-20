#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL


class Dictbug(QtGui.QWidget):
    """ display playing list """

    def __init__(self, dict_bug, parent=None):
        """ initialisation """
        super(Dictbug, self).__init__()

        self.parent = parent

        self.list_dictbug = dict_bug
        self.eltdictbug = []

        self.populate()

    def populate(self):
        """ create layout """
        
        self.mainLayout = QtGui.QGridLayout(self)

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 0, 0, 1, 4)

        ## title
        self.mainLayout.addWidget(QtGui.QLabel('Next-episode'), 1, 0)
        arrowlabelt = QtGui.QLabel(u"→")
        arrowlabelt.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(arrowlabelt, 1, 1)
        self.mainLayout.addWidget(QtGui.QLabel('Down'), 1, 2)

        ## add line
        self.lineedit_ne = QtGui.QLineEdit()
        arrowlabel = QtGui.QLabel(u"→")
        arrowlabel.setAlignment(Qt.AlignHCenter)
        self.lineedit_d = QtGui.QLineEdit()
        button_add = QtGui.QPushButton("Add dict bug")
        button_add.connect(button_add, SIGNAL("clicked()"), self.addDictBug)
        self.mainLayout.addWidget(self.lineedit_ne, 2, 0)
        self.mainLayout.addWidget(arrowlabel, 2, 1)
        self.mainLayout.addWidget(self.lineedit_d, 2, 2)
        self.mainLayout.addWidget(button_add, 2, 3)

        ## data 
        for key in self.list_dictbug.keys():
            value = self.list_dictbug[key]
            self.addEntry(key, value)

        ## save button
        button_save = QtGui.QPushButton("Save config file")
        self.connect(button_save, SIGNAL("clicked()"), self.saveClicked)
        self.mainLayout.addWidget(button_save, 1000, 0)

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 1001, 0, 1, 4)

    def saveClicked(self):
        """ save config file"""
        self.parent.updateConf()

    def getListDictBug(self):
        """ return the dict of bug"""
        return self.list_dictbug
   
    def addDictBug(self):
        """ add an entry in dictbug"""
        key, value = str(self.lineedit_ne.text()).strip(), \
                     str(self.lineedit_d.text()).strip()
        self.list_dictbug[key] = value
        self.addEntry(key, value)

    def removeDictBug(self, data):
        """ remove an entry in dictbug"""
        del self.list_dictbug[data[1]]
        for i in range(4):
            self.eltdictbug[data[0]][i].hide()

    def addEntry(self, key, value):
        """ display the entry"""
        ind = len(self.eltdictbug)
        button = QtGui.QPushButton("Remove")
        button_callback = (lambda data = [ind, key]: \
            self.removeDictBug(data))
        button.connect(button, SIGNAL("clicked()"), button_callback)
        labelkey = QtGui.QLabel(key)
        labelarrow = QtGui.QLabel(u"→")
        labelarrow.setAlignment(Qt.AlignHCenter)
        labelvalue = QtGui.QLabel(value)
        self.eltdictbug.append([labelkey, labelarrow, labelvalue, button])
        self.mainLayout.addWidget(labelkey, 3 + ind, 0)
        self.mainLayout.addWidget(labelarrow, 3 + ind, 1)
        self.mainLayout.addWidget(labelvalue, 3 + ind, 2)
        self.mainLayout.addWidget(button, 3 + ind, 3)


