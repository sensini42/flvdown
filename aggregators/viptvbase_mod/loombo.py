""" get loombo links from viptv..."""
from .. import getPage
def getFlv(link, verbose):
    """ return the url of the file from loombo"""
    src = getPage(link)
    urlfile = ''
    for i in src:
        if "'file'" in i:
            urlfile = i.split("'")[3]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url :' + link + ')'
        return -1
    else:
        return (urlfile, None)
