#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """


from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL


class choiceFromList(QtGui.QMainWindow):
    """ display list """

    def __init__(self, listS, parent):
        """ initialisation """
        super(choiceFromList, self).__init__(parent)

        self.mainLayout = QtGui.QGridLayout(self)
        self.setLayout(self.mainLayout)

        # pylint warning
        self.list_cb = None
        self.listS = listS
        self.populate()

    def populate(self):
        """ create layout """

        ## combo list
        self.list_cb = QtGui.QComboBox()
        for i in self.listS:
            self.list_cb.addItem(i[0])
        self.mainLayout.addWidget(self.list_cb, 1, 0)
        
        ## btn doing something useful
        btn_choose = QtGui.QPushButton("Ok")
        self.mainLayout.addWidget(btn_choose, 1, 1)
        btn_choose.clicked.connect(self.chosen)
        
            
    def chosen(self):
        """ When the button is pushed """
        i = self.list_cb.currentIndex()
        super(choiceFromList, self).done(i)
        
    
   
