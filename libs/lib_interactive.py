import os
import sys
import lib_func

########################################################################
class interactive:
    """"""
    welcome="The interctive is start\nYou can use 'exit' 'quit' to quit it!"
    #----------------------------------------------------------------------
    def __init__(self):
        """my interactive for buyi"""
        self.__gvars=dict()
        self.__cmd=dict()
        self.prefix=self.defaultprefix
        self.share=None
    
    def reggvars(self,key,value):
        if key:
            self.__gvars[key]=value
            return 1
    
    def getcommandlist(self):
        return self.__cmd.keys()
    
    def getgvars(self,key):
        if self.__gvars.has_key(key):
            return self.__gvars[key]
    
        else:
            return None
        
    def regcommand(self,cmd,func):
        if cmd and func:
            if not self.__cmd.has_key(cmd):
                self.__cmd[cmd]=func
            else:
                print "Error: you can't reg exist command"
            return 1
        
    def defaultprefix(self):
        return "BlackMoon/Maintive:>"
    
        
    def start(self):
        print self.welcome
        while 1:
            cmds=raw_input(self.prefix())
            cmds=cmds.split(' ',1)
            if cmds[0] in ('exit','quit'):
                break
            if len(cmds)>1 and self.__cmd.has_key(cmds[0]):
                self.__cmd[cmds[0]](cmds[1])
            elif len(cmds)==1 and self.__cmd.has_key(cmds[0]):
                self.__cmd[cmds[0]](None)
            else:
                print "Error command!!!"
    
        print "Interactive is finish"

#i=interactive()
#i.start()
