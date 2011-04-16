#!/usr/bin/python
# -*- coding: utf-8 -*-
""" looks for links with submodules """
import os
import aggregators
import sys 


def getEpisodeLink(liste, verbose, interact):
    """ return the first link of the list or the user choice"""
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


def flvdown(tvshow, season, episode, options, list_site = None):
    """ search episode through modules """

    ##add a trailing 0 if num episode < 10
    if len(episode) == 1:
        filename = tvshow + '/' + tvshow + season + "0" + episode 
    else:
        filename = tvshow + '/' + tvshow + season + episode
        
    ##test if a file with similar name exist
    ret = os.system("ls " + filename + "* 2> /dev/null")
    if not ret :
        print 'there is a file name ' + filename + '...\n'
        choice = raw_input('continue ? (y/n)\n')
        if choice not in 'yYoO':
            return -1, None
    interact = 0
    verbose = 0
    ##process arguments
    if (options):
        if ("i" in options):
            interact = 1
            verbose = 2
        ## if ("l" in options):
        ##     #from loombo only
        ##     lonly = 1
        ## if ("n" in options):
        ##     #from novamov only
        ##     nonly = 1
        ## if ("z" in options):
        ##     #from zshare only
        ##     zonly = 1
        if ("v" in options):
            verbose = 1
    possible_links = []
    for i in aggregators.__all__:
        #        if verbose:
        print "checking", i
        __import__("aggregators." + i)
        possible_links += sys.modules["aggregators."+i].getLinks(tvshow, \
            season, episode)
    #    if verbose:
    print "done"
    if possible_links == []:
        print '\033[1;31mno link\033[0m found'
        return -1, None
    
    ##Sort possible_links
    if list_site != None :
        prio = dict(zip(['_mod.'.join(i.split(' : ')) \
                     for i in list_site], range(len(list_site))))
   
        possible_links = sorted(possible_links, key=lambda i: prio[i[1]])

    url_found = False
    while not url_found:
        (link, znl) = getEpisodeLink(possible_links, verbose, interact)
        __import__("aggregators." + znl)
        final = sys.modules["aggregators." + znl].getFlv(link, verbose)
        if final != -1:
            url_found = True
        else:
            possible_links.remove([link, znl])
            if possible_links == []:
                print '\033[1;31mno link\033[0m found'
                return -1, None
    final_url = final[0]

    ext = "." + final_url.split('.')[-1]

    return (final_url, filename + ext)

def getFile(source, dest):    

    if (not os.path.isdir(dest.split('/')[0])):
        os.mkdir(dest.split('/')[0])
        
    os.system("wget -c " + source + " -O " + dest)

    return 0

#find . \( -name "*pyc" -o -name "*~" \) -exec \rm -f {} \;



if __name__ == "__main__":
    #flvdown("fringe", "3" , "1", "vi")
    option = ""
    if (len(sys.argv)>4):
        option = sys.argv[4] 
    url, dest = flvdown(sys.argv[1], sys.argv[2], sys.argv[3], option)
    if url != -1:
        if len(sys.argv) > 4:
            print '\ndownloading file', url
        getFile(url, dest)


