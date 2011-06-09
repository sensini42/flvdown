# -*- conding: utf-8 -*-

import curses
from curse.menu_gen import MenuEntry

from curse.list_gen import List

class MenuManage(MenuEntry):
    """ create options menu """

    def __init__(self, parent):
        """ initialisation """
        MenuEntry.__init__(self, 'Manage TvShow')
        self.parent = parent

        self.addSubEntry(MenuEntry('Add a show', action=self.add))
        self.addSubEntry(MenuEntry('Remove a show', action=self.remove))
        self.addSubEntry(MenuEntry('Track a show', action=self.track))
        self.addSubEntry(MenuEntry('Untrack a show', \
                action=self.untrack))

    def dialog(self, title, list_elt, action, askuser=False):
        """ create dialog """
        (genheight, genwidth) = self.parent.scr.getmaxyx()
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
        listdisp.display(2, 4, min(6, len(list_elt)))
        screen.keypad(1)
        c = 0
        while c != 27 and c != 10:#ECHAP and ENTER
            c = screen.getch()
            if c == curses.KEY_UP:#UP
                listdisp.change(0)
            elif c == curses.KEY_DOWN:#DOWN
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
                        self.parent.update()
        screen.erase()
        self.parent.scr.refresh()
        

    def untrack(self):
        title = 'untrack'
        list_elt = self.parent.nextep.getTracked()
        action = self.parent.nextep.untrackShow
        self.dialog(title, list_elt, action)

    def track(self):
        title = 'track'
        list_elt = self.parent.nextep.getUntracked()
        action = self.parent.nextep.trackShow
        self.dialog(title, list_elt, action)

    def remove(self):
        title = 'remove'
        list_elt = self.parent.nextep.getListShow()
        action = self.parent.nextep.removeShow
        self.dialog(title, list_elt, action)

    def add(self):
        title = 'add a show'
        list_elt = self.parent.nextep.getSuggestions()
        action = self.parent.nextep.addShow
        self.dialog(title, list_elt, action, True)

