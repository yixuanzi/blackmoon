import pycurl
import sys
import urllib2
import gzip
import StringIO
from bs4 import *
from bmplugin import *

info={'desc':"this is a test",
      'cve':'',
      'init':0,  #0 maual init 1 init on start the program
      'link':"http://www.seclabx.com"} 

def init_plugin(main):
    active=main.maintive
    active.regcommand('test',test_func)
    #zoom=zoomeye()
    #return "zoomeye",zoom
    
    
    
def test_func(paras):
    lib_func.printstr("this is a tset\n %s" %paras)
