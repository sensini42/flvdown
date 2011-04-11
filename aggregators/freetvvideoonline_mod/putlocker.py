""" get putlocker links from free-tv-..."""

from .. import getPage
import random
import os
def getFlv(link, verbose):
    """ return the url of the file from putlocker"""
    
    ##episode page
    src = getPage(link)
    putlockerlink = ''
    for i in src:
        if ('src="http://www.putlocker.com/embed' in i):
            pllink = i.split("\"")[1]
            putlockerlink = "http://www.putlocker.com/get_file.php?embed_stream=" + i.split("\"")[1].split("/")[-1]

    if not putlockerlink:
        if verbose:			
            print '\033[1;31mputlocker link not found\033[0m (url: ' + link + ')'
        return -1

    if verbose :    
        print '\ndownloading ' + pllink

    ##putlockerlink page
    src = getPage(pllink)

    hashvalue = ''
    for i in src:
        if ('hash' in i):
            hashvalue = i.split('"')[3]
    print "using",hashvalue
    ##posting hash value
    ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    tmpfile = '/tmp/' + ''.join([random.choice(ascii) for _ in range(10)])

    os.system("wget " + pllink + " --post-data='hash=\"" +\
              hashvalue + "\"'  --save-cookies=" + tmpfile + ".cook -O " +\
              tmpfile + ".html -nv")
    
    the_page = open(tmpfile + ".html","r")
    src = the_page.read().split('\n')
    the_page.close()

    
    os.system("wget " + putlockerlink + " --post-data='hash=\"" +\
              hashvalue + "\"'  --save-cookies=" + tmpfile + ".cook -O " +\
              tmpfile + ".html -nv")
    
    the_page = open(tmpfile + ".html","r")
    src = the_page.read().split('\n')
    the_page.close()

    ##putlockerlink page
    urlfile = 'a'
    for i in src:
        print i
        if ('media:content' in i):
            urlfile = i.split('"')[5]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m (url: ' + putlockerlink + ')'
        return -1
    else:
        return (urlfile, None)
	
