# -*- coding: utf-8 -*-
"""
    generic menu
"""

import curses
import string

hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

_SEPARATOR = 1

class MenuEntry():
    """ create a new entry """

    def __init__(self, name, hotkey_pos=0, action=None):
        """ initialisation """
        self.name = name
        self.hotkey_pos = hotkey_pos
        self.hotkey = name[hotkey_pos]
        self.setsubentry = []
        self.width, self.height = 0, 0
        self.upper_pos, self.left_pos = 0, 0
        self.action = action

    def removeAllEntries(self):
        """ remove all subentry """
        self.setsubentry = []
        self.width, self.height = 0, 0

    def addSubEntry(self, subentry):
        """ add subentry """
        self.setsubentry.append(subentry)
        self.height += 1
        self.width = max(self.width, len(subentry.name))

    def addSeparator(self):
        """ add a separator """
        self.height += 1
        self.setsubentry.append(_SEPARATOR)

    def isActive(self, key):
        """ look if key is hotkey """
        return key == ord(string.upper(self.hotkey)) or \
            key == ord(string.lower(self.hotkey))

    def display(self, screen, upper_pos, left_pos):
        """ print entry in menu """
        self.upper_pos = upper_pos
        self.left_pos = left_pos
        screen.addstr(upper_pos, left_pos, \
            self.name[:self.hotkey_pos], menu_attr)
        screen.addstr(upper_pos, left_pos+len(self.name[:self.hotkey_pos]), \
            self.hotkey, hotkey_attr)
        screen.addstr(upper_pos, left_pos+len(self.name[:self.hotkey_pos])+1, \
            self.name[self.hotkey_pos+1:], menu_attr)
        return left_pos+len(self.name)
    
    def activate(self, screen, scr=None):
        """ open the submenu if exists or call action """
        if self.setsubentry != []:
            newscr = curses.newwin(self.height+2, self.width+4, \
                        self.upper_pos+1, self.left_pos-1)
            newscr.box()
            i = 1
            for subentry in self.setsubentry:
                if subentry == _SEPARATOR:
                    newscr.hline(2, 1, curses.ACS_HLINE, self.width+2)
                else:
                    subentry.display(newscr, i, 2)
                i += 1
            newscr.refresh()
            char = newscr.getch()
            for subentry in self.setsubentry:
                if subentry != _SEPARATOR and subentry.isActive(char):
                    subentry.activate(screen, newscr)
                    break
            screen.refresh()
        elif self.action:
            if scr:
                scr.erase()
            screen.refresh()
            self.action()


class Menu():
    """ create a menu """

    def __init__(self, screen, title=None):
        """ initialisation """
        self.setentry = []
        self.screen = screen
        self.title = title

    def addEntry(self, entry):
        """ add entry """
        self.setentry.append(entry)

    def display(self):
        """ display menu """
        width = self.screen.getmaxyx()[1]
        self.screen.hline(2, 1, curses.ACS_HLINE, width-2)
        left_pos = 2
        for entry in self.setentry:
            left_pos = entry.display(self.screen, 1, left_pos) + 3
        if self.title:
            self.screen.addstr(1, width-len(self.title)-4, self.title, \
                curses.A_STANDOUT)
        self.screen.refresh()

    def action(self, key):
        """ make an action """
        for entry in self.setentry:
            if entry.isActive(key):
                entry.activate(self.screen)
                return True
        return False

