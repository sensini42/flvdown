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
        while action != ord('6'):
            titre = "Please enter a number..."
            choices = [ "Play a show", "Download a show", "Options", \
                "Manage TvShow", "Update", "Exit"]
            action = self.printChoices(titre, choices)

            if action == ord('1'):
                self.play()
            elif action == ord('2'):
                self.down()
            elif action == ord('3'):
                self.chgoptions()
            elif action == ord('4'):
                self.manageTvShow()
            elif action == ord('5'):
                self.update()

        curses.endwin()

    def update(self):
        """ update """
        oschdir(self.options.conf['base_directory'])
        self.nextep.update(self.options.dict_bug, \
            self.options.conf['login'], self.options.conf['password'])
        self.list_ep = self.nextep.getList()
        
    def printChoices(self, titre, choices):
        """ print list choices """
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, titre)
        for i in range(len(choices)):
            self.screen.addstr(4+i, 4, str(i+1) + " - " + choices[i])
        self.screen.addstr(2, 3+len(titre), "")
        self.screen.refresh()
        return self.screen.getch()


    def populate(self, titre, condition):
        """ print list """
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, titre)
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
        self.screen.refresh()
        return setEpisodes

    def play(self):
        """ play a show """
        # print list
        setEpisodes = self.populate('Play a show...', True)
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
                titre = "Please enter a number..."
                choices = [ "Mark as read", "Mark and Delete", "Back"]
                action = self.printChoices(titre, choices)

                if action == ord('1'):
                    self.nextep.markAsRead(*(episode.ids))
                    self.list_ep.remove(episode)
                elif action == ord('2'):
                    self.nextep.markAsRead(*(episode.ids))
                    episode.removeFile()
                    self.list_ep.remove(episode)


    def down(self):
        """ down a show """
        setEpisodes = self.populate('Down a show...', False)
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

    def display(self, titre, listelt, action, user=False):
        """ display list """
        ####
        ## bug : check COLUMNS and LINES
        ###
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, titre)
        for i in range(len(listelt)):
            if type(listelt[i]) == str:
                elt = listelt[i]
            else:
                elt = listelt[i][0]
            self.screen.addstr(4+i, 4, str(i+1) + ' - ' + elt)
        if user:
            self.screen.addstr(6+i, 4, str(i+2) + ' - other')
        self.screen.addstr(2, 3+len(titre), "")
        self.screen.refresh()
        try:
            num = int(self.screen.getstr(2, 3+len(titre), 2))-1
        except: 
            pass
        else:
            if num >= 0 and num < len(listelt):
                if type(listelt[num]) == list:
                    elt = listelt[num][1:]
                elif type(listelt[num]) == str:
                    elt = [listelt[num]]
                else:
                    elt = [listelt[num][0]]
                action(*elt)
                self.update()
            elif user and num == len(listelt):
                self.screen.clear()
                self.screen.border(0)
                self.screen.addstr(2, 2, 'Enter a name:')
                elt = self.screen.getstr(4, 4, 100)
                action(elt)
                self.update()


    def manageTvShow(self):
        """ manage TvShow """
        titre = "Please enter a number..."
        choices = [ "Add a show", "Remove a show", "Track a show", \
            "Untrack a show", "Back"]
        action = self.printChoices(titre, choices)

        if action == ord('1'):
            titre = choices[0] + '...'
            lsuggest = self.nextep.getSuggestions()
            action = self.nextep.addShow
            self.display(titre, lsuggest, action, True)
        elif action == ord('2'):
            titre = choices[1] + '...'
            lshow = self.nextep.getListShow()
            action = self.nextep.removeShow
            self.display(titre, lshow, action)
        elif action == ord('3'):
            titre = choices[2] + '...'
            luntracked = self.nextep.getUntracked()
            action = self.nextep.trackShow
            self.display(titre, luntracked, action)
        elif action == ord('4'):
            titre = choices[3] + '...'
            ltracked = self.nextep.getTracked()
            action = self.nextep.untrackShow
            self.display(titre, ltracked, action)



