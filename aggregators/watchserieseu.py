"""module for free-tv-video-online.me"""
import freetvvideoonline_mod
from . import getPage

def getTvShowUrl(tvshow, season, episode):
    """get url for tvshow"""
    urlseason = 'http://watchseries.eu/season-'+ season + '/' + tvshow
    src_urlseason = getPage(urlsearch)
    urltv = ""
    for line in src_urlseason:
        if (tvshow + '_s' + season + '_e' + episode) in line:
            urltv = line.split('"')[1]
            break
    if urltv != "":
        idepisode = urltv.split('-')[-1].split('.')[0]
        urltv = 'http://watchseries.eu/getlinks.php?q=' + idepisode + '&domain=all'
    return urltv

def getLinks(tvshow, season, episode):
    """return all video links"""
    urltv = getTvShowUrl(tvshow, season, episode)
    possible_links = []
    if urltv != "":
        src_urltv = getPage(urltv)
        if src_urltv != -1:
            for line in src_urltv:
                #splitter correctement pour
                #trouver ..open/cale/5443107/idepisod/160752.html
                #
                #dans les modules, 
                #trouver http://watchseries.eu/gateway.php?link=YmZha2VkZWJlZWdlbGpoamRnZGRjZWdjYWFrZWZlY2FhY1NkZmRlamZpY2lpgoKCgoSEaGNiY2RlaGlqa2plY2dsY2hjZWlhaGxqa2tjYV9pZWZmZWphYmNmZ2hpaGlqZWdmZGNogoKChISEZmphZ2ZoY2lkY2RhYWlmZ2RkYV9pZWZnZWSCgoKEhIRkgoKCgoSEZGRiZF9pZWZnZWdiamZmbGxsZmRmYmtjaWVqYmJiYWtlZmVjaoKEhISEgmJkZGdsaGlhZ2c=" class="myButton">Click Here to Play</a>
                #
                #dans le module filebox 
                #trouver <div class="getpremium_heading4"><a href="http://alphacentauri.filebox.com:182/d/nrhotuiit3tew4mh3ot55lvzotbjw2e5odrxie5b4p5y5r5u3op4seos/TV-Release.Net_Psych.S06E16.HDTV.x264-COMPULSiON.mp4">Download File</a></div>



                for nameModule in watchserieseu_mod.__all__:
                    if nameModule in line:
                        href = line.split('href=')
                        link = href[1].split('"')[1]
                        print link
                        possible_links.append([link, \
                            "freetvvideoonline_mod." + nameModule])
    return possible_links
    
