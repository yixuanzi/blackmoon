import os
import sys
import ConfigParser
from bmplugin import *

main=None

class main_command:
    """blackMoon main class"""
    def __init__(self):
        global main
        self.maintive=lib_interactive.interactive()
        self.maintive.setdefaultgroups(PLUGINS_GROUPS)
        self.gdict={'plugins':{},'objects':{}}
        self.maintive.share=self.gdict
        self.pcf=lib_config.bmconfig(CONFIG_PATH)
        funcdict={'plugins':self.plugins,
                  'search':self.search,
                  'varobj':self.listobj,
                  'clear':self.clear,
                  'eval':self.bmeval,
                  'dump':self.dump,
                  'load':self.load,
                  'reload':self.reload}
        main=self
        for cmd,func in funcdict.iteritems():
            self.maintive.regcommand(cmd,func,func.__doc__)
            
    def plugins(self,paras=None):
        """list loaded plugins"""
        if not paras:
            lib_func.printlist(self.gdict['plugins'].keys(),1)
       
    def reloadconfig(self):
        self.pcf=lib_config.bmconfig(CONFIG_PATH)
        
    def search(self,paras):
        """search plugin for you key"""
        pass
            
    def listobj(self,paras):
        """list objection in the space"""
        for space,dt in self.gdict['objects'].iteritems():
            lib_func.printstr(space,"#####")
            for key in dt.keys():
                lib_func.printstr(key,"Object:")
        
    def clear(self,paras):
        """clear [-a] [-s space.name] """
        try:
            pd=lib_func.getparasdict(paras,"as:")
            if not pd:
                lib_func.printstr("You should input the vaild parameters",1)
                lib_func.printstr(self.clear.__doc__)
                return
        except Exception:
            lib_func.printstr(self.clear.__doc__)
            return
        if pd.has_key('a'):
            self.gdict['objects']=dict()
            return
        if pd.has_key('s'):
            sn=pd['s'].split('.',1)
            if len(sn)!=2:
                lib_func.printstr(self.clear.__doc__)
                return                
            if self.gdict['objects'].has_key(sn[0]) and self.gdict['objects'][sn[0]].has_key(sn[1]):
                self.gdict['objects'][sn[0]].pop(sn[1])
    
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
        
    def getobj_(self,name,space='buildins'):
        if self.gdict['objects'].has_key(space):
            if self.gdict['objects'][space].has_key(name):
                return self.gdict['objects'][space][name]
        lib_func.printstr("Have not %s in %s" %(name,space),1)
        return None


    def bmeval(self,sh):
        """eval python_segment"""
        try:
            rs=eval(sh)
            print rs
        except Exception:
            print "Error"

    def dump(self,paras):
        """dump [-o filename] [--space=space] objname"""
        try:
            pd=lib_func.getparasdict(paras,"o:",['space='])
            if (not pd) or len(pd['args'])!=1:
                lib_func.printstr("You should input the vaild parameters",1)
                lib_func.printstr(self.dump.__doc__)
                return
        except Exception:
            lib_func.printstr(self.dump.__doc__)
            return
        space=None
        if pd.has_key('space'):
            space=pd['space']
        if pd.has_key('o'):
            fp=pd['o']
        else:
            fp="%s/%.pkl" %(PWD_PATH,lib_func.getrandomstr())
        obj=getobj(pd['args'][0],space)
        if obj:
            lib_func.dumpobj(obj,fp)
        else:
            lib_func.printstr("Have not %s" %pd['args'][0])
            
    def load(self,paras):
        """load [-o objname] filename"""
        try:
            pd=lib_func.getparasdict(paras,"o:")
            if (not pd) or len(pd['args'])!=1:
                lib_func.printstr("You should input the vaild parameters",1)
                lib_func.printstr(self.load.__doc__)
                return
        except Exception:
            lib_func.printstr(self.load.__doc__)
            return
        if pd.has_key('o'):
            objname=pd['o']
        else:
            objname="pkl_%s" %lib_func.getrandomstr()
        obj=lib_func.loadobj(pd['args'][0])
        if obj:
            self.regobj(obj,objname)
    
    def reload(self,paras):
        """reload module_name"""
        try:
            pd=lib_func.getparasdict(paras,"")
        except Exception:
            lib_func.pris(self.reload.__doc__)
            return
        ddict=dict()
        if lib_func.setparas(pd,ddict,1):
            pass
        else:
            lib_func.pris(self.reload.__doc__)
            
    def getobj(self,name,space=None):
        if space:
            if self.gdict['objects'].has_key(space):
                if self.gdict['objects'][space].has_key(name):
                    return self.gdict['objects'][space][name]
        for space in self.gdict['objects']:
            if self.gdict['objects'][space].has_key(name):
                return self.gdict['objects'][space][name]
        return None
    
            