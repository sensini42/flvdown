#!/usr/bin/python
# -*- coding: utf-8 -*-
""" threads definition """

from PyQt4.QtCore import QThread, SIGNAL

from os import system as ossystem
from os import kill as oskill

import urllib
import traceback
import time
import subprocess
import signal

import links
import subdown

class NoSubFound(Exception):
    """ class exception """
    pass

class NoLinkFound(Exception):
    """ class exception """
    pass

class Abort(Exception):
    """ class exception """
    pass

class Down(QThread):
    """download an episode in a thread"""

    def __init__(self, episode, option, list_site, parent=None):
        """ initialisation """
        QThread.__init__(self, parent)

        self.proc = None
        self.stop = False

        self.episode = episode
        self.option = option
        self.list_site = list_site
        
    def run(self):
        """ download ep, sub, emit signal """
        try:
            link, filename, cook = links.flvdown(self.episode, self.option, \
                  self.list_site)
            if link:
                self.episode.createDir()
                if cook:
                    # use of wget
                    self.emit(SIGNAL("downStartWget()"))
                    links.getFile(link, filename, cook)
                    self.proc = subprocess.Popen(['wget -c ' + link + \
                        ' -O ' + filename], shell=True)
                    self.proc.wait()
                    if self.proc.returncode == 0:
                        if subdown.downSub(self.episode, self.option) == -1:
                            raise NoSubFound()
                    else:
                        raise Abort()
                else:    
                    self.emit(SIGNAL("downStart()"))
                    urllib.urlretrieve(link, filename, reporthook=self.downInfo)
                    if subdown.downSub(self.episode, self.option) == -1:
                        raise NoSubFound()
            else:
                raise NoLinkFound()
        except NoSubFound:
            self.emit(SIGNAL("downFinish(PyQt_PyObject, QString)"), \
                        True, "no sub found")
        except NoLinkFound:
            self.emit(SIGNAL("downFinish(PyQt_PyObject, QString)"), \
                        False, "no link found")
        except Abort:
            self.emit(SIGNAL("downFinish(PyQt_PyObject, QString)"), \
                        False, "download aborted")
        except:
            traceback.print_exc()
            self.emit(SIGNAL("downFinish(PyQt_PyObject, QString)"), \
                        False, "download error")
        else:
            self.emit(SIGNAL("downFinish(PyQt_PyObject, QString)"), \
                        True, "download finished")

    def stopDown(self):
        """ stop """
        if self.proc:
            oskill(self.proc.pid, signal.SIGUSR1)
        self.stop = True

    def downInfo(self, infobloc, taillebloc, totalblocs):
        """ report hook """
        if self.stop:
            raise Abort
        self.emit(SIGNAL("downInfo(PyQt_PyObject)"), \
                  [infobloc, taillebloc, totalblocs])


class Hook(QThread):
    """ progress of wget downloading """

    def __init__(self, parent=None):
        """ initialisation """
        QThread.__init__(self, parent)
        self.stop = False
        
    def run(self):
        """ play in the background """
        while not self.stop:
            time.sleep(1)
            self.emit(SIGNAL("downInfo(PyQt_PyObject)"), \
                  [0, 0, 0])

    def stopDown(self):
        """ stop """
        self.stop = True


class Video(QThread):
    """ play in a thread """

    def __init__(self, episode, player, parent=None):
        """ initialisation """
        QThread.__init__(self, parent)
        self.cmd = player + " " + episode.getVideoName() 
        
    def run(self):
        """ play in the background """
        ossystem(self.cmd)

