""" get videoweed links from free-tv-..."""

from .. import getPage

def getFlv(link, verbose):
    """ return the url of the file from videoweed"""
    
    ##episode page
    src = getPage(link)
    videoweedlink = ''
    for i in src:
        if ("src='http://embed.videoweed.com/embed" in i):
            videoweedlink = i.split("'")[3]

    if not videoweedlink:
        if verbose:			
            print '\033[1;31mvideoweed link not found\033[0m (url: ' + link + ')'
        return -1

    if verbose :    
        print '\ndownloading ' + videoweedlink

    ##videoweed page
    src = getPage(videoweedlink)
    urlfile = ''
    for i in src:
        if ('flashvars.file' in i):
            urlfile = i.split('"')[1]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m (url: ' + videoweedlink + ')'
        return -1
    else:
        print urlfile
        return (urlfile, None)

