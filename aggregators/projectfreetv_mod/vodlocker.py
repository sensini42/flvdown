""" get vodlocker links from free-tv-..."""
from .. import getPage
def getFlv(link, verbose):
    """ return the url of the file from vodlocker"""
    ##episode page
    src = getPage(link)
    link = ''
    for i in src:
        if (("embed" in i)and("vodlocker" in i)):
            link=i.split('"')[1]
    if (not link) or (link == 'no'):
        if verbose:			
            print '\033[1;31mvodlocker link not found\033[0m \
                   (url :' + link + ')'
        return None, None

    if verbose :    
        print '\ndownloading ' + link
    print link
    ##vodlocker page
    src = getPage(link)
    urlfile = ''
    try:
        for i in src:
            if ('file:' in i):
                urlfile = i.split('"')[1]
                print urlfile
                break
    except:
        return None, None
    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url vodlocker:' + link + ')'
        return None, None
    else:
        return (urlfile, None)
