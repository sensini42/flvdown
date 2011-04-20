#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import os
from nextepisode import NextEpisode


from os import path as ospath
from os import system as ossystem
from os import chdir as oschdir

from gui.playing import Playing
from gui.downloading import Downloading
from gui.options import Options
from gui.siteorder import Siteorder
from gui.dictbug import Dictbug

conf2 = {}
dict_bug2 = {}

class Flvgui(QtGui.QWidget):
    """ Gui for flvdown"""
        
    def __init__(self, parent=None):
        """ nothing special here"""
        super(Flvgui, self).__init__()

        if (self.checkConfigFile()==-1):
            QtGui.QMessageBox.warning(self, 'Config File', \
                'Please check config', \
                QtGui.QMessageBox.StandardButton(QtGui.QMessageBox.Ok))
        
        ## to delete
        conf2['login'] = self.conf['login'] 
        conf2['password'] = self.conf['password']
        for key in self.dict_bug.keys():
            dict_bug2[key] = self.dict_bug[key]
        ##

        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('icon/flvgui.xpm'), self)
        self.trayIcon.activated.connect(self.toggle)
        self.trayIcon.show()

        self.setWindowTitle('flvgui')

        self.list_ep = []
        self.nextep = NextEpisode(self.conf['login'], self.conf['password'], \
                                  self.dict_bug)
        self.mainlayout()

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
            return 1
        except IOError:
            print "check config"
            return -1

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
        
    def mainlayout(self):
        """ define the main layout"""
        mainLayout = QtGui.QGridLayout(self)

        tab_widget = QtGui.QTabWidget()
        mainLayout.addWidget(tab_widget, 0, 0, 1, 3)

        self.playing = Playing(self.nextep)
        tab_widget.addTab(self.playing, "Playing")

        self.downloading = Downloading(self.nextep, parent=self)
        tab_widget.addTab(self.downloading, "Downloading")

        self.options = Options(self.conf, parent=self)
        tab_widget.addTab(self.options, "Options")

        self.siteorder = Siteorder(self.list_site, parent=self)
        tab_widget.addTab(self.siteorder, "Site order")

        self.dictbug = Dictbug(self.dict_bug, parent=self)
        tab_widget.addTab(self.dictbug, "Dict Bug")

        tab_widget.setCurrentIndex(1)
        self.update()

        button_sub = QtGui.QPushButton("Subtitles")
        mainLayout.addWidget(button_sub, 1, 0)
        self.connect(button_sub, SIGNAL("clicked()"), self.downsub)
                
        button_refresh = QtGui.QPushButton("Refresh")
        mainLayout.addWidget(button_refresh, 1, 1)
        self.connect(button_refresh, SIGNAL("clicked()"), self.update)
                
        button_close = QtGui.QPushButton("Close")
        mainLayout.addWidget(button_close, 1, 2)
        button_close.clicked.connect(self.close)

        self.setLayout(mainLayout)

        
    def toggle(self):
        """ toggle main frame """
        if self.isVisible(): 
            self.hide()
        else: 
            self.show()


    def updateConf(self):
        """ update the config"""
        conf = self.options.getOptions()
        self.conf.update(conf)
        self.list_site = self.siteorder.getListSite()
        dict_bug = self.dictbug.getListDictBug()
        self.dict_bug.update(dict_bug)
        self.saveConf()

        self.playing.update(player=self.conf['player'])
        self.downloading.update(list_site=self.list_site)

    def saveConf(self):
        """ save the config"""
        if (not os.path.exists(ospath.expanduser('~') + "/.config/flvdown/")):
            os.mkdir(ospath.expanduser('~') + "/.config/flvdown/")
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


    @classmethod
    def downsub(cls):
        """ when a button_sub is clicked """
        #data from combo
        ossystem("downsub.sh")

    def update(self):
        "populate the tab_widget"
        oschdir(self.conf['base_directory'])
        self.playing.update(self.conf['player'])
        self.downloading.update(list_site=self.list_site)

    def closeEvent(self, event):
        if self.downloading.isInProgress():
            reply = QtGui.QMessageBox.question(self, 'Message', \
                  "Are you sure to quit?", QtGui.QMessageBox.Yes | \
                  QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()
    

def main():
    """ main """
    app = QtGui.QApplication([])
    flv = Flvgui()
    flv.show()
    app.exec_()    


if __name__ == '__main__':
    main()

