#!/usr/bin/env python3
#- *- coding:utf-8 -*-
"""Ma petite API poiur l'amélioration du PI
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
from subprocess import run, Popen



# Other libs
pass



# Owned libs
pass



# Constants
## Logger
logger = getLogger('myApi')

## Systemctl bash commands
TEST_RUNNING = ['is-active']
TEST_STOPPED = ['is-failed']
START = ['unmask','start']
STOP = ['stop', 'mask']



# Classes

class Server:
    name=None
    services=[] # List of daemons listed in the order of enable (disabled in reverse order)
    preStart=[] # List of bash commands before enabling 
    postStart=[]# List of bash commands after enabling
    preStop=[]  # List of bash commands before disabling
    postStop=[] # List of bash commands after disabling


    def loadFromDict(self, content:dict):
        logger.debug('Loading from dict')
        for key in content:
            self.__setattr__(key, content[key])
            logger.debug(f'Key {key} loaded')


    def unmaskAndStart(self):
        logger.debug(f'Requesting {name} start')
        for cmd in self.preStart:
            _executeBash(bashCmd = cmd)
        _executeSystemctl(services=self.services,actions=START)
        for cmd in self.postStart:
            _executeBash(bashCmd = cmd)


    def stopAndMask(self):
        logger.debug(f'Requesting {name} stop')
        for cmd in self.preStop:
            _executeBash(bashCmd = cmd)
        _executeSystemctl(services=self.services.reverse(),actions=STOP)
        for cmd in self.postStop:
            _executeBash(bashCmd = cmd)


    def status(self)->str:
        logger.debug(f'Requesting {name} status')
        status=[True]
        for service in self.services:
            if _executeSystemctl(self.services,TEST_RUNNING, '--quiet') == 0:
                status.append(True)
            elif _executeSystemctl(self.services,TEST_STOPPED, '--quiet') !=0:
                status.append(False)
            else:
                logger.warning(f'{service} of {self.name} is in error')
                return 'error'
        if all(status):
            logger.debug(f'All services of {self.name} are up')
            return 'running'
        elif all(status):
            logger.debug(f'All services of {self.name} are down')
            return 'stopped'
        else:
            logger.info(f'At least one service of {self.name} is down')
            return 'unstable'


def _executeSystemctl(services:list, actions:list, sudo:bool=False, *args)->int:
    for service in services:
        for action in actions:
            logger.debug(f'Dealing {action} for service {service}')
            bashCmd = ['systemctl', action, service] + args
            runCmd = _executeBash(bashCmd=bashCmd, sudo=sudo)
            if runCmd != 0:
                logger.debug(f'{runCmd} returned a non-zero response code')
                return runCmd
    return 0


def _executeBash(bashCmd:list, sudo:bool=False)->int:
    runCmd = (['sudo'] if sudo else [])\
        + ['bash','-c']\
        + [' '.join(bashCmd)]
    (logger.warning if sudo else logger.info)(f'Executing bash command {runCmd}')
    execution = run(command, capture_output=True)
    if execution.returncode != 0:
        logger.debug(f'{runCmd} returned a non-zero response code')
        return execution.returncode
    return 0
