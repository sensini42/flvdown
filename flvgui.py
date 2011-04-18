#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QThread
from PyQt4.QtCore import QCoreApplication

import os
import links
import subdown
import time
import traceback
######################################################################
###take care of cookies
######################################################################
from tempfile import NamedTemporaryFile
cookieFile = NamedTemporaryFile(suffix='.cookies-next.lwp')
cookieFileName = cookieFile.name

from os import path as ospath
from os import system as ossystem
from os import chdir as oschdir
cj = None
cookielib = None

import cookielib            
import urllib2    
import urllib
urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
request = urllib2.Request

if cookielib:
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
##end of cookies
######################################################################

conf = {'login':'login', 'password':'password', 'player':'mplayer', \
        'base_directory':'/tmp'}
dict_bug = {}#'The Office (US)' : 'The Office', \
#        'Brothers & Sisters' : 'Brothers and Sisters'}

class DownThread(QThread):
    """download an episode in a thread"""
    def __init__(self, tvshow, season, episode, option, list_site, \
                 infofile, parent = None):
        self.tvshow = tvshow
        self.season = season
        self.episode = episode
        self.option = option
        self.list_site = [str(list_site.item(i).text()) \
                          for i in range(list_site.count())]
        self.infofile = infofile
        self.parent = parent
        
        QThread.__init__(self, parent)
        
    def run(self):
        "download ep, sub, emit signal"
        try:
            ret, filename = links.flvdown(self.tvshow, self.season, \
                   self.episode, self.option, self.list_site)
            if ret != -1:
                if (not os.path.isdir(self.tvshow)):
                    os.mkdir(self.tvshow)
                self.emit(SIGNAL("downStart( QString )"), filename )
                urllib.urlretrieve(ret, filename, reporthook=self.downInfo)
                subdown.downSub(self.tvshow, self.tvshow, self.season, \
                     self.episode, self.option)
        except:
            traceback.print_exc()
            self.emit(SIGNAL("downFinished(QString, QString , \
                  PyQt_PyObject)"), "download error", \
                  self.tvshow + " " + self.season + " " + self.episode, \
                  self.infofile)
        else:
            self.emit(SIGNAL("downFinished( QString, QString , \
                  PyQt_PyObject)"), "download finished", \
                  self.tvshow + " " + self.season + " " + self.episode, \
                  self.infofile)

    def downInfo(self, infobloc, taillebloc, totalblocs):
        self.emit(SIGNAL("downInfo( PyQt_PyObject )"), \
                  [infobloc, taillebloc, totalblocs])



class VideoThread(QThread):
    """play in a thread"""
    def __init__(self, cmd, parent = None):
        self.cmd = cmd
        QThread.__init__(self, parent)
        
    def run(self):
        "play in the background"
        ossystem(self.cmd)



def checkConfigFile():
    """ read config file """
    try:
        fileconf = open(ospath.expanduser('~') + "/.config/flvdown/flv.conf", \
                         "rb", 0)
        for line in fileconf:
            tmp = line.split("=")
            if (tmp[0] != 'order' and tmp[0] != 'dict_bug'):
                conf[tmp[0]] = tmp[1].replace('"','')[:-1]
        fileconf.close()
        return 1
    except IOError:
        print "check config"
        return -1


def existFile(tvshow, season, episode):
    """ test if a matching file exists """
    import glob
    if (len(episode)==1):
        episode = "0" + episode
    tvshow_ = '_'.join(tvshow.split()).lower()
    return glob.glob(tvshow_ + '/' + tvshow_ + season + episode + '.*')
    

def addToNextEpisode(title):
    """ add 'title' to next-episode watch-list """
    urltitle = '-'.join(title.split(' ')) + '/'
    src = getSrcPageNextEpisode(urltitle)
    url = src.split('to watchlist')[0].split('"')[-2]
    
    src = getSrcPageNextEpisode(url)

def removeFromNextEpisode(movieId, userId, seasonId, episodeId):
    """ mark as read in next-episode """

    import urllib
    txdata = urllib.urlencode ({"username" : conf['login'], \
        "password" : conf['password']})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}
    urlbase = "http://next-episode.net/"
    try:
        req = request(urlbase, txdata, txheaders)
        urlopen(req)
    except IOError:
        print "could not login"
        return ""

    cj.save(cookieFileName)

    url = urlbase + 'PAGES/stufftowatch_files/ajax/ajax_requests_stuff.php'    
    txdata = urllib.urlencode ({"showCat" : "episode",
                                "movieId" : movieId,
                                "userId" : userId,
                                "seasonId" : seasonId,
                                "episodeId" : episodeId,
                                "parsedString" : seasonId + "x" + episodeId})
    req = request(url, txdata, txheaders)
    
    src = urlopen(req).read()
    print src



def getSrcPageNextEpisode(url):
    """ return the source page from next-episode """

    import urllib
    txdata = urllib.urlencode ({"username" : conf['login'], \
        "password" : conf['password']})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}

    try:
        req = request("http://next-episode.net/", txdata, txheaders)
        urlopen(req)
    except IOError:
        print "could not login"
        return ""

    txdata = None

    cj.save(cookieFileName)
    req = request("http://next-episode.net/" + url, txdata, txheaders)
    src = urlopen(req).read()
    return src


def getListEpisode():
    """
    return the list of episode from next-episode
    in format (tvshow, season, listepisodeOnDisk, listepisodeNotOnDisk)
    listepisode contains for each episode
    (movieId, userId, seasonId, episodeId)
    """
    source = getSrcPageNextEpisode("track/")
    if (source == ""):
        return []
    
    src = source.split('showName">')

    listep = []
    for i in src[1:]:
        lines = i.split('\n')
        if lines[0].endswith("</a>"):
            #else: tvshow not tracked
            item_ep_ondisk = []
            item_ep_notondisk = []
            for i in lines:
                if "removeEpisode" in i:
                    tv_name = lines[0][:-4]
                    if tv_name in dict_bug:
                        tv_name = dict_bug[tv_name]
                    item_se = i.split()[9][1:-2]
                    num_ep = i.split()[10][1:-2]
                    strlist = i.split("removeEpisode(")[1].split(')')[0]
                    epilist = [x[1:-1] for x in strlist.split(', ')[:-1]]
                    if(not existFile(tv_name, item_se, num_ep)):
                        item_ep_notondisk.append(num_ep)
                    else:
                        item_ep_ondisk.append(epilist)
            if(item_ep_ondisk or item_ep_notondisk):
                listep.append((tv_name, item_se, item_ep_ondisk, \
                               item_ep_notondisk))
    return listep

class InfoDown(QtGui.QWidget):
    """ info about down """

    def __init__(self):
        super(InfoDown, self).__init__()

        self.filedown = QtGui.QLabel("")
        self.barre = QtGui.QProgressBar(self)
        self.barre.hide()
        self.infodown = QtGui.QLabel("")

        mainLayout = QtGui.QGridLayout(self)

        mainLayout.addWidget(self.filedown, 0, 0, 1, 1)
        mainLayout.addWidget(self.barre, 0, 1, 1, 2)
        mainLayout.addWidget(self.infodown, 0, 3, 1, 1)

    def downStart(self, msg):
        self.time_begin = time.time()
        self.filedown.setText(msg)
        self.barre.reset()
        self.barre.setRange(0, 100)
        self.barre.setValue(0)
        self.barre.show()

    def downInfo(self, msg):
        bloc, taille, total = msg
        if total > 0:
            p = int(float(bloc)*float(taille)/float(total)*100)
            self.barre.setValue(p)
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
                sel.barre.setRange(0, 0)

class EltListDictBug(QtGui.QWidget):

    def __init__(self, key, value):
        super(EltListDictBug, self).__init__()

        self.key = key
        self.value = value

        mainLayout = QtGui.QHBoxLayout(self)

        arrowlabel = QtGui.QLabel("->")
        arrowlabel.setAlignment(Qt.AlignHCenter)
        button_rmv = QtGui.QPushButton("Remove")
        button_rmv.connect(button_rmv, SIGNAL("clicked()"), \
            self.removeDictBug)
        mainLayout.addWidget(QtGui.QLabel(key))
        mainLayout.addWidget(arrowlabel)
        mainLayout.addWidget(QtGui.QLabel(value))
        mainLayout.addWidget(button_rmv)

    def removeDictBug(self):
        self.emit(SIGNAL("removeDictBug( PyQt_PyObject )"), [self.key, \
             self.value])


class LineTvShow(QtGui.QWidget):
    """ tvshow line """

    def __init__(self, tvshow, season, info, ondisk):
        super(LineTvShow, self).__init__()

        mainLayout = QtGui.QHBoxLayout(self)
        mainLayout.addWidget(QtGui.QLabel(tvshow))
        mainLayout.addWidget(QtGui.QLabel(season))

        if ondisk:
            combo_ondisk = QtGui.QComboBox(self)
            for (_, _, _, episodeId) in info:
                combo_ondisk.addItem(str(episodeId))
            mainLayout.addWidget(combo_ondisk)
            ##play
            button_play = QtGui.QPushButton("Play")
            mainLayout.addWidget(button_play)
            btn_callbackPlay = (lambda data = (tvshow, season, \
                combo_ondisk): self.playClicked(data))
            self.connect(button_play, SIGNAL("clicked()"), btn_callbackPlay) 
            ##mark
            button_mark = QtGui.QPushButton("Mark as read")
            mainLayout.addWidget(button_mark)
            btn_callbackMark = (lambda data = (combo_ondisk, \
                info): self.markClicked(data))
            self.connect(button_mark, SIGNAL("clicked()"), btn_callbackMark)
            ##delete
            button_delete = QtGui.QPushButton("Mark and Delete")
            mainLayout.addWidget(button_delete)
            btn_callbackDelete = (lambda data = (tvshow, season, \
                    combo_ondisk, info): self.deleteClicked(data))
            self.connect(button_delete, SIGNAL("clicked()"), btn_callbackDelete)
        else: #notondisk
            combo_notondisk = QtGui.QComboBox(self)
            for num in info:
                combo_notondisk.addItem(num)
            mainLayout.addWidget(combo_notondisk)
            ##down
            button_down = QtGui.QPushButton("Down")
            mainLayout.addWidget(button_down)
            btn_callback = (lambda data = (tvshow, season, \
                combo_notondisk): self.downClicked(data))
            self.connect(button_down, SIGNAL("clicked()"), btn_callback)
            ##downAll
            button_downAll = QtGui.QPushButton("All")
            mainLayout.addWidget(button_downAll)
            btn_callbackAll = (lambda data = (tvshow, season, \
                combo_notondisk): self.downAllClicked(data))
            self.connect(button_downAll, SIGNAL("clicked()"), btn_callbackAll) 
            
    def downAllClicked(self, data):
        self.emit(SIGNAL("downAllClicked( PyQt_PyObject )"), data)
        
    def downClicked(self, data):
        self.emit(SIGNAL("downClicked( PyQt_PyObject )"), data)
        
    def playClicked(self, data):
        """ when a button_play is clicked """
        #data from combo
        tvshow = str(data[0])
        season = str(data[1])
        tvshow = "_".join(tvshow.split(' ')).lower()
        episode = str(data[2].currentText())
        if (len(episode)==1):
            episode = "0" + episode
        files = os.listdir(tvshow)
        _file = ""
        for _file in files :
            if _file.startswith(tvshow + season + episode) and \
              not _file.endswith('srt'):
                _file = tvshow + "/" + _file
                break
        VideoThread((conf['player']+ " " + _file), self).start()

    @classmethod
    def markClicked(cls, data):
        """ when a button_mark is clicked """
        #data from combo
        (movieId, userId, seasonId, episodeId) = data[1][data[0].currentIndex()]
        removeFromNextEpisode(movieId, userId, seasonId, episodeId)

    @classmethod
    def deleteClicked(cls, data):
        """ when a button_delete is clicked """
        tvshow = str(data[0])
        season = str(data[1])
        tvshow = "_".join(tvshow.split(' ')).lower()
        episode = str(data[2].currentText())
        (movieId, userId, seasonId, episodeId) = data[3][data[2].currentIndex()]
        removeFromNextEpisode(movieId, userId, seasonId, episodeId)
        if (len(episode)==1):
            episode = "0" + episode
        ossystem("rm " + tvshow + "/" + tvshow + season + episode + "*")

            
class Flvgui(QtGui.QWidget):
    """ Gui for flvdown"""
        
    def __init__(self, parent=None):
        """ nothing special here"""
        super(Flvgui, self).__init__()

        if (checkConfigFile()==-1):
            QtGui.QMessageBox.warning(self, 'Config File', \
                'Please check config', \
                QtGui.QMessageBox.StandardButton(QtGui.QMessageBox.Ok))

        self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('icon/flvgui.xpm'), self)
        self.trayIcon.activated.connect(self.toggle)
        self.trayIcon.show()

        self.setWindowTitle('flvgui')

        self.list_ep = []
        self.linetvshow = []

        self.mainlayout()

  
    def mainlayout(self):
        
        mainLayout = QtGui.QGridLayout(self)

        tab_widget = QtGui.QTabWidget()
        mainLayout.addWidget(tab_widget, 0, 0, 1, 3)

        self.tab1 = QtGui.QWidget()
        tab_widget.addTab(self.tab1, "Playing")
        self.maketab1()

        self.tab2 = QtGui.QWidget()
        tab_widget.addTab(self.tab2, "Downloading")
        self.maketab2()

        self.tab3 = QtGui.QWidget()
        tab_widget.addTab(self.tab3, "Options")
        self.maketab3()

        self.tab4 = QtGui.QWidget()
        tab_widget.addTab(self.tab4, "Site order")
        self.maketab4()

        self.tab5 = QtGui.QWidget()
        tab_widget.addTab(self.tab5, "Dict Bug")
        self.maketab5()

        tab_widget.setCurrentIndex(1)
        self.refresh()

        button_sub = QtGui.QPushButton("Subtitles")
        mainLayout.addWidget(button_sub, 1, 0)
        self.connect(button_sub, SIGNAL("clicked()"), self.downsub)
                
        button_refresh = QtGui.QPushButton("Refresh")
        mainLayout.addWidget(button_refresh, 1, 1)
        self.connect(button_refresh, SIGNAL("clicked()"), self.refresh)
                
        button_close = QtGui.QPushButton("Close")
        mainLayout.addWidget(button_close, 1, 2)
        #self.connect(button_close, SIGNAL("clicked()"), self, SLOT("close()"))
        button_close.clicked.connect(self.close)

        self.setLayout(mainLayout)


    def maketab1(self):
        """ playing tab """
        grid1 = QtGui.QGridLayout(self.tab1)
  
        ## data from next-episode
        self.dataondisk = QtGui.QGridLayout(None)
        grid1.addLayout(self.dataondisk, 1, 0)
        
    def maketab2(self):
        """ downloading tab """
        grid2 = QtGui.QGridLayout(self.tab2)

        ## info line
        grid2.addWidget(QtGui.QLabel('Tv show'), 0, 0)
        grid2.addWidget(QtGui.QLabel('Season'), 0, 1)
        grid2.addWidget(QtGui.QLabel('Episode'), 0, 2)

        ## episode not on next-episode
        edit_tv = QtGui.QLineEdit()
        edit_se = QtGui.QLineEdit()
        edit_ep = QtGui.QLineEdit()
        button_edit = QtGui.QPushButton("Down")
        btn_edit_callback = (lambda data = (edit_tv, \
             edit_se, edit_ep): self.downClicked(data))
        self.connect(button_edit, \
             SIGNAL("clicked()"), btn_edit_callback)
        button_all_edit = QtGui.QPushButton("All")
        btn_edit_callbackAll = (lambda data = (edit_tv, \
             edit_se, edit_ep): self.downAllClicked(data))
        self.connect(button_all_edit, \
             SIGNAL("clicked()"), btn_edit_callbackAll) 
        grid2.addWidget(edit_tv, 1, 0)
        grid2.addWidget(edit_se, 1, 1)
        grid2.addWidget(edit_ep, 1, 2)
        grid2.addWidget(button_edit, 1, 3)
        grid2.addWidget(button_all_edit, 1, 4)

        ## data from next-episode
        self.datanotondisk = QtGui.QGridLayout(None)
        grid2.addLayout(self.datanotondisk, 2, 0, 1, 5)
        
        ## button down all
        button_downAllES = QtGui.QPushButton("Down All")
        grid2.addWidget(button_downAllES, 3, 3, 1, 2)
        btn_callbackAllES = lambda data = (self.list_ep): \
               self.downAllESClicked(data)
        self.connect(button_downAllES, SIGNAL("clicked()"), btn_callbackAllES)

        ## add tvshows
        ed_addShow = QtGui.QLineEdit()
        grid2.addWidget(ed_addShow, 4, 0, 1, 3)
        button_addShow = QtGui.QPushButton("Add tvshow")
        grid2.addWidget(button_addShow, 4, 3, 1, 2)
        btn_callbackAddShow = lambda data = (ed_addShow): \
                              self.addShow(data)
        self.connect(button_addShow, SIGNAL("clicked()"), btn_callbackAddShow)

        ## info down
        self.stackedWidget = QtGui.QStackedWidget()
        grid2.addWidget(self.stackedWidget, 5, 0, 1, 4)
        self.nextbutton = QtGui.QPushButton("Next")
        self.nextbutton.clicked.connect(self.nextstacked)
        self.nextbutton.hide()
        grid2.addWidget(self.nextbutton, 5, 4)

    def maketab3(self):
        """ options tab """
        grid3 = QtGui.QGridLayout(self.tab3)

        self.ed_checkbox = QtGui.QCheckBox('Interactive', self)
        grid3.addWidget(self.ed_checkbox, 0, 0)
            
        i = 0
        self.list_edit = []
        for key in conf.keys():
            grid3.addWidget(QtGui.QLabel(key), i+1, 0)
            self.list_edit.append([key, QtGui.QLineEdit()])
            grid3.addWidget(self.list_edit[i][1], i+1, 1, 1, 1) 
            if key == 'password':
                self.list_edit[i][1].setEchoMode(2)
            self.list_edit[i][1].setText(conf[key])
            i += 1

        button_save = QtGui.QPushButton("Save config file")
        self.connect(button_save, SIGNAL("clicked()"), self.saveClicked)
        grid3.addWidget(button_save, 5, 0)
        
    def maketab4(self):
        """ site order tab """
        grid4 = QtGui.QGridLayout(self.tab4)

        self.list_site = QtGui.QListWidget()
        self.getSites()
        self.orderSites()

        button_up = QtGui.QPushButton("Up")
        button_down = QtGui.QPushButton("Down")
        self.connect(button_up, SIGNAL("clicked()"), self.moveUp)
        self.connect(button_down, SIGNAL("clicked()"), self.moveDown)
        
        grid4.addWidget(self.list_site, 0, 1, 2, 1)
        grid4.addWidget(button_up, 0, 2)
        grid4.addWidget(button_down, 1, 2)

        button_save = QtGui.QPushButton("Save config file")
        self.connect(button_save, SIGNAL("clicked()"), self.saveClicked)
        grid4.addWidget(button_save, 2, 1)
        
    def maketab5(self):
        """ dict bug tab """
        grid5 = QtGui.QGridLayout(self.tab5)

        grid5.addWidget(QtGui.QLabel('Next-episode'), 0, 0)
        grid5.addWidget(QtGui.QLabel('  ->  '), 0, 1)
        grid5.addWidget(QtGui.QLabel('Down'), 0, 2)
        grid5.addWidget(QtGui.QLabel(""), 0, 3)

        self.lineedit_ne = QtGui.QLineEdit()
        self.lineedit_d = QtGui.QLineEdit()
        button_add = QtGui.QPushButton("Add dict bug")
        self.connect(button_add, SIGNAL("clicked()"), self.addDictBug)
        grid5.addWidget(self.lineedit_ne, 1, 0)
        grid5.addWidget(QtGui.QLabel(""), 1, 1)
        grid5.addWidget(self.lineedit_d, 1, 2)
        grid5.addWidget(button_add, 1, 3)

        self.dictbug = QtGui.QGridLayout()
        grid5.addLayout(self.dictbug, 2, 0, 1, 4)

        button_save = QtGui.QPushButton("Save config file")
        self.connect(button_save, SIGNAL("clicked()"), self.saveClicked)
        grid5.addWidget(button_save, 3, 0)

        self.list_dictbug = self.getDictBug()
        self.eltdictbug = []
        self.refresh5()

    def addDictBug(self):
        self.list_dictbug.append([str(self.lineedit_ne.text()), \
          str(self.lineedit_d.text())])
        self.refresh5()

    def removeDictBug(self, data):
        self.list_dictbug.remove(data)
        self.refresh5()

    def refresh5(self):    
        for i in self.eltdictbug:
            i.setParent(None)
            del(i)

        self.eltdictbug = []
        for (key, value) in self.list_dictbug:
            tmp = EltListDictBug(key, value)
            self.connect(tmp, SIGNAL("removeDictBug(PyQt_PyObject)"), \
                self.removeDictBug)
            self.dictbug.addWidget(tmp)
            self.eltdictbug.append(tmp)

    def toggle(self):
        """ toggle main frame """
        if self.isVisible(): 
            self.hide()
        else: 
            self.show()


    def refresh(self):
        "populate the tab_widget"
        oschdir(conf['base_directory'])
        self.list_ep = getListEpisode()

        for i in self.linetvshow:
            i.setParent(None)
            del(i)

        self.linetvshow = []
        for (i,(tvshow, season, ondisk, notondisk)) in enumerate(self.list_ep):
            if(ondisk != []):
                tmp = LineTvShow(tvshow, season, ondisk, True)
                self.linetvshow.append(tmp)
                self.dataondisk.addWidget(tmp)
            if(notondisk != []):
                tmp = LineTvShow(tvshow, season, notondisk, False)
                self.connect(tmp, SIGNAL("downClicked(PyQt_PyObject)"), \
                    self.downClicked)
                self.connect(tmp, SIGNAL("downAllClicked(PyQt_PyObject)"), \
                    self.downAllClicked)
                self.linetvshow.append(tmp)
                self.datanotondisk.addWidget(tmp)

    def nextstacked(self):
        if self.stackedWidget.count > 1:
            if self.stackedWidget.currentIndex() != self.stackedWidget.count()-1:
                self.stackedWidget.setCurrentIndex( \
                self.stackedWidget.currentIndex() + 1)
            else:
                self.stackedWidget.setCurrentIndex(0)
                

    @classmethod
    def addShow(cls, data):
        """ when we want to add a tvshow """
        addToNextEpisode(str(data.text()))
    
    def saveClicked(self):
        """ when save button is clicked"""
        if (not os.path.exists(ospath.expanduser('~') + "/.config/flvdown/")):
            os.mkdir(ospath.expanduser('~') + "/.config/flvdown/")
        fileconf = open(ospath.expanduser('~') + \
            "/.config/flvdown/flv.conf", "w", 0)
        for [key, line] in self.list_edit:
            fileconf.write(key + '="' + str(line.text()) + '\"\n')
            conf[key] = str(line.text())
        fileconf.write('order="')
        for row_item in range(self.list_site.count()):
            fileconf.write(self.list_site.item(row_item).text() + ', ')
        fileconf.write('"\n')
        fileconf.write('dict_bug="')
        for (key, value) in self.list_dictbug:
            fileconf.write(key + ' : ' + value + ', ')
        fileconf.write('"\n')
        
        fileconf.close()

    def runThread(self, tvshow, season, episode):
        """ run a download thread """
        option = ""
        if self.ed_checkbox.isChecked():
            option += "i"
        tvshow = "_".join(tvshow.split(' ')).lower()
        infoline = InfoDown()
        self.stackedWidget.addWidget(infoline)
        if self.stackedWidget.count() > 1:
            self.nextbutton.show()
        dth = DownThread(tvshow, season, episode, option, self.list_site,
             infoline, self)
        self.connect(dth, SIGNAL("downStart(QString)"), infoline.downStart)
        self.connect(dth, SIGNAL("downInfo(PyQt_PyObject)"), infoline.downInfo)
        self.connect(dth, SIGNAL("downFinished(QString, QString, \
             PyQt_PyObject)"), self.endThread)
        dth.start() 

    def endThread(self, titre, message, infoline):
        """ when a download is finished """
        print titre, message
        self.trayIcon.showMessage(titre, message)
        self.stackedWidget.removeWidget(infoline)
        if self.stackedWidget.count() < 2:
            self.nextbutton.hide()

    def downClicked(self, data):
        """ when a button is clicked """
        # data = [tv, season, numepisode, fromsite, interactif]
        if type(data[0]) == type(""):
            #data from combo
            tvshow = str(data[0])
            season = str(data[1])
            episode = str(data[2].currentText())
        else:
            #data from first line
            tvshow = str(data[0].text())
            season = str(data[1].text())
            episode = str(data[2].text())

        self.runThread(tvshow, season, episode)

    def downAllClicked(self, data):
        """ when a buttonall is clicked """
        if type(data[0]) == type(""):
            #data from combo
            tvshow = str(data[0])
            season = str(data[1])
            for i in range(data[2].count()):
                self.runThread(tvshow, season, str(data[2].itemText(i)))
        else:
            #data from first line
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
                self.runThread(tvshow, season, str(i))

    def downAllESClicked(self, data):
        """ when the buttondownalles is clicked """
        print data[0]
        for (tvshow, season, _, notondisk) in data[0]:
            for epi in notondisk:
                self.runThread(tvshow, str(season), str(epi))

    @classmethod
    def downsub(cls):
        """ when a button_sub is clicked """
        #data from combo
        ossystem("downsub.sh")

    def getDictBug(self):
        list_dictbug = []
        try:
            fileconf = open(ospath.expanduser('~') + \
                            "/.config/flvdown/flv.conf", "rb", 0)
            for line in fileconf:
                tmp = line.split("=")
                if (tmp[0] == 'dict_bug'):
                    list_dict = tmp[1].replace('"', '').split(',')[:-1]
                    for ld in list_dict:
                        list_dictbug.append([ld.split(':')[0], \
                            ld.split(':')[1]])
        except IOError:
            print "check config"
        return list_dictbug

    def getSites(self):
        """ check modules to populate list_site"""
        import sys
        import aggregators
        self.list_site.clear()
        for i in aggregators.__all__:
            site = "aggregators." + i + "_mod"
            __import__(site)
            for j in sys.modules[site].__all__:
                subsite = i + " : " + j
                item = QtGui.QListWidgetItem(subsite)
                self.list_site.addItem(item)
        
    def orderSites(self):
        """
        order list_site wrt config files
        unknown (new) modules go at the end
        """
        list_order = []
        try:
            fileconf = open(ospath.expanduser('~') + \
                            "/.config/flvdown/flv.conf", "rb", 0)
            for line in fileconf:
                tmp = line.split("=")
                if (tmp[0] == 'order'):
                    list_order = tmp[1].replace(' : ', '.').split(',')[:-1]
        except IOError:
            print "check config"
        for i in list_order[::-1]:
            site = ' : '.join(i[1:].split('.'))
            for j in range(self.list_site.count()):
                if (self.list_site.item(j).text()==site):
                    item = self.list_site.takeItem(j)
                    self.list_site.insertItem(0, item)
        self.list_site.setCurrentRow(0)
    
    def moveUp(self):
        """ up is clicked """
        cur_row = self.list_site.currentRow()
        nxt_row = max(cur_row - 1, 0)
        item = self.list_site.takeItem(cur_row)
        self.list_site.insertItem(nxt_row, item)
        self.list_site.setCurrentRow(nxt_row)
        
    def moveDown(self):
        """ down is clicked """
        cur_row = self.list_site.currentRow()
        nxt_row = min(cur_row + 1, self.list_site.count() -1)
        item = self.list_site.takeItem(cur_row)
        self.list_site.insertItem(nxt_row, item)
        self.list_site.setCurrentRow(nxt_row)
        



def main():
    """ main """
    app = QtGui.QApplication([])
    flv = Flvgui()
    flv.show()
    app.exec_()    


if __name__ == '__main__':
    main()

