# -*- coding: utf-8 -*-
""" actions for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import QStringList
from PyQt4.Qt import QAction
from PyQt4.QtCore import SIGNAL
from PyQt4.Qt import QKeySequence
from gui.menusettings import Settings
from gui.menusiteorder import SiteOrder
from gui.menudictbug import Dictbug
from gui.DisplayShowOnly import DisplayShowOnly
class Actions(QtGui.QWidget):
    """ actions for gui """

    def __init__(self, nextep, parent=None):
        """ initialisation """
        super(Actions, self).__init__()
        self.parent = parent
        self.nextep = nextep
        self.listActions = []
        self.listActionsFile = []
        self.listActions.append(("&File", self.listActionsFile))
        self.listActionsPref = []
        self.listActions.append(("&Options", self.listActionsPref))
        self.listActionsMT = []
        self.listActions.append(("&Manage TvShow", self.listActionsMT))
        
        separator = QAction(self.parent)
        separator.setSeparator(True)

        # Define actions
        # Options
        self.addActionToList("&Settings", self.listActionsPref, self.setApp, 
                "Open settings window.", QKeySequence.Preferences) 

        self.addActionToList("Site O&rder", self.listActionsPref, self.sortApp,
                "Define which site to download from first")
        
        self.addActionToList("&Dict bug", self.listActionsPref, self.dictApp,
                "Dictbug")
        
        self.listActionsPref.append(separator)

        self.addActionToList("&Interactive", self.listActionsPref, self.intApp,
                "If checked, user is asked some things")
        self.listActionsPref[len(self.listActionsPref) - 1].setCheckable(True)

        # Manage TvShow
        self.addActionToList("&Add a show", self.listActionsMT, self.addApp,
                "To track a new show.")
        
        self.addActionToList("&Remove a show", self.listActionsMT, self.delApp,
                "Remove a show from watching list.")
        
        self.addActionToList("&Track a show", self.listActionsMT, self.trackS,
                "To track a show.")
        
        self.addActionToList("&Untrack", self.listActionsMT, self.untrackS,
                "To Untrack a show.")
        

        # File
        self.addActionToList("&Update", self.listActionsFile, self.refreshApp,
                "Update from nextep.", QKeySequence.Refresh)
        
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
        #if self.parent.centralWidget.close():
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
    

    def addApp(self):
        """ popup to add a show"""
        listsuggest = self.nextep.getSuggestions()
        listsug = QStringList()
        for i in listsuggest:
            listsug.append(i[0])
        (tvshow, ok) = QtGui.QInputDialog.getItem (self.parent.centralWidget, \
                      "add a tv show", 'Which show do you want to track?', \
                      listsug, editable = True)
        if (ok and tvshow):
            self.parent.centralWidget.nextep.addShow(str(tvshow))
            print "should add", tvshow, " :p"


    def delApp(self):
        """ popup to del a show """
        #ltracked = self.nextep.getTracked() #tv, ids, idu
        #luntracked = self.nextep.getUntracked()#tv, ids
        listShow = self.nextep.getListShow() #tv
        lShows = []
        #removeShow needs tvname only
        for i in listShow:
            lShows.append([i, i])
        lShows.sort()

        delDisplay = DisplayShowOnly(lShows, self.nextep.removeShow, 'delete')
        returnValue = delDisplay.exec_()
  

    def trackS(self):
        """ popup to trakc a show """
        luntracked = self.nextep.getUntracked()#tv, ids
        #track needs ids only
        tDisplay = DisplayShowOnly(luntracked, self.nextep.trackShow, 'track')
        returnValue = tDisplay.exec_()
      

    def untrackS(self):
        """ popup to untrack a show """
        ltracked = self.nextep.getTracked()#tv, ids, idu
        #untrack needs ids and idu only
        uDisplay = DisplayShowOnly(ltracked, self.nextep.untrackShow, 'untrack')
        returnValue = uDisplay.exec_()
      
