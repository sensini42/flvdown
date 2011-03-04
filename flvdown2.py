#!/usr/bin/python
""" download flv"""

def getpage(link):
    """ return the lines list of the page link """
    try:
        response = urlopen(link)
    except IOError:
        print '\033[1;31mlink not found\033[0m (url:' + link + ')'
        return ""
    else:
        the_page = response.read()
        return the_page.split('\n')

def getepisodelink(liste, verbose, interact):
    """ return the link of the episode page"""
    if verbose:
        print 'possible links'
        for number, (name, znl) in enumerate(liste):
            print number, '-', znl, '-', name

    choice_ep = 0
    if interact:
        choice_ep = int(raw_input('enter your choice\n'))
    (link, znl) = liste[choice_ep]
    if verbose :    
        print '\ndownloading ', link, znl
    return (link, znl)

def waiting(sec, verbose):
    """ wait sec seconds """
    import time
    print "waiting " + str(sec) + " sec..."
    for i in range (sec + 1):
        time.sleep(1)
        if verbose:
            print (sec - i)


def getloombo(link, verbose):
    """ return the url of the file from loombo"""
    ##episode page
    src = getpage(link)
    loombolink = ''
    for i in src:
        if ("src='http://loombo.com/embed" in i):
            loombolink = i.split("'")[5]

    if not loombolink:
        if verbose:			
            print '\033[1;31mloombo link not found\033[0m \
                   (url loombo:' + link + ')'
        return -1

    if verbose :    
        print '\ndownloading ' + loombolink

    ##loombo page
    src = getpage(loombolink)
    urlfile = ''
    for i in src:
        if ('file' in i):
            urlfile = i.split("'")[3][7:]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m \
            (url loombo:' + loombolink + ')'
        return -1
    else:
        return urlfile


def getzshare(link, verbose):
    """ return the url of the file from zshare"""
    ##episode page
    src = getpage(link)
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
    src = getpage(zsharelink.replace(" ","%20"))
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

    waiting(50, verbose)

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m (urls zshare:' +\
              zshareform + ' and ' + zsharelink+ ')'
        return -1

    urlfile = " --load-cookies=" + tmpfile + ".cook --save-cookies=" +\
              tmpfile + ".cook --keep-session-cookies " + urlfile
    return urlfile


def getnovamov(link, verbose):
    """ return the url of the file from novamov"""
    
    ##episode page
    src = getpage(link)
    novamovlink = ''
    for i in src:
        if ("src='http://www.novamov.com/embed" in i):
            novamovlink = i.split("'")[13]

    if not novamovlink:
        if verbose:			
            print '\033[1;31mnovamov link not found\033[0m (url: ' + link + ')'
        return -1

    if verbose :    
        print '\ndownloading ' + novamovlink

    ##novamov page
    src = getpage(novamovlink)
    urlfile = ''
    for i in src:
        if ('flashvars.file' in i):
            urlfile = i.split('"')[1]

    if urlfile == '':
        if verbose:			
            print '\033[1;31mfile not found\033[0m (url: ' + novamovlink + ')'
        return -1
    else:
        return urlfile


def cmpPrio(plx, ply):
    "compare function to sort possible links"
    priority = {'z':0, 'l':1, 'n':2}
    if priority[plx[1]] > priority[ply[1]]:
        return 1
    elif priority[plx[1]] == priority[ply[1]]:
        return 0
    else:
        return -1


from urllib2 import urlopen
import os
import random
global tmpfile
tmpfile = ''
def flvdown(tvshow, season, episode, options):
    "main fctn"
    ##Some var
    global tmpfile
    tmpfile = ''
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
    if (options):
        if ("i" in options):
            interact = 1
            verbose = 2
        if ("l" in options):
            #from loombo only
            lonly = 1
        if ("n" in options):
            #from novamov only
            nonly = 1
        if ("z" in options):
            #from zshare only
            zonly = 1
        if ("v" in options):
            verbose = 1

    ##tvshow page
    urlbase = 'http://www.free-tv-video-online.me/internet/'
    urltv = urlbase + tvshow + '/season_' + season + '.html'
    src_urltv = getpage(urltv)

    ##lists of possible links
    possible_links = []
    for line in src_urltv:
        if (('loombo' in line) and
            (('Episode '+episode + '<') in line) and
            (not zonly) and
            (not nonly)):
            possible_links.append([line.split('"')[1],'l'])
        elif (('zshare' in line) and
              (('Episode '+episode + '<') in line) and
              (not lonly) and (not nonly)):
            possible_links.append([line.split('"')[1],'z'])
        elif (('novamov' in line) and
              (('Episode '+episode + '<') in line) and
              (not lonly) and (not zonly)):
            possible_links.append([line.split('"')[1],'n'])

    if possible_links == []:
        print '\033[1;31mno loombo/zshare/novamov link found\033[0m \
    (url tv show:' + urltv + ')'
        exit(1)


    possible_links.sort(cmpPrio)


    url_found = False
    while not url_found :
        (link, znl) = getepisodelink(possible_links, verbose, interact)
        if znl == 'z':
            final_url = getzshare(link, verbose)
        elif znl == 'l':
            final_url = getloombo(link, verbose)
        else:
            final_url = getnovamov(link, verbose)
        if final_url != -1:
            url_found = True
        else:
            possible_links.remove([link, znl])
            if possible_links == []:
                print '\033[1;31mno more loombo/zshare/novamov link\033[0m \
                    (url tv show:' + urltv + ')'
                exit(1)

    print '\ndownloading file', final_url

    if (not os.path.isdir(tvshow)):
        os.mkdir(tvshow)

    ext = "." + final_url.split('.')[-1]

    os.system("wget -c " + final_url + " -O " + tvshow + "/" + filename + ext)

    if (len(tmpfile)>0):
        os.remove(tmpfile + ".html")
        os.remove(tmpfile + ".cook")

