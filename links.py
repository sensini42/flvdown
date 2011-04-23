#!/usr/bin/python
# -*- coding: utf-8 -*-
""" looks for links with submodules """
import os
import aggregators
import sys 
import re

import episodetv

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
    if verbose:    
        print '\ndownloading ', link, znl
    return (link, znl)


def flvdown(episode, options, list_site = None):
    """ search episode through modules """

    filename = episode.tvshow_ + '/' + episode.getBaseName()
        
    ##test if a file with similar name exist
    ret = os.system("ls " + filename + "* 2> /dev/null")
    if not ret :
        print 'there is a file name ' + filename + '...\n'
        choice = raw_input('continue ? (y/n)\n')
        if choice not in 'yYoO':
            return None, None

    interact = 0
    verbose = 0
    ##process arguments
    if (options):
        if ("i" in options):
            interact = 1
            verbose = 1
        if ("v" in options):
            verbose = 1

    possible_links = []
    if interact or not list_site:
        #check all site
        for i in aggregators.__all__:
            #        if verbose:
            print "checking", i
            __import__("aggregators." + i)
            possible_links += sys.modules["aggregators."+i].getLinks( \
                episode.tvshow, episode.strSeason, \
                str(int(episode.strEpisode)))
        print "done"
        if possible_links == []:
            print '\033[1;31mno link\033[0m found'
            return None, None
        (link, znl) = getEpisodeLink(possible_links, verbose, interact)
        __import__("aggregators." + znl)
        final = sys.modules["aggregators." + znl].getFlv(link, verbose)
        if final == -1:
            print '\033[1;31mno link\033[0m found'
            return None, None
    else:
    ##Sort possible_links
#        prio = dict(zip(['_mod.'.join(i.split(' : ')) \
#                     for i in list_site], range(len(list_site))))
#        print prio
        list_sites = list_site[:]
        url_found = False
        modulesChecked = []
        while ((not url_found) and  list_sites):
            hmod, hsite = list_sites.pop(0).split(' : ')
            print "checking", hmod, hsite
            if hmod not in modulesChecked:
                i = "aggregators." + hmod
                __import__(i)
                modulesChecked.append(hmod)
                possible_links += sys.modules[i].getLinks( \
                    episode.tvshow, episode.strSeason, \
                    str(int(episode.strEpisode)))
            links_for_sites = [l for l in possible_links \
                              if hmod + "_mod." + hsite in l]
            while (links_for_sites and (not url_found)):
                (link, znl) = getEpisodeLink(links_for_sites, verbose, interact)
                __import__("aggregators." + znl)
                final = sys.modules["aggregators." + znl].getFlv(link, verbose)
                if final != -1:
                    url_found = True
                else:
                    links_for_sites.remove([link, znl])
        if not url_found:
            print '\033[1;31mno link\033[0m found'
            return None, None
    final_url = final[0]

    ext = "." + final_url.split('.')[-1]

    if re.match("^\d", final_url):
        final_url = 'http://' + final_url 

    if verbose:
        print final_url
    print final_url
    return (None, None)
    return (final_url, filename + ext)

def getFile(source, dest):    

    if (not os.path.isdir(dest.split('/')[0])):
        os.mkdir(dest.split('/')[0])
        
    os.system("wget -c " + source + " -O " + dest)

    return 0

if __name__ == "__main__":
    #flvdown("fringe", "3" , "1", "vi")
    option = ""
    if (len(sys.argv)>4):
        option = sys.argv[4] 
    episode = episodetv.episodeTV(sys.argv[1], sys.argv[2], sys.argv[3])
    url, dest = flvdown(episode, option)
    if url:
        if option:
            print '\ndownloading file', url, 'to', dest
        getFile(url, dest)


