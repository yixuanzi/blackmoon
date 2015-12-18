import sys
import os
from bs4 import *
import pycurl
import gzip
import StringIO
import re
import urllib2
from bmplugin import *

info={'desc':"shu xiang recharge brute",
      'cve':'',
      'link':''} 

def init_plugin(main): 
    #jenkins=jenkins_unauth()
    active=main.maintive
    active.regcommand('sxrecbrute',sxrecharge_brute,"shu xiang recharge brute")