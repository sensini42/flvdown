""" get watch-streaming-tv-... links from sidereel"""
from .. import getPage
from loombo import getFlv as getLoombo
from vidxden import getFlv as getVidx
def getFlv(link, verbose):
    """ return the url of the file from w-s-t-e.c"""
    loombolink, _ = getLoombo(link, verbose)
    if loombolink:
        return loombolink, None
    vidxlink, _ = getVidx(link, verbose)
    if vidxlink:
        return vidxlink, None
    return None, None
