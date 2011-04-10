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

def cmpPrio(plx, ply):
    "compare function to sort possible links"
    priority = {'z':0, 'l':1, 'n':2}
    if priority[plx[1]] > priority[ply[1]]:
        return 1
    elif priority[plx[1]] == priority[ply[1]]:
        return 0
    else:
        return -1





def flvdown(tvshow, season, episode, options):
    """ search episode through modules """

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
        __import__("aggregators." + i)
        possible_links += sys.modules["aggregators."+i].getLinks(tvshow, \
            season, episode)

    ##Sort possible_links
    
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
                exit(1)
    final_url = final[0]
    ##  print final_url
    ##  return 
    if verbose:
        print '\ndownloading file', final_url

    if (not os.path.isdir(tvshow)):
        os.mkdir(tvshow)
        
    ext = "." + final_url.split('.')[-1]

    os.system("wget -c " + final_url + " -O " + tvshow + "/" + filename + ext)
    tmpfile = final[1]
    if (tmpfile):
        os.remove(tmpfile + ".html")
        os.remove(tmpfile + ".cook")

#find . \( -name "*pyc" -o -name "*~" \) -exec \rm -f {} \;



if __name__ == "__main__":
    """ executed if called from command line"""
    #flvdown("fringe", "3" , "1", "vi")
    if (len(sys.argv)>4):
        option = sys.argv[4] 
    flvdown(sys.argv[1], sys.argv[2], sys.argv[3], option)

