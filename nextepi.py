#!/usr/bin/python
# -*- coding: utf-8 -*-
""" connect to next-episode and manage episode """

## from tempfile import NamedTemporaryFile

## cookieFile = NamedTemporaryFile(suffix='.cookies-next.lwp')
## cookieFileName = cookieFile.name

## cj = None
## cookielib = None

## import cookielib            
## import urllib2    
## import urllib
## urlopen = urllib2.urlopen
## cj = cookielib.LWPCookieJar()
## request = urllib2.Request

## if cookielib:
##     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
##     urllib2.install_opener(opener)

from episodetv import episodeTV
class nextepi():
    """ connect to next-episode and manage episode """

    def __init__(self, login, password):
        self.__login = login
        self.__pwd = password
        self.__log()
        self.__userId = None        ## to delete show
        self.__list = self.__listToWatch()

    def __log(self):
        """ first connexion to next-episode : log in, fill userID """
        pass
    #http://stackoverflow.com/questions/2030652/logging-into-facebook-with-python
        ## cookie = cookielib.CookieJar()
        ## opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cookie ) )
        ## urllib2.install_opener( opener )

    ###ou vont les cookies ? 
        ## import urllib
        ## txdata = urllib.urlencode ({"username" : conf['login'], \
        ##     "password" : conf['password']})
        ## txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}

        ## try:
        ##     req = request("http://next-episode.net/", txdata, txheaders)
        ##     urlopen(req)
        ## except IOError:
        ##     print "could not login"
        ##     return ""
        ## txdata = None
        ## cj.save(cookieFileName)

    def __listToWatch(self):
        """ return the list of episode not seen """
        ##epi = episodeTV(show, bla, bli)
        ## return  a list of epi
    ## source = getSrcPageNextEpisode("track/")
    ## if (source == ""):
    ##     return []
    
    ## src = source.split('showName">')

    ## dict_bug = {'The Office (US)' : 'The Office'}
    ## listep = []
    ## for i in src[1:]:
    ##     lines = i.split('\n')
    ##     if lines[0].endswith("</a>"):
    ##         #else: tvshow not tracked
    ##         item_ep_ondisk = []
    ##         item_ep_notondisk = []
    ##         for i in lines:
    ##             if "removeEpisode" in i:
    ##                 tv_name = lines[0][:-4]
    ##                 if tv_name in dict_bug:
    ##                     tv_name = dict_bug[tv_name]
    ##                 item_se = i.split()[9][1:-2]
    ##                 num_ep = i.split()[10][1:-2]
    ##                 strlist = i.split("removeEpisode(")[1].split(')')[0]
    ##                 epilist = [x[1:-1] for x in strlist.split(', ')[:-1]]
    ##                 if(not existFile(tv_name, item_se, num_ep)):
    ##                     item_ep_notondisk.append(num_ep)
    ##                 else:
    ##                     item_ep_ondisk.append(epilist)
    ##         if(item_ep_ondisk or item_ep_notondisk):
    ##             listep.append((tv_name, item_se, item_ep_ondisk, \
    ##                            item_ep_notondisk))
    ## return listep

        pass

    def getList(self):
        return self.__list

    def addShow(self, title):
        """ add the _title_ show to watch """
        pass
        ## urltitle = '-'.join(title.split(' ')) + '/'
        ## src = getSrcPageNextEpisode(urltitle)
        ## url = src.split('to watchlist')[0].split('"')[-2]
        ## src = getSrcPageNextEpisode(url)


    def markAsRead(self, episode):
        """ mark the episode as read"""
        pass
    ## import urllib
    ## txdata = urllib.urlencode ({"username" : conf['login'], \
    ##     "password" : conf['password']})
    ## txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Win NT)'}
    ## urlbase = "http://next-episode.net/"
    ## try:
    ##     req = request(urlbase, txdata, txheaders)
    ##     urlopen(req)
    ## except IOError:
    ##     print "could not login"
    ##     return ""

    ## cj.save(cookieFileName)

    ## url = urlbase + 'PAGES/stufftowatch_files/ajax/ajax_requests_stuff.php'    
    ## txdata = urllib.urlencode ({"showCat" : "episode",
    ##                             "movieId" : movieId,
    ##                             "userId" : userId,
    ##                             "seasonId" : seasonId,
    ##                             "episodeId" : episodeId,
    ##                             "parsedString" : seasonId + "x" + episodeId})
    ## req = request(url, txdata, txheaders)
    
    ## src = urlopen(req).read()
    ## print src

    


    def __getSrc(url):
        """ return the source page from next-episode """
        pass
        ## req = request("http://next-episode.net/" + url, txdata, txheaders)
        ## src = urlopen(req).read()
        ## return src


#some ideas
    def isSeasonFinished(title):
        """ bla """
        pass

    def listNextSeason(title):
        """ bla """
        pass

    def removeShow(title):
        """ bla """
        pass

    def trackShow(title):
        """ bla """
        pass

    def untrackShow(title):
        """ bla """
        pass

    def getSuggestions():
        """ bla """
        pass
