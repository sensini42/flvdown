# -*- coding: utf-8 -*-

from os import path as ospath
from os import mkdir as osmkdir
from subprocess import Popen as subpopen
from subprocess import PIPE

import curses

from util import episodes
import links
from curse.tab_gen import TabEntry
from curse.menu_gen import MenuEntry
from curse.list_gen import List 

class TabDownloading(TabEntry):
    """ playing tab """

    def __init__(self, parent):
        """ initialisation """
        TabEntry.__init__(self, 'Downloading', None)
        self.parent = parent

    def display(self):
        """ display the tab """
        self.changeMenu()
        self.setEpi = episodes(self.parent.list_ep, False)
        self.visible = List(self.screen, \
                [x.getBaseName() for x in self.setEpi])
        self.visible.display(10, 4, 10)

    def changeMenu(self):
        """ change entry in action """
        self.parent.action_menu.removeAllEntries()
        self.parent.action_menu.addSubEntry(MenuEntry('Down', \
                action=self.down))
        self.parent.action_menu.addSubEntry(MenuEntry('Down All', 5,
                action=self.downAll)) 
    
    def error(self, msg):
        """ print an error """
        (genheight, genwidth) = self.parent.scr.getmaxyx()
        screen = curses.newwin(3, len(msg)+4, (genheight-10)/2, \
                    (genwidth-len(msg))/2)
        screen.box()
        screen.addstr(1, 2, msg, curses.A_STANDOUT)
        screen.getch()
        screen.erase()
        self.parent.scr.refresh()

    def downepi(self, episode):
        """ down a show """
        (y, x, l) = self.visible.posend
        url, dest, cook = links.flvdown(episode, "")
        if url:
            try:
                if (not ospath.isdir(dest.split('/')[0])):
                    osmkdir(dest.split('/')[0])
                cmd = "wget -c " + url + " -O " + dest
                p = subpopen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
                while p.poll() is None:
                    li = p.stderr.readline()
                    self.screen.addstr(y, x+l, li.split('.'))
                    self.screen.refresh()
            except:
                p.kill()
                self.error(episode.getBaseName() + ': down error')
            else:
                self.error(episode.getBaseName() + ': down finish')
                episode.isOnDisk = True
                self.display()
        else:
            self.error(episode.getBaseName() + ': url not found')

    def downAll(self):
        """ down a show """
        for epi in self.setEpi:
            self.downepi(epi)

    def down(self):
        """ down a show """
        self.downepi(self.setEpi[self.visible.active])


