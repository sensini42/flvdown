""" get zshare links from free-tv-..."""
from .. import getPage
from .. import waiting
import random
import os
def getFlv(link, verbose):
    """ return the url of the file from zshare"""

    ##episode page
    src = getPage(link)
    zsharelink = ''
    for i in src:
        if ("src='http://www.zshare.net/videoplayer" in i):
            zsharelink = i.split("'")[3]

    if not zsharelink:
        if verbose:			
            print '\033[1;31mzshare link not found\033[0m (url zshare:' +\
              link + ')'
        return -1
        
    if verbose :    
        print '\ndownloading ' + zsharelink


    ##zshare page
    src = getPage(zsharelink.replace(" ","%20"))
    zshareform = ''
    for i in src:
        if ('.net/download' in i):
            zshareform = i.split('"')[1]

    if zshareform == '':
        ##zsharelink may be a good url...
        if verbose:			
            print '\033[1;31mform not found\033[0m (url zshare:' +\
              zsharelink + ')'
        return -1

    if verbose :    
        print '\ndownloading ' + zshareform

    ##zshare form
    ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    tmpfile = '/tmp/' + ''.join([random.choice(ascii) for _ in range(10)])

    os.system("wget " + zshareform + " --post-data='download=1&referer2=\"" +\
              zsharelink + "\"'  --save-cookies=" + tmpfile + ".cook -O " +\
              tmpfile + ".html -nv")
    
    the_page = open(tmpfile + ".html","r")
    src = the_page.read().split('\n')
    the_page.close()
    
    urlfile = ''
    for i in src:
        if ('link_enc' in i):
            urlfile = ''.join(eval('[' + i.split('(')[1].split(')')[0] + ']'))

    waiting(50, verbose)

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m (urls zshare:' +\
              zshareform + ' and ' + zsharelink+ ')'
        return -1

    urlfile = " --load-cookies=" + tmpfile + ".cook --save-cookies=" +\
              tmpfile + ".cook --keep-session-cookies " + urlfile
    return (urlfile, tmpfile)

