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
        self.action_menu.removeAllEntries()
        self.action_menu.addSubEntry(MenuEntry('Play', action=self.play))
        self.action_menu.addSubEntry(MenuEntry('Mark as read', \
                action=self.mark))
        self.action_menu.addSubEntry(MenuEntry('Mark and Delete', 9, \
                action=self.delete))
        screen.addstr(1, 1, 'coucou')

    def delete(self):
        pass

    def mark(self):
        pass

    def play(self):
        pass

    def dispdown(self, screen):
        """ display down list """
        self.action_menu.removeAllEntries()
        self.action_menu.addSubEntry(MenuEntry('Down', action=self.down))
        screen.addstr(6, 6, 'bouh')

    def down(self):
        pass

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


