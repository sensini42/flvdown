"""module for free-tv-video-online.me"""
import watchtvshows_mod
from urllib2 import unquote
from . import getPage

def getTvShowUrl(tvshow, season,episode):
    """get url for tvshow"""
    urlbase = 'http://watchtvshows.info/watch-'
    urltv = urlbase + tvshow + '-season-' + season + '-episode-'+episode+'-online/'
    print urltv
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    tvshow=tvshow.replace('_','-')
    urltv = getTvShowUrl(tvshow, season,episode)
    urlbase = 'https://www.watchepisode.co/'
    src_urltv = (''.join(getPage(urltv))).split('</a>')
    possible_links = []
    if (src_urltv == -1):
        return possible_links
    epi=''
    #for line in src_urltv:
    #   if ('Open video' in line)):
    #       epi = line.split('href=')[1].split('"')[1]
    #       break
    #if not epi:
    #    return possible_links 
    #print "--"+epi
    #src_urltv = (''.join(getPage(epi))).split('<a ')
    for line in src_urltv:
        if ('Open video' in line):
            for nameModule in watchtvshows_mod.__all__:
                if nameModule in line:
                    link = line.split('href=')[1].split('"')[1]
                    possible_links.append([link, \
                    "watchtvshows_mod." + nameModule])
    print tvshow
    print possible_links
    return possible_links
    
