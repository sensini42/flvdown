#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt
import aggregators

class Dictbug(QtGui.QDialog):
    """ display dict bug """

    def __init__(self, dict_bug, parent=None):
        """ initialisation """
        super(Dictbug, self).__init__(parent)

        self.parent = parent
        self.resize(600, 200)
        ## pylint warning
        self.mainLayout = None
        self.show_cb = None
        self.site_cb = None
        self.lineedit = None

        self.parent = parent

        self.dict_bug = dict_bug

        self.populate()
        self.changeCB()

    def populate(self):
        """ create layout """
       
        self.mainLayout = QtGui.QGridLayout(self)

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 0, 0, 1, 4)

        ## title
        self.mainLayout.addWidget(QtGui.QLabel('The show:'), 1, 0)
        self.mainLayout.addWidget(QtGui.QLabel('on the site:'), 1, 1)
        self.mainLayout.addWidget(QtGui.QLabel('is named:'), 1, 2)
       
        ## comboboxes
        listS = self.dict_bug.keys()
        listS.sort()
        self.show_cb = QtGui.QComboBox()
        for i in listS:
            self.show_cb.addItem(i)
        self.show_cb.currentIndexChanged.connect(self.changeCB)
        self.mainLayout.addWidget(self.show_cb, 2, 0)
        
        self.site_cb = QtGui.QComboBox()
        self.site_cb.addItem('default')
        self.site_cb.addItem('tvsubtitles')
        ## mettre dans un update
        for i in aggregators.__all__:
            self.site_cb.addItem(i)
        self.site_cb.currentIndexChanged.connect(self.changeCB)
        self.mainLayout.addWidget(self.site_cb, 2, 1)

        self.lineedit = QtGui.QLineEdit()
        self.connect(self.lineedit, SIGNAL("textEdited(QString)"), self.updateDict,)

        self.mainLayout.addWidget(self.lineedit, 2, 2)

        
        ## save button
        button_saveConf = QtGui.QPushButton("Save config file")
        button_saveConf.clicked.connect(self.saveClicked)
        self.mainLayout.addWidget(button_saveConf, 1000, 0)

        button_cancel = QtGui.QPushButton("Cancel")
        button_cancel.clicked.connect(self.reject)
        self.mainLayout.addWidget(button_cancel, 1000, 1)

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 1001, 0, 1, 4)



    def updateDict(self, txt):
        """ dict is updated """
        show = str(self.show_cb.currentText())
        site = str(self.site_cb.currentText())
        self.dict_bug[show][site] = str(txt)

    def saveClicked(self):
        """ saveConf button clicked """
        self.parent.updateDict(self.dict_bug)
        super(Dictbug, self).accept()

    def changeCB(self):
        """ when a combo box is changed """
        show = str(self.show_cb.currentText())
        site = str(self.site_cb.currentText())
        if site in self.dict_bug[show]:
            name = self.dict_bug[show][site]
        else:
            name = ""
        self.lineedit.setText(name)
