#!/usr/bin/python
# -*- coding: utf-8 -*-
""" handle episodes """

from os import mkdir as osmkdir
from os import path as ospath
from os import system as ossystem
from glob import glob as gglob
from os import listdir as oslistdir

class episodeTV():
    """ one instance for one episode """
    def __init__(self, tvshow, season, episode, ids=None, dictTV=None):
        if dictTV:
            self.tvshow = dictTV['default'].lower()
            self.dictTV = dictTV
        else:  
            self.tvshow = tvshow.lower()
            self.dictTV = {}
            self.dictTV['default'] = self.tvshow
        self.tvshow_ = "_".join(self.tvshow.split(" "))
        self.listName = self.tvshow_.split("_")
        self.tvshowSpace = " ".join(self.listName)
        self.numSeason = int(season)
        self.numEpisode = int(episode)
        self.strSeason = str(self.numSeason)
        if (self.numEpisode < 10):
            self.strEpisode = "0" + str(self.numEpisode)
        else:
            self.strEpisode = str(self.numEpisode)
        self.ids = ids
        self.isOnDisk = (self.existFile() != [])

    def getBaseName(self):
        """ return foo_101 """
        return self.tvshow_ + "_" + self.strSeason + self.strEpisode

    def getSrtName(self):
        """ return the name of the srt file (once downloaded) """
        tvfiles = oslistdir(self.tvshow_)
        srtFile = ""
        for _file in tvfiles:
            if _file == self.getBaseName() + '.srt':
                srtFile = self.tvshow_ + "/" + _file
                break
        return srtFile

    def createDir(self):
        """ create directory if it doesn't exist """
        if (not ospath.isdir(self.tvshow_)):
            osmkdir(self.tvshow_)
            
    
    def removeFile(self):
        """ delete the files """
        ossystem("rm " + self.tvshow_ + "/" + self.getBaseName() + ".*")
    
    
    def existFile(self):
        """ test if a file match the name """
        return gglob(self.tvshow_ + '/' + self.getBaseName() + '.*')
    
    def getVideoName(self):
        """ return the name of the video file (once downloaded) """
        tvfiles = oslistdir(self.tvshow_)
        videoFile = ""
        for _file in tvfiles:
            if (_file.startswith(self.getBaseName()) and \
              not _file.endswith('.srt')):
                videoFile = self.tvshow_ + "/" + _file
                break
        return videoFile
    
