#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """


from PyQt4 import QtGui
from PyQt4.QtCore import QThread
from PyQt4.QtCore import Qt


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

    def __init__(self, nextep, player='mplayer'):
        """ initialisation """
        super(Playing, self).__init__()

        # pylint warning
        self.list_ep = None
        self.player = None
        self.show_cb = None
        self.season_l = None
        self.episode_cb = None
        self.info = None
        self.nextep = nextep
        self.populate()
        self.update(player)

    def populate(self):
        """ create layout """
        
        mainLayout = QtGui.QGridLayout(self)

        ## better display
        mainLayout.addWidget(QtGui.QStackedWidget(), 0, 0, 1, 6)
        
        ## nothingtoplay
        self.nothingtoplay = QtGui.QLabel('Nothing to play')
        self.nothingtoplay.setAlignment(Qt.AlignHCenter)
        mainLayout.addWidget(self.nothingtoplay, 1, 0, 1, 6)

        ## title
        self.show_label = QtGui.QLabel('Show')
        self.season_label = QtGui.QLabel('Season')
        self.episode_label = QtGui.QLabel('Episode')
        mainLayout.addWidget(self.show_label, 1, 0)
        mainLayout.addWidget(self.season_label, 1, 1)
        mainLayout.addWidget(self.episode_label, 1, 2)

        ## combo show
        self.show_cb = QtGui.QComboBox()
        self.show_cb.currentIndexChanged.connect(self.changeShow)
        mainLayout.addWidget(self.show_cb, 2, 0)

        ## label season
        self.season_l = QtGui.QLabel('')
        mainLayout.addWidget(self.season_l, 2, 1)

        ## combo episode
        self.episode_cb = QtGui.QComboBox()
        mainLayout.addWidget(self.episode_cb, 2, 2)

        ## button play
        self.button_play = QtGui.QPushButton("Play")
        mainLayout.addWidget(self.button_play, 2, 3)
        self.button_play.clicked.connect(self.playClicked)

        ## button mark
        self.button_mark = QtGui.QPushButton("Mark as read")
        mainLayout.addWidget(self.button_mark, 2, 4)
        self.button_mark.clicked.connect(self.markClicked)

        ## button delete
        self.button_delete = QtGui.QPushButton("Mark and Delete")
        mainLayout.addWidget(self.button_delete, 2, 5)
        self.button_delete.clicked.connect(self.deleteClicked)

        ## better display
        mainLayout.addWidget(QtGui.QStackedWidget(), 3, 0, 1, 6)

        self.displayButtons(False)

    def displayButtons(self, value):
        """ display or not Buttons """
        self.show_cb.setVisible(value)
        self.season_l.setVisible(value)
        self.episode_cb.setVisible(value)
        self.button_play.setVisible(value)
        self.button_mark.setVisible(value)
        self.button_delete.setVisible(value)
        self.show_label.setVisible(value)
        self.season_label.setVisible(value)
        self.episode_label.setVisible(value)
        self.nothingtoplay.setVisible(not value)

    def update(self, player=None):
        """ update """
        if player:
            self.player = player
        list_ep = self.nextep.getList()
        if list_ep:
            self.list_ep = list_ep
            self.show_cb.clear()
            for episode in self.list_ep:
                tvshow = episode.tvshowSpace
                if episode.isOnDisk and \
                     (self.show_cb.findText(episode.tvshowSpace) == -1):
                    self.show_cb.addItem(tvshow)
            if self.show_cb.count() > 0:
                self.changeShow()
                self.displayButtons(True)
            else:
                self.displayButtons(False)
            
    def changeShow(self):
        """ when show_cb is changed """
        show = self.show_cb.currentText()
        self.episode_cb.clear()
        self.info = []
        for episode in self.list_ep:
            tvshow = episode.tvshowSpace
            strepi = episode.strEpisode
            season = episode.strSeason
            if show == tvshow:
                self.season_l.setText(season)
                if episode.isOnDisk:
                    self.episode_cb.addItem(strepi)
                    self.info.append(episode)

    def playClicked(self):
        """ when a button_play is clicked """
        episode = self.info[self.episode_cb.currentIndex()]
        videoName = episode.getVideoName()
        VideoThread((self.player+ " " + videoName), self).start()

    def markClicked(self):
        """ when a button_mark is clicked """
        episode = self.info[self.episode_cb.currentIndex()]
        #print "mark", (movieId, userId, seasonId, episodeId)
        self.nextep.markAsRead(*(episode.ids))


    def deleteClicked(self):
        """ when a button_delete is clicked """
        self.markClicked()
        episode = self.info[self.episode_cb.currentIndex()]
        episode.removeFile()
