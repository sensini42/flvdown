""" get vidbull links from free-tv-..."""
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
        if ("src='http://vidbull.com/embed" in i.lower().replace('"',"'")):
            print i
            divxlink = i.replace('"',"'").split("'")[1]

    if not divxlink:
        if verbose:      
            print '\033[1;31mvidbull link not found\033[0m (url:' +\
              link + ')'
        return None, None 
    
    if verbose :    
        print '\ndownloading ' + divxlink


    ##divxden page
    src = getPage(divxlink.replace(" ","%20"))
    
    packfunction = ''
    for i in src:
        if ('eval(function(p,a,c,k,e,d)' in i):
            print i
            packfunction = i.split('>')[1]

    if not packfunction:
        if verbose:
            print '\033[1;31mvidxden link not found\033[0m (url:' +\
              divxlink + ')'
        return None, None

    arguments = packfunction[115:-13].split(',')
    pjs = ','.join(arguments[:-3])[1:-1]
    ajs = int(arguments[-3])
    cjs = int(arguments[-2])
    kjs = arguments[-1][1:-1].split('|')
    pjs = pjs.translate(None, '\\')
    res = [i for i in trad(pjs, ajs, cjs, kjs).split(',') \
         if i.startswith("jwplayer")][0]
    urlfile = res.split('"')[3]
    print res, urlfile    
    return (urlfile, None)

