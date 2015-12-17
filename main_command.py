import os
import sys
import ConfigParser
from bmplugin import *

class main_command:
    
    def __init__(self):
        self.maintive=lib_interactive.interactive()
        self.gdict={'plugins':{}}
        self.maintive.share=self.gdict
        self.pcf=lib_config.bmconfig(os.getcwd()+'/plugins/plugins.ini')
        funcdict={'plugins':self.plugins,\
                  'search':self.search,\
                  'commands':self.commands,\
                  'varobj':self.varobj,\
                  'clear':self.clear,
                  'help':self.commands}
        
        for key,value in funcdict.iteritems():
            self.maintive.regcommand(key,value)
            
    def plugins(self,paras=None):
        if not paras:
            lib_func.printlist(self.gdict['plugins'].keys(),1)
        pass
    
    def search(self,paras):
        pass
    
    def commands(self,paras=None):
        if paras:
            pd=lib_func.getparasdict(paras,'v')
            if pd.has_key('v'):
                lib_func.printlist(self.maintive.getcommandlist(),1)
                return
        lib_func.printlist(self.maintive.getcommandlist())

    
    def varobj(self,paras):
        pass
    
    def clear(self,paras):
        pass
    
    def start(self):
        self.maintive.start()

        