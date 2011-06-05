#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses

from curse.menu_gen import MenuEntry, Menu
from curse.tab_gen import TabEntry, Tab


class Curse():
    """ curse version """

    def __init__(self, screen):
        """ initialisation """

        self.scr = screen
        self.close = False

        (y, x) = screen.getmaxyx()
        self.scr = screen.subwin(y, x, 0, 0)
        self.scr.box()

        menu = self.makemenu()
        menu.display()

        tabs = self.maketabs()
        tabs.display()

        while not self.close:
            c = self.scr.getkey()
            if not menu.action(c):
                if c == '@':
                    tabs.next()
                

    def maketabs(self):
        """ create tab """
        playing_tab = TabEntry('Playing', self.dispplay)
        downloading_tab = TabEntry('Downloading', self.dispdown)
        
        tabs = Tab(self.scr)
        tabs.addTab(playing_tab)
        tabs.addTab(downloading_tab)
        return tabs

    def dispplay(self, screen):
        """ display play list """
        screen.addstr(1, 1, 'coucou')

    def dispdown(self, screen):
        """ display down list """
        screen.addstr(6, 6, 'bouh')

    def makemenu(self):
        """ create menu """
        file_menu = MenuEntry('File')
        file_menu.addSubEntry(MenuEntry('Update', action=self.update))
        file_menu.addSeparator()
        file_menu.addSubEntry(MenuEntry('Quit', action=self.quit))

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

        menu = Menu(self.scr, ' >>>>> Flvcurse <<<<< ')
        menu.addEntry(file_menu)
        menu.addEntry(option_menu)
        menu.addEntry(manage_menu)
        return menu

    def untrack(self):
        self.scr.addstr(6, 6, "untrack")

    def track(self):
        self.scr.addstr(6, 6, "track")

    def remove(self):
        self.scr.addstr(6, 6, "remove")

    def add(self):
        self.scr.addstr(6, 6, "add")

    def dictbug(self):
        self.scr.addstr(6, 6, "dictbug")

    def siteorder(self):
        self.scr.addstr(6, 6, "siteorder")

    def setting(self):
        self.scr.addstr(6, 6, "setting")

    def update(self):
        self.scr.addstr(6, 6, "update")

    def quit(self):
        self.close = True
    

def main():
    """ main """

    #config
    #options = Options()
    #if options.error:
    #    print "check config"

    #nextep
    #nextep = NextEpisode(options.conf['login'], options.conf['password'], \
    #            options.dict_bug)

    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        Curse(stdscr)#, options, nextep)
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


