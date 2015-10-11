""" get gorillavid links from free-tv-..."""
from .. import getPage
def getFlv(link, verbose):
    """ return the url of the file from gorillavid"""
    ##episode page
    #src = getPage(link)
    gorillavidlink = link
    #for i in src:
    #    if ("src='http://gorillavid.in/embed" in i.lower().replace('"',"'")):
    #        gorillavidlink = i.replace('"',"'").split("'")[1]
#
#    if (not gorillavidlink) or (gorillavidlink == 'no'):
#        if verbose:			
#            print '\033[1;31mgorillavid link not found\033[0m \
#                   (url gorillavid:' + link + ')'
#        return None, None

#    if verbose :    
#        print '\ndownloading ' + gorillavidlink

    ##gorillavid page
    src = getPage(gorillavidlink)
    urlfile = ''
    for i in src:
        if ('options.playlist' in i):
            urlfile = i.split('"')[3]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url gorillavid:' + gorillavidlink + ')'
        return None, None
    else:
        return (urlfile, None)
