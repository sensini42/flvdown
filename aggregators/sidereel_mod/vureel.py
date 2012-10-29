""" get vureel links from sidereel"""
from .. import getPage
def getFlv(vureellink, verbose):
    """ return the url of the file from vureel"""
    ##episode page
    ## src = getPage(link)
    ## vureellink = ''
    ## for i in src:
    ##     if ("src='http://vureel.com/embed" in i):
    ##         vureellink = i.split("'")[5]

    ## if (not vureellink) or (vureellink == 'no'):
    ##     if verbose:			
    ##         print '\033[1;31mvureel link not found\033[0m \
    ##                (url vureel:' + link + ')'
    ##     return None, None

    ## if verbose :    
    ##     print '\ndownloading ' + vureellink

    ##vureel page
    src = getPage(vureellink)
    urlfile = ''
    for i in src:
        if ('file:' in i) and not (('No such file') in i):
            urlfile = i.split('"')[1]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url vureel:' + vureellink + ')'
        return None, None
    else:
        return (urlfile, None)
