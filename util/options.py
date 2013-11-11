# -*- coding: utf-8 -*-
""" options """

import sys

from os import path as ospath
from os import mkdir as osmkdir

class Options():
    """ manage options """

    def __init__(self):

        self.conf = None
        self.list_site = None
        self.dict_bug = {}
        self.checkConfigFile()
        self.error = False

    def checkConfigFile(self):
        """ read config file """
        self.list_site = self.getSites()
        self.conf = {'login':'login', 'password':'password', \
            'player':'mplayer', 'base_directory':'/tmp'}
        self.dict_bug = {}
        try:
            fileconf = open(ospath.expanduser('~') + \
                    "/.config/flvdown/flv.conf", "rb", 0)
            for line in fileconf:
                tmp = line.split("=")
                if tmp[0] == 'order':
                    list_order = tmp[1].replace('"', '').split(',')[:-1]
                    for (i, site) in enumerate(list_order):
                        if site in self.list_site:
                            self.list_site.remove(site.strip())
                            self.list_site.insert(i, site.strip())
                elif tmp[0] == 'dict_bug':
                    self.dict_bug = eval(tmp[1])
                else:
                    self.conf[tmp[0]] = tmp[1].replace('"','')[:-1]
            fileconf.close()
        except IOError:
            print "check config"
            self.error = True

    @classmethod
    def getSites(cls):
        """ check modules to populate list_site"""
        import aggregators
        list_site = []
        for i in aggregators.__all__:
            site = "aggregators." + i + "_mod"
            __import__(site)
            for j in sys.modules[site].__all__:
                subsite = i + " : " + j
                list_site.append(subsite)
        return list_site
        
    def saveConf(self):
        """ save the config"""
        if (not ospath.exists(ospath.expanduser('~') + "/.config/flvdown/")):
            osmkdir(ospath.expanduser('~') + "/.config/flvdown/")
        fileconf = open(ospath.expanduser('~') + \
            "/.config/flvdown/flv.conf", "w", 0)
        for key in self.conf.keys():
            fileconf.write(key + '="' + self.conf[key] + '\"\n')
        fileconf.write('order="')
        for elt in self.list_site:
            fileconf.write(elt + ', ')
        fileconf.write('"\n')
        fileconf.write('dict_bug=')
        fileconf.write(repr(self.dict_bug))
        fileconf.write('\n')
        
        fileconf.close()


