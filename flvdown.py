#!/usr/bin/python
""" download flv"""

def getpage(link):
    """ return the lines list of the page link """
    try:
        response = urlopen(link)
    except IOError, e:
        print '\033[1;31mlink not found\033[0m (url:' + link + ')'
        exit(1)
    else:
        the_page = response.read()
        return the_page.split('\n')

def getepisodelink(liste):
    """ return the link of the episode page"""
    if verbose:
        print 'possible links'
        for number, name in enumerate(liste):
            print number, '-', name

    choice_ep = 0
    if interact:
        choice_ep = int(raw_input('enter your choice\n'))
    link = liste[choice_ep]
    if verbose :    
        print '\ndownloading ' + link
    return link

def waiting(sec):
    """ wait sec seconds """
    import time
    print "waiting " + str(sec) + " sec..."
    for i in range (sec + 1):
        time.sleep(1)
        if verbose:
            print (sec - i)


def getloombo():
    """ return the url of the file from loombo"""
    link = getepisodelink(listeloombo)
    
    ##episode page
    src = getpage(link)
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
    src = getpage(loombolink)
    urlfile = ''
    for i in src:
        if ('file' in i):
            urlfile = i.split("'")[3][7:]

    if urlfile == '':
        print '\033[1;31mfile not found\033[0m (url loombo:' + loombolink + ')'
        exit(1)
    else:
        return urlfile


def getzshare():
    """ return the url of the file from zshare"""
    link = getepisodelink(listezshare)

    ##episode page
    src = getpage(link)
    zsharelink = ''
    for i in src:
        if ("src='http://www.zshare.net/videoplayer" in i):
            zsharelink = i.split("'")[3]

    if not zsharelink:
        print '\033[1;31mzshare link not found\033[0m (url zshare:' +\
              link + ')'
        exit(1)
        
    if verbose :    
        print '\ndownloading ' + zsharelink


    ##zshare page
    src = getpage(zsharelink.replace(" ","%20"))
    zshareform = ''
    for i in src:
        if ('.net/download' in i):
            zshareform = i.split('"')[1]

    if zshareform == '':
        ##zsharelink may be a good url...
        print '\033[1;31mform not found\033[0m (url zshare:' +\
              zsharelink + ')'
        exit(1)

    if verbose :    
        print '\ndownloading ' + zshareform

    ##zshare form
    ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    global tmpfile
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

    waiting(50)

    if urlfile == '':
        print '\033[1;31mfile not found\033[0m (urls zshare:' +\
              zshareform + ' and ' + zsharelink+ ')'
        exit(1)

    urlfile = " --load-cookies=" + tmpfile + ".cook --save-cookies=" +\
              tmpfile + ".cook --keep-session-cookies " + urlfile
    return urlfile


def getnovamov():
    """ return the url of the file from novamov"""
    link = getepisodelink(listenovamov)
    
    ##episode page
    src = getpage(link)
    novamovlink = ''
    for i in src:
        if ("src='http://www.novamov.com/embed" in i):
            novamovlink = i.split("'")[13]

    if not novamovlink:
        print '\033[1;31mnovamov link not found\033[0m (url: ' + link + ')'
        exit(1)

    if verbose :    
        print '\ndownloading ' + novamovlink

    ##novamov page
    src = getpage(novamovlink)
    urlfile = ''
    for i in src:
        if ('flashvars.file' in i):
            urlfile = i.split('"')[1]

    if urlfile == '':
        print '\033[1;31mfile not found\033[0m (url: ' + novamovlink + ')'
        exit(1)
    else:
        return urlfile




##Some var
from urllib2 import urlopen
from urllib import urlencode
import sys
import os
import random

global tmpfile
tmpfile = ''
tvshow = sys.argv[1]
season = str(int(sys.argv[2]))
episode = str(int(sys.argv[3]))
interact = 0
lonly = 0
nonly = 0
zonly = 0
verbose = 0

##add a trailing 0 if num episode < 10
if len(episode) == 1:
    filename = tvshow + season + "0" + episode 
else:
    filename = tvshow + season + episode 

##test if a file with similar name exist
ret = os.system("ls " + filename + "* 2> /dev/null")
if not ret :
    print 'there is a file name ' + filename + '...\n'
    choice = raw_input('continue ? (y/n)\n')
    if choice not in 'yYoO':
        exit(0)

##process arguments
if (len(sys.argv)>4):
    if ("i" in ''.join(sys.argv[4:])):
        interact = 1
        verbose = 2
    if ("l" in ''.join(sys.argv[4:])):
        #from loombo only
        lonly = 1
    if ("n" in ''.join(sys.argv[4:])):
        #from novamov only
        nonly = 1
    if ("z" in ''.join(sys.argv[4:])):
        #from zshare only
        zonly = 1
    if ("v" in ''.join(sys.argv[4:])):
        verbose = 1

##tvshow page
urlbase = 'http://www.free-tv-video-online.me/internet/'
urltv = urlbase + tvshow + '/season_' + season + '.html'
src_urltv = getpage(urltv)

##lists of possible links
listeloombo = []
listezshare = []
listenovamov = []
for line in src_urltv:
    if ('loombo' in line) and ( ('Episode '+episode + '<') in line):
        listeloombo += [line.split('"')[1]]
    elif ('zshare' in line) and ( ('Episode '+episode + '<') in line):
        listezshare += [line.split('"')[1]]
    elif ('novamov' in line) and ( ('Episode '+episode + '<') in line):
        listenovamov += [line.split('"')[1]]


##get the url of the file
if (listezshare != []) and (not lonly) and (not nonly):
    final_url = getzshare()
elif (listeloombo != []) and (not zonly) and (not nonly):
    final_url = getloombo()
elif (listenovamov != []) and (not lonly) and (not zonly):
    final_url = getnovamov()
else:
    print '\033[1;31mno loombo/zshare/novamov link found\033[0m \
(url tv show:' + urltv + ')'
    exit(1)


if (not os.path.isdir(tvshow)):
    os.mkdir(tvshow)
    
print '\ndownloading file', final_url
ext = "." + final_url.split('.')[-1]

os.system("wget -c " + final_url + " -O " + tvshow + "/" + filename + ext)

if (len(tmpfile)>0):
    os.remove(tmpfile + ".html")
    os.remove(tmpfile + ".cook")
