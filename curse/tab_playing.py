# -*- coding: utf-8 -*-
"""
    playing tab
"""

from subprocess import Popen as subpopen
from subprocess import PIPE

from curse.tab_gen import TabEntry
from curse.menu_gen import MenuEntry
from curse.list_gen import List 

import util.subdown as subdown

def episodes(list_ep, condition):
    """ create a list with episode checking condition """
    setShows = []
    setEpisodes = []
    for episode in list_ep:
        if episode.isOnDisk == condition and \
          episode.tvshowSpace not in setShows:
            setShows.append(episode.tvshowSpace)
            setEpisodes.append(episode)
    return setEpisodes


class TabPlaying(TabEntry):
    """ playing tab """

    def __init__(self, parent):
        """ initialisation """
        TabEntry.__init__(self, 'Playing')
        self.parent = parent
        self.setEpi = None

    def display(self):
        """ display the tab """
        self.changeMenu()
        self.setEpi = episodes(self.parent.list_ep, True)
        self.visible = List(self.screen, \
                [x.getBaseName() for x in self.setEpi])
        self.visible.display(10, 4, 10)

    def changeMenu(self):
        """ change entry in action """
        self.parent.action_menu.removeAllEntries()
        self.parent.action_menu.addSubEntry(MenuEntry('Play', \
                action=self.play))
        self.parent.action_menu.addSubEntry(MenuEntry('Mark as read', \
                action=self.mark))
        self.parent.action_menu.addSubEntry(MenuEntry('Mark and Delete', 9, \
                action=self.delete))

    def delete(self):
        """ mark and delete """
        episode = self.setEpi[self.visible.active]
        episode.removeFile()
        self.parent.nextep.markAsRead(*(episode.ids))
        self.parent.list_ep.remove(episode)
        self.display()

    def mark(self):
        """ mark """
        episode = self.setEpi[self.visible.active]
        self.parent.nextep.markAsRead(*(episode.ids))
        self.parent.list_ep.remove(episode)
        self.display()

    def play(self):
        """ play a show """
        episode = self.setEpi[self.visible.active]
        if episode.getSrtName() == "":
            subdown.downSub(episode, "")
        cmd = self.parent.options.conf['player'] + ' ' + episode.getVideoName()
        subpopen(cmd, shell=True, stderr=PIPE, stdout=PIPE)




