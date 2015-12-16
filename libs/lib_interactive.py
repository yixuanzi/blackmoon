import os
import sys

########################################################################
class interactive:
    """"""
    welcome="The interctive is start\nYou can use 'exit' 'quit' to quit it!"
    #----------------------------------------------------------------------
    def __init__(self):
        """my interactive for buyi"""
        self.__gvars={}
        self.__fdict={"prefix":self.defaultprefix}
        self.share=None
    
    def reggvars(self,key,value):
        if key:
            self.__gvars[key]=value
            return 1
    
    def getcommandlist(self):
        return self.__fdict.keys()
    
    def getgvars(self,key):
        if self.__gvars.has_key(key):
            return self.__gvars[key]
    
        else:
            return None
        
    def regcommand(self,cmd,func):
        if cmd and func:
            if not self.__fdict.has_key(cmd):
                self.__fdict[cmd]=func
            else:
                print "Error: you can't reg exist command"
            return 1
        
    def defaultprefix(self):
        return "blackMoon:>"
    
    
    def start(self):
        print self.welcome
        while 1:
            cmds=raw_input(self.__fdict['prefix']())
            cmds=cmds.split(' ',1)
            if cmds[0] in ('exit','quit'):
                break
            if len(cmds)>1 and self.__fdict.has_key(cmds[0]):
                self.__fdict[cmds[0]](cmds[1])
            elif len(cmds)==1 and self.__fdict.has_key(cmds[0]):
                self.__fdict[cmds[0]](None)
            else:
                print "Error command!!!"
    
        print "Interactive is finish"
