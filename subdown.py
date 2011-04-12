#!/usr/bin/python
""" download subtitles"""

from urllib2 import Request, urlopen
from urllib import urlencode
from zipfile import ZipFile
import sys
import re
import tempfile
import string


def downSub(rep, tvshow, season, episode, options):

    interact = 0
    verbose = 0
    ##process arguments
    if (options):
        if ("i" in options):
            interact = 1
            verbose = 2
        if ("v" in options):
            verbose = 1

    if verbose:
        print tvshow, "season", season, "episode", episode

    subname = ''
    if rep != '':
        subname = rep + "/"
    subname = subname + tvshow.replace(' ', '_') + season + \
         episode + ".srt"

    """search page"""

    ##search page
    urlbase = 'http://www.tvsubtitles.net/'
    urlsearch = urlbase + 'search.php'
    lang = "en"

    values = {"q" : tvshow } 

    req = Request(urlsearch, urlencode(values))
    response = urlopen(req)
    the_page = response.read().lower()

    src = the_page.split('\n')

    for i in src:
        if tvshow in i:
            a = i.split('<div')
            possible = [ j.split('<')[1] for j in a if tvshow in j ]

    couple = [ (i.split('"')[1], i.split('>')[1]) for i in possible ]
 
    if verbose:
        print 'possible tvshows matching ' + tvshow + ':'
        for (i, (url, name)) in enumerate(couple):
            print i, '-', name

    choice = 0
    if interact:
        choice = int(raw_input('enter your choice\n'))
    #tvshow = couple[choice]
    urltv = urlbase +  couple[choice][0].replace('.','-' + season +'.')

    if verbose :    
        print '\ndownloading from ' + couple[choice][1]
        if verbose >1:
            print "url tv show:", urltv


    ##tvshow page
    req = Request(urltv, urlencode(values))
    response = urlopen(req)
    the_page = response.read().lower()

    src = the_page.split('<tr')

    urlsub = ''
    for i in src:
        if (season + 'x' + episode) in i:
            for j in i.split("<a"):
                if 'flags/' + lang + '.gif' in j:
                    urlsub = urlbase + j.split('"')[1]

    if not urlsub:
        print '\033[1;31m('+subname+') sub not found\033[0m (url tv show:'+urltv+')'
        return -1

    if verbose > 1:
        print "url subtitle:", urlsub

    if 'episode' in urlsub:
        urlepi = urlsub

        ##episode page
        req = Request(urlepi, urlencode(values))
        response = urlopen(req)
        the_page = response.read().lower()

        src = the_page.split('<a href="/subtitle-')

        possible = []
        for i in src:
            if "green" in i:
                ratio = re.sub('<[^>]*>', '', ('<' + i)).split('\n')[1].strip()
                name = re.sub('<[^>]*>', '', ('<' + i)).split('\n')[2].strip()
                ndownload = re.sub('<[^>]*>', '', ('<' + i)).split('\n')[12].strip()
                url = "subtitle-" + i.split('"')[0]
                if ('720p' not in name):
                    possible += [(ratio, name, ndownload, url)]
    
        if verbose:
            print 'possible subtitles:'
            for (i, (r, n, d, _)) in enumerate(possible):
                print i, "-", n, "ratio:", r, "(downloaded", d, "times)"

        choice = 0
        if interact:
            choice = int(raw_input('enter your choice\n'))
        urlsub = urlbase + possible[choice][3]    
        if verbose:
            print '\ndownloading from',choice,'-', possible[choice][1]
 

    ##subtitle page

    req = Request(urlsub, urlencode(values))
    response = urlopen(req)
    the_page = response.read().lower()

    src = the_page.split('\n')

    link = urlbase + [ i.split('"')[1] for i in src if 'download-' in i][0]

    if verbose > 1:
        print link


    ##save zipfile
    filename = tempfile.NamedTemporaryFile(suffix='.zip').name

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
    videoname = sys.argv[1]
    rep = string.join(videoname.split('/')[:-1],'/')
    query = videoname.split('/')[-1].split('.')[0]

    option = ""
    if (len(sys.argv)>2):
        option = sys.argv[2] 

    tvshow = re.search('[a-z _&]*', query).group(0).replace('_',' ')
    season = re.search('(?<=0)?[0-9]{1,2}(?=[0-9]{2})', query).group(0)
    episode = re.search('[0-9]{2}$', query).group(0)

    downSub(rep, tvshow, season, episode, option) 


