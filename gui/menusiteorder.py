#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class SiteOrder(QtGui.QDialog):
    """ display playing list """

    def __init__(self, list_site, parent=None):
        """ initialisation """
        super(SiteOrder, self).__init__()

        self.parent = parent
        self.resize(400, 300)
        ## pylint warning
        self.list_site = list_site

        self.populate(self.list_site)

    def populate(self, list_site):
        """ create layout """
        
        mainLayout = QtGui.QGridLayout(self)

        self.list_site = QtGui.QListWidget()
        for i in list_site:
            item = QtGui.QListWidgetItem(i)
            self.list_site.addItem(item)

        button_up = QtGui.QPushButton("Up")
        button_down = QtGui.QPushButton("Down")
        self.connect(button_up, SIGNAL("clicked()"), self.moveUp)
        self.connect(button_down, SIGNAL("clicked()"), self.moveDown)
        
        mainLayout.addWidget(self.list_site, 0, 0, 4, 1)
        mainLayout.addWidget(button_up, 0, 1)
        mainLayout.addWidget(button_down, 1, 1)

        button_save = QtGui.QPushButton("Save config file")
        button_save.clicked.connect(self.saveClicked)
        mainLayout.addWidget(button_save, 5, 0)

        button_cancel = QtGui.QPushButton("Cancel")
        button_cancel.clicked.connect(self.reject)
        mainLayout.addWidget(button_cancel, 5, 1)
        
    def moveUp(self):
        """ up is clicked """
        cur_row = self.list_site.currentRow()
        nxt_row = max(cur_row - 1, 0)
        item = self.list_site.takeItem(cur_row)
        self.list_site.insertItem(nxt_row, item)
        self.list_site.setCurrentRow(nxt_row)
        
    def moveDown(self):
        """ down is clicked """
        cur_row = self.list_site.currentRow()
        nxt_row = min(cur_row + 1, self.list_site.count() -1)
        item = self.list_site.takeItem(cur_row)
        self.list_site.insertItem(nxt_row, item)
        self.list_site.setCurrentRow(nxt_row)
        
    def saveClicked(self):
        """ save button clicked """
        list_site = []
        for i in range(self.list_site.count()):
            list_site.append(str(self.list_site.item(i).text()))
        self.parent.updateListSite(list_site)
        super(SiteOrder, self).accept()
   
