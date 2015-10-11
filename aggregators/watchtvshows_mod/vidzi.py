""" get novamov links from free-tv-..."""

from .. import getPage

def getFlv(link, verbose):
    """ return the url of the file from novamov"""
    
    ##episode page
#    src = getPage(link)
    novamovlink = link 
#    for i in src:
#        if ("src='http://www.novamov.com/embed" in i.lower().replace('"',"'")):
#            novamovlink = i.replace('"',"'").split("'")[13]
#
#    if not novamovlink:
#        if verbose:			
#            print '\033[1;31mnovamov link not found\033[0m (url: ' + link + ')'
#        return None, None 
#
#    if verbose :    
#        print '\ndownloading ' + novamovlink

    ##novamov page
    src = getPage(novamovlink)
    urlfile = ''
    for i in src:
        if (i.strip().startswith('file: ')):
            urlfile = i.split('"')[1]
    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m (url: ' + novamovlink + ')'
        return None, None
    print "url vidzi: " + urlfile
    finalurl = urlfile
    return (finalurl, None)

