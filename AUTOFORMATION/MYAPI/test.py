#!/usr/bin/env python3
#- *- coding:utf-8 -*-
"""Tests unitaires
"""
__author__='Charles Dubos'
__license__='GNUv3'
__credits__='Charles Dubos'
__version__="2022.001"
__maintainer__='Charles Dubos'
__email__='pi.dubs@sfr.fr'
__status__='Development'



# Built-in
import unittest
from unittest import mock



# Other libs
pass



# Owned libs
from myApi import *



# Constants



# Classes
## TestCases

class GlobalTests(unittest.IsolatedAsyncioTestCase):

    async def testHome(self):
        result = await home()
        self.assertIs(type(result['status']), str)
        



class IptvTests(unittest.IsolatedAsyncioTestCase):
    pass



# Main part

if __name__=="__main__":
    unittest.main()