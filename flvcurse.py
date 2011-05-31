#!/usr/bin/python
# -*- coding: utf-8 -*-
""" curses version """

from os import chdir as oschdir
from os import system as ossystem
import curses
import threads, links

class Curse():
    """ curse version """

    def __init__(self, options, nextep):
        """ nothing special here """

        self.options = options
        oschdir(self.options.conf['base_directory'])
        self.nextep = nextep
        self.nextep.update(self.options.dict_bug)
        self.list_ep = self.nextep.getList()

        self.screen = curses.initscr()
        action = 0
        while action != ord('5'):
            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(2, 2, "Please enter a number...")
            self.screen.addstr(4, 4, "1 - Play a show")
            self.screen.addstr(5, 4, "2 - Download a show")
            self.screen.addstr(6, 4, "3 - Options")
            self.screen.addstr(7, 4, "4 - Manage TvShow")
            self.screen.addstr(8, 4, "5 - Exit")
            self.screen.addstr(2, 26, "")
            self.screen.refresh()

            action = self.screen.getch()

            if action == ord('1'):
                self.play()
            elif action == ord('2'):
                self.down()
            elif action == ord('3'):
                self.chgoptions()
            elif action == ord('4'):
                self.manageTvShow()

        curses.endwin()

    def populate(self, condition):
        """ print list """
        setShows = []
        setEpisodes = []
        if self.list_ep:
            for episode in self.list_ep:
                if episode.isOnDisk == condition and \
                  episode.tvshowSpace not in setShows:
                    self.screen.addstr(4 + len(setShows), 4, \
                      str(len(setShows)+1) + ' - ' + episode.getBaseName())
                    setShows.append(episode.tvshowSpace)
                    setEpisodes.append(episode)
        return setEpisodes

    def play(self):
        """ play a show """
        # print list
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, "Play a show...")
        setEpisodes = self.populate(True)
        self.screen.refresh()
        try:
            num = int(self.screen.getstr(2, 18, 2))-1
        except: 
            pass
        else:
            # play episode
            if num >= 0 and num < len(setEpisodes):
                episode = setEpisodes[num]

                curses.endwin()
                ossystem(self.options.conf['player'] + " " + \
                    episode.getVideoName())

                # actions 
                self.screen = curses.initscr()
                self.screen.clear()
                self.screen.border(0)
                self.screen.addstr(2, 2, "Please enter a number...")
                self.screen.addstr(4, 4, "1 - Mark as read")
                self.screen.addstr(5, 4, "2 - Mark and Delete")
                self.screen.addstr(6, 4, "3 - Pass")
                self.screen.addstr(2, 26, "")
                self.screen.refresh()

                action = self.screen.getch()

                if action == ord('1'):
                    self.nextep.markAsRead(*(episode.ids))
                    self.list_ep.remove(episode)
                elif action == ord('2'):
                    self.nextep.markAsRead(*(episode.ids))
                    episode.removeFile()
                    self.list_ep.remove(episode)


    def down(self):
        """ down a show """
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, "Down a show...")
        setEpisodes = self.populate(False)
        self.screen.refresh()
        try:
            num = int(self.screen.getstr(2, 18, 2))-1
        except: 
            pass
        else:
            # play episode
            if num >= 0 and num < len(setEpisodes):
                episode = setEpisodes[num]

                curses.endwin()
                url, dest, cook = links.flvdown(episode, "vi")
                if url:
                    try:
                        links.getFile(url, dest, cook)
                    except:
                        pass
                    else:
                        episode.isOnDisk = True

    
    def chgoptions(self):
        """ options list """
        pass

    def manageTvShow(self):
        """ manage TvShow """
        pass



