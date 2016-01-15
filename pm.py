import os
import sys
from bmplugin import *

def init_plugins(main):
    init_plugins4path(main,PWD_PATH)
    [init_plugins4path(main,path) for path in PLUGINS_PATH]
    

def init_plugins4path(main,path):
    #sys.path.append(pp)
    for name in os.listdir(path):
        if len(name)>6 and name[-3:]=='.py' and name[:7]=='plugin_':
            #try:
            mod=__import__(name.split('.',1)[0])
            mod.init_plugin(main)
            main.gdict['plugins'][mod.__name__]=[mod,mod.info]
            #except Exception:
                #lib_func.printstr("Have Error in load %s" %name,2)
