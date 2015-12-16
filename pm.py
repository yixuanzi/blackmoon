import os
import sys

def init_plugins(main):
    #sys.path.append(pp)
    for name in os.listdir(os.getcwd()+'/plugins'):
        if len(name)>6 and name[-3:]=='.py' and name[:7]=='plugin_':
            mod=__import__(name.split('.',1)[0])
            mod.init_plugin(main)
            main.gdict['plugins'][mod.__name__]=[mod,mod.info]