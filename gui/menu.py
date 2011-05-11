# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class Menu(QtGui.QWidget):
    """ info about down """

    def __init__(self, actions, parent=None):
        """ initialisation """
        super(Menu, self).__init__()
        self.parent = parent
        self.menus = []
        for name, listAction in actions.listActions:
            self.menus.append(QtGui.QMenu(name, self.parent))
            self.menus[len(self.menus) - 1].addActions(listAction)

    def __del__(self):
        print "dying"
