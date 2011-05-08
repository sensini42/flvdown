""" get wisevid links from free-tv-..."""
from .. import getPage
import os
from tempfile import NamedTemporaryFile

### js functions from wisevid ###

END_OF_INPUT = -1
arrChrs = [
    'A','B','C','D','E','F','G','H',
    'I','J','K','L','M','N','O','P',
    'Q','R','S','T','U','V','W','X',
    'Y','Z','a','b','c','d','e','f',
    'g','h','i','j','k','l','m','n',
    'o','p','q','r','s','t','u','v',
    'w','x','y','z','0','1','2','3',
    '4','5','6','7','8','9','+','/'
]

def setgetFStr(str):
    global getFStr 
    global getFCount 
    getFStr = str
    getFCount = 0

def readgetF():    
    global getFCount 
    if not getFStr:
        return END_OF_INPUT
    if (getFCount >= len(getFStr)): 
        return END_OF_INPUT
    c = ord(getFStr[getFCount]) & 0xff
    getFCount = getFCount+1
    return c

def readReversegetF():   
    global getFCount 
    if not getFStr:
        return END_OF_INPUT
    while True:      
        if getFCount >= len(getFStr):
            return END_OF_INPUT
        nextCharacter = getFStr[getFCount]
        getFCount = getFCount+1
        return arrChrs.index(nextCharacter)
    return END_OF_INPUT

def ntos(n):
    n='%x' % n
    if len(n) == 1:
        n="0"+n
    n="%"+n
    import urllib
    return urllib.unquote(n)

def getF(str):
    setgetFStr(str)
    result = ""
    inBuffer = [0,0,0,0]
    done = False
    inBuffer[0] = readReversegetF()
    inBuffer[1] = readReversegetF()
    while not done and inBuffer[0] != END_OF_INPUT \
        and inBuffer[1] != END_OF_INPUT:
        inBuffer[2] = readReversegetF()
        inBuffer[3] = readReversegetF()
        result = result + ntos((((inBuffer[0] << 2) & 0xff)| inBuffer[1] >> 4))
        if (inBuffer[2] != END_OF_INPUT):
            result =  result + ntos((((inBuffer[1] << 4) & 0xff)| inBuffer[2] >> 2))
            if (inBuffer[3] != END_OF_INPUT):
                result = result +  ntos((((inBuffer[2] << 6)  & 0xff) | inBuffer[3]))
            else :
                done = True
        else :
            done = True
        inBuffer[0] = readReversegetF()
        inBuffer[1] = readReversegetF()
    return result

### end js functions ###

def getFlv(link, verbose):
    """ return the url of the file from wisevid """
    ### episod page
    src = getPage(link)
    wisevidlink = ''
    for i in src:
        if "wisevid.com/play" in i:
            wisevidlink = i.split("'")[1]

    if not wisevidlink:
        if verbose:
            print '\033[1;31mwisevid link not found\033[0m (url:' + link + ')'
            return None, None

    if verbose:
        print '\ndownloading ' + wisevidlink

    ##wisevid page
    htmltmp = NamedTemporaryFile(suffix='.html')
    htmltmpfile = htmltmp.name
    num = wisevidlink.split('=')[1]
    os.system('wget ' + wisevidlink + ' --post-data=\'a=1&v=' + num + '\'' + \
        ' -O ' + htmltmpfile + ' -nv')

    the_page = open(htmltmpfile, 'r')
    src = the_page.read().split('\n')
    the_page.close()
    file = ''
    for i in src:
        if 'file' in i:
            file = i.split("'")[5]

    if not file:
        if verbose:
            print '\033[1;31mwisevid link not found\033[0m (url:' + wisevidlink + ')'
            return None, None

    return (getF(file), None)        
