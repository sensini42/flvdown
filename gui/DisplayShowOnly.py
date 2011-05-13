#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """


from PyQt4 import QtGui
from PyQt4.QtCore import Qt



class DisplayShowOnly(QtGui.QWidget):
    """ display list """

    def __init__(self, nextep, functionCalled):
        """ initialisation """
        super(Display, self).__init__()

        self.mainLayout = QtGui.QGridLayout(self)
        self.setLayout(self.mainLayout)

        # pylint warning
        self.list_ep = None
        self.show_cb = None
        self.btn_func = None
        self.info = None
        self.nothingtodo = None

        self.nextep = nextep
        self.functionCalled = functionCalled
        self.populate()

    def populate(self):
        """ create layout """

        ## nothingtodo
        self.nothingtodo = QtGui.QLabel('Nothing to do')
        self.nothingtodo.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(self.nothingtodo, 1, 0, 1, 6)

        ## combo show
        self.show_cb = QtGui.QComboBox()
        self.mainLayout.addWidget(self.show_cb, 1, 0)

        ## btn doing something useful
        self.btn_func = QtGui.QPushButton("do something")
        self.mainLayout.addWidget(self.show_cb, 1, 0)
        btn_callback = (lambda data = (self.show_cb.currentText): \
                        self.functionCalled(data))
        self.connect(button_edit, SIGNAL("clicked()"), btn_edit_callback)
        self.displayButtons(False)

    def displayButtons(self, value):
        """ display or not Buttons """
        self.show_cb.setVisible(value)
        self.nothingtodo.setVisible(not value)

    def update(self):
        """ update """
        list_ep = self.nextep.getList()
        if list_ep:
            self.list_ep = list_ep
            self.show_cb.clear()
            for episode in self.list_ep:
                self.show_cb.addItem(episode.tvshowSpace)
            if self.show_cb.count() > 0:
                self.changeShow()
                self.displayButtons(True)
            else:
                self.displayButtons(False)
            
    
