#!/usr/bin/python
# -*- coding: utf-8 -*-


from os import chdir as oschdir

from util.nextepisode import NextEpisode
from util.options import Options

import curses
from curse.menu_gen import MenuEntry, Menu
from curse.menu_options import MenuOptions
from curse.menu_managetvshow import MenuManage
from curse.tab_gen import Tab
from curse.tab_playing import TabPlaying
from curse.tab_downloading import TabDownloading

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

        self.scr.keypad(1)
        while not self.close:
            c = self.scr.getch()
            if c == ord('@'):
                self.tabs.next()
            elif c == curses.KEY_UP:
                self.tabs.getActiveTab().change(0)
            elif c == curses.KEY_DOWN:
                self.tabs.getActiveTab().change(1)
            elif c == 10:#ENTER
                self.action_menu.setsubentry[0].action()
            else:
                menu.action(c)

    def maketabs(self):
        """ create tab """
        tabs = Tab(self.scr)
        tabs.addTab(TabPlaying(self))
        tabs.addTab(TabDownloading(self))
        return tabs

    def makemenu(self):
        """ create menu """
        menu = Menu(self.scr, ' >>>>> Flvcurse <<<<< ')
        self.action_menu = MenuEntry('Actions')
        menu.addEntry(self.action_menu)
        menu.addEntry(MenuOptions(self))
        menu.addEntry(MenuManage(self))
        menu.addEntry(MenuEntry('Update', action=self.update))
        menu.addEntry(MenuEntry('Quit', action=self.quit))
        return menu

    def update(self):
        """ update """
        oschdir(self.options.conf['base_directory'])
        self.nextep.update(self.options.dict_bug, \
            self.options.conf['login'], self.options.conf['password'])
        self.list_ep = self.nextep.getList()
        self.tabs.update()

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


