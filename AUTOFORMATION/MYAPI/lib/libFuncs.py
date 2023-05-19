#!/usr/bin/env python3
#- *- coding:utf-8 -*-
"""Fonctions utiles.
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



# Other libs
pass



# Owned libs
pass



# Module directives
## Constants
ROOTPATH=''
logger = getLogger('myApi')



# Functions
def toAbsPath(path:str) -> str:
    if path[0] == '/':
        logger.debug(f"Path {path} is absolute")
        return path
    else:
        return ROOTPATH + '/' + path
