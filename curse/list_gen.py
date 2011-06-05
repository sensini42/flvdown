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

    def display(self, left=None, up=None, maxline=None):
        """ display the list """
        if maxline: self.pos[2] = maxline
        if up: self.pos[1] = up
        if left: self.pos[0] = left
        self.active = 0
        self.deb = 0
        self.update()

    def update(self):
        """ update """
        i = 0
        for num_elt in range(self.deb, len(self.list_elt)):
            if (i == 0 and self.deb != 0) or \
              (i == self.pos[2]-1 and num_elt != len(self.list_elt)-1):
                self.screen.addstr(self.pos[1]+i, self.pos[0], '...')
                clr = ' '*(self.screen.getmaxyx()[1]-5-self.pos[0])
                self.screen.addstr(self.pos[1]+i, self.pos[0]+3, clr)
            else:
                if self.isactive and num_elt == self.active: 
                    style = curses.A_STANDOUT
                else: 
                    style = curses.A_NORMAL
                elt = self.list_elt[num_elt]
                clr = ' '*(self.screen.getmaxyx()[1]-2-self.pos[0]-len(elt))
                self.screen.addstr(self.pos[1]+i, self.pos[0], elt, style)
                self.screen.addstr(self.pos[1]+i, self.pos[0]+len(elt), clr)
            i += 1
            if i == self.pos[2]:
                break
        self.screen.refresh()

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




