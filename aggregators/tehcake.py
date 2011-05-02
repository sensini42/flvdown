"""module for tehcake.com"""
import tehcake_mod
from . import getPage

def getTvShowUrl(tvshow, season, episode):
    """get url for tvshow"""
    urlbase = 'http://www.tehcake.com/video/'
    ntvshow = ''.join(tvshow.split('_')).capitalize()
    urltv = urlbase + ntvshow + '/' + season + 'x' + str(int(episode)) + '.html'
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    urltv = getTvShowUrl(tvshow, season, episode)
    src_urltv = getPage(urltv)
    possible_links = []
    if (src_urltv == -1):
        return possible_links
    for line in src_urltv:
        for nameModule in tehcake_mod.__all__:
            if (nameModule in line):
                possible_links.append([urltv, \
                    "tehcake_mod." + nameModule])
    return possible_links
    
