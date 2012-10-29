""" get novamov links from free-tv-..."""

from .. import getPage

def getFlv(link, verbose):
    """ return the url of the file from novamov"""
    
    ##episode page
    ## src = getPage(link)
    ## novamovlink = ''
    ## for i in src:
    ##     if ("src='http://www.novamov.com/embed" in i):
    ##         novamovlink = i.split("'")[13]

    ## if not novamovlink:
    ##     if verbose:			
    ##         print '\033[1;31mnovamov link not found\033[0m (url: ' + link + ')'
    ##     return None, None 

    ## if verbose :    
    ##     print '\ndownloading ' + novamovlink

    ##novamov page
    src = getPage(link)
    urlfile = ''
    for i in src:
        if ('flashvars.file=' in i):
            urlfile = i.split('"')[1]
        if ('flashvars.filekey=' in i):
            urlfilekey = i.split('"')[1]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m (url: ' + link + ')'
        return None, None
    urlapi = 'http://www.novamov.com/api/player.api.php?pass=undefined&file=' \
             + urlfile + '&user=undefined&codes=1&key=' + urlfilekey
    src = getPage(urlapi)
    finalurl = src[0].split('&')[0].split('=')[1]
    return (finalurl, None)

