# -*- coding: utf-8 -*-

import curses
from curse.tab_gen import TabEntry
from curse.menu_gen import MenuEntry
from curse.list_gen import List 

class TabSettings(TabEntry):
    """ setting tab """

    def __init__(self, parent):
        """ initialisation """
        TabEntry.__init__(self, 'Settings', None)
        self.parent = parent

    def display(self):
        """ display the tab """
        self.changeMenu()
        self.listkeys = self.parent.options.conf.keys()
        listvalues = []
        for key in self.listkeys:
            listvalues.append(self.parent.options.conf[key])
        self.visible2 = List(self.screen, self.listkeys, False)
        self.visible2.display(10, 4, 15)
        self.visible = List(self.screen, listvalues, True)
        self.visible.display(28, 4, 15)

    def changeMenu(self):
        """ change entry in action """
        self.parent.action_menu.removeAllEntries()
        self.parent.action_menu.addSubEntry(MenuEntry('Change value', 7, \
                action=self.changevalue))
        self.parent.action_menu.addSubEntry(MenuEntry('Save', \
                action=self.savesetting))
        self.parent.action_menu.addSubEntry(MenuEntry('Close', \
                action=self.parent.tabs.closeActiveTab))

    def changevalue(self):
        """ change a setting value """
        (y, x, l) = self.visible.posend
        width = self.screen.getmaxyx()[1]-32
        self.screen.addstr(y, x, ' '*width)
        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        self.screen.move(y, x)
        name = self.screen.getstr()
        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()
        if name!='': self.visible.list_elt[self.visible.active] = name
        self.visible.update()

    def savesetting(self):
        """ save the settings """
        opt = {}
        for i in range(len(self.listkeys)):
            opt[self.listkeys[i]] = self.visible.list_elt[i]
        self.parent.options.conf.update(opt)
        self.parent.options.saveConf()




