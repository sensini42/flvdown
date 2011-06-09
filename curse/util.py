# -*- coding: utf-8 -*-

def episodes(list_ep, condition):
    """ create a list with episode checking condition """
    setShows = []
    setEpisodes = []
    for episode in list_ep:
        if episode.isOnDisk == condition and \
            episode.tvshowSpace not in setShows:
              setShows.append(episode.tvshowSpace)
              setEpisodes.append(episode)
    return setEpisodes


