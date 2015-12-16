import os
import sys
from bmplugin import *

class main_command:
    
    def __init__(self):
        self.maintive=lib_interactive.interactive()
        self.gdict={'plugins':{}}
        self.maintive.share=self.gdict
        funcdict={'plugins':self.plugins,\
                  'search':self.search,\
                  'commands':self.commands,\
                  'varobj':self.varobj,\
                  'clear':self.clear}
        
        for key,value in funcdict.iteritems():
            self.maintive.regcommand(key,value)
            
    def plugins(self,paras=None):
        if not paras:
            lib_func.printlist(self.gdict['plugins'].keys())
        pass
    
    def search(self,paras):
        pass
    
    def commands(self,paras=None):
        lib_func.printlist(self.maintive.getcommandlist())
        pass
    
    def varobj(self,paras):
        pass
    
    def clear(self,paras):
        pass
    
    def start(self):
        self.maintive.start()