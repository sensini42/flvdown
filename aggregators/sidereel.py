"""module for free-tv-video-onine.me"""
import sidereel_mod
from . import getPage

def getTvShowUrl(tvshow, season, episode, numPage):
    """get url for tvshow"""
    tv2 = "_".join([i.capitalize() for i in tvshow.split('_')])
    epi2 = str(int(episode)) #get ride of trailing 0
    urlbase = 'http://www.sidereel.com/'
    urltv = urlbase + tv2 + '/season-' + season + \
            '/episode-' + epi2 + '/search?page=' + str(numPage)
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    numPage = 1
    possible_links = []
    doNext = True
    while(doNext):
        urltv = getTvShowUrl(tvshow, season, episode, numPage)
        src_urltv = getPage(urltv)
        if (src_urltv == -1):
            return possible_links
        npage = False
        for line in src_urltv:
            if ("next_page" in line):
                npage = True
            if ("disabled next_page" in line):
                doNext = False
            for nameModule in sidereel_mod.__all__:
                realName = sidereel_mod.__all2__[nameModule]
                if ((realName in line) and ('data-viewable-url') in line):
                    possible_links.append([line.split('"')[5], \
                                           "sidereel_mod." + nameModule])
        numPage += 1
        if (npage == False):
            doNext = False
    return possible_links
    
        
    

    ## liste=[]
    ## for i in sidereel_mod.__all__:
    ##     __import__("aggregators.sidereel_mod." + i)
    ##     liste += sys.modules["aggregators.sidereel_mod."+i].getFlv(a)
    ## return liste

