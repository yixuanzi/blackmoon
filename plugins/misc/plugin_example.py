import pycurl
import sys
import urllib2
import gzip
import StringIO
from bs4 import *
#this module is must be load
from bmplugin import *

info={'desc':"this is a example for you",
      'cve':'',
      'link':"http://www.seclabx.com"} 

def init_plugin(main):
    active=main.maintive
    active.regcommand('example',test_func,"this is example plugin")

    
    
    
def test_func(paras):
    """example test_string"""
    lib_func.printstr("this is a example plugin")
    lib_func.printstr("this is your input for parameter")
    lib_func.printstr(paras,"PARAS:")
    lib_func.printstr("You can you everything here now!!!")
