#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QRegExp

import os

######################################################################
###take care of cookies
######################################################################
import random
ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
cookieFile = '/tmp/' + ''.join([random.choice(ascii) for _ in range(10)])

cookieFile = cookieFile + 'cookies-next.lwp'
from os import path as ospath
from os import remove as osremove
from os import system as ossystem
from os import chdir as oschdir
cj = None
cookielib = None

import cookielib            
import urllib2    
urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
request = urllib2.Request

if ospath.isfile(cookieFile):
    cj.load(cookieFile)
if cookielib:
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
##end of cookies
######################################################################

conf = {'login':'login', 'password':'password', 'player':'mplayer', 'base_directory':'/tmp'}

def checkConfigFile():
    """ read config file """
    try:
        fileconf = open(ospath.expanduser('~') + "/.config/flvdown/flv.conf", \
                         "rb", 0)
        for line in fileconf.read().split():
            tmp = line.split("=")
            conf[tmp[0]] = tmp[1].replace('"','')
        fileconf.close()
    except IOError:
        print "check config"


def existFile(tvshow, season, episode):
    """ test if a matching file exists """
    import glob
    if (len(episode)==1):
        episode = "0" + episode
    tvshow_ = '_'.join(tvshow.split()).lower()
    return glob.glob(tvshow_ + '/' + tvshow_ + season + episode + '.*')
    

def removeFromNextEpisode(movieId, userId, seasonId, episodeId):
    """ return the source page from next-episode """

    import urllib
    txdata = urllib.urlencode ({"username" : conf['login'], "password" : conf['password']})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}
    urlbase = "http://next-episode.net/"
    try:
        req = request(urlbase, txdata, txheaders)
        urlopen(req)
    except IOError:
        print "could not login"
        return ""

    cj.save(cookieFile)

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


def getSrcPageNextEpisode():
    """ return the source page from next-episode """

    import urllib
    txdata = urllib.urlencode ({"username" : conf['login'], "password" : conf['password']})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}

    try:
        req = request("http://next-episode.net/", txdata, txheaders)
        urlopen(req)
    except IOError:
        print "could not login"
        return ""

    cj.save(cookieFile)
    req = request("http://next-episode.net/track/", txdata, txheaders)
    src = urlopen(req).read()
    return src


def getListEpisode():
    """
    return the list of episode from next-episode
    in format (tvshow, season, listepisodeOnDisk, listepisodeNotOnDisk)
    listepisode contains for each episode
    (movieId, userId, seasonId, episodeId)
    """
    source = getSrcPageNextEpisode()
    if (source == ""):
        return []
    
    src = source.split('showName">')
    ## for i in src[1:]:
    ##     lines = i.split('\n')
    ##     if lines[0].endswith("</a>"):
    ##         #else: tvshow not tracked
    ##         item_ep = []
    ##         for i in lines:
    ##             if "removeEpisode" in i:
    ##                 strlist = i.split("removeEpisode(")[1].split(')')[0]
    ##                 k=[int(x[1:-1]) for x in strlist.split(', ')[:-1]]
    ##                 print "«««", lines[0][:-4], "___",k,"»»»"
    ##                 print

    dict_bug = {'The Office (US)' : 'The Office'}
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
            listep.append((tv_name, item_se, item_ep_ondisk, item_ep_notondisk))
    osremove(cookieFile)
    return listep



            
class Flvgui(QtGui.QWidget):
    """ Gui for flvdown"""
    msgAlert = None
        
    def __init__(self):
        """ nothing special here"""
        super(Flvgui, self).__init__()

        checkConfigFile()

        Flvgui.msgAlert = QtGui.QSystemTrayIcon(self)
        Flvgui.msgAlert.show()
        
        self.tab_widget = QtGui.QTabWidget()
        
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()

        self.tab_widget.addTab(self.tab1, "Playing")
        self.tab_widget.addTab(self.tab2, "Downloading")
        self.tab_widget.addTab(self.tab3, "Options")

        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.tab_widget)

        self.populate()
        
        button_sub = QtGui.QPushButton("Subtitles")
        mainLayout.addWidget(button_sub)
        self.connect(button_sub, SIGNAL("clicked()"), self.downsub)
                
        button_refresh = QtGui.QPushButton("Refresh")
        mainLayout.addWidget(button_refresh)
        self.connect(button_refresh, SIGNAL("clicked()"), self.populate)
                
        button_close = QtGui.QPushButton("Close")
        mainLayout.addWidget(button_close)
        self.connect(button_close, SIGNAL("clicked()"), self, SLOT("close()"))

        self.setLayout(mainLayout)
        self.setWindowTitle('flvgui')


    def populate(self):

        oschdir(conf['base_directory'])

        self.tab_widget.removeTab(2)
        self.tab_widget.removeTab(1)
        self.tab_widget.removeTab(0)
        del(self.tab1)
        del(self.tab2)
        del(self.tab3)
        
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        
        self.grid1 = QtGui.QGridLayout(self.tab1)
        self.grid2 = QtGui.QGridLayout(self.tab2)
        self.grid3 = QtGui.QGridLayout(self.tab3)
        
        self.tab_widget.addTab(self.tab1, "Playing")
        self.tab_widget.addTab(self.tab2, "Downloading")
        self.tab_widget.addTab(self.tab3, "Options")


        ##option
        i = 0
        list_edit = []
        for key in conf.keys():
            self.grid3.addWidget(QtGui.QLabel(key), i, 0)
            list_edit.append([key, QtGui.QLineEdit()])
            self.grid3.addWidget(list_edit[i][1], i, 1) 
            if key == 'password':
              list_edit[i][1].setEchoMode(2)
            list_edit[i][1].setText(conf[key])
            i += 1
        button_save = QtGui.QPushButton("Save config file")
        btn_save_callback = (lambda data = (list_edit) : \
             self.saveClicked(data))
        self.connect(button_save, SIGNAL("clicked()"), btn_save_callback)
        self.grid3.addWidget(button_save, 5, 0)
        
        ##titles
        empty_label = QtGui.QLabel("")
        second = 6
        self.grid2.addWidget(QtGui.QLabel('Tv show'), 0, 0 + second)
        self.grid2.addWidget(QtGui.QLabel('Season'), 0, 1 + second)
        self.grid2.addWidget(QtGui.QLabel('Episode'), 0, 2 + second)
        self.grid2.addWidget(empty_label, 0, 3 + second)
        self.grid2.addWidget(empty_label, 0, 4 + second)
        self.grid2.addWidget(QtGui.QLabel('Only from'), 0, 5 + second)
        self.grid2.addWidget(QtGui.QLabel('Interactive'), 0, 6 + second)

        #first line
        edit_tv = QtGui.QLineEdit()
        edit_se = QtGui.QLineEdit()
        edit_ep = QtGui.QLineEdit()
        
        ed_radio1 = QtGui.QRadioButton("*")
        ed_radio2 = QtGui.QRadioButton("z")
        ed_radio3 = QtGui.QRadioButton("l")
        ed_radio4 = QtGui.QRadioButton("n")
        ed_radio1.setChecked(1)
        ed_widg = QtGui.QWidget()
        ed_layoutRadio = QtGui.QHBoxLayout(ed_widg)
        ed_layoutRadio.addWidget(ed_radio1)
        ed_layoutRadio.addWidget(ed_radio2)
        ed_layoutRadio.addWidget(ed_radio3)
        ed_layoutRadio.addWidget(ed_radio4)
        ed_widg.setLayout(ed_layoutRadio)
        self.grid2.addWidget(ed_widg, 1, 5 + second)
        ed_checkbox = QtGui.QCheckBox(self)
        self.grid2.addWidget(ed_checkbox, 1, 6 + second)
            
        button_edit = QtGui.QPushButton("Down")
        btn_edit_callback = (lambda data = (edit_tv, \
             edit_se, edit_ep, ed_layoutRadio, \
             ed_checkbox): self.downClicked(data))
        self.connect(button_edit, \
             SIGNAL("clicked()"), btn_edit_callback)
        button_all_edit = QtGui.QPushButton("All")
        btn_edit_callbackAll = (lambda data = (edit_tv, \
             edit_se, edit_ep, ed_layoutRadio, \
             ed_checkbox): self.downAllClicked(data))
        self.connect(button_all_edit, \
             SIGNAL("clicked()"), btn_edit_callbackAll) 
#        self.connect(button_edit, \
#             SIGNAL("pressed()"), btn_edit_callback) 
        self.grid2.addWidget(edit_tv, 1, 0 + second)
        self.grid2.addWidget(edit_se, 1, 1 + second)
        self.grid2.addWidget(edit_ep, 1, 2 + second)
        self.grid2.addWidget(button_edit, 1, 3 + second)
        self.grid2.addWidget(button_all_edit, 1, 4 + second)
        
        
        #lines from next-episode
        list_ep = getListEpisode()

        combo_ondisk = []
        combo_notondisk = []
        ## radio1 = []
        ## radio2 = []
        ## radio3 = []
        ## radio4 = []
        ## layoutRadio = []
        ## widg = []
        ## checkbox = []
        button_down = []
        button_downAll = []
        button_play = []
        button_mark = []
        button_delete = []

        btn_callback = []
        btn_callbackAll = []
        btn_callbackPlay = []
        btn_callbackMark = []
        btn_callbackDelete = []

        i = 0

        for (i,(tvshow, season, ondisk, notondisk)) in enumerate(list_ep):
            if(ondisk != []):
                self.grid1.addWidget(QtGui.QLabel(tvshow), 2 + i, 0)
                self.grid1.addWidget(QtGui.QLabel(season), 2 + i, 1)
                combo_ondisk.append(QtGui.QComboBox(self))
                for (_movieId, _userId, _seasonId, episodeId) in ondisk:
                    combo_ondisk[i].addItem(str(episodeId))
                self.grid1.addWidget(combo_ondisk[i], 2 + i, 2)
                ##play
                button_play.append(QtGui.QPushButton("Play"))
                self.grid1.addWidget(button_play[i], 2 + i, 3)
                btn_callbackPlay.append(lambda data = (tvshow, season, \
                    combo_ondisk[i]): self.playClicked(data))
                self.connect(button_play[i], \
                    SIGNAL("clicked()"), btn_callbackPlay[i]) 
                ##mark
                button_mark.append(QtGui.QPushButton("Mark as read"))
                self.grid1.addWidget(button_mark[i], 2 + i, 4)
                btn_callbackMark.append(lambda data = (combo_ondisk[i], \
                    ondisk): self.markClicked(data))
                self.connect(button_mark[i], \
                    SIGNAL("clicked()"), btn_callbackMark[i])
                ##delete
                button_delete.append(QtGui.QPushButton("Delete"))
                self.grid1.addWidget(button_delete[i], 2 + i, 5)
                btn_callbackDelete.append(lambda data = (tvshow, season, \
                    combo_ondisk[i]): self.deleteClicked(data))
                self.connect(button_delete[i], \
                    SIGNAL("clicked()"), btn_callbackDelete[i]) 
            else:
                combo_ondisk.append([])
                button_play.append([])
                button_delete.append([])
                button_mark.append([])
                btn_callbackPlay.append([])
                btn_callbackDelete.append([])
                btn_callbackMark.append([])
#                self.grid1.addWidget(QtGui.QLabel("Nothing to watch"), 2 + i, 0)
                
            if(notondisk != []):
                self.grid2.addWidget(QtGui.QLabel(tvshow), 2 + i, 0 + second)
                self.grid2.addWidget(QtGui.QLabel(season), 2 + i, 1 + second)
                combo_notondisk.append(QtGui.QComboBox(self))
                for num in notondisk:
                    combo_notondisk[i].addItem(num)
                self.grid2.addWidget(combo_notondisk[i], 2 + i, 2 + second)
                ##down
                button_down.append(QtGui.QPushButton("Down"))
                self.grid2.addWidget(button_down[i], 2 + i, 3 + second)
                btn_callback.append(lambda data = (tvshow, season, \
                    combo_notondisk[i], ed_layoutRadio, \
                    ed_checkbox): self.downClicked(data))
                self.connect(button_down[i], \
                    SIGNAL("clicked()"), btn_callback[i])
                ##downAll
                button_downAll.append(QtGui.QPushButton("All"))
                self.grid2.addWidget(button_downAll[i], 2 + i, 4 + second)
                btn_callbackAll.append(lambda data = (tvshow, season, \
                    combo_notondisk[i], ed_layoutRadio, \
                    ed_checkbox): self.downAllClicked(data))
                self.connect(button_downAll[i], \
                    SIGNAL("clicked()"), btn_callbackAll[i]) 
            else:
                combo_notondisk.append([])
                button_down.append([])
                button_downAll.append([])
                btn_callback.append([])
                btn_callbackAll.append([])
# self.grid2.addWidget(QtGui.QLabel("Nothing to download"), 2 + i, 0 + second)
        self.grid2.addWidget(empty_label, 3 + i, 3 + second)

    @classmethod
    def saveClicked(cls, data):
        """ when a button is clicked """
        # data = [ [key, QLineEdit] , ... ]
        if (not os.path.exists(ospath.expanduser('~') + "/.config/flvdown/")):
            os.mkdir(ospath.expanduser('~') + "/.config/flvdown/")
        fileconf = open(ospath.expanduser('~') + "/.config/flvdown/flv.conf", "w", 0)
        for [key, line] in data:
            fileconf.write(key + "=\"" + str(line.text()) + "\"\n")
            conf[key] = str(line.text())
        fileconf.close()

    @classmethod
    def downClicked(cls, data):
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

        option = ""
        if (data[3].itemAt(1).widget().isChecked()):
            option += "z"
        elif (data[3].itemAt(2).widget().isChecked()):
            option += "l"
        elif (data[3].itemAt(3).widget().isChecked()):
            option += "n"
        if (data[4].isChecked()):
            option += "i"
        tvshow = "_".join(tvshow.split(' ')).lower()
        ret = ossystem("flvdown.py " + tvshow + " " + \
                  season + " " + episode + " " +option)#+ " &")
        if not ret:

            #cls.msgAlert.setIcon(QtGui.QIcon(''))
            cls.msgAlert.showMessage("flvgui", tvshow + season +\
                                     episode + "Done")
        


    @classmethod
    def downAllClicked(cls, data):
        """ when a buttonAll is clicked """
        if type(data[0]) == type(""):
            #data from combo
            tvshow = str(data[0])
            season = str(data[1])
            tvshow = "_".join(tvshow.split(' ')).lower()
            for i in range(data[2].count()):
                ossystem("flvdown.py " + tvshow + " " + \
                    season + " " + str(data[2].itemText(i)))
        else:
            #data from first line
            tvshow = str(data[0].text())
            season = str(data[1].text())
            tvshow = "_".join(tvshow.split(' ')).lower()
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
                ossystem("flvdown.py " + tvshow + " " + \
                    season + " " + str(i))


    @classmethod
    def downsub(cls):
        """ when a button_sub is clicked """
        #data from combo
        ossystem("downsub.sh")
        cls.msgAlert.showMessage("flvgui", "Subtitles, done")


    @classmethod
    def playClicked(cls, data):
        """ when a button_play is clicked """
        #data from combo
        tvshow = str(data[0])
        season = str(data[1])
        tvshow = "_".join(tvshow.split(' ')).lower()
        episode = str(data[2].currentText())
        if (len(episode)==1):
            episode = "0" + episode
        ossystem(conf['player']+ " " + tvshow + "/" + tvshow + season + episode + "*")

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
        if (len(episode)==1):
            episode = "0" + episode
#parent = ?
#        reply = QtGui.QMessageBox.question(self, 'Message',
#            "Are you sure you want to delete?", QtGui.QMessageBox.Yes | 
#            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
#        if reply:
        ossystem("rm " + tvshow + "/" + tvshow + season + episode + "*")




def main():
    """ main """
    app = QtGui.QApplication([])
    flv = Flvgui()
    flv.show()
    app.exec_()    


if __name__ == '__main__':
    main()

