import sys
import os
from bs4 import *
import pycurl
import gzip
import StringIO
import re
import urllib2

from bmplugin import *

info={'desc':"baidupcs in this",
      'cve':'',
      'link':''} 

def init_plugin(main): 
    sys.path.append(lib_func.getcwd4file(__file__)+'\\baidupcs')
    active=main.maintive
    import bdcloud_manager
    bdcloud_manager.bdcloud.main=main
    active.regcommand('bdpcs',bdcloud_manager.start,"baidu pcs for intertive",__file__)
    
    