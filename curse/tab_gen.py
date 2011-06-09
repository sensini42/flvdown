# -*- coding: utf-8 -*-

import curses

class TabEntry():
    """ create a new entry tab """

    def __init__(self, name):
        """ initialisation """
        self.name = name
        self.screen = None
        self.visible = None

    def setScreen(self, screen):
        """ set the screen """
        self.screen = screen

    def change(self, direction):
        """ change the current active entry """
        self.visible.change(direction)


class Tab():
    """ create a tab """

    def __init__(self, screen):
        """ initialisation """
        self.setentry = []
        (height, width) = screen.getmaxyx()
        self.screen = screen.subwin(height-4, width-2, 3, 1)
        self.subscreen = screen.subwin(height-9, width-4, 6, 2)
        self.active = None

    def addTab(self, tabentry):
        """ add tab """
        self.setentry.append(tabentry)
        tabentry.setScreen(self.subscreen)
        self.active = len(self.setentry)-1

    def closeTab(self, number):
        """ close a tab """
        self.setentry.remove(self.setentry[number])
        if self.active == len(self.setentry):
            self.active = 0
        self.update()
  
    def closeActiveTab(self):
        """ close active tab """
        self.closeTab(self.active)

    def getActiveTab(self):
        """ return the active tab """
        return self.setentry[self.active]

    def display(self):
        """ display tabs """
        self.update()

    def update(self):
        """ show active tab """
        self.screen.clear()
        self.screen.box()
        (height, width) = self.screen.getmaxyx()
        self.screen.hline(2, 1, curses.ACS_HLINE, width-2)
        left_pos, shift = 2, (width-2)/len(self.setentry)
        for num_entry in range(len(self.setentry)):
            entry = self.setentry[num_entry]
            title = entry.name + " "*(shift-len(entry.name)-2) 
            if num_entry == self.active:
                style = curses.A_STANDOUT | curses.A_BOLD
            else:
                style = curses.A_NORMAL
            self.screen.addstr(1, left_pos, title, style)
            left_pos += shift
            if num_entry < len(self.setentry)-1:
                self.screen.vline(1, left_pos-2, curses.ACS_VLINE, 1)
        self.setentry[self.active].display()
        self.screen.refresh()
        
    def next(self):
        """ display nexttab """
        if self.active >= len(self.setentry)-1:
            self.active = 0
        else:
            self.active += 1
        self.update()

    def select(self, num):
        """ select a tab """
        self.active = num
        self.update()

