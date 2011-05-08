#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """


from PyQt4 import QtGui

from gui.display import Display
from threads import Video

import subdown


class Playing(Display):
    """ display playing list """

    def __init__(self, nextep, player='mplayer'):
        """ initialisation """

        # pylint warning
        self.player = None
        self.button_play = None
        self.button_mark = None
        self.button_delete = None

        super(Playing, self).__init__(nextep, True)
        self.update(player)

    def populate(self):
        """ create layout """

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 0, 0, 1, 6)
        
        ## button play
        self.button_play = QtGui.QPushButton("Play")
        self.mainLayout.addWidget(self.button_play, 2, 3)
        self.button_play.clicked.connect(self.playClicked)

        ## button mark
        self.button_mark = QtGui.QPushButton("Mark as read")
        self.mainLayout.addWidget(self.button_mark, 2, 4)
        self.button_mark.clicked.connect(self.markClicked)

        ## button delete
        self.button_delete = QtGui.QPushButton("Mark and Delete")
        self.mainLayout.addWidget(self.button_delete, 2, 5)
        self.button_delete.clicked.connect(self.deleteClicked)

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 3, 0, 1, 6)

        super(Playing, self).populate()
        

    def displayButtons(self, value):
        """ display or not Buttons """
        self.button_play.setVisible(value)
        self.button_mark.setVisible(value)
        self.button_delete.setVisible(value)
        super(Playing, self).displayButtons(value)

    def update(self, player=None):
        """ update """
        if player:
            self.player = player
        super(Playing, self).update()
        
    def playClicked(self):
        """ when a button_play is clicked """
        episode = self.info[self.episode_cb.currentIndex()]
        videoName = episode.getVideoName()
        if episode.getSrtName() == "":
            subdown.downSub(episode)
            if episode.getSrtName() == "":
                reply = QtGui.QMessageBox.question(self, 'Message', \
                   "srt file missing. continue?", QtGui.QMessageBox.Yes | \
                   QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.No:
                    return
        Video(episode, self.player, self).start()

    def markClicked(self):
        """ when a button_mark is clicked """
        episode = self.info[self.episode_cb.currentIndex()]
        self.nextep.markAsRead(*(episode.ids))
        self.removeEpisode(episode)

    def deleteClicked(self):
        """ when a button_delete is clicked """
        episode = self.info[self.episode_cb.currentIndex()]
        self.nextep.markAsRead(*(episode.ids))
        episode.removeFile()
        self.removeEpisode(episode)


