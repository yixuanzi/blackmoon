import pycurl
import sys
import urllib2
import gzip
import StringIO
import os
import re

from bmplugin import *

info={'desc':"This is a method searching vluns of the RCE.",
      'cve':'',
      #'init':0,  #0 maual init 1 init on start the program
      'link':"http://www.seclabx.com"} 

def init_plugin(main):
    active=main.maintive
    active.regcommand('searchRCE',searchRCE_func)
    #zoom=zoomeye()
    #return "zoomeye",zoom
    
    
    
def searchRCE_func(testURL):
    #print "Input the URL:"
    #stringA=raw_input()
    r=urllib2.urlopen(testURL)
    page=r.read()
    #index=len(page)
    
    soup=BeautifulSoup(page)
    lt=soup.find('a',{'href':'http://jenkins-ci.org/'})
    rfc=re.search('(\d+)\.(\d+)(\.\d)*',lt.contents[0])
    ver=rfc.group()
    
    if ver[:]!='1.625.2':
        if (ver[0]>'1')or(ver[0]<'0'):
            print "The version is wrong!"
        else: 
            lib_func.printstr("Warning:The URL\n %s" %testURL)
            print "\nexist the vluns of RCE!"
    else:
        print "The URL does not exist the vluns of RCE!"