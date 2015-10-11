""" get streamin links from free-tv-..."""
from .. import getPage
def getFlv(link, verbose):
    """ return the url of the file from streamin"""
    ##episode page
    print link
    src = getPage(link)
    link = ''
    for i in src:
        if (("embed" in i)and("streamin" in i)):
            link=i.split('"')[1]
    if (not link) or (link == 'no'):
        if verbose:			
            print '\033[1;31mstreamin link not found\033[0m \
                   (url :' + link + ')'
        return None, None

    if verbose :    
        print '\ndownloading ' + link

    ##streamin page
    src = getPage(link)
    urlfile = ''
    for i in src:
        if ('modes:' in i):
            urlfile = i.split("'")[1]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url streamin:' + link + ')'
        return None, None
    else:
        return (urlfile, None)
