#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for downloading tab """

### to delete when nextepisode class ok 

from os import path as ospath
conf = {}

def checkConfigFile():
    """ read config file """
    try:
        fileconf = open(ospath.expanduser('~') + "/.config/flvdown/flv.conf", \
                         "rb", 0)
        for line in fileconf:
            tmp = line.split("=")
            if (tmp[0] != 'order' and tmp[0] != 'dict_bug'):
                conf[tmp[0]] = tmp[1].replace('"','')[:-1]
        fileconf.close()
        return 1
    except IOError:
        print "check config"
        return -1


from tempfile import NamedTemporaryFile
cookieFile = NamedTemporaryFile(suffix='.cookies-next.lwp')
cookieFileName = cookieFile.name

import urllib2, cookielib, urllib
cj = cookielib.LWPCookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def addToNextEpisode(title):
    """ add 'title' to next-episode watch-list """
    urltitle = '-'.join(title.split(' ')) + '/'
    src = getSrcPageNextEpisode(urltitle)
    url = src.split('to watchlist')[0].split('"')[-2]
    
    src = getSrcPageNextEpisode(url)

def getSrcPageNextEpisode(url):
    """ return the source page from next-episode """

    txdata = urllib.urlencode ({"username" : conf['login'], \
        "password" : conf['password']})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}

    try:
        req = urllib2.Request("http://next-episode.net/", txdata, txheaders)
        urllib2.urlopen(req)
    except IOError:
        print "could not login"
        return ""

    txdata = None

    cj.save(cookieFileName)
    req = urllib2.Request("http://next-episode.net/" + url, txdata, txheaders)
    src = urllib2.urlopen(req).read()
    return src

###

from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL

from os import path as ospath
from os import mkdir as osmkdir

import traceback
import time

import subdown

class DownThread(QThread):
    """download an episode in a thread"""

    def __init__(self, (tvshow, season, episode), option, list_site, \
                 infofile, parent = None):
        """ initialisation """
        self.tvshow = tvshow
        self.season = season
        self.episode = episode
        self.option = option
        self.list_site = [str(list_site.item(i).text()) \
                      for i in range(list_site.count())]
        self.infofile = infofile
        self.parent = parent
        
        QThread.__init__(self, parent)
        
    def run(self):
        """ download ep, sub, emit signal """
        try:
            ret, filename = links.flvdown(self.tvshow, self.season, \
                   self.episode, self.option, self.list_site)
            if ret != -1:
                if (not ospath.isdir(self.tvshow)):
                    osmkdir(self.tvshow)
                self.emit(SIGNAL("downStart( QString )"), filename )
                urllib.urlretrieve(ret, filename, reporthook=self.downInfo)
                subdown.downSub(self.tvshow, self.tvshow, self.season, \
                     self.episode, self.option)
        except:
            traceback.print_exc()
            self.emit(SIGNAL("downFinished(QString, QString , \
                  PyQt_PyObject)"), "download error", \
                  self.tvshow + " " + self.season + " " + self.episode, \
                  self.infofile)
        else:
            self.emit(SIGNAL("downFinished( QString, QString , \
                  PyQt_PyObject)"), "download finished", \
                  self.tvshow + " " + self.season + " " + self.episode, \
                  self.infofile)

    def downInfo(self, infobloc, taillebloc, totalblocs):
        """ report hook """
        self.emit(SIGNAL("downInfo( PyQt_PyObject )"), \
                  [infobloc, taillebloc, totalblocs])


class InfoDown(QtGui.QWidget):
    """ info about down """

    def __init__(self, show):
        """ initialisation """
        super(InfoDown, self).__init__()

        self.filedown = QtGui.QLabel(show)
        self.barre = QtGui.QProgressBar(self)
        self.barre.hide()
        self.infodown = QtGui.QLabel("")

        mainLayout = QtGui.QGridLayout(self)

        mainLayout.addWidget(self.filedown, 0, 0, 1, 1)
        mainLayout.addWidget(self.barre, 0, 1, 1, 2)
        mainLayout.addWidget(self.infodown, 0, 3, 1, 1)
    
        # pylint warning
        self.time_begin = None

    def downStart(self, msg):
        """ down start """
        self.time_begin = time.time()
        self.filedown.setText(msg)
        self.barre.reset()
        self.barre.setRange(0, 100)
        self.barre.setValue(0)
        self.barre.show()

    def downInfo(self, msg):
        """ down info """
        bloc, taille, total = msg
        if total > 0:
            value = int(float(bloc)*float(taille)/float(total)*100)
            self.barre.setValue(value)
            try:
                speed = float(bloc*taille) / float(time.time()-self.time_begin)
                time_left = float(total-bloc*taille) / speed
                self.infodown.setText( str("%.2f ko/s " %float(speed/1024)) + \
                   str("time_left: %s:%02d:%02d" %(int(time_left/3600.0), \
                   (time_left%3600)/60.0, (time_left%3600)%60)) )
            except ZeroDivisionError:
                pass
        else:
            if self.barre.maximum > 0:
                self.barre.reset()
                self.barre.setRange(0, 0)


class Downloading(QtGui.QWidget):
    """ display playing list """

    def __init__(self, list_ep=None, list_site=None, parent=None):
        """ initialisation """
        super(Downloading, self).__init__()

        # to remove when nextepisode class is ok
        checkConfigFile()

        self.parent = parent

        # pylint warning
        self.info = None
        self.ed_checkbox = None
        self.stackedWidget = None
        self.list_ep = None
        self.list_site = None
        self.show_cb = None
        self.episode_cb = None
        self.season_l = None
        self.button_downall = None
        self.button_down = None
        self.button_all = None
        self.nextbutton = None

        self.populate()
        self.update(list_ep, list_site)

    def populate(self):
        """ create layout """
        
        mainLayout = QtGui.QGridLayout(self)

        ## better display
        mainLayout.addWidget(QtGui.QStackedWidget(), 0, 0, 1, 5)

        ## title
        mainLayout.addWidget(QtGui.QLabel("show"), 1, 0)
        mainLayout.addWidget(QtGui.QLabel("season"), 1, 1)
        mainLayout.addWidget(QtGui.QLabel("episode"), 1, 2)

        ## episode not on next-episode
        edit_tv = QtGui.QLineEdit()
        edit_se = QtGui.QLineEdit()
        edit_ep = QtGui.QLineEdit()
        button_edit = QtGui.QPushButton("Down")
        btn_edit_callback = (lambda data = (edit_tv, \
             edit_se, edit_ep): self.downFreeClicked(data))
        self.connect(button_edit, SIGNAL("clicked()"), btn_edit_callback)
        mainLayout.addWidget(edit_tv, 2, 0)
        mainLayout.addWidget(edit_se, 2, 1)
        mainLayout.addWidget(edit_ep, 2, 2)
        mainLayout.addWidget(button_edit, 2, 3, 1, 2)

        ## combo show
        self.show_cb = QtGui.QComboBox()
        self.show_cb.currentIndexChanged.connect(self.changeShow)
        mainLayout.addWidget(self.show_cb, 3, 0)

        ## label season
        self.season_l = QtGui.QLabel('')
        mainLayout.addWidget(self.season_l, 3, 1)

        ## combo episode
        self.episode_cb = QtGui.QComboBox()
        mainLayout.addWidget(self.episode_cb, 3, 2)

        ## button down 
        self.button_down = QtGui.QPushButton("Down")
        mainLayout.addWidget(self.button_down, 3, 3)
        self.button_down.clicked.connect(self.downClicked)

        ## button all
        self.button_all = QtGui.QPushButton("All")
        mainLayout.addWidget(self.button_all, 3, 4)
        self.button_all.clicked.connect(self.allClicked)

        ## checkbox interactive
        self.ed_checkbox = QtGui.QCheckBox('Interactive download', self)
        mainLayout.addWidget(self.ed_checkbox, 4, 1, 1, 2)

        ## button downall
        self.button_downall = QtGui.QPushButton("Down All")
        mainLayout.addWidget(self.button_downall, 4, 3, 1, 2)
        self.button_downall.clicked.connect(self.downallClicked)

        ## add tvshows
        ed_addShow = QtGui.QLineEdit()
        mainLayout.addWidget(ed_addShow, 5, 0, 1, 3)
        button_addShow = QtGui.QPushButton("Add tvshow")
        mainLayout.addWidget(button_addShow, 5, 3, 1, 2)
        btn_callbackAddShow = (lambda data = (ed_addShow): \
                                  self.addShow(data))
        self.connect(button_addShow, SIGNAL("clicked()"), btn_callbackAddShow)

        ## info down
        self.stackedWidget = QtGui.QStackedWidget()
        mainLayout.addWidget(self.stackedWidget, 6, 0, 1, 4)
        self.nextbutton = QtGui.QPushButton("Next")
        self.nextbutton.clicked.connect(self.nextstacked)
        self.nextbutton.hide()
        mainLayout.addWidget(self.nextbutton, 6, 4)

        ## better display
        mainLayout.addWidget(QtGui.QStackedWidget(), 7, 0, 1, 5)

        self.displayButtons(False)

    def displayButtons(self, value):
        """ display or not buttons """
        self.show_cb.setVisible(value)
        self.season_l.setVisible(value)
        self.episode_cb.setVisible(value)
        self.button_down.setVisible(value)
        self.button_all.setVisible(value)
        self.button_downall.setVisible(value)
        

    def update(self, list_ep=None, list_site=None):
        """ update """
        if list_ep:
            self.list_ep = list_ep
            self.show_cb.clear()
            for (tvshow, _, _, notondisk) in self.list_ep:
                if notondisk:
                    self.show_cb.addItem(tvshow)
            if self.show_cb.count() != 0:
                self.changeShow()
                self.displayButtons(True)
            else:
                self.displayButtons(False)
        if list_site:
            self.list_site = list_site
            
    def changeShow(self):
        """ when show_cb is changed """
        show = self.show_cb.currentText()
        for (tvshow, season, _, notondisk) in self.list_ep:
            if show == tvshow:
                self.season_l.setText(str(season))
                self.episode_cb.clear()
                self.info = []
                for epi in notondisk:
                    self.episode_cb.addItem(epi)
                    self.info.append([tvshow, season, epi])

    @classmethod
    def addShow(cls, data):
        """ when we want to add a tvshow """
        addToNextEpisode(str(data.text()))

    def nextstacked(self):
        """ view next downloading """
        swc = self.stackedWidget.count()
        if swc > 1:
            swci = self.stackedWidget.currentIndex()
            if swci != swc -1:
                self.stackedWidget.setCurrentIndex( swci + 1)
            else:
                self.stackedWidget.setCurrentIndex(0)

    def runThread(self, tvshow, season, episode):
        """ run a download thread """
        option = ""
        if self.ed_checkbox.isChecked():
            option += "i"
        tvshow = "_".join(tvshow.split(' ')).lower()
        infoline = InfoDown(tvshow + " " + season + " " + episode)
        self.stackedWidget.addWidget(infoline)
        if self.stackedWidget.count() > 1:
            self.nextbutton.show()
        dth = DownThread((tvshow, season, episode), option, self.list_site,
             infoline, self)
        self.connect(dth, SIGNAL("downStart(QString)"), infoline.downStart)
        self.connect(dth, SIGNAL("downInfo(PyQt_PyObject)"), infoline.downInfo)
        self.connect(dth, SIGNAL("downFinished(QString, QString, \
             PyQt_PyObject)"), self.endThread)
        dth.start() 

    def endThread(self, titre, message, infoline):
        """ when a download is finished """
        print titre, message
        self.parent.trayIcon.showMessage(titre, message)
        self.stackedWidget.removeWidget(infoline)
        if self.stackedWidget.count() < 2:
            self.nextbutton.hide()

    def downFreeClicked(self, data):
        """ when down from form """
        tvshow = str(data[0].text())
        season = str(data[1].text())
        episodes = str(data[2].text())
        set_ep = set()
        for range_epi in episodes.split(","):
            epi_min = int(range_epi.split("-")[0])
            epi_max = int(range_epi.split("-")[-1])
            for num_epi in range(epi_min, epi_max + 1):
                set_ep.add(num_epi)
        list_ep = list(set_ep)
        list_ep.sort()
        for i in list_ep:
            self.runThread(tvshow, season, str(i))

    def downClicked(self):
        """ when down from combo """
        (tvshow, season, episode) = self.info[self.episode_cb.currentIndex()]
        self.runThread(tvshow, season, episode)

    def allClicked(self):
        """ when all from combo """
        for i in range(self.episode_cb.count()):
            (tvshow, season, episode) = self.info[i]
            self.runThread(tvshow, season, episode)

    def downallClicked(self):
        """ when downall is clicked """
        for (tvshow, season, _, notondisk) in self.list_ep:
            for episode in notondisk:
                self.runThread(tvshow, season, episode)


   
