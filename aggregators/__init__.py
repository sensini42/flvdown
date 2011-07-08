__all__ = ["freetvvideoonline", "sidereel", "viptvbase", "tehcake"]
from urllib2 import urlopen
def getPage(link, verbose=''):
    """ return the lines list of the page link """
    try:
        response = urlopen(link)
    except IOError:
        if verbose:
            print '\033[1;31mlink not found\033[0m (url:' + link + ')'
        return -1
    else:
        the_page = response.read()
        return the_page.split('\n')


def waiting(sec, verbose):
    """ wait sec seconds """
    import time
    if verbose:
        print "waiting " + str(sec) + " sec..."
    for i in range (sec + 1):
        time.sleep(1)
        if verbose:
            print (sec - i)

