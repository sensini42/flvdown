# -*- coding: utf-8 -*-
"""
    dict bug tab
"""

import curses
from curse.tab_gen import TabEntry
from curse.menu_gen import MenuEntry
from curse.list_gen import List 

import aggregators

class TabDictBug(TabEntry):
    """ setting tab """

    def __init__(self, parent):
        """ initialisation """
        TabEntry.__init__(self, 'Dict Bug')
        self.parent = parent
        self.dictbug = {}
        self.dictbug.update(self.parent.options.dict_bug)
        self.dico = None

    def display(self):
        """ display the tab """
        self.screen.erase()
        self.changeMenu()
        self.dico = []
        for key in self.dictbug.keys():
            tmp = {}
            tmp.update(self.dictbug[key])
            if '_'.join(key.split(' ')) != tmp['default']:
                self.dico.append('_'.join(key.split(' ')) + \
                    '  --  default  --  ' + tmp['default'])
            del tmp['default']
            for key2 in tmp.keys():
                self.dico.append('_'.join(key.split(' ')) + \
                    '  --  ' + key2 + '  --  ' + tmp[key2])
        self.visible = List(self.screen, self.dico, True)
        self.visible.display(10, 4, 15)

    def changeMenu(self):
        """ change entry in action """
        self.parent.action_menu.removeAllEntries()
        self.parent.action_menu.addSubEntry(MenuEntry('Modify', \
                action=self.modify))
        self.parent.action_menu.addSubEntry(MenuEntry('Add', \
                action=self.add))
        self.parent.action_menu.addSubEntry(MenuEntry('Delete', \
                action=self.delete))
        self.parent.action_menu.addSubEntry(MenuEntry('Save', \
                action=self.savesetting))
        self.parent.action_menu.addSubEntry(MenuEntry('Close', \
                action=self.parent.tabs.closeActiveTab))

    def user(self, listshow, listsite, userentry, modify):
        """ add/modify an entry """
        (genheight, genwidth) = self.parent.scr.getmaxyx()
        width = 0
        for i in listshow + listsite:
            width = max(width, len(i))
        width += 10
        scr = curses.newwin(8, width, (genheight-15)/2, (genwidth-width)/2)
        scr.box()
        List(scr, ['show:', 'site:', ' bug:'], False).display(2, 1, 3)
        lshow = List(scr, listshow, False)
        lshow.display(8, 1, 1)
        lsite = List(scr, listsite, False)
        lsite.display(8, 2, 1)
        scr.addstr(3, 8, userentry)
        scr.addstr(5, (width-4)/2, 'save', curses.A_STANDOUT)
        modi = 3
        scr.refresh()
        scr.keypad(1)
        modify.append(3)
        char = 0
        change = True
        while change and char != 27:
            char = scr.getch()
            if char == 9: #TAB
                if modi == 3: 
                    scr.addstr(5, (width-4)/2, 'save')
                    if 1 in modify:
                        lshow.isactive = True
                        lshow.update()
                        modi = 0
                    else:
                        scr.addstr(3, 8, ' '*(width-10))
                        scr.addstr(3, 8, userentry, curses.A_STANDOUT)
                        scr.move(3, 8)
                        curses.curs_set(1)
                        modi = 2
                elif modi == 2:
                    curses.curs_set(0)
                    scr.addstr(3, 8, userentry)
                    modi = 3
                    scr.addstr(5, (width-4)/2, 'save', curses.A_STANDOUT)
                elif modi == 1:
                    lsite.isactive = False
                    lsite.update()
                    scr.addstr(3, 8, ' '*(width-10))
                    scr.addstr(3, 8, userentry, curses.A_STANDOUT)
                    scr.move(3, 8)
                    curses.curs_set(1)
                    modi = 2
                elif modi == 0:
                    lshow.isactive = False
                    lshow.update()
                    lsite.isactive = True
                    lsite.update()
                    modi = 1
            elif char == curses.KEY_UP:
                if modi == 0:
                    lshow.change(0)
                elif modi == 1:
                    lsite.change(0)
            elif char == curses.KEY_DOWN:
                if modi == 0:
                    lshow.change(1)
                elif modi == 1:
                    lsite.change(1)
            elif char == 10:#ENTER
                if modi == 3:
                    show = lshow.list_elt[lshow.active]
                    site = lsite.list_elt[lsite.active]
                    if userentry != "":
                        self.dictbug[' '.join(show.split('_'))][site] = \
                                userentry 
                    change = False
                elif modi == 2:
                    curses.echo()
                    scr.addstr(3, 8, ' '*(width-10), curses.A_STANDOUT)
                    userentry = scr.getstr(3, 8)
                    scr.addstr(3, 8, ' '*(width-10))
                    scr.addstr(3, 8, userentry, curses.A_STANDOUT)
                    curses.noecho()
        curses.curs_set(0)
        scr.erase()
        self.screen.refresh()
        self.display()

    def add(self):
        """ add a value """
        listsites = ['default', 'tvsubtitles']
        for i in aggregators.__all__:
            listsites.append(i)
        listshows = self.parent.nextep.getListShow()
        self.user(listshows, listsites, "", [0, 1, 2])

    def modify(self):
        """ modify a value """
        info = self.dico[self.visible.active].split('  --  ')
        self.user([info[0]], [info[1]], info[2], [2])

    def delete(self):
        """ delete an entry """
        info = self.dico[self.visible.active].split('  --  ')
        if info[1] == 'default':
            self.dictbug[' '.join(info[0].split('_'))]['default'] = info[0]
        else:
            del self.dictbug[' '.join(info[0].split('_'))][info[1]]
        self.display()

    def savesetting(self):
        """ save the settings """
        self.parent.options.dict_bug = {}
        self.parent.options.dict_bug.update(self.dictbug)
        self.parent.options.saveConf()


