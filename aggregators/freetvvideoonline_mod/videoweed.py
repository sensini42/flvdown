""" get videoweed links from free-tv-..."""
import re
from .. import getPage
from urllib import unquote
def wise(w,i,s,e):
    w1=w[:5]
    w2=w[5:]
    i1=i[:5]
    i2=i[5:]
    s1=s[:5]
    s2=s[5:]
    var3=''.join([''.join(y) for y in map(lambda *t: filter(lambda x: x is not None,t),w2,i2,s2)])
    var4=''.join([''.join(y) for y in zip(w1,i1,s1)]) #ne marche pas pour var3 car w,i,s peuvent etre de tailles differentes. Zip tronque -> lamba fonction
    var1=0
    var5=[]
    length3=len(var3)
    length4=len(var4)
    for var0 in range(0,length3,2):
        var8=-1
        if(ord(var4[var1])%2):
            var8=1
        var5.append(chr(int(var3[var0:var0+2],36)-var8))
        var1+=1
        if(var1>=length4):
            var1=0
    return ''.join(var5)


def getFlv(link, verbose):
    """ return the url of the file from videoweed"""
    
    ##episode page
    src = getPage(link)
    videoweedlink = ''
    for i in src:
        if ("src='http://embed.videoweed." in i.lower().replace('"',"'")):
            videoweedlink = i.replace('"',"'").split("'")[3]

    if not videoweedlink:
        if verbose:      
            print '\033[1;31mvideoweed link not found\033[0m (url: ' + \
                link + ')'
        return None, None

    if verbose :    
        print '\ndownloading ' + videoweedlink

    ##videoweed page
    src = getPage(videoweedlink)
    urlfile = ''
    wisePresent = False
    for i in src:
        if (';eval(function(w,i,s,e)' in i):
            p=i[:]
            wisePresent = True
            while (';eval(function(w,i,s,e)' in p):
                p=wise((''.join(p)).split("'")[-8],
                       (''.join(p)).split("'")[-6],
                       (''.join(p)).split("'")[-4],
                       (''.join(p)).split("'")[-2])
    urlfile = ''
    if (not wisePresent):
        p=''.join(src)
    for i in p.split(';'):
        if ('flashvars.domain=' in i):
            urldomain = i.split('"')[1]
        if ('flashvars.file=' in i):
            urlfile = i.split('"')[1]
        if re.search("var .*=\"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*-.*-\"", i):
            print i
            print i.split('"')
            urlfilekey = i.split('"')[1]

    if urlfile == '':
        if verbose:      
            print '\033[1;31mfile not found\033[0m (url: ' + videoweedlink + ')'
        return None, None

    urlapi = urldomain + '/api/player.api.php?pass=undefined&file=' \
             + urlfile + '&user=undefined&codes=1&key=' + urlfilekey
    print "urlapi: " + urlapi
    src = getPage(urlapi)
    finalurl = unquote(src[0].split('&')[0].split('=')[1])
    return (finalurl, None)


