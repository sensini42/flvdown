#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT


###take care of cookies
cookieFile = 'cookies-next.lwp'
from os import path as ospath
from os import system as ossystem
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

def getListEpisode():
    """ return the list of episode from next-episode """    
    try:                                
        fileconf = open(ospath.expanduser('~') + "/.config/flvdown/flv.conf", \
                         "rb", 0)
        try:
            conffile = fileconf.read().split()
            login = conffile[0]
            password = conffile[1]
        except IndexError:
            print "bad format:"
            print 'echo -n "login\npassword" > ~/.config/flvdown/flv.conf'
            exit(1)
        finally:
            fileconf.close()              
    except IOError:
        print "conf file not found"
        print "mkdir ~/.config/flvdown"
        print 'echo -n "login\npassword" > ~/.config/flvdown/flv.conf'
        return []

    import urllib
    txdata = urllib.urlencode ({"username" : login, "password" : password})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}

    try:
        req = request("http://next-episode.net/", txdata, txheaders)
        urlopen(req)
    except IOError:
        print "could not login"
        return []

    cj.save(cookieFile)
    
    req = request("http://next-episode.net/track/", txdata, txheaders)
    src = urlopen(req).read().split('showName">')
    listep = []
    for i in src[1:]:
        lines = i.split('\n')
        if lines[0].endswith("</a>"):
            #else: tvshow not tracked
            item_ep = []
            for i in lines:
                if "removeEpisode" in i:
                    item_se = i.split()[9][1:-2]
                    item_ep.append(i.split()[10][1:-2])
            listep.append((lines[0][:-4], item_se, item_ep))

    return listep



            
class Flvgui(QtGui.QWidget):
    """ Gui for flvdown"""
    
    def __init__(self):
        """ nothing special here"""
        super(Flvgui, self).__init__()


        grid = QtGui.QGridLayout()

        ##titles
        grid.addWidget(QtGui.QLabel('Tv show'), 0, 0)
        grid.addWidget(QtGui.QLabel('Season'), 0, 1)
        grid.addWidget(QtGui.QLabel('Episode'), 0, 2)

        edit_tv = QtGui.QLineEdit()
        edit_se = QtGui.QLineEdit()
        edit_ep = QtGui.QLineEdit()
        self.button_edit = QtGui.QPushButton("Down")
        self.btn_edit_callback = (lambda data = (edit_tv, \
             edit_se, edit_ep): self.downClicked(data))
        self.connect(self.button_edit, \
             SIGNAL("clicked()"), self.btn_edit_callback) 
#        self.connect(self.button_edit, \
#             SIGNAL("pressed()"), self.btn_edit_callback) 



        grid.addWidget(edit_tv, 1, 0)
        grid.addWidget(edit_se, 1, 1)
        grid.addWidget(edit_ep, 1, 2)
        grid.addWidget(self.button_edit, 1, 3)
        ###Should get the list from next-episode
        list_ep = getListEpisode()

        self.combo = []
        self.button_down = []
        self.button_downAll = []
        self.btn_callback = []
        self.btn_callbackAll = []
        i = 0
        for (i,(tvshow, season, num_list)) in enumerate(list_ep):
            grid.addWidget(QtGui.QLabel(tvshow), 2 + i, 0)
            grid.addWidget(QtGui.QLabel(season), 2 + i, 1)
            self.combo.append(QtGui.QComboBox(self))
            for num in num_list:
                self.combo[i].addItem(num)
            grid.addWidget(self.combo[i], 2 + i, 2)

            self.button_down.append(QtGui.QPushButton("Down"))
            grid.addWidget(self.button_down[i], 2 + i, 3)
            self.btn_callback.append(lambda data = (tvshow, season, \
                 self.combo[i]): self.downClicked(data))
            self.connect(self.button_down[i], \
                         SIGNAL("clicked()"), self.btn_callback[i]) 
            self.button_downAll.append(QtGui.QPushButton("All episodes"))
            grid.addWidget(self.button_downAll[i], 2 + i, 4)
            self.btn_callbackAll.append(lambda data = (tvshow, season, \
                 self.combo[i]): self.downAllClicked(data))
            self.connect(self.button_downAll[i], \
                         SIGNAL("clicked()"), self.btn_callbackAll[i]) 

  

        empty_label = QtGui.QLabel("")
        grid.addWidget(empty_label, 3 + i, 3)
        
        button_close = QtGui.QPushButton("Close")
        grid.addWidget(button_close, 4 + i, 2)
        self.connect(button_close, SIGNAL("clicked()"), self, SLOT("close()"))
#        self.connect(button_close, SIGNAL("pressed()"), self, SLOT("close()"))

        self.setLayout(grid)
        self.setWindowTitle('flvgui')

    @classmethod
    def downClicked(cls, data):
        """ when a button is clicked """
        # data = [tv, season, numepisode]
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
        tvshow = "_".join(tvshow.split(' ')).lower()
        ossystem("flvdown.py " + tvshow + " " + \
                  season + " " + episode )#+ " &")


    @classmethod
    def downAllClicked(cls, data):
        """ when a buttonAll is clicked """
        #data from combo
        tvshow = str(data[0])
        season = str(data[1])
        tvshow = "_".join(tvshow.split(' ')).lower()
        for i in range(data[2].count()):
            ossystem("flvdown.py " + tvshow + " " + \
                  season + " " + str(data[2].itemText(i)))

def main():
    """ main """
    app = QtGui.QApplication([])
    flv = Flvgui()
    flv.show()
    app.exec_()    


if __name__ == '__main__':
    main()
