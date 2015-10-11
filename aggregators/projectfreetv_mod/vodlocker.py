""" get vodlocker links from free-tv-..."""
from .. import getPage
import re

def trad(pjs, ajs, cjs, kjs):
    """js function from p,a,c,k,e,d """
    while(cjs > 0):
        cjs -= 1
        if(kjs[cjs]):
            cdtb = str(convDecToBase(cjs, ajs))
            if (not cdtb):
                cdtb = str(0)
            regexp = re.compile('\\b' + cdtb + '\\b')
            pjs = regexp.sub(kjs[cjs], pjs)
    return pjs

def convDecToBase(num, base, ddd=False):
    """ convert int in some base"""
    if not ddd:
        ddd = dict(zip(range(36), '0123456789abcdefghijklmnopqrstuvwxyz'))
    if num == 0:
        return ''
    num, rem = divmod(num, base)
    return convDecToBase(num, base, ddd) + ddd[rem]

def getFlv(link, verbose):
    """ return the url of the file from divxden"""
    ##episode page
    src = getPage(link)
    divxlink = ''
    for i in src:
        if ("src='http://vodlocker.com/embed" in i.lower().replace('"',"'")):
            print i
            divxlink = i.replace('"',"'").split("'")[1]

    if not divxlink:
        if verbose:      
            print '\033[1;31mvodlocker link not found\033[0m (url:' +\
              link + ')'
        return None, None 
    
    if verbose :    
        print '\ndownloading ' + divxlink


    ##divxden page
    src = getPage(divxlink.replace(" ","%20"))

    for i in src:
        if ('file' in i) and not (('No such file') in i):
            urlfile = i.split('"')[1]
            break

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url vodlocker:' + divxlink + ')'
        return None, None
    else:
        return (urlfile, None)
