"""module for free-tv-video-online.me"""
import projectfreetv_mod
from urllib2 import unquote
from . import getPage

def getTvShowUrl(tvshow, season, episode):
    """get url for tvshow"""
    urlbase = 'http://projectfreetv.so/'
    urltv = urlbase + tvshow.replace('_','-') + '-season-' + season + '-episode-'+episode+'/'
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    urltv = getTvShowUrl(tvshow, season,episode)
    urlbase = 'http://projectfreetv.so'
    src_urltv = (''.join(getPage(urltv))).split('</a>')
    possible_links = []
    if (src_urltv == -1):
        return possible_links
    for line in src_urltv:
        for nameModule in projectfreetv_mod.__all__:
            if ((nameModule in line) and (('aff_id') in line)):
                link = line.split('"')[1]
                possible_links.append([link, \
                    "projectfreetv_mod." + nameModule])
    #print possible_links
    return possible_links
    
