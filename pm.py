import os
import sys
import lib_interactive

def init_plugs(p="/plugins"):
    pp=sys.path[0]+p
    sys.path.append(pp)
    for name in os.listdir(pp):
        if len(name)>6 and name[-3:]=='.py' and name[:6]=='plugin':
            mod=__import__(name.split('.',1)[0])

zoom=zoomeye()
devs=zoom.zoomsearch("esgcc.com.cn")
zoom.printdevinfo(devs)
