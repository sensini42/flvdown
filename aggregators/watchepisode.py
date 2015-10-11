"""module for free-tv-video-online.me"""
import watchepisode_mod
from urllib2 import unquote
from . import getPage

def getTvShowUrl(tvshow, season):
    """get url for tvshow"""
    urlbase = 'https://www.watchepisode.co/'
    urltv = urlbase + tvshow #+ '/season_' + season + '.html'
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    tvshow=tvshow.replace('_','-')
    urltv = getTvShowUrl(tvshow, season)
    urlbase = 'https://www.watchepisode.co/'
    src_urltv = (''.join(getPage(urltv))).split('</a>')
    possible_links = []
    if (src_urltv == -1):
        return possible_links
    epi=''
    for line in src_urltv:
       if ((('Season '+season) in line) and (('Episode '+episode + '<') in line)):
           epi = line.split('href=')[1].split('"')[1]
    if not epi:
        return possible_links 
    print "--"+epi
    src_urltv = (''.join(getPage(epi))).split('<a ')
    for line in src_urltv[1:]:
        for nameModule in watchepisode_mod.__all__:
            if ((nameModule in line) and (('season-'+season) in line) and (('episode-'+episode) in line)):
                href = line.split('data-actuallink=')
                link = href[1].split('"')[1]
                #link = urlbase + unquote(link.split('=')[1].split('&')[0])
#                print link
                possible_links.append([link, \
                    "watchepisode_mod." + nameModule])
    return possible_links
    
