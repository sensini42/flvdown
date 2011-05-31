#!/usr/bin/python
# -*- coding: utf-8 -*-
""" curses version """

from os import chdir as oschdir
from os import system as ossystem
import curses
import threads, links, aggregators

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
            choices = [ "Play a show", "Download a show", "Options", \
                "Manage TvShow", "Update", "Exit"]
            action = self.printChoices(choices)

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
        
    def listChoices(self, choices, line, column):
        """ print list choices """
        for i in range(len(choices)):
            self.screen.addstr(line+i, column, str(i+1) + " - " + choices[i])

    def printChoices(self, choices):
        """ print list choices """
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, 'Please enter a number...')
        self.listChoices(choices, 4, 4)
        self.screen.addstr(2, 27, "")
        self.screen.refresh()
        return self.screen.getch()


    def printEpisodes(self, titre, condition):
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
        setEpisodes = self.printEpisodes('Play a show...', True)
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
                choices = [ "Mark as read", "Mark and Delete", "Back"]
                action = self.printChoices(choices)

                if action == ord('1'):
                    self.nextep.markAsRead(*(episode.ids))
                    self.list_ep.remove(episode)
                elif action == ord('2'):
                    self.nextep.markAsRead(*(episode.ids))
                    episode.removeFile()
                    self.list_ep.remove(episode)


    def down(self):
        """ down a show """
        setEpisodes = self.printEpisodes('Down a show...', False)
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

    def settings(self):
        """ settings pane """
        listkeys = self.options.conf.keys()

        action = '0'
        while action != ord('2') and action != ord('3'):

            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(2, 2, 'Settings')
            num = 0
            opt = {}
            for key in listkeys:
                opt[key] = self.options.conf[key]
                self.screen.addstr(4+num, 6, key)
                if key != 'password':
                    self.screen.addstr(4+num, 21, self.options.conf[key])
                else:
                    self.screen.addstr(4+num, 21, "******")
                num += 1
            self.screen.addstr(5+num, 4, '1 - Modify   2 - Save   3 - Back   ')

            action = self.screen.getch()

            if action == ord('1'):
                self.listChoices(listkeys, 6+num, 6)
                action2 = '0'
                while action2 <= ord('0') or action2 >= ord('5'):
                    action2 = self.screen.getch()
                if action2 == ord('1'):
                    self.screen.move(4, 21)
                    self.screen.clrtoeol()
                    value = self.screen.getstr()
                    opt[listkeys[0]] = value
                elif action2 == ord('2'):
                    self.screen.move(5, 21)
                    self.screen.clrtoeol()
                    value = self.screen.getstr()
                    opt[listkeys[1]] = value
                elif action2 == ord('3'):
                    self.screen.move(6, 21)
                    self.screen.clrtoeol()
                    value = self.screen.getstr()
                    opt[listkeys[2]] = value
                elif action2 == ord('4'):
                    self.screen.move(7, 21)
                    self.screen.clrtoeol()
                    value = self.screen.getstr()
                    opt[listkeys[3]] = value
                    
            elif action == ord('2'):
                self.options.conf.update(opt)
                self.options.saveConf()
                self.update()


    def siteorder(self):
        """ site order pane """
        listsites = self.options.list_site

        action = '0'
        while action != ord('2') and action != ord('3'):
            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(2, 2, 'Site order')
            self.listChoices(listsites, 4, 4)
            self.screen.addstr(5+len(listsites), 6, \
                '1 - Modify   2 - Save   3 - Back   ')

            action = self.screen.getch()

            if action == ord('1'):
                # selection
                self.screen.addstr(6+len(listsites), 8, 'select a site: ')
                (y, x) = self.screen.getyx()
                oldpos = '0' 
                while not oldpos.isdigit() or \
                    int(oldpos) <= 0 or int(oldpos) > len(listsites):
                  self.screen.addstr(y, x, "     ")
                  self.screen.move(y, x)
                  oldpos = self.screen.getstr()
                oldpos = int(oldpos) - 1
                # new position
                self.screen.addstr(7+len(listsites), 8, 'new position: ')
                (y, x) = self.screen.getyx()
                newpos = '0'
                while not newpos.isdigit() or \
                    int(newpos) <= 0 or int(newpos) > len(listsites):
                  self.screen.addstr(y, x, "     ")
                  self.screen.move(y, x)
                  newpos = self.screen.getstr()
                newpos = int(newpos) - 1
                # change
                listsites.insert(newpos, listsites.pop(oldpos))
            elif action == ord('2'):
                self.options.list_site = listsites
                self.options.saveConf()


    def dictbug(self):
        """ dict bug pane """
        dictbug = {}
        dictbug.update(self.options.dict_bug)

        listsites = ['default', 'tvsubtitles']
        for i in aggregators.__all__:
            listsites.append(i)

        listshows = self.nextep.getListShow()

        action = '0'
        while action != ord('3') and action != ord('4'):
            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(2, 2, 'Dict bug')
            dico = []
            for key in dictbug.keys():
                tmp = {}
                tmp.update(dictbug[key])
                if '_'.join(key.split(' ')) != tmp['default']:
                    dico.append('_'.join(key.split(' ')) +  \
                      '  --  default  --  ' + tmp['default'])
                del tmp['default']
                for key2 in tmp.keys():
                    dico.append('_'.join(key.split(' ')) +  \
                      '  --  ' + key2 + '  --  ' + tmp[key2])
            self.listChoices(dico, 4, 4)
            self.screen.addstr(5+len(dico), 6, \
                '1 - Add/Modify   2 - Delete   3 - Save   4 - Back   ')

            action = self.screen.getch()

            if action == ord('1'):
                self.screen.addstr(6+len(dico), 8, 'enter a show: ')
                (y, x) = self.screen.getyx()
                show = ''
                while not show in listshows:
                    self.screen.addstr(y, x, "                 ")
                    self.screen.move(y, x)
                    show = self.screen.getstr()
                self.screen.addstr(7+len(dico), 8, 'enter a site: ')
                (y, x) = self.screen.getyx()
                site = ''
                while not site in listsites:
                    self.screen.addstr(y, x, "                 ")
                    self.screen.move(y, x)
                    site = self.screen.getstr()
                self.screen.addstr(8+len(dico), 8, 'enter dict bug: ')
                db = self.screen.getstr()
                dictbug[' '.join(show.split('_'))][site] = db
            elif action == ord('2'):
                self.screen.addstr(6+len(dico), 8, 'select a dictbug: ')
                (y, x) = self.screen.getyx()
                select = '0' 
                while not select.isdigit() or \
                    int(select) <= 0 or int(select) > len(dico):
                  self.screen.addstr(y, x, "     ")
                  self.screen.move(y, x)
                  select = self.screen.getstr()
                select = int(select) - 1
                info = dico[select].split('  --  ')
                if info[1] == 'default':
                    dictbug[' '.join(info[0].split('_'))]['default'] = info[0]
                else:
                    del dictbug[' '.join(info[0].split('_'))][info[1]]
            elif action == ord('3'):
                self.options.dict_bug = {}
                self.options.dict_bug.update(dictbug)
                self.options.saveConf()
                self.update()
            
    
    def chgoptions(self):
        """ options list """
        choices = [ "Settings", "Site order", "Dict Bug", "Back"]
        action = self.printChoices(choices)

        if action == ord('1'):
            self.settings()
        elif action == ord('2'):
            self.siteorder()
        elif action == ord('3'):
            self.dictbug()


    def printShows(self, titre, listelt, action, user=False):
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
        choices = [ "Add a show", "Remove a show", "Track a show", \
            "Untrack a show", "Back"]
        action = self.printChoices(choices)

        if action == ord('1'):
            titre = choices[0] + '...'
            lsuggest = self.nextep.getSuggestions()
            action = self.nextep.addShow
            self.printShows(titre, lsuggest, action, True)
        elif action == ord('2'):
            titre = choices[1] + '...'
            lshow = self.nextep.getListShow()
            action = self.nextep.removeShow
            self.printShows(titre, lshow, action)
        elif action == ord('3'):
            titre = choices[2] + '...'
            luntracked = self.nextep.getUntracked()
            action = self.nextep.trackShow
            self.printShows(titre, luntracked, action)
        elif action == ord('4'):
            titre = choices[3] + '...'
            ltracked = self.nextep.getTracked()
            action = self.nextep.untrackShow
            self.printShows(titre, ltracked, action)



