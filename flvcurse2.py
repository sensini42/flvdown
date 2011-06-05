#!/usr/bin/python
# -*- coding: utf-8 -*-


from os import chdir as oschdir
from subprocess import Popen as subpopen
from subprocess import PIPE

from nextepisode import NextEpisode
from options import Options

import curses
from curse.menu_gen import MenuEntry, Menu
from curse.tab_gen import TabEntry, Tab
from curse.list_gen import List

import links, aggregators

def min(x, y):
    if x < y:
        return x
    else:
        return y

def max(x, y):
    if x > y:
        return x
    else:
        return y


class Curse():
    """ curse version """

    def __init__(self, screen, options, nextep):
        """ initialisation """

        self.scr = screen
        self.close = False

        self.options = options
        oschdir(self.options.conf['base_directory'])
        self.nextep = nextep
        self.nextep.update(self.options.dict_bug)
        self.list_ep = self.nextep.getList()

        (y, x) = screen.getmaxyx()
        self.scr = screen.subwin(y, x, 0, 0)
        self.scr.box()

        menu = self.makemenu()
        menu.display()

        self.tabs = self.maketabs()
        self.tabs.display()

        while not self.close:
            c = self.scr.getch()
            if c == ord('@'):
                self.tabs.next()
            elif c == 65:#UP
                self.visible.change(0)
            elif c == 66:#DOWN
                self.visible.change(1)
            elif c == 10:#ENTER
                self.action_menu.setsubentry[0].action()
            else:
                menu.action(c)
                
                

    def maketabs(self):
        """ create tab """
        playing_tab = TabEntry('Playing', self.dispplay)
        downloading_tab = TabEntry('Downloading', self.dispdown)
        
        tabs = Tab(self.scr)
        tabs.addTab(playing_tab)
        tabs.addTab(downloading_tab)
        return tabs

    def episodes(self, condition):
        """ create list_episode """
        setShows = []
        setEpisodes = []
        for episode in self.list_ep:
            if episode.isOnDisk == condition and \
                episode.tvshowSpace not in setShows:
                  setShows.append(episode.tvshowSpace)
                  setEpisodes.append(episode)
        return setEpisodes

    def dispplay(self, screen):
        """ display play list """
        self.action_menu.removeAllEntries()
        self.action_menu.addSubEntry(MenuEntry('Play', action=self.play))
        self.action_menu.addSubEntry(MenuEntry('Mark as read', \
                action=self.mark))
        self.action_menu.addSubEntry(MenuEntry('Mark and Delete', 9, \
                action=self.delete))

        self.setEpi = self.episodes(True)
        self.visible = List(screen, [x.getBaseName() for x in self.setEpi])
        self.visible.display(10, 4, 15)


    def delete(self):
        """ mark and delete """
        episode = self.setEpi[self.visible.active]
        episode.removeFile()
        self.nextep.markAsRead(*(episode.ids))
        self.list_ep.remove(episode)
        self.tabs.update()

    def mark(self):
        """ mark """
        episode = self.setEpi[self.visible.active]
        self.nextep.markAsRead(*(episode.ids))
        self.list_ep.remove(episode)
        self.tabs.update()

    def play(self):
        """ play a show """
        episode = self.setEpi[self.visible.active]
        cmd = self.options.conf['player'] + ' ' + episode.getVideoName()
        subpopen(cmd, shell=True, stderr=PIPE, stdout=PIPE)

    def dispdown(self, screen):
        """ display down list """
        self.action_menu.removeAllEntries()
        self.action_menu.addSubEntry(MenuEntry('Down', action=self.down))
        
        self.setEpi = self.episodes(False)
        self.visible = List(screen, [x.getBaseName() for x in self.setEpi])
        self.visible.display(10, 4, 15)

    def error(self, msg):
        """ print an error """
        (genheight, genwidth) = self.scr.getmaxyx()
        screen = curses.newwin(3, len(msg)+4, (genheight-10)/2, \
                    (genwidth-len(msg))/2)
        screen.box()
        screen.addstr(1, 2, msg, curses.A_STANDOUT)
        screen.getch()
        screen.erase()
        self.scr.refresh()

    def down(self):
        """ down a show """
        episode = self.setEpi[self.visible.active]
        url, dest, cook = links.flvdown(episode, "")
        if url:
            try:
                links.getFile(url, dest, cook)
            except:
                self.error('down error')
            else:
                episode.isOnDisk = True
        else:
            self.error('url not found')

    def makemenu(self):
        """ create menu """
        self.action_menu = MenuEntry('Actions')

        option_menu = MenuEntry('Options')
        option_menu.addSubEntry(MenuEntry('Settings', action=self.setting))
        option_menu.addSubEntry(MenuEntry('Site order', 6, self.siteorder))
        option_menu.addSubEntry(MenuEntry('Dict bug', action=self.dictbug))

        manage_menu = MenuEntry('Manage TvShow')
        manage_menu.addSubEntry(MenuEntry('Add a show', action=self.add))
        manage_menu.addSubEntry(MenuEntry('Remove a show', action=self.remove))
        manage_menu.addSubEntry(MenuEntry('Track a show', action=self.track))
        manage_menu.addSubEntry(MenuEntry('Untrack a show', \
                action=self.untrack))

        update_menu = MenuEntry('Update', action=self.update)
        quit_menu = MenuEntry('Quit', action=self.quit)

        menu = Menu(self.scr, ' >>>>> Flvcurse <<<<< ')
        menu.addEntry(self.action_menu)
        menu.addEntry(option_menu)
        menu.addEntry(manage_menu)
        menu.addEntry(update_menu)
        menu.addEntry(quit_menu)
        return menu

    def dialog(self, title, list_elt, action, askuser=False):
        """ create dialog """
        (genheight, genwidth) = self.scr.getmaxyx()
        if askuser:
            list_elt.append('other')
        # check max_width
        max_width = len(title) 
        list_tmp = []
        for elt in list_elt:
            if type(elt) != str:
                elt = elt[0]
            list_tmp.append(elt)
            max_width = max(max_width, len(elt))
        max_width += 4
        # check height
        height = 6 + min(6, len(list_elt))
        screen = curses.newwin(height, max_width, (genheight-height-7)/2, \
                    (genwidth-max_width)/2)
        screen.box()
        screen.addstr(1, (max_width-len(title))/2, title, curses.A_BOLD)
        screen.hline(2, 1, curses.ACS_HLINE, max_width-2)
        listdisp = List(screen, list_tmp)
        listdisp.display(2, 4, 6)
        ok = True
        while ok:
            c = screen.getch()
            if c == 65:#UP
                listdisp.change(0)
            elif c == 66:#DOWN
                listdisp.change(1)
            elif c == 10:#ENTER
                if len(list_elt) != 0:
                    if askuser and listdisp.active == len(list_elt)-1:
                        curses.curs_set(1)
                        curses.nocbreak()
                        curses.echo()
                        screen2 = curses.newwin(3, genwidth-6, \
                            (genheight-3)/2, 3)
                        screen2.box()
                        screen2.addstr(1, 2, 'name: ')
                        name = screen2.getstr()
                        curses.noecho()
                        curses.curs_set(0)
                        curses.cbreak()
                        if name != "": action(name)
                        self.update()
                    else:
                        if type(list_elt[listdisp.active]) == list:
                            elt = list_elt[listdisp.active][1:]
                        elif type(list_elt[listdisp.active]) == str:
                            elt = [list_elt[listdisp.active]]
                        else:
                            elt = [list_elt[listdisp.active][0]]
                        action(*elt)
                        self.update()
                ok = False
            elif c == ord('q') or c == ord('Q'):
                ok = False
        screen.erase()
        self.scr.refresh()
        

    def untrack(self):
        title = 'untrack'
        list_elt = self.nextep.getTracked()
        action = self.nextep.untrackShow
        self.dialog(title, list_elt, action)

    def track(self):
        title = 'track'
        list_elt = self.nextep.getUntracked()
        action = self.nextep.trackShow
        self.dialog(title, list_elt, action)

    def remove(self):
        title = 'remove'
        list_elt = self.nextep.getListShow()
        action = self.nextep.removeShow
        self.dialog(title, list_elt, action)

    def add(self):
        title = 'add a show'
        list_elt = self.nextep.getSuggestions()
        action = self.nextep.addShow
        self.dialog(title, list_elt, action, True)

    def dictbug(self):
        self.scr.addstr(6, 6, "dictbug")

    def siteorder(self):
        self.scr.addstr(6, 6, "siteorder")

    def setting(self):
        self.scr.addstr(6, 6, "setting")

    def update(self):
        """ update """
        oschdir(self.options.conf['base_directory'])
        self.nextep.update(self.options.dict_bug, \
            self.options.conf['login'], self.options.conf['password'])
        self.list_ep = self.nextep.getList()

    def quit(self):
        self.close = True
    

def main():
    """ main """

    ##config
    options = Options()
    if options.error:
        print "check config"

    ##nextep
    nextep = NextEpisode(options.conf['login'], options.conf['password'], \
                options.dict_bug)

    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        Curse(stdscr, options, nextep)
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
    except:
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()


