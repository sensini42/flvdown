#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for downloading tab """


from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from gui.display import Display

import episodetv


class Downloading(Display):
    """ display playing list """

    def __init__(self, nextep, progress, parent=None):
        """ initialisation """
        self.parent = parent
        self.progress = progress

        # pylint warning
        self.ed_checkbox = None
        self.button_downall = None
        self.button_down = None
        self.button_all = None

        super(Downloading, self).__init__(nextep)
        self.update()


    def populate(self):
        """ create layout """

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 0, 0, 1, 5)


        ## episode not on next-episode
        edit_tv = QtGui.QLineEdit()
        edit_se = QtGui.QLineEdit()
        edit_ep = QtGui.QLineEdit()
        button_edit = QtGui.QPushButton("Down")
        btn_edit_callback = (lambda data = (edit_tv, \
             edit_se, edit_ep): self.downFreeClicked(data))
        self.connect(button_edit, SIGNAL("clicked()"), btn_edit_callback)
        self.mainLayout.addWidget(edit_tv, 3, 0)
        self.mainLayout.addWidget(edit_se, 3, 1)
        self.mainLayout.addWidget(edit_ep, 3, 2)
        self.mainLayout.addWidget(button_edit, 3, 3, 1, 2)


        ## button down 
        self.button_down = QtGui.QPushButton("Down")
        self.mainLayout.addWidget(self.button_down, 2, 3)
        self.button_down.clicked.connect(self.downClicked)

        ## button all
        self.button_all = QtGui.QPushButton("All")
        self.mainLayout.addWidget(self.button_all, 2, 4)
        self.button_all.clicked.connect(self.allClicked)

        ## checkbox interactive
        self.ed_checkbox = QtGui.QCheckBox('Interactive download', self)
        self.mainLayout.addWidget(self.ed_checkbox, 4, 1, 1, 2)

        ## button downall
        self.button_downall = QtGui.QPushButton("Down All")
        self.mainLayout.addWidget(self.button_downall, 4, 3, 1, 2)
        self.button_downall.clicked.connect(self.downallClicked)

        ## add tvshows
        ed_addShow = QtGui.QLineEdit()
        self.mainLayout.addWidget(ed_addShow, 5, 0, 1, 3)
        button_addShow = QtGui.QPushButton("Add tvshow")
        self.mainLayout.addWidget(button_addShow, 5, 3, 1, 2)
        btn_callbackAddShow = (lambda data = (ed_addShow): \
                                  self.addShow(data))
        self.connect(button_addShow, SIGNAL("clicked()"), btn_callbackAddShow)

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 6, 0, 1, 5)

        super(Downloading, self).populate()

    def displayButtons(self, value):
        """ display or not buttons """
        self.button_down.setVisible(value)
        self.button_all.setVisible(value)
        self.button_downall.setVisible(value)
        super(Downloading, self).displayButtons(value)

    def update(self):
        """ update """
        super(Downloading, self).update(False)
        
    def changeShow(self):
        """ when show_cb is changed """
        super(Downloading, self).changeShow(False)

    def addShow(self, data):
        """ when we want to add a tvshow """
        self.nextep.addShow(str(data.text()))

    def runThread(self, episode):
        """ run a download thread """
        option = ""
        if self.ed_checkbox.isChecked():
            option += "i"
        self.progress.addLine(episode, option)

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
            epi = episodetv.episodeTV(tvshow, season, str(i), None)
            self.runThread(epi)

    def downClicked(self):
        """ when down from combo """
        episode = self.info[self.episode_cb.currentIndex()]
        self.runThread(episode)

    def allClicked(self):
        """ when all from combo """
        for i in range(self.episode_cb.count()):
            episode = self.info[i]
            self.runThread(episode)

    def downallClicked(self):
        """ when downall is clicked """
        for episode in self.list_ep:
            if not episode.isOnDisk:
                self.runThread(episode)

