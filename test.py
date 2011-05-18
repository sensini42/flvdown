#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL



from PyQt4.QtCore import SIGNAL, SLOT





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



from PyQt4.Qt import QAction
from PyQt4.Qt import QKeySequence

class Actions(QtGui.QWidget):
    """ actions for gui """

    def __init__(self, parent=None):
        """ initialisation """
        self.parent = parent
        self.listActions = []
        self.listActionsFile = []
        self.listActions.append(("&File", self.listActionsFile))
        self.listActionsMT = []
        self.listActions.append(("&Manage TvShow", self.listActionsMT))
        
        # Manage TvShow
        self.addActionToList("&Add a show", self.listActionsMT, self.addApp,
                "To track a new show.")

        # File
        self.addActionToList("&Quit", self.listActionsFile, self.quitApp,
                "Quit the app.", QKeySequence.Quit)


    def addActionToList(self, txtMenu, whichList, fctnCalled,
                        status="", shortkey=""):
        

        theAction = QAction(txtMenu, self.parent)
        #theAction.setToolTip(toolTip)
        #theAction.setWhatsThis(what)
        theAction.setStatusTip(status)
        theAction.setShortcut(shortkey)
        #theAction.setIconSet(QIconSet(QPixmap(closeIcon)))
        self.connect(theAction, SIGNAL("triggered()"),
                     fctnCalled)
        whichList.append(theAction)
        
    def quitApp(self):
        """ close the app (check if downloads are running)"""
        self.parent.close()
    
    def addApp(self):
        """ popup to add a show"""
        print " test "

    


class Flvgui(QtGui.QMainWindow):
    """ Gui for flvdown"""
        
    def __init__(self, *args):
        """ nothing special here"""
        apply(QtGui.QMainWindow.__init__, (self,) + args)

        self.actions = Actions(parent=self)
        self.menu = Menu(self.actions, parent=self)

        self.setWindowTitle('flvgui')

        self.statusBar()

        menubar = self.menuBar()
        actionMenu = []
        for i in self.menu.menus:
            actionMenu.append(menubar.addMenu(i))


import sys
def main(args):
    """ main """
    app = QtGui.QApplication(args)
    flv = Flvgui()
    flv.show()
    app.exec_()    


if __name__ == '__main__':
    main(sys.argv)

