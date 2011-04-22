""" get watch-streaming-tv-... links from sidereel"""
from .. import getPage
from loombo import getFlv as getLoombo
from vidxden import getFlv as getVidx
def getFlv(link, verbose):
    """ return the url of the file from w-s-t-e.c"""
    loombolink = getLoombo(link, verbose)
    if (loombolink != -1):
        return loombolink
    vidxlink = getVidx(link, verbose)
    if (vidxlink != -1):
        return vidxlink
    return -1
