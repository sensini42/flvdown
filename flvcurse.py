#!/usr/bin/python
# -*- coding: utf-8 -*-
""" curses version """

import curses

class Curse():
    """ curse version """

    def __init__(self, options, nextep):
        """ nothing special here """

        self.options = options
        self.nextep = nextep
        self.nextep.update(self.options.dict_bug)

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


    def play(self):
        """ play a show """
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, "Play a show...")
        setShow = []
        list_ep = self.nextep.getList()
        if list_ep:
            for episode in list_ep:
                if episode.isOnDisk == True: #and episode.tvshowSpace not in setShow:
                    self.screen.addstr(4 + len(setShow), 4, \
                      str(len(setShow)+1) + ' - ' + episode.tvshowSpace + \
                      ' season ' + episode.strSeason + \
                      ' episode ' + episode.strEpisode)
                    setShow.append(episode.tvshowSpace)
                    break
        self.screen.refresh()
        self.screen.getstr(2, 18, 2)

    def down(self):
        """ down a show """
        pass
    
    def chgoptions(self):
        """ options list """
        pass

    def manageTvShow(self):
        """ manage TvShow """
        pass



