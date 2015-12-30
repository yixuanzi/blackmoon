import pycurl
import sys
import urllib2
import gzip
import StringIO
import os
import re
from bs4 import *
from bmplugin import *

info={'desc':"this is a test",
      'cve':'',
      'init':0,  #0 maual init 1 init on start the program
      'link':"http://www.sina.com"} 

def init_plugin(main):
    active=main.maintive
    active.regcommand('testing',testing_func)
    pass
    #zoom=zoomeye()
    #return "zoomeye",zoom
    
    
    
def testing_func(theURL):
       
    r=urllib2.urlopen(theURL)       
    page=r.read()    
    soup=BeautifulSoup(page)
    p=soup.find('p',{'id':'footerVersion'})  
    ver=re.search('(\d+\.)+\d+',p.contents[0])
    #contents[0]
    ver1=ver.group()
    vers=['9.2.3.0','9.2.4.0','10.0.0.0','10.0.1.0','10.0.2.0','10.2.6.0','10.3.0.0','10.3.1.0','10.3.2.0','10.3.4.0','10.3.5.0','12.1.1.0']
    if ver1 in vers:
        print 'This is a dangerous URL'
    else:
        print 'This is a safe URL'