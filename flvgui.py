#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from nextepisode import NextEpisode


from os import path as ospath
from os import mkdir as osmkdir
from os import chdir as oschdir

from gui.playing import Playing
from gui.downloading import Downloading
#from gui.options import Options
#from gui.siteorder import Siteorder
#from gui.dictbug import Dictbug
from gui.menu import Menu
from gui.actions import Actions
#from gui.progress import Progress

from threads import ToolTip

class FlvMain(QtGui.QWidget):
    """ Main Widget for flvdown"""
        
    def __init__(self, parent=None):
        """ nothing special here"""
        super(FlvMain, self).__init__()
        self.parent = parent

        ## pylint warning
        self.conf = None
        self.list_site = None
        self.dict_bug = None

        self.checkConfigFile()
        
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('icon/flvgui.xpm'), \
            self)
        self.connect(self.trayIcon,
        SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.activated)
        self.trayIcon.show()

        self.nextep = NextEpisode(self.conf['login'], self.conf['password'], \
                                  self.dict_bug)
        self.playing = Playing(self.nextep)
        #self.progress = Progress(self.list_site, parent=self)
        self.downloading = Downloading(self.nextep, self.list_site, parent=self)
#        self.options = Options(self.conf, parent=self)
#        self.siteorder = Siteorder(self.list_site, parent=self)
#        self.dictbug = Dictbug(self.dict_bug, parent=self)

        self.populate()
        self.tooltip = ToolTip(self.trayIcon, self.downloading)
        self.tooltip.start()


    def checkConfigFile(self):
        """ read config file """
        self.list_site = self.getSites()
        self.conf = {'login':'login', 'password':'password', \
            'player':'mplayer', 'base_directory':'/tmp'}
        self.dict_bug = {}
        try:
            fileconf = open(ospath.expanduser('~') + \
                    "/.config/flvdown/flv.conf", "rb", 0)
            for line in fileconf:
                tmp = line.split("=")
                if tmp[0] == 'order':
                    list_order = tmp[1].replace('"', '').split(',')[:-1]
                    for (i, site) in enumerate(list_order):
                        self.list_site.remove(site.strip())
                        self.list_site.insert(i, site.strip())
                elif tmp[0] == 'dict_bug':
                    list_dict = tmp[1].replace('"', '').split(',')[:-1]
                    self.dict_bug = dict(map(str.strip, i.split(':')) \
                                         for i in list_dict)
                else:
                    self.conf[tmp[0]] = tmp[1].replace('"','')[:-1]
            fileconf.close()
        except IOError:
            print "check config"
            QtGui.QMessageBox.warning(self, 'Config File', \
                'Please check config', \
                QtGui.QMessageBox.StandardButton(QtGui.QMessageBox.Ok))

    @classmethod
    def getSites(cls):
        """ check modules to populate list_site"""
        import sys
        import aggregators
        list_site = []
        for i in aggregators.__all__:
            site = "aggregators." + i + "_mod"
            __import__(site)
            for j in sys.modules[site].__all__:
                subsite = i + " : " + j
                list_site.append(subsite)
        return list_site
        
    def populate(self):
        """ define the main layout"""
        mainLayout = QtGui.QGridLayout(self)

        tab_widget = QtGui.QTabWidget()
        mainLayout.addWidget(tab_widget, 0, 0, 1, 2)

        tab_widget.addTab(self.playing, "Playing")
        tab_widget.addTab(self.downloading, "Downloading")
#        tab_widget.addTab(self.options, "Options")
#        tab_widget.addTab(self.siteorder, "Site order")
#        tab_widget.addTab(self.dictbug, "Dict Bug")
        #tab_widget.addTab(self.progress, "Progress")

        tab_widget.setCurrentIndex(1)
        self.update()

        button_refresh = QtGui.QPushButton("Refresh")
        mainLayout.addWidget(button_refresh, 1, 0)
        self.connect(button_refresh, SIGNAL("clicked()"), self.update)
                
        button_close = QtGui.QPushButton("Close mainwidget...")
        mainLayout.addWidget(button_close, 1, 1)
        button_close.clicked.connect(self.close)

        self.setLayout(mainLayout)

    def activated(self, reason):
        """ call when trayIcon is activated """
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.setVisible(not self.isVisible())
        
    def showMessage(self, title, message):
        """ tray icon notification """
        self.trayIcon.showMessage(title, message)

    def updateOptions(self, opt):
        """ update the config"""
        self.conf.update(opt)
        self.saveConf()
        self.update()
        
    def updateListSite(self, listSite):
        """ update the config"""
        self.list_site = listSite
        self.saveConf()
        
    def updateDict(self, dico):
        """ update the config"""
        self.dict_bug = {}
        self.dict_bug.update(dico)
        self.saveConf()
        self.update()

    def saveConf(self):
        """ save the config"""
        if (not ospath.exists(ospath.expanduser('~') + "/.config/flvdown/")):
            osmkdir(ospath.expanduser('~') + "/.config/flvdown/")
        fileconf = open(ospath.expanduser('~') + \
            "/.config/flvdown/flv.conf", "w", 0)
        for key in self.conf.keys():
            fileconf.write(key + '="' + self.conf[key] + '\"\n')
        fileconf.write('order="')
        for elt in self.list_site:
            fileconf.write(elt + ', ')
        fileconf.write('"\n')
        fileconf.write('dict_bug="')
        for key in self.dict_bug:
            fileconf.write(key + ' : ' + self.dict_bug[key] + ', ')
        fileconf.write('"\n')
        
        fileconf.close()


    def update(self):
        """ update tab """
        oschdir(self.conf['base_directory'])
        self.nextep.update(self.dict_bug, self.conf['login'], \
               self.conf['password'])
        self.playing.update(self.conf['player'])
        self.downloading.update(self.list_site)
        #self.progress.update(self.list_site)

    def closeEvent(self, event):
        """ call when close_button is clicked """
        if self.downloading.isInProgress():
            reply = QtGui.QMessageBox.question(self, 'Message', \
                  "Are you sure you want to quit?", QtGui.QMessageBox.Yes | \
                  QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()


from PyQt4.QtCore import SIGNAL, SLOT
class Flvgui(QtGui.QMainWindow):
    """ Gui for flvdown"""
        
    def __init__(self, *args):
        """ nothing special here"""
        apply(QtGui.QMainWindow.__init__, (self,) + args)

        self.centralWidget = FlvMain(self)
        self.actions = Actions(self.centralWidget.nextep, parent=self)
        self.menu = Menu(self.actions, parent=self)
        self.setCentralWidget(self.centralWidget)


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

