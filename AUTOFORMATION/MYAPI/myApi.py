#!/usr/bin/env python3
#- *- coding:utf-8 -*-
"""Ma petite API pour la gestion du PI
"""
__author__='Charles Dubos'
__license__='GNUv3'
__credits__='Charles Dubos'
__version__="2022.001"
__maintainer__='Charles Dubos'
__email__='pi.dubs@sfr.fr'
__status__='Development'



# Built-in

import logging.config, logging
import json
from pathlib import Path



# Other libs

from fastapi import FastAPI, HTTPException, Form



# Owned libs

from lib.libFuncs import *
import lib.libIptv
import lib.libServers



# Constants
## Conf file
CONFFILE='ressources/conf.json'


# Module directives

## Root dir
lib.libFuncs.ROOTPATH = str(Path( __file__ ).parent.absolute())

## Configuration
with open(toAbsPath(path=CONFFILE)) as fp:
    configuration = json.load(fp=fp)

## Creating specially-configured logger
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers':False,
    'formatters':{
        'default_formatter':{
            'format':'%(levelname)s:%(asctime)s\t[%(filename)s][%(funcName)s]\t%(message)s',
        },
    },
    'handlers':{
        "myApi_file_handler":{
            'class':'logging.FileHandler',
            'filename':toAbsPath(configuration['global']['logpath']),
            'encoding':'utf-8',
            'formatter':'default_formatter',
        },
    },
    'loggers':{
        'myApi':{
            'handlers':['myApi_file_handler'],
            'level':configuration['global']['loglevel'],
            'propagate':True
        }
    }
})
logger = logging.getLogger('myApi')
logger.debug(f'Logger loaded in {__name__}')



## IPTV
iptv_path = configuration['iptv']['channels_path']
iptv = lib.libIptv.channelsList(
    filename=toAbsPath(path=iptv_path)
)

## Servers
servers = [
    lib.libServers.Server().loadFromDict(
        content=server
    ) for server in configuration['servers']
]


## Definition of API
app = FastAPI()



# API points
@app.get('/')
async def home():
    """Point d'API d'entrée (retourne nom + version)
    """
    return {'name':__name__,
        'version':__version__,
        'status':__status__,
    }


@app.get('/iptv/')
async def iptvGet():
    """Liste l'ensemble des canaux disponibles

    Returns:
        list: Liste des JSON de canaux TV
    """
    
    return iptv.channels


@app.get('/iptv/{channel}/')
async def channelGet(channel:int):
    """Retourne le channel demandé

    Args:
        channel (int): Numéro du canal (commence à 1)

    Returns:
        json: canal TV tel que défini dans conf.json
    """
    return iptv.getChannel(channel=canal)



@app.delete('/iptv/{channel}/')
async def channelDelete(channel:int):
    """Supprime le canal demandé

    Args:
        channel (int): Numéro du canal (commence à 1)

    Returns:
        json: {"result":"OK"}
    """
    iptv.deleteChannel(channel=channel)
    return {"result":"OK"}



@app.post('/iptv/{channel}/')
async def channelSet(
    channel:int,
    name:str=Form()):
    """Crée ou modifie un canal

    Args:
        channel (int): Numéro du canal (commence à 1)
        content (json): Chaine fromattée. Valeurs données par formulaire (POST).

    Returns:
        json: {"result":"OK"}
    """
    try:
        iptv.setChannel(channel=channel, content=content)
        return {"result":"OK"}
    except:
        return {"result":"failed"}



@app.get('/servers/')
async def serversGet():
    """Retourne l'état des serveurs spécifiés dans la config

    Returns:
        json: Etat des serveurs
    """
    serversList=configuration['servers']
    for server in serversList:
        state = server[services]
    return channels[index]



