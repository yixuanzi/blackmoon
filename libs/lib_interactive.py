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
        self.prefix="$BlackMoon$Maintive>"
        self.share=None
        self.defgroups=('buildins',)
        self.regcommand('help',self.tivehelp,self.tivehelp.__doc__)
    
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
        
    def setdefaultprefix(self,prefix):
        if prefix:
            self.prefix=prefix
            return prefix

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
            cmds=raw_input(self.prefix)
            cmds=cmds.strip().split(' ',1)
            if cmds[0] in ('exit','quit'):
                break
            func=self.getfunction(cmds[0])
            if len(cmds)>1 and type(func)!=str:
                self.run(func,cmds[1].strip())
            elif len(cmds)==1 and type(func)!=str:
                self.run(func,"")
            else:
                lib_func.printstr("Not exist command in default groups!!!",2)
    
        lib_func.printstr("Interactive is finish")
    
    def run(self,func,paras=""):
        try:
            func(paras)
        except Exception:
            lib_func.printstr("have error in %s %s" %(func.__name__,paras),2)
            
    def tivehelp(self,paras):
        """print help msg for you question"""
        try:
            pd=lib_func.getparasdict(paras,'v')
            if not pd:
                for group,dt in self.getcmddict().iteritems():
                    lib_func.printstr(group,'####')
                    for name,cmdmsg in dt.iteritems():
                        print '*'+name,
                    print ''
                return
            if pd.has_key('v'):
                for group,dt in self.getcmddict().iteritems():
                    lib_func.printstr(group,'####')
                    for name,cmdmsg in dt.iteritems():
                        lib_func.printstr("%s\t%s" %(name,cmdmsg[1]),'*')
                return
            if pd.has_key('args') and len(pd['args'])==1:
                lib_func.printstr(self.getfunction(pd['args'][0],tp=2),'SRCFILE:')
                lib_func.printstr(self.getfunction(pd['args'][0],tp=3),'HelpMSG:')
        except Exception:
            lib_func.printstr("You parameter vaild",2)
           

#i=interactive()
#i.start()
