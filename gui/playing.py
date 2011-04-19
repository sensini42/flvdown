#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """

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

def removeFromNextEpisode(movieId, userId, seasonId, episodeId):
    """ mark as read in next-episode """

    txdata = urllib.urlencode ({"username" : conf['login'], \
        "password" : conf['password']})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}
    urlbase = "http://next-episode.net/"
    try:
        req = urllib2.Request(urlbase, txdata, txheaders)
        urllib2.urlopen(req)
    except IOError:
        print "could not login"
        return ""

    cj.save(cookieFileName)

    url = urlbase + 'PAGES/stufftowatch_files/ajax/ajax_requests_stuff.php'    
    txdata = urllib.urlencode ({"showCat" : "episode",
                                "movieId" : movieId,
                                "userId" : userId,
                                "seasonId" : seasonId,
                                "episodeId" : episodeId,
                                "parsedString" : seasonId + "x" + episodeId})
    req = urllib2.Request(url, txdata, txheaders)
    src = urllib2.urlopen(req).read()
    print src

###

from PyQt4 import QtGui
from PyQt4.QtCore import QThread

from os import system as ossystem
from os import listdir as oslistdir
from os import remove as osremove

class VideoThread(QThread):
    """play in a thread"""

    def __init__(self, cmd, parent = None):
        """ initialisation """
        self.cmd = cmd
        QThread.__init__(self, parent)
        
    def run(self):
        """ play in the background """
        ossystem(self.cmd)


class Playing(QtGui.QWidget):
    """ display playing list """

    def __init__(self, list_ep=None, player='mplayer'):
        """ initialisation """
        super(Playing, self).__init__()

        # to remove when nextepisode class is ok
        checkConfigFile()

        # pylint warning
        self.list_ep = None
        self.player = None
        self.show_cb = None
        self.season_l = None
        self.episode_cb = None
        self.info = None

        self.populate()
        self.update(list_ep, player)

    def populate(self):
        """ create layout """
        
        mainLayout = QtGui.QGridLayout(self)

        ## title
        mainLayout.addWidget(QtGui.QLabel("show"), 0, 0)
        mainLayout.addWidget(QtGui.QLabel("season"), 0, 1)
        mainLayout.addWidget(QtGui.QLabel("episode"), 0, 2)

        ## combo show
        self.show_cb = QtGui.QComboBox()
        self.show_cb.currentIndexChanged.connect(self.changeShow)
        mainLayout.addWidget(self.show_cb, 1, 0)

        ## label season
        self.season_l = QtGui.QLabel('')
        mainLayout.addWidget(self.season_l, 1, 1)

        ## combo episode
        self.episode_cb = QtGui.QComboBox()
        mainLayout.addWidget(self.episode_cb, 1, 2)

        ## button play
        self.button_play = QtGui.QPushButton("Play")
        mainLayout.addWidget(self.button_play, 1, 3)
        self.button_play.clicked.connect(self.playClicked)

        ## button mark
        self.button_mark = QtGui.QPushButton("Mark as read")
        mainLayout.addWidget(self.button_mark, 1, 4)
        self.button_mark.clicked.connect(self.markClicked)

        ## button delete
        self.button_delete = QtGui.QPushButton("Mark and Delete")
        mainLayout.addWidget(self.button_delete, 1, 5)
        self.button_delete.clicked.connect(self.deleteClicked)

        ## better display
        mainLayout.addWidget(QtGui.QStackedWidget(), 2, 0, 1, 6)

        self.displayButtons(False)

    def displayButtons(self, value):
        """ display or not Buttons """
        self.show_cb.setVisible(value)
        self.season_l.setVisible(value)
        self.episode_cb.setVisible(value)
        self.button_play.setVisible(value)
        self.button_mark.setVisible(value)
        self.button_delete.setVisible(value)

    def update(self, list_ep=None, player=None):
        """ update """
        if player:
            self.player = player
        if list_ep:
            self.list_ep = list_ep
            self.show_cb.clear()
            for (tvshow, _, ondisk, _) in self.list_ep:
                if ondisk:
                    self.show_cb.addItem(tvshow)
            if self.show_cb.count() > 0:
                self.changeShow()
                self.displayButtons(True)
            else:
                self.displayButtons(False)
            
    def changeShow(self):
        """ when show_cb is changed """
        show = self.show_cb.currentText()
        for (tvshow, season, ondisk, _) in self.list_ep:
            if show == tvshow:
                self.season_l.setText(str(season))
                self.episode_cb.clear()
                self.info = []
                for (mid, uid, sid, epi) in ondisk:
                    self.episode_cb.addItem(epi)
                    self.info.append([tvshow, season, (mid, uid, sid, epi)])

    def playClicked(self):
        """ when a button_play is clicked """
        (tvshow, season, (_, _, _, episode)) = \
            self.info[self.episode_cb.currentIndex()]
        tvshow = "_".join(tvshow.split(' ')).lower()
        if (len(episode)==1):
            episode = "0" + episode
        files = oslistdir(tvshow)
        _file = ""
        for _file in files :
            if _file.startswith(tvshow + season + episode) and \
              not _file.endswith('srt'):
                _file = tvshow + "/" + _file
                break
        #print "play " + self.player + " " + _file
        VideoThread((self.player+ " " + _file), self).start()

    def markClicked(self):
        """ when a button_mark is clicked """
        (_, _, (movieId, userId, seasonId, episodeId)) = \
            self.info[self.episode_cb.currentIndex()]
        #print "mark", (movieId, userId, seasonId, episodeId)
        removeFromNextEpisode(movieId, userId, seasonId, episodeId)

    def deleteClicked(self):
        """ when a button_delete is clicked """
        self.markClicked()
        (tvshow, season, (_, _, _, episode)) = \
            self.info[self.episode_cb.currentIndex()]
        tvshow = "_".join(tvshow.split(' ')).lower()
        if (len(episode)==1):
            episode = "0" + episode
        files = oslistdir(tvshow)
        for _file in files :
            if _file.startswith(tvshow + season + episode):
                #print "remove", tvshow + "/" + _file
                osremove(tvshow + "/" + _file)
   
