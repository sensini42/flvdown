#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
import cookielib



###take care of cookies

COOKIEFILE = 'cookies-next.lwp'
import os.path
cj = None
ClientCookie = None
cookielib = None
try:                      
    import cookielib            
except ImportError:
    pass
else:
    import urllib2    
    urlopen = urllib2.urlopen
    cj = cookielib.LWPCookieJar()
    Request = urllib2.Request
if not cookielib:                
    try:                                            
        import ClientCookie 
    except ImportError:
        import urllib2
        urlopen = urllib2.urlopen
        Request = urllib2.Request
    else:
        urlopen = ClientCookie.urlopen
        cj = ClientCookie.LWPCookieJar()
        Request = ClientCookie.Request
if cj != None:
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)
    if cookielib:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    else:
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)
##end of cookie




def getpage(urlp,  txdatap, txheadersp):
    """ return the source of urlp"""
    try:
        reqp = Request(urlp, txdatap, txheadersp)
        handlep = urlopen(reqp)
    except IOError, erp:
        print 'We failed to open "%s".' % urlp
        if hasattr(erp, 'code'):
            print 'We failed with error code - %s.' % erp.code
    else:
        pass
    return handlep


def getListEpisode():
    """ return the list of episode from next-episode """
    
    try:                                
        fileconf = open("flv.conf", "rb", 0)
        try:
            conffile = fileconf.read().split()
            login = conffile[0]
            password = conffile[1]
        except Exception:
            print "bad format:"
            print 'echo -n "login\npassword" >flv.conf'
            exit(1)
        finally:
            fileconf.close()              
    except IOError:
        print "conf file not found"
        print 'echo -n "login\npassword" >flv.conf'
        return []


    theurl = "http://next-episode.net/"
    import urllib
    txdata = urllib.urlencode ({"username" : login, "password" : password})
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    try:
        req = Request(theurl, txdata, txheaders)
        handle = urlopen(req)
    except IOError, e:
        print "could not login", e
        return []

    if cj == None:
        print "We don't have a cookie library available - sorry."
        print "I can't show you any cookies."
    else:
        #print 'These are the cookies we have received so far :'
        for index, cookie in enumerate(cj):
            pass #print index, cookie
        cj.save(COOKIEFILE)
    
    url = theurl + "track/"
    handle = getpage(url,  txdata, txheaders)
    src = handle.read().split('showName">')
    listep = []
    for i in src[1:]:
        lines = i.split('\n')
        item_tv = lines[0][:-4]
        if lines[0].endswith("</a>"):
            #else: show not tracked
            item_ep = []
            for i in lines:
                if "removeEpisode" in i:
                    item_se = i.split()[9][1:-2]
                    item_ep.append(i.split()[10][1:-2])
            listep.append((item_tv, item_se, item_ep))

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
        edit_se = QtGui.QLineEdit("n")
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
        self.btn_callback = []
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
#            self.connect(self.button_down[i], \
#                         SIGNAL("pressed()"), self.btn_callback[i]) 
  

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
        print tvshow, season, episode
        import os
        #test here if file exists ?
        os.system("flvdown.py " + tvshow + " " + \
                  season + " " + episode )#+ " &")

def main():
    """ main """
    app = QtGui.QApplication([])
    flv = Flvgui()
    flv.show()
    app.exec_()    


if __name__ == '__main__':
    main()
