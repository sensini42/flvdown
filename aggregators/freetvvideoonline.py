"""module for free-tv-video-online.me"""
import freetvvideoonline_mod
from . import getPage

def getTvShowUrl(tvshow, season):
    """get url for tvshow"""
    urlbase = 'http://www.free-tv-video-online.me/internet/'
    urltv = urlbase + tvshow + '/season_' + season + '.html'
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    urltv = getTvShowUrl(tvshow, season)
    src_urltv = (''.join(getPage(urltv))).split('</a>')
    possible_links = []
    if (src_urltv == -1):
        return possible_links
    for line in src_urltv:
        for nameModule in freetvvideoonline_mod.__all__:
            if ((nameModule in line) and (('Episode '+episode + '<') in line)):
                href = line.split('href=')
                link = href[1].split('"')[1]
                print link
                possible_links.append([link, \
                    "freetvvideoonline_mod." + nameModule])
    return possible_links
    
