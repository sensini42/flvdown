"""module for free-tv-video-online.me"""
import viptvbase_mod
from . import getPage
import re

def getTvShowUrl(tvshow):
    """get url for tvshow"""
    urlsearch = 'http://viptvbase.com/shows'
    src_urlsearch = getPage(urlsearch)
    urltv = ""
    for line in src_urlsearch:
        if tvshow in line.lower():
            urltv = line.split('"')[1]
            break
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    urltv = getTvShowUrl(tvshow)
    possible_links = []
    if urltv != "":
        # found tvshow
        if season > 1:
            urltv = urltv + str(int(season)-1)
        urlepi = "/".join(urltv.split("/")[:-1]) + "/" + str(season) + \
           "/" + str(episode)
        src_urltv = getPage(urltv)
        if src_urltv != -1:
            for line in src_urltv:
                if urlepi in line:
                    if '.html' in line:
                        urlepi = urlepi + '.html'
                    else:
                        urlepi = urlepi + '.htm'
                    break
            src_urlepi = getPage(urlepi)
            for line in src_urlepi:
                for nameModule in viptvbase_mod.__all__:
                    if nameModule in line:
                        regex = re.compile("'(http[^']*"+nameModule+"[^']*)'")
                        resul = regex.search(line)
                        possible_links.append([resul.group(1), \
                            "viptvbase_mod." + nameModule])
    return possible_links
    

