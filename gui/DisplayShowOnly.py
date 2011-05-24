#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """


from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL


class DisplayShowOnly(QtGui.QDialog):
    """ display list """

    def __init__(self, listS, functionCalled, todo):
        """ initialisation """
        super(DisplayShowOnly, self).__init__()

        self.mainLayout = QtGui.QGridLayout(self)
        self.setLayout(self.mainLayout)

        # pylint warning
        self.show_cb = None
        self.btn_func = None
        self.info = None
        self.nothingtodo = None
        self.todo = todo
        self.listS = listS
        self.functionCalled = functionCalled
        self.populate()

    def populate(self):
        """ create layout """

        ## nothingtodo
        self.nothingtodo = QtGui.QLabel('Nothing to ' + self.todo)
        self.nothingtodo.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(self.nothingtodo, 1, 0, 1, 6)

        ## combo show
        self.show_cb = QtGui.QComboBox()
        for i in self.listS:
            self.show_cb.addItem(i[0])
        self.mainLayout.addWidget(self.show_cb, 1, 0)
        
        ## btn doing something useful
        self.btn_func = QtGui.QPushButton(self.todo)
        self.mainLayout.addWidget(self.btn_func, 1, 1)
        self.connect(self.btn_func, SIGNAL("clicked()"), self.btn_pushed)
        
        self.update()
        
    def displayButtons(self, value):
        """ display or not Buttons """
        self.show_cb.setVisible(value)
        self.btn_func.setVisible(value)
        self.nothingtodo.setVisible(not value)

    def btn_pushed(self):
        """ When the button is pushed """
        i = self.show_cb.currentIndex()
        self.show_cb.removeItem(i)
        _tv_name = self.listS[i][0]
        others = self.listS[i][1:]
        self.functionCalled(*others)
        del(self.listS[i])
        
        self.update()
        
    def update(self):
        """ show buttons? """
        if len(self.listS)>0:
            self.displayButtons(True)
        else:
            self.displayButtons(False)
