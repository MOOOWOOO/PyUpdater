# -*- coding:utf-8 -*-
"""
    
"""
import platform

__author__ = 'Jux.Liu'


class Platform():
    """Class for check platform system

    platform = Platform()
    """
    pathSplit = '/'
    tmpFolder = r'/tmp'

    def __init__(self):
        system = platform.system()
        if system == "Windows":
            self.pathSplit = '\\'
            self.tmpFolder = r'C:\\tmp\\'
        elif system == "Linux":
            self.pathSplit = '/'
            self.tmpFolder = r'/tmp/'
        else:
            raise SystemError
