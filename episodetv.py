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
    def __init__(self, tvshow, season, episode, ids):
        self.tvshow = tvshow.lower()
        self.tvshow_ = "_".join(self.tvshow.split(" "))
        self.tvshowSpace = " ".join(self.tvshow.split("_"))
        self.numSeason = int(season)
        self.numEpisode = int(episode)
        self.strSeason = str(self.numSeason)
        if (self.numEpisode < 10):
            self.strEpisode = "0" + str(self.numEpisode)
        else:
            self.strEpisode = str(self.numEpisode)
        self.ids = ids
        self.isOnDisk = self.existFile()

    def getBaseName(self):
        """ return foo101 """
        return self.tvshow_ + self.strSeason + self.strEpisode

    def getSrtName(self):
        """ return foo_1_01.srt """
        return self.getBaseName() + ".srt"

    def createDir(self):
        """ create directory if it doesn't exist """
        if (not ospath.isdir(self.tvshow)):
            osmkdir(self.tvshow)
            
    
    def removeFile(self):
        """ delete the file """
        ossystem("rm " + tvshow + "/" + tvshow + season + episode + "*")
    
    
    def existFile(self):
        """ test if a file match the name """
        return gglob(self.tvshow_ + '/' + self.getBaseName() + '.*')
    
    def getVideoName(self):
        """ return the name of the video file (once downloaded) """
        tvfiles = oslistdir(self.tvshow_)
        videoFile = ""
        for videoFile in tvfiles:
            if (videoFile.startswith(self.getBasename()) and \
              not (videoFile == self.getSrtName())):
                videoFile = self.tvshow_ + "/" + videoFile
                break
        return videoFile
    
