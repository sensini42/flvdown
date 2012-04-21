""" get loombo links from free-tv-..."""
from .. import getPage
import base64
def getFlv(link, verbose):
    """ return the url of the file from loombo"""
    ##episode page
    src = getPage(link)
    fileboxlink = ''
    for i in src:
        if ("watchseries.eu/gateway.php?link=" in i):
            fileboxlink = i.split('"')[1]
            # = fileboxlink.split('=')[1] + "=="
            base1 = i.split('"')[1][39:]
            base2 = base64.urlsafe_b64decode(base1)
            print i
            print fileboxlink
            print base1
            print base2
            break

    if (not fileboxlink) or (fileboxlink == 'no'):
        if verbose:			
            print '\033[1;31mfilebox link not found\033[0m \
                   (url filebox:' + link + ')'
        return None, None

    if verbose :    
        print '\ndownloading ' + fileboxlink

    ##filebox page
    src = getPage(fileboxlink)
    urlfile = ''
    for i in src:
        if ('getpremium_heading4' in i) and  (('Download File') in i):
            urlfile = i.split('"')[3]
            break

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url filebox:' + fileboxlink + ')'
        return None, None
    else:
        return (urlfile, None)

#http://www.bpaste.net/raw/20983/
