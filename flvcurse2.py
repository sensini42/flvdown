#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses

from curse.menu_gen import Entry, Menu


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

        while not self.close:
            c = self.scr.getkey()
            self.scr.addstr(10, 10, c)
            self.scr.refresh()
            menu.action(c)

    def makemenu(self):
        """ create menu """
        file_menu = Entry('File')
        file_menu.addSubEntry(Entry('Update', action=self.update))
        file_menu.addSeparator()
        file_menu.addSubEntry(Entry('Quit', action=self.quit))
        option_menu = Entry('Options')
        option_menu.addSubEntry(Entry('Settings', action=self.setting))
        option_menu.addSubEntry(Entry('Site order', 6, self.siteorder))
        option_menu.addSubEntry(Entry('Dict bug', action=self.dictbug))
        manage_menu = Entry('Manage TvShow')
        manage_menu.addSubEntry(Entry('Add a show', action=self.add))
        manage_menu.addSubEntry(Entry('Remove a show', action=self.remove))
        manage_menu.addSubEntry(Entry('Track a show', action=self.track))
        manage_menu.addSubEntry(Entry('Untrack a show', action=self.untrack))

        menu = Menu(self.scr, '>>>>> Flvcurse <<<<<')
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


