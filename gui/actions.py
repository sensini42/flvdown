# -*- coding: utf-8 -*-
""" actions for flvdown """
from PyQt4 import QtGui
from PyQt4.Qt import QAction
from PyQt4.QtCore import SIGNAL
from PyQt4.Qt import QKeySequence
from gui.menusettings import Settings
from gui.menusiteorder import SiteOrder
from gui.menudictbug import Dictbug
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
        # Options
        self.addActionToList("&Settings", self.listActionsPref, self.setApp, 
                "Open settings window.", QKeySequence.Preferences) 

        self.addActionToList("Site O&rder", self.listActionsPref, self.sortApp,
                "Define which site to download from first")
        
        self.addActionToList("&Dict bug", self.listActionsPref, self.dictApp,
                "Dictbug")
        
        self.addActionToList("&Interactive", self.listActionsPref, self.intApp,
                "If checked, user is asked some things")
        self.listActionsPref[len(self.listActionsPref) - 1].setCheckable(True)

        # File
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

    def intApp(self):
        """ interactive download """
        if self.listActionsPref[len(self.listActionsPref) - 1].isChecked():
            print "interactive download checked"
        else:
            print "interactive download unchecked"


    def dictApp(self):
        """ open dictbug windows """
        dict_bug = self.parent.centralWidget.dict_bug
        dictDialog = Dictbug(dict_bug, self.parent.centralWidget)
        returnValue = dictDialog.exec_()
        if returnValue:
            print 'dict saved' #dans systray/status
    
