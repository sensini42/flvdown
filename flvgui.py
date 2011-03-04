#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QThread

import os
import flvdown2
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

conf = {'login':'login', 'password':'password', \
    'player':'mplayer', 'base_directory':'/tmp'}

class DownThread(QThread):
    """download an episode in a thread"""
    def __init__(self, tvshow, season, episode, option, parent = None):
        self.tvshow = tvshow
        self.season = season
        self.episode = episode
        self.option = option
        QThread.__init__(self, parent)
        
    def run(self):
        "download ep, sub, emit signal"
        flvdown2.flvdown(self.tvshow, self.season, self.episode, self.option)
        ossystem("downsub.sh")
        self.emit(SIGNAL("downFinished( QString )"), \
                  self.tvshow + " " + self.season + " " + self.episode)

        ## ret = ossystem("flvdown.py " + self.tvshow + " " + \
        ##     self.season + " " + self.episode + " " +self.option)


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
        for line in fileconf.read().split():
            tmp = line.split("=")
            conf[tmp[0]] = tmp[1].replace('"','')
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
    

def removeFromNextEpisode(movieId, userId, seasonId, episodeId):
    """ return the source page from next-episode """

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
    txdata = urllib.urlencode ({"username" : conf['login'], \
        "password" : conf['password']})
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
        
    def __init__(self):
        """ nothing special here"""
        super(Flvgui, self).__init__()

        if (checkConfigFile()==-1):
            QtGui.QMessageBox.warning(self, 'Config File', \
                'Please check config', \
                QtGui.QMessageBox.StandardButton(QtGui.QMessageBox.Ok))

        self.tab_widget = QtGui.QTabWidget()
        
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()

        self.tab_widget.addTab(self.tab1, "Playing")
        self.tab_widget.addTab(self.tab2, "Downloading")
        self.tab_widget.addTab(self.tab3, "Options")
        self.tab_widget.setCurrentIndex(1)
        mainLayout = QtGui.QGridLayout(self)
        mainLayout.addWidget(self.tab_widget, 0, 0, 1, 3)

        self.populate()
        
        button_sub = QtGui.QPushButton("Subtitles")
        mainLayout.addWidget(button_sub, 1, 0)
        self.connect(button_sub, SIGNAL("clicked()"), self.downsub)
                
        button_refresh = QtGui.QPushButton("Refresh")
        mainLayout.addWidget(button_refresh, 1, 1)
        self.connect(button_refresh, SIGNAL("clicked()"), self.populate)
                
        button_close = QtGui.QPushButton("Close")
        mainLayout.addWidget(button_close, 1, 2)
        self.connect(button_close, SIGNAL("clicked()"), self, SLOT("close()"))

        self.setLayout(mainLayout)
        self.setWindowTitle('flvgui')


    def populate(self):
        "populate the tab_widget"
        oschdir(conf['base_directory'])
        focusingOn = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(2)
        self.tab_widget.removeTab(1)
        self.tab_widget.removeTab(0)
        del(self.tab1)
        del(self.tab2)
        del(self.tab3)

        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        
        grid1 = QtGui.QGridLayout(self.tab1)
        grid2 = QtGui.QGridLayout(self.tab2)
        grid3 = QtGui.QGridLayout(self.tab3)
        
        self.tab_widget.addTab(self.tab1, "Playing")
        self.tab_widget.addTab(self.tab2, "Downloading")
        self.tab_widget.addTab(self.tab3, "Options")
        
        self.tab_widget.setCurrentIndex(focusingOn)

        ##option
        ed_radio1 = QtGui.QRadioButton("*")
        ed_radio2 = QtGui.QRadioButton("z")
        ed_radio3 = QtGui.QRadioButton("l")
        ed_radio4 = QtGui.QRadioButton("n")
        ed_radio1.setChecked(1)
        ed_widg = QtGui.QWidget()
        ed_layoutRadio = QtGui.QHBoxLayout(ed_widg)
        ed_layoutRadio.addWidget(QtGui.QLabel('Only from : '))
        ed_layoutRadio.addWidget(ed_radio1)
        ed_layoutRadio.addWidget(ed_radio2)
        ed_layoutRadio.addWidget(ed_radio3)
        ed_layoutRadio.addWidget(ed_radio4)
        ed_widg.setLayout(ed_layoutRadio)
        grid3.addWidget(ed_widg, 0, 1)
        ed_checkbox = QtGui.QCheckBox('Interactive', self)
        grid3.addWidget(ed_checkbox, 0, 2)
            
        i = 0
        list_edit = []
        for key in conf.keys():
            grid3.addWidget(QtGui.QLabel(key), i+1, 0)
            list_edit.append([key, QtGui.QLineEdit()])
            grid3.addWidget(list_edit[i][1], i+1, 1, 1, 2) 
            if key == 'password':
                list_edit[i][1].setEchoMode(2)
            list_edit[i][1].setText(conf[key])
            i += 1
        button_save = QtGui.QPushButton("Save config file")
        btn_save_callback = (lambda data = (list_edit) : \
             self.saveClicked(data))
        self.connect(button_save, SIGNAL("clicked()"), btn_save_callback)
        grid3.addWidget(button_save, 5, 0)
        
        ##titles
        empty_label = QtGui.QLabel("")
        grid1.addWidget(QtGui.QLabel('Tv show'), 0, 0 )
        grid1.addWidget(QtGui.QLabel('Season'), 0, 1 )
        grid1.addWidget(QtGui.QLabel('Episode'), 0, 2 )

        grid2.addWidget(QtGui.QLabel('Tv show'), 0, 0)
        grid2.addWidget(QtGui.QLabel('Season'), 0, 1)
        grid2.addWidget(QtGui.QLabel('Episode'), 0, 2)
        grid2.addWidget(empty_label, 0, 3)
        grid2.addWidget(empty_label, 0, 4)

        #first line
        edit_tv = QtGui.QLineEdit()
        edit_se = QtGui.QLineEdit()
        edit_ep = QtGui.QLineEdit()
        
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
        grid2.addWidget(edit_tv, 1, 0)
        grid2.addWidget(edit_se, 1, 1)
        grid2.addWidget(edit_ep, 1, 2)
        grid2.addWidget(button_edit, 1, 3)
        grid2.addWidget(button_all_edit, 1, 4)
        
        
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

        i_ondisk = 0
        i_notondisk = 0

        for (i,(tvshow, season, ondisk, notondisk)) in enumerate(list_ep):
            if(ondisk != []):
                grid1.addWidget(QtGui.QLabel(tvshow), 1 + i_ondisk, 0)
                grid1.addWidget(QtGui.QLabel(season), 1 + i_ondisk, 1)
                combo_ondisk.append(QtGui.QComboBox(self))
                for (_movieId, _userId, _seasonId, episodeId) in ondisk:
                    combo_ondisk[i].addItem(str(episodeId))
                grid1.addWidget(combo_ondisk[i], 1 + i_ondisk, 2)
                ##play
                button_play.append(QtGui.QPushButton("Play"))
                grid1.addWidget(button_play[i], 1 + i_ondisk, 3)
                btn_callbackPlay.append(lambda data = (tvshow, season, \
                    combo_ondisk[i]): self.playClicked(data))
                self.connect(button_play[i], \
                    SIGNAL("clicked()"), btn_callbackPlay[i]) 
                ##mark
                button_mark.append(QtGui.QPushButton("Mark as read"))
                grid1.addWidget(button_mark[i], 1 + i_ondisk, 4)
                btn_callbackMark.append(lambda data = (combo_ondisk[i], \
                    ondisk): self.markClicked(data))
                self.connect(button_mark[i], \
                    SIGNAL("clicked()"), btn_callbackMark[i])
                ##delete
                button_delete.append(QtGui.QPushButton("Mark and Delete"))
                grid1.addWidget(button_delete[i], 1 + i_ondisk, 5)
                btn_callbackDelete.append(lambda data = (tvshow, season, \
                    combo_ondisk[i], ondisk): self.deleteClicked(data))
                self.connect(button_delete[i], \
                    SIGNAL("clicked()"), btn_callbackDelete[i]) 
                i_ondisk += 1
            else:
                combo_ondisk.append([])
                button_play.append([])
                button_delete.append([])
                button_mark.append([])
                btn_callbackPlay.append([])
                btn_callbackDelete.append([])
                btn_callbackMark.append([])
# grid1.addWidget(QtGui.QLabel("Nothing to watch"), 2 + i, 0)
                
            if(notondisk != []):
                grid2.addWidget(QtGui.QLabel(tvshow), 2 + i_notondisk, 0)
                grid2.addWidget(QtGui.QLabel(season), 2 + i_notondisk, 1)
                combo_notondisk.append(QtGui.QComboBox(self))
                for num in notondisk:
                    combo_notondisk[i].addItem(num)
                grid2.addWidget(combo_notondisk[i], 2 + i_notondisk, 2)
                ##down
                button_down.append(QtGui.QPushButton("Down"))
                grid2.addWidget(button_down[i], 2 + i_notondisk, 3)
                btn_callback.append(lambda data = (tvshow, season, \
                    combo_notondisk[i], ed_layoutRadio, \
                    ed_checkbox): self.downClicked(data))
                self.connect(button_down[i], \
                    SIGNAL("clicked()"), btn_callback[i])
                ##downAll
                button_downAll.append(QtGui.QPushButton("All"))
                grid2.addWidget(button_downAll[i], 2 + i_notondisk, 4)
                btn_callbackAll.append(lambda data = (tvshow, season, \
                    combo_notondisk[i], ed_layoutRadio, \
                    ed_checkbox): self.downAllClicked(data))
                self.connect(button_downAll[i], \
                    SIGNAL("clicked()"), btn_callbackAll[i]) 
                i_notondisk += 1
            else:
                combo_notondisk.append([])
                button_down.append([])
                button_downAll.append([])
                btn_callback.append([])
                btn_callbackAll.append([])
        button_downAllES = QtGui.QPushButton("Down All")
        grid2.addWidget(button_downAllES, 3 + i_notondisk, 3, 1, 2)
        btn_callbackAllES = lambda data = (list_ep): \
            self.downAllESClicked(data)
        self.connect(button_downAllES, SIGNAL("clicked()"), btn_callbackAllES)


    @classmethod
    def saveClicked(cls, data):
        """ when a button is clicked """
        # data = [ [key, QLineEdit] , ... ]
        if (not os.path.exists(ospath.expanduser('~') + "/.config/flvdown/")):
            os.mkdir(ospath.expanduser('~') + "/.config/flvdown/")
        fileconf = open(ospath.expanduser('~') + \
            "/.config/flvdown/flv.conf", "w", 0)
        for [key, line] in data:
            fileconf.write(key + "=\"" + str(line.text()) + "\"\n")
            conf[key] = str(line.text())
        fileconf.close()


    def downFinished(self, message):
        """ when a download is finished """
        print "Download finished", message

#    @classmethod
    def downclicked(self, data):
        """ when a button is clicked """
        # data = [tv, season, numepisode, fromsite, interactif]
        if type(data[0]) == type(""):
            #data from combo
            tvshow = str(data[0])
            season = str(data[1])
            episode = str(data[2].currenttext())
        else:
            #data from first line
            tvshow = str(data[0].text())
            season = str(data[1].text())
            episode = str(data[2].text())

        option = ""
        if (data[3].itemat(1).widget().ischecked()):
            option += "z"
        elif (data[3].itemat(2).widget().ischecked()):
            option += "l"
        elif (data[3].itemat(3).widget().ischecked()):
            option += "n"
        if (data[4].ischecked()):
            option += "i"
        tvshow = "_".join(tvshow.split(' ')).lower()
        dth = downthread(tvshow, season, episode, option, self)
        self.connect(dth, signal("downfinished( qstring ) "), self.downfinished)
        dth.start() 

    #@classmethod
    def downallclicked(self, data):
        """ when a buttonall is clicked """
        if type(data[0]) == type(""):
            #data from combo
            tvshow = str(data[0])
            season = str(data[1])
            tvshow = "_".join(tvshow.split(' ')).lower()
            for i in range(data[2].count()):
                dth = downthread(tvshow, season, str(data[2].itemtext(i)),\
                                 "", self)
                self.connect(dth, signal("downfinished( qstring ) "),\
                             self.downfinished)
                dth.start() 
                
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
                dth = downthread(tvshow, season, str(i), "",\
                                 self)
                self.connect(dth, signal("downfinished( qstring ) "),\
                             self.downfinished)
                dth.start()




#    @classmethod
    def downallesclicked(self, data):
        """ when the buttondownalles is clicked """
        for (tvshow, season, _ondisk, notondisk) in data:
            tvshow = "_".join(tvshow.split(' ')).lower()
            for epi in notondisk:
                dth = downthread(tvshow, str(season), str(epi), "", self)
                self.connect(dth, signal("downfinished( qstring ) "), self.downfinished)
                dth.start()

    @classmethod
    def downsub(cls):
        """ when a button_sub is clicked """
        #data from combo
        ossystem("downsub.sh")

#    @classmethod
    def playClicked(self, data):
        """ when a button_play is clicked """
        #data from combo
        tvshow = str(data[0])
        season = str(data[1])
        tvshow = "_".join(tvshow.split(' ')).lower()
        episode = str(data[2].currentText())
        if (len(episode)==1):
            episode = "0" + episode
        VideoThread((conf['player']+ " " + tvshow + "/" + tvshow + \
            season + episode + "*"), self).start()

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

