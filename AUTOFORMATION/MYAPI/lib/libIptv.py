#!/usr/bin/env python3
#- *- coding:utf-8 -*-
"""Bibliothèque des fonctions utiles à la gestion des chaines
Utilise un fichier json pour la sauvegarde.
"""
__author__='Charles Dubos'
__license__='GNUv3'
__credits__='Charles Dubos'
__version__="2022.001"
__maintainer__='Charles Dubos'
__email__='pi.dubs@sfr.fr'
__status__='Development'



# Built-in
from logging import getLogger
import json



# Other libs
pass



# Owned libs
pass



# Constants
emptyChannel = {'populated':False}
logger = getLogger('myApi')



# Classes

class channelsList:
    filename=None
    channels=None

    def __init__(self, filename:str):
        self.filename = filename
        logger.info(f"Loading channels from {filename}")
        self.loadChannels()


    def loadChannels(self):
        with open(file=self.filename, mode='rt') as fp:
            self.channels = json.load(fp=fp)
        logger.debug(f"{str(len(self.channels))} channel(s) loaded")


    def saveChannels(self):
        with open(file=self.filename, mode='wt') as fp:
            json.dump(obj=self.channels, fp=fp)
        logger.debug(f"{str(len(self.channels))} channel(s) saved to {self.filename}")


    def getChannel(self, channel:int)->dict:
        index = channel - 1
        assert index in range(len(self.channels)), 'Out of bounds'
        logger.debug(f'Returning channel #{str(channel)}')
        return self.channels[index]


    def setChannel(self, channel:int, content:dict):
        index = channel - 1
        assert index > 0 , 'Out of bounds'
        logger.info(f'Modifying channel #{str(channel)}')
        self.enlargeChannels(channel)
        self.channels[index] = content
        self.saveChannels()

    
    def deleteChannel(self, channel:int):
        index = channel-1
        assert index in range(len(self.channels)), 'Out of bounds'
        logger.warning(f'Removing channel #{str(channel)}')
        self.channels[index]=emptyChannel
        self.reduceChannels()
        self.saveChannels()

    
    def enlargeChannels(self, size:int):
        for i in range(start=len(self.channels)-1, stop=size):
            logger.debug(f'Creating empty channel #{str(i+1)}')
            self.channels.append(emptyChannel)


    def reduceChannels(self):
        for i in range(start=len(self.channels)-1, stop=0, step=-1):
            if self.channels[i] == emptyChannel:
                logger.debug(f'Removing empty channel #{str(i+1)}')
                del self.channels[i]
            else:
                break
        self.saveChannels()

