#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for downloading tab """


from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from gui.display import Display

import episodetv

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
        self.msg = ""

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
        self.connect(self.down, SIGNAL("downFinish(PyQt_PyObject, QString)"), \
                self.downFinish)
        self.running = True
        self.down.start()

    def getToolTip(self):
        """ return tooltip """
        return self.episode.getBaseName()+": "+self.msg

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
            self.emit(SIGNAL("removeInfodown(PyQt_PyObject)"), self)

    def downFinish(self, down, msgdown):
        """ down finish """
        if self.hook:
            self.hook.stopDown()
        self.barre.hide()
        self.msg = msgdown
        if self.time_begin:
            ttime = time.time() - self.time_begin
            self.msg = self.msg + " (" + str("%s:%02d:%02d" %(int(ttime/3600), \
                 (ttime%3600)/60.0, (ttime%3600)%60)) + ")"
        self.infodown.setText(self.msg)
        self.running = False
        self.button.setText("Remove")
        self.button.show()
        self.emit(SIGNAL("downFinished(PyQt_PyObject, PyQt_PyObject, \
                QString)"), down, self.episode, msgdown)

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
                self.msg = str("time_left: %s:%02d:%02d" \
                  %(int(time_left/3600.0), (time_left%3600)/60.0, \
                  (time_left%3600)%60)) 
                self.infodown.setText( str("%.2f ko/s " %float(speed/1024)) + \
                   str("time_left: %s" %(self.msg)) )
            except ZeroDivisionError:
                pass
        else:
            if self.barre.maximum > 0:
                self.barre.reset()
                self.barre.setRange(0, 0)


class Downloading(Display):
    """ display playing list """

    def __init__(self, nextep, list_site, parent=None):
        """ initialisation """
        self.parent = parent
        self.list_site = list_site

        # pylint warning
        self.ed_checkbox = None
        self.button_downall = None
        self.button_down = None
        self.button_all = None
        self.stackedWidget = None
        self.nextbutton = None

        super(Downloading, self).__init__(nextep, False)
        self.update()


    def populate(self):
        """ create layout """

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 0, 0, 1, 5)


        ## episode not on next-episode
        edit_tv = QtGui.QLineEdit()
        edit_se = QtGui.QLineEdit()
        edit_ep = QtGui.QLineEdit()
        button_edit = QtGui.QPushButton("Down")
        btn_edit_callback = (lambda data = (edit_tv, \
             edit_se, edit_ep): self.downFreeClicked(data))
        self.connect(button_edit, SIGNAL("clicked()"), btn_edit_callback)
        self.mainLayout.addWidget(edit_tv, 3, 0)
        self.mainLayout.addWidget(edit_se, 3, 1)
        self.mainLayout.addWidget(edit_ep, 3, 2)
        self.mainLayout.addWidget(button_edit, 3, 3, 1, 2)


        ## button down 
        self.button_down = QtGui.QPushButton("Down")
        self.mainLayout.addWidget(self.button_down, 2, 3)
        self.button_down.clicked.connect(self.downClicked)

        ## button all
        self.button_all = QtGui.QPushButton("All")
        self.mainLayout.addWidget(self.button_all, 2, 4)
        self.button_all.clicked.connect(self.allClicked)

        ## checkbox interactive
        self.ed_checkbox = QtGui.QCheckBox('Interactive download', self)
        self.mainLayout.addWidget(self.ed_checkbox, 4, 1, 1, 2)

        ## button downall
        self.button_downall = QtGui.QPushButton("Down All")
        self.mainLayout.addWidget(self.button_downall, 4, 3, 1, 2)
        self.button_downall.clicked.connect(self.downallClicked)

        ## add tvshows
        ed_addShow = QtGui.QLineEdit()
        self.mainLayout.addWidget(ed_addShow, 5, 0, 1, 3)
        button_addShow = QtGui.QPushButton("Add tvshow")
        self.mainLayout.addWidget(button_addShow, 5, 3, 1, 2)
        btn_callbackAddShow = (lambda data = (ed_addShow): \
                                  self.addShow(data))
        self.connect(button_addShow, SIGNAL("clicked()"), btn_callbackAddShow)

        ## info down
        self.stackedWidget = QtGui.QStackedWidget()
        self.mainLayout.addWidget(self.stackedWidget, 6, 0, 1, 4)
        self.nextbutton = QtGui.QPushButton("Next")
        self.nextbutton.clicked.connect(self.nextstacked)
        self.nextbutton.hide()
        self.mainLayout.addWidget(self.nextbutton, 6, 4)

        ## better display
        self.mainLayout.addWidget(QtGui.QStackedWidget(), 7, 0, 1, 5)

        super(Downloading, self).populate()

    def displayButtons(self, value):
        """ display or not buttons """
        self.button_down.setVisible(value)
        self.button_all.setVisible(value)
        self.button_downall.setVisible(value)
        super(Downloading, self).displayButtons(value)

    def addShow(self, data):
        """ when we want to add a tvshow """
        self.nextep.addShow(str(data.text()))

    def nextstacked(self):
        """ view next downloading """
        swc = self.stackedWidget.count()
        if swc > 1:
            swci = self.stackedWidget.currentIndex()
            if swci != swc -1:
                self.stackedWidget.setCurrentIndex(swci + 1)
            else:
                self.stackedWidget.setCurrentIndex(0)

    def removestacked(self, infoline):
        """ remove an entry """
        self.stackedWidget.removeWidget(infoline)
        if self.stackedWidget.count() < 2:
            self.nextbutton.hide()

    def getToolTip(self):
        """ return down infos """
        tooltip = 'Flvgui\n------------\n'
        if self.stackedWidget.count() == 0:
            tooltip += 'no active download' 
        else:
            for i in range(self.stackedWidget.count()):
                tooltip += self.stackedWidget.widget(i).getToolTip() + '\n'
        return tooltip

    def endThread(self, down, episode, message):
        """ when a down is finished """
        self.parent.showMessage(episode.getBaseName(), message)
        if down:
            self.removeEpisode(episode)
            self.parent.playing.addEpisode(episode)

    def runThread(self, episode):
        """ run a download thread """
        option = ""
        if self.ed_checkbox.isChecked():
            option += "i"
        tmp = InfoDown(episode, option, self.list_site)
        self.connect(tmp, SIGNAL("removeInfodown(PyQt_PyObject)"), \
                self.removestacked)
        self.connect(tmp, SIGNAL("downFinished(PyQt_PyObject, PyQt_PyObject, \
                QString)"), self.endThread)
        self.stackedWidget.addWidget(tmp)
        if self.stackedWidget.count() > 1:
            self.nextbutton.show()

    def isInProgress(self):
        """ check if there is some download in progress """
        return self.stackedWidget.count() > 0

    def downFreeClicked(self, data):
        """ when down from form """
        tvshow = str(data[0].text())
        season = str(data[1].text())
        episodes = str(data[2].text())
        set_ep = set()
        for range_epi in episodes.split(","):
            epi_min = int(range_epi.split("-")[0])
            epi_max = int(range_epi.split("-")[-1])
            for num_epi in range(epi_min, epi_max + 1):
                set_ep.add(num_epi)
        list_ep = list(set_ep)
        list_ep.sort()
        for i in list_ep:
            epi = episodetv.episodeTV(tvshow, season, str(i), None)
            self.runThread(epi)

    def update(self, list_site=None):
        """ update """
        if list_site:
            self.list_site = list_site
        super(Downloading, self).update()

    def downClicked(self):
        """ when down from combo """
        episode = self.info[self.episode_cb.currentIndex()]
        self.runThread(episode)

    def allClicked(self):
        """ when all from combo """
        for i in range(self.episode_cb.count()):
            episode = self.info[i]
            self.runThread(episode)

    def downallClicked(self):
        """ when downall is clicked """
        for episode in self.list_ep:
            if not episode.isOnDisk:
                self.runThread(episode)

