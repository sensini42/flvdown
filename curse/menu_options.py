# -*- conding: utf-8 -*-
"""
    options menu entry
"""

from curse.menu_gen import MenuEntry
from curse.tab_settings import TabSettings
from curse.tab_siteorder import TabSiteOrder
from curse.tab_dictbug import TabDictBug

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
        """ dictbug """
        self.parent.tabs.addTab(TabDictBug(self.parent))
        self.parent.tabs.update()

    def siteorder(self):
        """ siteorder """
        self.parent.tabs.addTab(TabSiteOrder(self.parent))
        self.parent.tabs.update()

    def setting(self):
        """ settings """
        self.parent.tabs.addTab(TabSettings(self.parent))
        self.parent.tabs.update()

