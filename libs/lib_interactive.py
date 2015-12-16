import os
import sys

########################################################################
class interactive:
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """my interactive for buyi"""
        self.gvars={}
        self.fdict={"prefix":self.defaultprefix}
    
    def reggvars(self,key,value):
        if key:
            self.gvars[key]=value
            return 1
    
    def getgvars(self,key):
        if self.gvars.has_key(key):
            return self.gvars[key]
    
        else:
            return None
        
    def regcommand(self,cmd,func):
        if cmd and func:
            self.fdict[cmd]=func
            return 1
        
    def defaultprefix(self):
        return "blackMoon:>"
    
    def start(self):
        while 1:
            cmds=raw_input(self.fdict['prefix']())
            cmds=cmds.split(' ',1)
            if cmds[0] in ('exit','quit'):
                break
            if len(cmds)>1 and self.fdict.has_key(cmds[0]):
                self.fdict[cmds[0]](cmds[1])
            elif len(cmds)==1 and self.fdict.has_key(cmds[0]):
                self.fdict[cmds[0]](None)
            else:
                print "Error command!!!"
    
        print "Interactive is finish"


    