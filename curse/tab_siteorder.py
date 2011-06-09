# -*- coding: utf-8 -*-

import curses
from curse.tab_gen import TabEntry
from curse.menu_gen import MenuEntry
from curse.list_gen import List 

class TabSiteOrder(TabEntry):
    """ setting tab """

    def __init__(self, parent):
        """ initialisation """
        TabEntry.__init__(self, 'Site Order')
        self.parent = parent

    def display(self):
        """ display the tab """
        self.changeMenu()
        self.listsites = self.parent.options.list_site

        self.visible = List(self.screen, self.listsites, True)
        self.visible.display(10, 4, 15)

    def changeMenu(self):
        """ change entry in action """
        self.parent.action_menu.removeAllEntries()
        self.parent.action_menu.addSubEntry(MenuEntry('Change order', 7, \
                action=self.changeorder))
        self.parent.action_menu.addSubEntry(MenuEntry('Save', \
                action=self.savesetting))
        self.parent.action_menu.addSubEntry(MenuEntry('Close', \
                action=self.parent.tabs.closeActiveTab))

    def changeorder(self):
        """ change a setting value """
        c = 0
        while c != 10: #ENTER
            c = self.parent.scr.getch()
            if c == curses.KEY_UP:
                self.visible.swap(0)
            elif c == curses.KEY_DOWN:
                self.visible.swap(1)
            elif c == 10:
                self.listsites = self.visible.list_elt

    def savesetting(self):
        """ save the settings """
        self.parent.options.list_site = self.listsites
        self.parent.options.saveConf()




