#!/usr/bin/python
# -*- coding: utf-8 -*-
""" connect to next-episode and manage episode """

from urllib import urlencode
from urllib2 import Request, build_opener, HTTPCookieProcessor, \
   install_opener, urlopen
from cookielib import LWPCookieJar
from tempfile import NamedTemporaryFile

import re
from re import findall

from episodetv import episodeTV
from operator import attrgetter

chgcs = re.compile("changeCurrentSeason\('(.*)', '(.*)', '(.*)', '(.*)', '(.*)', .*\)")
rmve = re.compile("removeEpisode\('(.*)', '(.*)', '(.*)', '(.*)', .*\)")
stop = re.compile("\('(.*)', '(.*)', '(.*)', .*\)")

class NextEpisode():
    """ class to deal with next-episode.net """

    def __init__(self, login, password, dict_bug):
        # save parameters
        self.__login = login
        self.__pwd = password
        self.dict_bug = dict_bug
        
        # misc
        self.__txheaders = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; WinNT)'}
        self.__urlbase = 'http://next-episode.net/'
        self.__list = None
        
        # take care of cookies
        self.__cookieFile = NamedTemporaryFile()
        self.__cj = LWPCookieJar()
        opener = build_opener(HTTPCookieProcessor(self.__cj))
        install_opener(opener)
        
        self.__connect()
        #self.update(dict_bug)


    def __getSrcPage(self, url, txdata=None):
        """ return the source page from next-episode """
        req = Request(self.__urlbase + url, txdata, self.__txheaders)
        src = urlopen(req).read()
        self.__cj.save(self.__cookieFile.name)
        return src

    def __connect(self):
        """ first connexion to next-episode : log in """
        txdata = urlencode({"username": self.__login, "password": self.__pwd})
        try:
            self.__getSrcPage('userlogin', txdata)
        except:
            raise Exception('Connect Error')
        

    def __getListEpisode(self):
        """ get list episode from next-episode """
        source = self.__getSrcPage('track/?mode=Tree')
        if not source:
            return []

        src = source.split('stopTracking')
        listep = set()
        
        for i in src[1:]:
            lines = i.split('\n')
            resul = stop.search(lines[0])
            idshow = resul.group(1)
            iduser = resul.group(2)
            tv_name = resul.group(3).lower()
            if tv_name not in self.dict_bug:
                self.dict_bug[tv_name] = {}
                name = '_'.join(tv_name.split(' ')).lower()
                self.dict_bug[tv_name]['default'] = name
            for i in lines:
                if ("hiddenValues_" + idshow) in i:
                    lepi = i.split('"')[3].split(',')[:-1]
                    for sxe in lepi:
                        idseason, idepisode = sxe.split('x')
                        epitv = episodeTV(tv_name, idseason, idepisode, \
                                     (idshow, iduser, idseason, idepisode), \
                                     self.dict_bug[tv_name])
                        listep.add(epitv)
        listep = sorted(listep, key=attrgetter('tvshow_', 'strSeason', 'strEpisode'))

        return listep

    def getTracked(self):
        """ get list of tracked tv shows"""
        source = self.__getSrcPage('track/?mode=Tree')
        if not source:
            return []

        src = source.split('stopTracking')
        listS = []
        
        for i in src[1::2]:
            lines = i.split('\n')
            resul = stop.search(lines[0])
            idshow = resul.group(1)
            iduser = resul.group(2)
            tv_name = resul.group(3).lower()
            if tv_name in self.dict_bug:
                tv_name = self.dict_bug[tv_name]['default']
            listS.append([tv_name, idshow, iduser])

        listS.sort()

        return listS
    
    def getUntracked(self):
        """ get list of untracked tv shows"""
        source = self.__getSrcPage('track/?mode=Tree')
        if not source:
            return []

        src = source.split('?startTracking=')
        listS = []
        
        for i in src[1:]:
            lines = i.split('\n')
            idshow = lines[0].split('"')[0]
            tv_name = lines[0].split('class="showName">')[1][:-10]
            if tv_name in self.dict_bug:
                tv_name = self.dict_bug[tv_name]['default']
            listS.append([tv_name, idshow])
        listS.sort()

        return listS
    
    def addShow(self, title):
        """ add the _title_ show to watchlist """
        src = self.__getSrcPage('-'.join(title.split(' ')))
        url = src.split('to watchlist')[0].split('"')[-2]
        self.__getSrcPage(url)

    def markAsRead(self, movieId, userId, seasonId, episodeId):
        """ mark the episode as read"""
        url = 'PAGES/stufftowatch_files/ajax/ajax_requests_stuff.php'
        txdata = urlencode({"showCat": "episode", \
                            "movieId": movieId, \
                            "userId": userId, \
                            "seasonId": seasonId, \
                            "episodeId": episodeId, \
                            "parsedString": seasonId + "x" + episodeId})
        self.__getSrcPage(url, txdata)


    def update(self, dict_bug, login=None, password=None):
        """ update the list of episodes """
#        for i in self.__list:
#            del(i)#utile?
        self.dict_bug = {}
        self.dict_bug.update(dict_bug)
        changeLP = False
        if login:
            self.__login = login
            changeLP = True
        if password:
            self.__pwd = password
            changeLP = True
        if changeLP:
            self.__connect()
        self.__list = self.__getListEpisode()
        
    def getList(self):
        """ return the list of episodes """
        return self.__list
        
    def printList(self):
        """ print the list of episodes """
        for i in  self.__list:
            print i.getBaseName()
        
    def removeShow(self, title):
        """ remove the _title_show from watchlist """
        src = self.__getSrcPage('-'.join(title.split(' ')))
        url = src.split('from watchlist')[0].split('"')[-2]
        self.__getSrcPage(url)

    def trackShow(self, movieId):
        """ trackshow """
        self.__getSrcPage('track?startTracking=' + movieId)

    def untrackShow(self, movieId, userId):
        """ untrack show """
        url = 'PAGES/stufftowatch_files/ajax/ajax_requests_stuff.php'
        txdata = urlencode({"showCat": "stopTracking", \
                            "movieId": movieId, \
                            "userId": userId, \
                            "seasonId": 0, \
                            "episodeId": 0, \
                            "parsedString": 0})
        self.__getSrcPage(url, txdata)

    def getListShow(self):
        """
        return the list of current show
        """
        source = self.__getSrcPage('settings?action=manageWL')
        if not source:
            return []
        src = source.split('\n')
        show = []
        for i in src:
            if 'addedShows[' in i:
                res = findall('"([^_]*)_', i)
                tv_name = res[0].lower()
                if tv_name in self.dict_bug:
                    tv_name = self.dict_bug[tv_name]['default']
                show.append(tv_name)
        return show

    def getSuggestions(self):
        """
        return the list of suggestion
        in format (tvshow, movieid)
        """
        source = self.__getSrcPage('we_suggest/')
        if not source:
            return []
        src = source.split('\n')
        sugges = []
        for i in src:
            if 'hideid' in i:
                res = findall('href="([^"]*)"', i)
                for i in range(len(res)-1):
                    if 'hideid' in res[i+1]:
                        sugges.append( (res[i].split('/')[-1], \
                            res[i+1].split('=')[-1]) )
                break
        return sugges


import sys
if __name__ == '__main__':
    ne = NextEpisode(sys.argv[1], sys.argv[2])
    ne.printList()
    #print ne.getListEpisode()
    #ne.addShow('chelsea lately')
    #ne.removeEpisode('619', '66436', '5', '7')


