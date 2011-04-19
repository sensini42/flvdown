#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gui for playing tab """

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL


class EltListDictBug(QtGui.QWidget):

    def __init__(self, nature, key='', value=''):
        super(EltListDictBug, self).__init__()
        self.mainLayout = QtGui.QHBoxLayout(self)
    
        self.arrowlabel = QtGui.QLabel("->")
        self.arrowlabel.setAlignment(Qt.AlignHCenter)

        if nature == 0:
            self.createTitle()
        elif nature == 1:
            self.createNew()
        elif nature == 2:
            self.createEntry(key, value)
        else:
            raise Exception('unknown nature')


    def createTitle(self):
        self.mainLayout.addWidget(QtGui.QLabel('Next-episode'))
        self.mainLayout.addWidget(self.arrowlabel)
        self.mainLayout.addWidget(QtGui.QLabel('Down'))
        self.mainLayout.addWidget(QtGui.QLabel(''))
    
    def createNew(self):
        self.lineedit_ne = QtGui.QLineEdit()
        self.lineedit_d = QtGui.QLineEdit()
        button_add = QtGui.QPushButton("Add dict bug")
        button_add.connect(button_add, SIGNAL("clicked()"), self.addDictBug)
        self.mainLayout.addWidget(self.lineedit_ne)
        self.mainLayout.addWidget(self.arrowlabel)
        self.mainLayout.addWidget(self.lineedit_d)
        self.mainLayout.addWidget(button_add)

    def createEntry(self, key, value):
        button_rmv = QtGui.QPushButton("Remove")
        button_rmv_callback = (lambda data = [key, value]: \
            self.removeDictBug(data))
        button_rmv.connect(button_rmv, SIGNAL("clicked()"), \
            button_rmv_callback)
        self.mainLayout.addWidget(QtGui.QLabel(key))
        self.mainLayout.addWidget(self.arrowlabel)
        self.mainLayout.addWidget(QtGui.QLabel(value))
        self.mainLayout.addWidget(button_rmv)

    def removeDictBug(self, data):
        self.emit(SIGNAL("removeDictBug( PyQt_PyObject )"), data)

    def addDictBug(self):
        self.emit(SIGNAL("addDictBug( PyQt_PyObject )"), \
           [self.lineedit_ne.text(), self.lineedit_d.text()])

class Dictbug(QtGui.QWidget):
    """ display playing list """

    def __init__(self, dict_bug, parent=None):
        """ initialisation """
        super(Dictbug, self).__init__()

        self.parent = parent

        self.list_dictbug = dict_bug
        self.eltdictbug = []

        self.populate()

    def populate(self):
        """ create layout """
        
        mainLayout = QtGui.QVBoxLayout(self)

        mainLayout.addWidget(EltListDictBug(0))

        add = EltListDictBug(1)
        self.connect(add, SIGNAL("addDictBug(PyQt_PyObject)"), \
            self.addDictBug)
        mainLayout.addWidget(add)

        self.dictbug = QtGui.QGridLayout()
        mainLayout.addLayout(self.dictbug)

        button_save = QtGui.QPushButton("Save config file")
        self.connect(button_save, SIGNAL("clicked()"), self.saveClicked)
        mainLayout.addWidget(button_save)

        self.refresh5()

    def saveClicked(self):
        self.parent.updateConf()

    def getListDictBug(self):
        return self.list_dictbug
   
    def addDictBug(self, data):
        self.list_dictbug[str(data[0])] = str(data[1])
        self.refresh5()

    def removeDictBug(self, data):
        del self.list_dictbug[data[0]]
        self.refresh5()

    def refresh5(self):    
        for i in self.eltdictbug:
            i.setParent(None)
            del(i)

        self.eltdictbug = []
        for key in self.list_dictbug.keys():
            tmp = EltListDictBug(2, key, self.list_dictbug[key])
            self.connect(tmp, SIGNAL("removeDictBug(PyQt_PyObject)"), \
                self.removeDictBug)
            self.dictbug.addWidget(tmp)
            self.eltdictbug.append(tmp)
