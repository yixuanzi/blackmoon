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
        self.defgroups=('builds')
        
    
    def setdefaultgroups(self,groups):
        self.defgroups=groups
        
    def reggvars(self,key,value):
        if key:
            self.__gvars[key]=value
            return 1
    
    def getcmddict(self):
        return self.__cmd
 
    def getgvars(self,key):
        if self.__gvars.has_key(key):
            return self.__gvars[key]
    
        else:
            return None
        
    def regcommand(self,cmd,func,msg="No desc msg",sfile="buildins"):
        """plugin sfile must be __file__"""
        if sfile=="buildins":
            sfile=sfile
            group=sfile
        else:
            p,sfile=os.path.split(sfile)
            group=os.path.split(p)[1]
        if cmd and func:
            if self.__cmd.has_key(group):
                if self.__cmd[group].has_key(cmd):
                    lib_func.printstr("You can't reg exist command",2)
                    return -1
                else:
                    self.__cmd[group][cmd]=(func,msg,sfile)
            else:
                self.__cmd[group]=dict()
                self.__cmd[group][cmd]=(func,msg,sfile)

        return 0
        
    def defaultprefix(self):
        return "$BlackMoon$Maintive>"
    

    def getfunction(self,name,groups=None,tp=0):
        """0 function\t 1 desc message\t 2 help message"""
        if not groups:
            groups=self.defgroups
        for group in groups:
            if self.__cmd.has_key(group) and self.__cmd[group].has_key(name):
                if tp in (0,1,2):
                    return self.__cmd[group][name][tp]
                else:
                    return self.__cmd[group][name][0].__doc__
        return "Not exist command"
                
    def start(self):
        print self.welcome
        while 1:
            cmds=raw_input(self.prefix())
            cmds=cmds.strip().split(' ',1)
            if cmds[0] in ('exit','quit'):
                break
            func=self.getfunction(cmds[0])
            if len(cmds)>1 and type(func)!=str:
                func(cmds[1].strip())
            elif len(cmds)==1 and type(func)!=str:
                func("")
            else:
                lib_func.printstr("Not exist command in default groups!!!",2)
    
        lib_func.printstr("Interactive is finish")

#i=interactive()
#i.start()
