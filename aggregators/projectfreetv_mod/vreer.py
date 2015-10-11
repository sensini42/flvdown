"""get vreer links from free-tv-..."""
from .. import getPage
def getFlv(link, verbose):
    """ return the url of the file from vreer"""
    ##episode page
    src = getPage(link)
    vreerlink = ''
    for i in src:
        if ("src='http://vreer.com/embed" in i.lower().replace('"',"'")):
            vreerlink = i.replace('"',"'").split("'")[1]

    if (not vreerlink) or (vreerlink == 'no'):
#        if verbose:			
        print '\033[1;31mvreer link not found\033[0m \
                   (url vreer:' + link + ')'
        return None, None

#    if verbose :    
    print '\ndownloading ' + vreerlink

    ##vreer page
    src = getPage(vreerlink)
    urlfile = ''
    for i in src:
        if ('file:' in i):
            urlfile = i.split('"')[1]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url vreer:' + vreerlink + ')'
        return None, None
    else:
        return (urlfile, None)
