#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """


from PyQt4 import QtGui
from PyQt4.QtCore import Qt



class Display(QtGui.QWidget):
    """ display list """

    def __init__(self, nextep, condition):
        """ initialisation """
        super(Display, self).__init__()

        self.mainLayout = QtGui.QGridLayout(self)
        self.setLayout(self.mainLayout)

        # pylint warning
        self.list_ep = None
        self.show_cb = None
        self.season_cb = None
        self.episode_cb = None
        self.info = None
        self.show_label = None
        self.season_label = None
        self.episode_label = None
        self.nothingtodo = None

        self.nextep = nextep
        self.condition = condition
        self.populate()

    def populate(self):
        """ create layout """

        ## nothingtodo
        self.nothingtodo = QtGui.QLabel('Nothing to do')
        self.nothingtodo.setAlignment(Qt.AlignHCenter)
        self.mainLayout.addWidget(self.nothingtodo, 1, 0, 1, 6)

        ## title
        self.show_label = QtGui.QLabel('Show')
        self.season_label = QtGui.QLabel('Season')
        self.episode_label = QtGui.QLabel('Episode')
        self.mainLayout.addWidget(self.show_label, 1, 0)
        self.mainLayout.addWidget(self.season_label, 1, 1)
        self.mainLayout.addWidget(self.episode_label, 1, 2)

        ## combo show
        self.show_cb = QtGui.QComboBox()
        self.show_cb.currentIndexChanged.connect(self.changeShow)
        self.mainLayout.addWidget(self.show_cb, 2, 0)

        ## combo season
        self.season_cb = QtGui.QComboBox()
        self.season_cb.currentIndexChanged.connect(self.changeSeason)
        self.mainLayout.addWidget(self.season_cb, 2, 1)

        ## combo episode
        self.episode_cb = QtGui.QComboBox()
        self.mainLayout.addWidget(self.episode_cb, 2, 2)

        self.displayButtons(False)

    def displayButtons(self, value):
        """ display or not Buttons """
        self.show_cb.setVisible(value)
        self.season_cb.setVisible(value)
        self.episode_cb.setVisible(value)
        self.show_label.setVisible(value)
        self.season_label.setVisible(value)
        self.episode_label.setVisible(value)
        self.nothingtodo.setVisible(not value)

    def update(self):
        """ update """
        list_ep = self.nextep.getList()
        if list_ep:
            self.list_ep = list_ep
            self.show_cb.clear()
            for episode in self.list_ep:
                if (episode.isOnDisk == self.condition) and \
                     (self.show_cb.findText(episode.tvshowSpace) == -1):
                    self.show_cb.addItem(episode.tvshowSpace)
            if self.show_cb.count() > 0:
                self.changeShow()
                self.displayButtons(True)
            else:
                self.displayButtons(False)
            
    def changeShow(self):
        """ when show_cb is changed """
        show = self.show_cb.currentText()
        self.season_cb.clear()
        for episode in self.list_ep:
            tvshow = episode.tvshowSpace
            if show == tvshow:
                if episode.isOnDisk == self.condition and \
                     (self.season_cb.findText(episode.strSeason) == -1):
                    self.season_cb.addItem(episode.strSeason)
        self.changeSeason()

    def changeSeason(self):
        """ when season_cb is changed """
        show = self.show_cb.currentText()
        season = self.season_cb.currentText()
        self.episode_cb.clear()
        self.info = []
        for episode in self.list_ep:
            tvshow = episode.tvshowSpace
            tvseason = episode.strSeason
            if show == tvshow and season == tvseason:
                if episode.isOnDisk == self.condition:
                    self.episode_cb.addItem(episode.strEpisode)
                    self.info.append(episode)

    def removeEpisode(self, episode):
        """ delete an entry """
        if episode in self.info:
            self.info.remove(episode)
            index = self.episode_cb.findText(episode.strEpisode, \
                          flags=Qt.MatchExactly)
            self.episode_cb.removeItem(index)
            if self.episode_cb.count() == 0:
                index = self.season_cb.findText(episode.strSeason, \
                              flags=Qt.MatchExactly)
                self.season_cb.removeItem(index)
                if self.season_cb.count() == 0:
                    index = self.show_cb.findText(episode.tvshowSpace, \
                                  flags=Qt.MatchExactly)
                    self.show_cb.removeItem(index)
                    if self.show_cb.count() == 0:
                        self.displayButtons(False)
            if self.condition: ##playing
                self.list_ep.remove(episode)

    def addEpisode(self, episode):
        """ add an entry """
        if not episode.isOnDisk: #update during downloading
            episode.isOnDisk = True
            if (self.show_cb.findText(episode.tvshowSpace) == -1):
                self.show_cb.addItem(episode.tvshowSpace)
                if self.show_cb.count() == 1:
                    self.changeShow()
                    self.displayButtons(True)
                else:
                    self.displayButtons(False)
            elif self.show_cb.currentText() == episode.tvshowSpace:
                if self.season_cb.findText(episode.strSeason) == -1:
                    self.season_cb.addItem(episode.strSeason)
                elif self.season_cb.currentText() == episode.strSeason:
                    self.episode_cb.addItem(episode.strEpisode)
                    self.info.append(episode)

    
