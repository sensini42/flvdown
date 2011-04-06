"""module for free-tv-video-online.me, testing different modules"""
import free2_mod
from . import getPage

def getTvShowUrl(tvshow, season):
    """get url for tvshow"""
    urlbase = 'http://www.free-tv-video-online.me/internet/'
    urltv = urlbase + tvshow + '/season_' + season + '.html'
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    urltv = getTvShowUrl(tvshow, season)
    src_urltv = getPage(urltv)
    possible_links = []
    for line in src_urltv:
        for nameModule in free2_mod.__all__:
            if ((nameModule in line) and (('Episode '+episode + '<') in line)):
                possible_links.append([line.split('"')[1], \
                    "free2_mod." + nameModule])
    return possible_links
    
        
    

    ## liste=[]
    ## for i in free1_mod.__all__:
    ##     __import__("aggregators.free1_mod." + i)
    ##     liste += sys.modules["aggregators.free1_mod."+i].getFlv(a)
    ## return liste

