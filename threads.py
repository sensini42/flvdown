#!/usr/bin/python
# -*- coding: utf-8 -*-
""" threads definition """

from PyQt4.QtCore import QThread, SIGNAL

from os import system as ossystem

import urllib
import traceback

import links
import subdown

class Abort(Exception):
    """ class exception """
    pass

class Down(QThread):
    """download an episode in a thread"""

    def __init__(self, episode, option, list_site, parent=None):
        """ initialisation """
        QThread.__init__(self, parent)

        self.stop = False

        self.episode = episode
        self.option = option
        self.list_site = list_site
        
    def run(self):
        """ download ep, sub, emit signal """
        try:
            link, filename = links.flvdown(self.episode, self.option, \
                  self.list_site)
            if link:
                self.episode.createDir()
                self.emit(SIGNAL("downStart()"))
                urllib.urlretrieve(link, filename, reporthook=self.downInfo)
                subdown.downSub(filename, self.option)
        except Abort:
            self.emit(SIGNAL("downFinish(PyQt_PyObject)"), False)
        except:
            traceback.print_exc()
            self.emit(SIGNAL("downFinish(PyQt_PyObject)"), False)
        else:
            self.emit(SIGNAL("downFinish(PyQt_PyObject)"), True)

    def stopDown(self):
        """ stop """
        self.stop = True

    def downInfo(self, infobloc, taillebloc, totalblocs):
        """ report hook """
        if self.stop:
            raise Abort
        self.emit(SIGNAL("downInfo(PyQt_PyObject)"), \
                  [infobloc, taillebloc, totalblocs])


class Video(QThread):
    """ play in a thread """

    def __init__(self, episode, player, parent=None):
        """ initialisation """
        QThread.__init__(self, parent)
        self.cmd = player + " " + episode.getVideoName() 
        
    def run(self):
        """ play in the background """
        ossystem(self.cmd)

