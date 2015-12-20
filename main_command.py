import os
import sys
import ConfigParser
from bmplugin import *

class main_command:
    """blackMoon main class"""
    def __init__(self):
        self.maintive=lib_interactive.interactive()
        self.maintive.setdefaultgroups(PLUGINS_GROUPS)
        self.gdict={'plugins':{},'objects':{}}
        self.maintive.share=self.gdict
        self.pcf=lib_config.bmconfig(CONFIG_PATH)
        funcdict={'plugins':self.plugins,\
                  'search':self.search,\
                  'varobj':self.listobj,\
                  'clear':self.clear,
                  'help':self.bmhelp}
        
        for cmd,func in funcdict.iteritems():
            self.maintive.regcommand(cmd,func,func.__doc__)
            
    def plugins(self,paras=None):
        """list loaded plugins"""
        if not paras:
            lib_func.printlist(self.gdict['plugins'].keys(),1)
        pass
    
    def search(self,paras):
        """search plugin for you key"""
        pass
    
    def bmhelp(self,paras):
        """print help msg for you question"""
        try:
            pd=lib_func.getparasdict(paras,'v')
            if not pd:
                for group,dt in self.maintive.getcmddict().iteritems():
                    lib_func.printstr(group,'####')
                    for name,cmdmsg in dt.iteritems():
                        print '*'+name,
                    print ''
                return
            if pd.has_key('v'):
                for group,dt in self.maintive.getcmddict().iteritems():
                    lib_func.printstr(group,'####')
                    for name,cmdmsg in dt.iteritems():
                        lib_func.printstr("%s\t%s" %(name,cmdmsg[1]),'*')
                return
            if pd.has_key('args') and len(pd['args'])==1:
                lib_func.printstr(self.maintive.getfunction(pd['args'][0],tp=2),'SRCFILE:')
                lib_func.printstr(self.maintive.getfunction(pd['args'][0],tp=3),'HelpMSG:')
        except Exception:
            lib_func.printstr("You parameter vaild",2)
           
        
    def listobj(self,paras):
        """list objection in the space"""
        for space,dt in self.gdict['objects'].iteritems():
            print space
            for key,value in dt:
                print '\t',key,value
        pass
    
    def clear(self,paras):
        """clear object """
        pass
    
    def start(self):
        self.maintive.start()
        
    def regobj(self,obj,name,space='buildins'):
        if self.gdict['objects'].has_key(space):
            if self.gdict['objects'][space].has_key(name):
                lib_func.printstr("you can't reg same name objects in %s" %space)
                return
            else:
                self.gdict['objects'][space][name]=obj
        else:
            self.gdict['objects'][space]=dict()
            self.gdict['objects'][space][name]=obj
        lib_func.printstr("You reg object %s in %s succfully" %(name,space))

        