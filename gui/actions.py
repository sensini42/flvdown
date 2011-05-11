# -*- coding: utf-8 -*-
""" actions for flvdown """
from PyQt4 import QtGui
from PyQt4.Qt import QAction
from PyQt4.QtCore import SIGNAL
from PyQt4.Qt import QKeySequence
from gui.menusettings import Settings
from gui.menusiteorder import SiteOrder
class Actions(QtGui.QWidget):
    """ info about down """

    def __init__(self, parent=None):
        """ initialisation """
        self.parent = parent
        self.listActions = []
        self.listActionsFile = []
        self.listActions.append(("&File", self.listActionsFile))
        self.listActionsPref = []
        self.listActions.append(("&Options", self.listActionsPref))
        
        # Define actions
        self.addActionToList("&Settings", self.listActionsPref, self.setApp, 
                "Open settings window.", QKeySequence.Preferences) 

        self.addActionToList("Site O&rder", self.listActionsPref, self.sortApp,
                "Define which site to download from first")

        self.addActionToList("&Update", self.listActionsFile, self.refreshApp,
                "Update from nextep.", QKeySequence.Refresh)
        separator = QAction(self.parent)
        separator.setSeparator(True)
        self.listActionsFile.append(separator)

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
        if self.parent.centralWidget.close():
            self.parent.close()
    
        
    def setApp(self):
        """ open settings windows """
        conf = self.parent.centralWidget.conf
        settDialog = Settings(conf, self.parent.centralWidget)
        returnValue = settDialog.exec_()
        if returnValue:
            print 'conf saved' #dans systray/status
        
    def sortApp(self):
        """ open settings windows """
        list_site = self.parent.centralWidget.list_site
        settDialog = SiteOrder(list_site, self.parent.centralWidget)
        returnValue = settDialog.exec_()
        if returnValue:
            print 'list order saved' #dans systray/status
    
    def refreshApp(self):
        """ refresh """
        self.parent.centralWidget.update()
