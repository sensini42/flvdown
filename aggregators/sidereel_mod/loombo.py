""" get loombo links from sidereel"""
from .. import getPage
def getFlv(loombolink, verbose):
    """ return the url of the file from loombo"""
    ##episode page
    ## src = getPage(link)
    ## loombolink = ''
    ## for i in src:
    ##     if ("src='http://loombo.com/embed" in i):
    ##         loombolink = i.split("'")[5]

    ## if (not loombolink) or (loombolink == 'no'):
    ##     if verbose:			
    ##         print '\033[1;31mloombo link not found\033[0m \
    ##                (url loombo:' + link + ')'
    ##     return None, None

    ## if verbose :    
    ##     print '\ndownloading ' + loombolink

    ##loombo page
    src = getPage(loombolink)
    urlfile = ''
    for i in src:
        if ('file' in i) and not (('No such file') in i):
            urlfile = i.split("'")[3][7:]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url loombo:' + loombolink + ')'
        return None, None
    else:
        return (urlfile, None)
