__all__ = ["freetvvideoonline", "sidereel", "viptvbase", "tehcake", "watchserieseu"]
from urllib2 import Request, urlopen

def getPage(link, splitting = '\n', referer = None, useragent = "Firefox"):
    """ return the lines list of the page link """
    request = Request(link)
    if referer:
        request.add_header('Referer', referer)
    if useragent:
        request.add_header('User-agent', useragent)
    try:
        response = urlopen(request)
    except IOError:
        #print '\033[1;31mlink not found\033[0m (url:' + link + ')'
        return -1
    else:
        the_page = response.read()
        return the_page.split(splitting)



def waiting(sec, verbose):
    """ wait sec seconds """
    import time
    if verbose:
        print "waiting " + str(sec) + " sec..."
    for i in range (sec + 1):
        time.sleep(1)
        if verbose:
            print (sec - i)

