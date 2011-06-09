# -*- conding: utf-8 -*-

from curse.menu_gen import MenuEntry
from curse.tab_settings import TabSettings

class MenuOptions(MenuEntry):
    """ create options menu """

    def __init__(self, parent):
        """ initialisation """
        MenuEntry.__init__(self, 'Options')
        self.parent = parent

        self.addSubEntry(MenuEntry('Settings', action=self.setting))
        self.addSubEntry(MenuEntry('Site order', 6, self.siteorder))
        self.addSubEntry(MenuEntry('Dict bug', action=self.dictbug))

    def dictbug(self):
        self.parent.scr.addstr(6, 6, "dictbug")

    def siteorder(self):
        self.parent.scr.addstr(6, 6, "siteorder")

    def setting(self):
        """ settings """
        settings_tab = TabSettings(self.parent)
        self.parent.tabs.addTab(settings_tab)
        self.parent.tabs.update()
