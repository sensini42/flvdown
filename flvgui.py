#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

from os import chdir as oschdir

from gui.central import CentralWidget
from gui.menu import Menu
from gui.actions import Actions

from util.nextepisode import NextEpisode
from util.options import Options
from util.threads import ToolTip


class Flvgui(QtGui.QMainWindow):
    """ Gui for flvdown"""
        
    def __init__(self, options, nextep):
        """ nothing special here"""
        super(Flvgui, self).__init__()

        self.options = options
        self.nextep = nextep
        listShows = []
        #add unknown show
        if(self.nextep.connectSuccess):
            listShows = self.nextep.getListShow()
        for show in listShows:
            if show not in self.options.dict_bug:
                self.options.dict_bug[show] = {}
                name = '_'.join(show.split(' ')).lower()
                self.options.dict_bug[show]['default'] = name
        
        # central widget
        self.centralWidget = CentralWidget(self.nextep, parent=self)
        self.setCentralWidget(self.centralWidget)
        self.update()

        self.setWindowTitle('flvgui')
        self.statusBar()

        # menu 
        self.actions = Actions(self.nextep, parent=self)
        self.menu = Menu(self.actions, parent=self)
        menubar = self.menuBar()
        actionMenu = []
        for i in self.menu.menus:
            actionMenu.append(menubar.addMenu(i))

        # tray icon
        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('icon/flvgui.xpm'), \
            self)
        self.connect(self.trayIcon,
        SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.activated)
        self.trayIcon.show()
        self.tooltip = ToolTip(self.trayIcon, self.centralWidget.downloading)
        self.tooltip.start()


    def updateOptions(self, opt):
        """ update the config"""
        self.options.conf.update(opt)
        self.options.saveConf()
        self.update()
        
    def updateListSite(self, listSite):
        """ update the config"""
        self.options.list_site = listSite
        self.options.saveConf()
        
    def updateDict(self, dico):
        """ update the config"""
        self.options.dict_bug = {}
        self.options.dict_bug.update(dico)
        self.options.saveConf()
        self.update()


    def update(self):
        """ update tab """
        oschdir(self.options.conf['base_directory'])
        self.nextep.update(self.options.dict_bug, self.options.conf['login'], \
               self.options.conf['password'])
        self.centralWidget.playing.update(self.options.conf['player'])
        
        if(self.nextep.connectSuccess):  
            self.centralWidget.downloading.update(self.options.list_site)

    def activated(self, reason):
        """ call when trayIcon is activated """
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.setVisible(not self.isVisible())
        
    def closeEvent(self, event):
        """ call when close_button is clicked """
        if self.centralWidget.downloading.isInProgress():
            reply = QtGui.QMessageBox.question(self, 'Message', \
                  "Are you sure you want to quit?", QtGui.QMessageBox.Yes | \
                  QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()


import sys
def main(args):
    """ main """

    #config
    options = Options()
    if options.error:
       QtGui.QMessageBox.warning(self, 'Config File', \
           'Please check config', \
           QtGui.QMessageBox.StandardButton(QtGui.QMessageBox.Ok))

    #nextep
    nextep = NextEpisode(options.conf['login'], options.conf['password'], \
                options.dict_bug)
    
    app = QtGui.QApplication(args)
    flv = Flvgui(options, nextep)
    flv.show()
    app.exec_()    


if __name__ == '__main__':
    main(sys.argv)

