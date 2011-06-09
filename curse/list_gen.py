# -*- coding: utf-8 -*-

import curses

UP, DOWN = 0, 1


class List():
    """ create a list with interaction """

    def __init__(self, screen, list_elt, isactive=True):
        """ initialisation """
        self.screen = screen
        self.list_elt = list_elt
        self.pos = [1, 1, self.screen.getmaxyx()[0]-2]
        self.isactive = isactive
        self.active = 0
        self.deb = 0
        self.posend = None

    def display(self, left=None, up=None, maxline=None):
        """ display the list """
        if maxline: self.pos[2] = min(maxline, self.pos[2])
        if up: self.pos[1] = up
        if left: self.pos[0] = left
        self.active = 0
        self.deb = 0
        self.update()

    def update(self):
        """ update """
        if len(self.list_elt) > 0:
            clr = ' '*(self.screen.getmaxyx()[1]-2-self.pos[0])
            if self.pos[2]==1:
                elt = self.list_elt[self.active]
                if self.isactive:
                    style = curses.A_STANDOUT
                    self.posend = (self.pos[1], self.pos[0], len(elt))
                else: 
                    style = curses.A_NORMAL
                self.screen.addstr(self.pos[1], self.pos[0], clr)
                self.screen.addstr(self.pos[1], self.pos[0], elt, style)
            else:
                i = 0
                for num_elt in range(self.deb, len(self.list_elt)):
                    if (i == 0 and self.deb != 0) or \
                      (i == self.pos[2]-1 and num_elt != len(self.list_elt)-1):
                        self.screen.addstr(self.pos[1]+i, self.pos[0], clr)
                        self.screen.addstr(self.pos[1]+i, self.pos[0], '...')
                    else:
                        elt = self.list_elt[num_elt]
                        if self.isactive and num_elt == self.active: 
                            style = curses.A_STANDOUT
                            self.posend = (self.pos[1]+i, self.pos[0], len(elt))
                        else: 
                            style = curses.A_NORMAL
                        self.screen.addstr(self.pos[1]+i, self.pos[0], clr)
                        self.screen.addstr(self.pos[1]+i, self.pos[0], elt, \
                              style)
                    i += 1
                    if i == self.pos[2]:
                        break
                for j in range(i, self.pos[2]):
                    self.screen.addstr(self.pos[1]+j, self.pos[0], clr)
        self.screen.refresh()

    def swap(self, direction):
        """ swap active elt """
        if not self.isactive:
            return
        oldpos = self.active
        if direction == UP:
            if self.active == 0:
                self.active = len(self.list_elt)-1
                self.deb = len(self.list_elt)-self.pos[2]
                if self.deb < 0: self.deb = 0
            else: 
                self.active -= 1
                if self.active == self.deb and \
                  self.active != 0:
                    self.deb -= 1
        elif direction == DOWN:
            if self.active == len(self.list_elt)-1: 
                self.active = 0
                self.deb = 0
            else: 
                self.active += 1
                if self.active == self.deb+self.pos[2]-1 and \
                  self.active != len(self.list_elt)-1:
                    self.deb += 1
        newpos = self.active
        self.list_elt.insert(newpos, self.list_elt.pop(oldpos))
        self.update()

    def change(self, direction):
        """ change active elt """
        if not self.isactive:
            return
        if direction == UP:
            if self.active == 0:
                self.active = len(self.list_elt)-1
                self.deb = len(self.list_elt)-self.pos[2]
                if self.deb < 0: self.deb = 0
            else: 
                self.active -= 1
                if self.active == self.deb and \
                  self.active != 0:
                    self.deb -= 1
        elif direction == DOWN:
            if self.active == len(self.list_elt)-1: 
                self.active = 0
                self.deb = 0
            else: 
                self.active += 1
                if self.active == self.deb+self.pos[2]-1 and \
                  self.active != len(self.list_elt)-1:
                    self.deb += 1
        self.update()




