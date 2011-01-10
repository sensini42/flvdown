#!/usr/bin/python
""" download flv"""

import sys
import os
tvshow = sys.argv[1]
season = str(int(sys.argv[2]))
episode = str(int(sys.argv[3]))
interact = 0
zfirst = 0
verbose = 0

if len(episode) == 1:
    filename = tvshow + season + "0" + episode 
else:
    filename = tvshow + season + episode 

ret = os.system("ls " + filename + "* 2> /dev/null")

if not ret :
    print 'there is a file name ' + filename + '...\n'
    choice = raw_input('continue ? (y/n)\n')
    if choice not in 'yYoO':
        exit(0)

if (len(sys.argv)>4):
    if ("i" in sys.argv[4]):
        interact = 1
        verbose = 2
    if ("z" in sys.argv[4]):
        #zshare first
        zfirst = 1
    if ("v" in sys.argv[4]):
        verbose = 1
    
if verbose:
    print tvshow, "season", season, "episode", episode


urlbase = 'http://www.free-tv-video-online.me/internet/'
urltv = urlbase + tvshow + '/season_' + season + '.html'

from urllib2 import Request, urlopen

##tvshow page
response = urlopen(urltv)
the_page = response.read().lower()

src = the_page.split('\n')

liste = []
for i in src:
    if ('loombo' in i) and ( ('episode '+episode + '<') in i):
        liste += [i.split('"')[1]]

if (liste != []) and (zfirst != 1):
    if verbose:
        print 'possible links'
        for i, j in enumerate(liste):
            print i, '-', j

    choice = 0
    if interact:
        choice = int(raw_input('enter your choice\n'))
    link = liste[choice]

    if verbose :    
        print '\ndownloading ' + link

    ##episode page
    response = urlopen(link)
    the_page = response.read().lower()

    src = the_page.split('\n')
    loombolink = ''
    for i in src:
        if ("src='http://loombo.com/embed" in i):
            loombolink = i.split("'")[5]

    if not loombolink:
        print '\033[1;31mloombo link not found\033[0m (url loombo:' + link + ')'
        exit(1)

    if verbose :    
        print '\ndownloading ' + loombolink


    ##loombo page
    response = urlopen(loombolink)
    the_page = response.read().lower()

    src = the_page.split('\n')
    urlfile = ''
    for i in src:
        if ('file' in i):
            urlfile = i.split("'")[3][5:]


    if urlfile == '':
        print '\033[1;31mfile not found\033[0m (url loombo:' + loombolink + ')'
        exit(1)
else:
    liste = []
    if verbose and not zfirst:
        print 'no loombo link, trying zshare'
    #zshare
    for i in src:
        if ('zshare' in i) and ( ('episode '+episode + '<') in i):
            liste += [i.split('"')[1]]

    if (liste != []):
        if verbose:
            print 'possible links'
            for i, j in enumerate(liste):
                print i, '-', j

        choice = 0
        if interact:
            choice = int(raw_input('enter your choice\n'))
        link = liste[choice]

        if verbose :    
            print '\ndownloading ' + link
        
        
        ##episode page
        response = urlopen(link)
        the_page = response.read()

        src = the_page.split('\n')
        zsharelink = ''
        for i in src:
            if ("src='http://www.zshare.net/videoplayer" in i):
                zsharelink = i.split("'")[3]

        if not zsharelink:
            print '\033[1;31mzshare link not found\033[0m (url zshare:' + zsharelink + ')'
            exit(1)

        if verbose :    
            print '\ndownloading ' + zsharelink



        ##zshare page
        response = urlopen(zsharelink)
        the_page = response.read()

        src = the_page.split('\n')
        zshareform = ''
        for i in src:
            if ('.net/download' in i):
                zshareform = i.split('"')[1]

        if zshareform == '':
            print '\033[1;31mform not found\033[0m (url zshare:' + zsharelink + ')'


        if verbose :    
            print '\ndownloading ' + zshareform

        import random
            
        ##zshare forme
        ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        tmpfile = '/tmp/' + ''.join([random.choice(ascii) for x in range(10)])
 
        os.system("wget " + zshareform + " --post-data='download=1&referer2=\"" + zsharelink + "\"'  --save-cookies=" + tmpfile + ".cook -O " + tmpfile + ".html")
        the_page = open(tmpfile + ".html","r").read()
        src = the_page.split('\n')
        urlfile = ''
        for i in src:
            if ('link_enc' in i):
                urlfile = ''.join(eval('[' + i.split('(')[1].split(')')[0] + ']'))
        import time
        print "waiting 50 sec..."
        for i in range (51):
            time.sleep(1)
            if verbose:
                print (50 - i)
            
        if urlfile == '':
            print '\033[1;31mfile not found\033[0m (url loombo:' + zsharelink + ')'
            exit(1)
            
        urlfile = " --load-cookies=" + tmpfile + ".cook --save-cookies=" + tmpfile + ".cook --keep-session-cookies " + urlfile
    else:
        print '\033[1;31mno loombo/zshare link found\033[0m (url tv show:' + urltv + ')'
        exit(1)


print '\ndownloading file', urlfile
ext = "." + urlfile.split('.')[-1]

if len(episode) == 1:
    filename = tvshow + season + "0" + episode + ext
else:
    filename = tvshow + season + episode + ext

os.system("wget " + urlfile + " -O " + filename)
