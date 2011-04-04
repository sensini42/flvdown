from .. import getPage
def getFlv(link, verbose, interact):
    """ return the url of the file from loombo"""
    ##episode page
    src = getPage(link)
    loombolink = ''
    for i in src:
        if ("src='http://loombo.com/embed" in i):
            loombolink = i.split("'")[5]

    if not loombolink:
        if verbose:			
            print '\033[1;31mloombo link not found\033[0m \
                   (url loombo:' + link + ')'
        return -1

    if verbose :    
        print '\ndownloading ' + loombolink

    ##loombo page
    src = getPage(loombolink)
    urlfile = ''
    for i in src:
        if ('file' in i):
            urlfile = i.split("'")[3][7:]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url loombo:' + loombolink + ')'
        return -1
    else:
        return (urlfile, None)
