#!/usr/bin/python
""" download subtitles"""

from urllib2 import Request, urlopen
from zipfile import ZipFile
import sys
import re
import tempfile
from episodetv import episodeTV

def getPage(link, splitting = '\n'):
    """ return the lines list of the page link """
    try:
        response = urlopen(link)
    except IOError:
        print '\033[1;31mlink not found\033[0m (url:' + link + ')'
        return -1
    else:
        the_page = response.read()
        return the_page.split(splitting)




def downSubVid(videoname, options=""):
    """ down subtitle """

    interact = 0
    verbose = 0
    ##process arguments
    if (options):
        if ("i" in options):
            interact = 1
            verbose = 2
        if ("v" in options):
            verbose = 1

    query = videoname.split('/')[-1].split('.')[0].split('_')
    tvshow = '_'.join(query[:-1])
    season = query[-1][:-2]
    episode = query[-1][-2:]

    epi = episodeTV(tvshow, season, episode)
    return downSub(epi, options)
    
def downSub(episode, options=""):
    """ down subtitle """
    interact = 0
    verbose = 0
    ##process arguments
    if (options):
        if ("i" in options):
            interact = 1
            verbose = 2
        if ("v" in options):
            verbose = 1

    tvshow = episode.tvshowSpace
    season = episode.strSeason
    numepi = episode.strEpisode
    subname = episode.getSrtName()
    if verbose:
        print tvshow, "season", season, "episode", numepi

    tvCap = episode.tvshowCapital

    ##search page
    urlbase = 'http://www.tvsubtitles.net/'
    urlsearch = urlbase + 'tvshows.html'
    lang = "en"

    src = getPage(urlsearch)

    alink = ""
    for i in src:
        if ("<b>" + tvCap + "</b>") in i:
            alink = i.split('"')[3]

    if not alink:
        print '\033[1;31m('+subname+" "+tvCap+') show not found\033[0m'
        return -1
        
    
    #alink : last season
    #ie tvshow-58-7.html
    nshow = alink.split('-')[1]
    reallink = "tvshow-" + nshow + "-" + season + ".html"
    urltv = urlbase + reallink
    if verbose :    
        print '\ndownloading from ' + urltv


    ##tvshow page
    src = getPage(urltv, '<tr')

    urlsub = ''
    for i in src:
        if (season + 'x' + numepi) in i:
            for j in i.split("<a"):
                if 'flags/' + lang + '.gif' in j:
                    urlsub = urlbase + j.split('"')[1]

    if not urlsub:
        print '\033[1;31m('+subname+') sub not found\033[0m \
                 (url tv show:'+urltv+')'
        return -1

    if verbose > 1:
        print "url subtitle:", urlsub

    if 'episode' in urlsub:
        urlepi = urlsub

        ##episode page
        src = getPage(urlepi, '<a href="/subtitle-')

        possible = []
        for i in src:
            if "green" in i:
                ratio = re.sub('<[^>]*>', '', ('<' + i)).split('\n')[1].strip()
                name = re.sub('<[^>]*>', '', ('<' + i)).split('\n')[2].strip()
                ndownload = re.sub('<[^>]*>', '', \
                     ('<' + i)).split('\n')[12].strip()
                url = "subtitle-" + i.split('"')[0]
                if ('720p' not in name):
                    possible += [(ratio, name, ndownload, url)]
    
        if verbose:
            print 'possible subtitles:'
            for (i, (ratio, name, times, _)) in enumerate(possible):
                print i, "-", name, "ratio:", ratio, "(downloaded", \
                      times, "times)"

        choice = 0
        if interact:
            choice = int(raw_input('enter your choice\n'))
        urlsub = urlbase + possible[choice][3]    
        if verbose:
            print '\ndownloading from', choice, '-', possible[choice][1]
 

    ##subtitle page
    src = getPage(urlsub, '\n')

    link = urlbase + [ i.split('"')[1] for i in src if 'download-' in i][0]

    if verbose > 1:
        print link


    ##save zipfile
    file_ = tempfile.NamedTemporaryFile(suffix='.zip')
    filename = file_.name

    if verbose:
        print "saving in", filename
    
    zipfilecontent = urlopen(link)
    output = open(filename, 'wb')
    output.write(zipfilecontent.read())
    output.close()

    ##extract zipfile

    zfile = ZipFile(filename, "r")

    for name in zfile.namelist():
        if 'srt' in name:
            if verbose:
                print "extraction of", name, "in", subname

            subfile = open(subname, 'wb')
            subfile.write(zfile.read(name))
            ##if windows encoding
            ##subfile.write(zfile.read(name).replace('\15',''))
            subfile.close()

    return 0


if __name__ == "__main__":
    _videoname = sys.argv[1]

    option = ""
    if (len(sys.argv)>2):
        option = sys.argv[2] 

    downSubVid(_videoname, option)  




