#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for flvdown """
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT

def getListEpisode():
    """ return the list of episode from next-episode """
    listep = []
    listep.append(("toto", "4", ["03", "04", "05"]))
    listep.append(("tata", "1", ["13", "14", "15"]))
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
        tvshow = "_".join(tvshow.split(' '))
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
