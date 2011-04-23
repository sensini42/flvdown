#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """


from PyQt4 import QtGui
from PyQt4.QtCore import Qt



class Display(QtGui.QWidget):
    """ display list """

    def __init__(self, nextep):
        """ initialisation """
        super(Display, self).__init__()

        self.mainLayout = QtGui.QGridLayout(self)
        self.setLayout(self.mainLayout)

        # pylint warning
        self.list_ep = None
        self.show_cb = None
        self.season_l = None
        self.episode_cb = None
        self.info = None
        self.show_label = None
        self.season_label = None
        self.episode_label = None
        self.nothingtodo = None

        self.nextep = nextep
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

        ## label season
        self.season_l = QtGui.QLabel('')
        self.mainLayout.addWidget(self.season_l, 2, 1)

        ## combo episode
        self.episode_cb = QtGui.QComboBox()
        self.mainLayout.addWidget(self.episode_cb, 2, 2)

        self.displayButtons(False)

    def displayButtons(self, value):
        """ display or not Buttons """
        self.show_cb.setVisible(value)
        self.season_l.setVisible(value)
        self.episode_cb.setVisible(value)
        self.show_label.setVisible(value)
        self.season_label.setVisible(value)
        self.episode_label.setVisible(value)
        self.nothingtodo.setVisible(not value)

    def update(self, condition=True):
        """ update """
        list_ep = self.nextep.getList()
        if list_ep:
            self.list_ep = list_ep
            self.show_cb.clear()
            for episode in self.list_ep:
                if (episode.isOnDisk == condition) and \
                     (self.show_cb.findText(episode.tvshowSpace) == -1):
                    self.show_cb.addItem(episode.tvshowSpace)
            if self.show_cb.count() > 0:
                self.changeShow()
                self.displayButtons(True)
            else:
                self.displayButtons(False)
            
    def changeShow(self, condition=True):
        """ when show_cb is changed """
        show = self.show_cb.currentText()
        self.episode_cb.clear()
        self.info = []
        for episode in self.list_ep:
            tvshow = episode.tvshowSpace
            if show == tvshow:
                self.season_l.setText(episode.strSeason)
                if episode.isOnDisk == condition:
                    self.episode_cb.addItem(episode.strEpisode)
                    self.info.append(episode)

