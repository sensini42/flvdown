#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for progress tab """


from PyQt4.QtCore import SIGNAL
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

import time

from threads import Down, Hook


class InfoDown(QtGui.QWidget):
    """ info about down """

    def __init__(self, episode, option, list_site):
        """ initialisation """
        super(InfoDown, self).__init__()

        self.episode = episode

        # pylint warning
        self.time_begin = None
        self.hook = None

        filedown = QtGui.QLabel(episode.getBaseName())
        self.barre = QtGui.QProgressBar(self)
        self.barre.hide()
        self.infodown = QtGui.QLabel("")
        self.button = QtGui.QPushButton("Stop")
        self.button.clicked.connect(self.buttonClicked)
        self.button.hide()

        mainLayout = QtGui.QGridLayout(self)
        mainLayout.addWidget(filedown, 0, 0)
        mainLayout.addWidget(self.barre, 0, 1)
        mainLayout.addWidget(self.infodown, 0, 2)
        mainLayout.addWidget(self.button, 0, 3)
        self.setLayout(mainLayout)
    
        self.down = Down(self.episode, option, list_site, self)
        self.connect(self.down, SIGNAL("downStart()"), self.downStart)
        self.connect(self.down, SIGNAL("downStartWget()"), self.downStartWget)
        self.connect(self.down, SIGNAL("downInfo(PyQt_PyObject)"), \
                self.downInfo)
        self.connect(self.down, SIGNAL("downFinish(QString)"), \
                self.downFinish)
        self.running = True
        self.down.start()

    def isRunning(self):
        """ check if downloading is running """
        return self.running

    def buttonClicked(self):
        """ stop downloading or hide InfoDown """
        if self.running:
            self.down.stopDown()
            self.running = False
            self.button.setText("Remove")
        else:
            self.hide()

    def downFinish(self, msgdown):
        """ down finish """
        if self.hook:
            self.hook.stopDown()
        self.barre.hide()
        msg = msgdown
        if self.time_begin:
            ttime = time.time() - self.time_begin
            msg = msg + " (" + str("%s:%02d:%02d" %(int(ttime/3600), \
                 (ttime%3600)/60.0, (ttime%3600)%60)) + ")"
        self.infodown.setText(msg)
        self.running = False
        self.button.setText("Remove")
        self.button.show()
        self.emit(SIGNAL("downFinished(QString, QString)"), \
                self.episode.getBaseName(), msgdown)

    def downStartWget(self):
        """ down start """
        self.downStart()
        self.hook = Hook(self)
        self.connect(self.hook, SIGNAL("downInfo(PyQt_PyObject)"), \
                self.downInfo)
        self.hook.start()
        self.button.hide()

    def downStart(self):
        """ down start """
        self.time_begin = time.time()
        self.barre.reset()
        self.barre.setRange(0, 100)
        self.barre.setValue(0)
        self.barre.show()
        self.button.show()

    def downInfo(self, msg):
        """ down info """
        bloc, taille, total = msg
        if total > 0:
            value = int(float(bloc)*float(taille)/float(total)*100)
            self.barre.setValue(value)
            try:
                speed = float(bloc*taille) / float(time.time()-self.time_begin)
                time_left = float(total-bloc*taille) / speed
                self.infodown.setText( str("%.2f ko/s " %float(speed/1024)) + \
                   str("time_left: %s:%02d:%02d" %(int(time_left/3600.0), \
                   (time_left%3600)/60.0, (time_left%3600)%60)) )
            except ZeroDivisionError:
                pass
        else:
            if self.barre.maximum > 0:
                self.barre.reset()
                self.barre.setRange(0, 0)
