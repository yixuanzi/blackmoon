import os
import sys
import lib_func
import ConfigParser

########################################################################
class bmconfig:
    """"""

    #----------------------------------------------------------------------
    def __init__(self,path):
        """Constructor"""
        self.path=path
        self.cf=ConfigParser.ConfigParser()
        self.cf.read(path)
        self.change=0


    def getconfig(self,section,key):
        return self.cf.get(section,key)

    
    def setconfig(self,section,key,value):
        self.cf.set(section,key,value)
        self.change=1
        
    def __del__(self):
        if self.change:
            self.cf.write(open(path,'w'))
    
    