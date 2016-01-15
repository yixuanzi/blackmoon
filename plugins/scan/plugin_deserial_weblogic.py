import pycurl
import sys
import urllib2
import gzip
import StringIO
import os
import re
from bs4 import *
from bmplugin import *

info={'desc':"scan java deserial vulns with weblogic",
      'cve':'',
      'author':'yb',
      'link':"http://www.seclabx.com"} 
mainobj=None
def init_plugin(main):
    global mainobj
    mainobj=main
    active=main.maintive
    active.regcommand('wlgds',scan_deserial_weblogics,"scan deserial weblogic host",__file__)
  
      
    
def scan_deserial_weblogic(theURL):
    r=urllib2.urlopen(theURL+'/console/login/LoginForm.jsp',timeout=5)
    page=r.read()    
    soup=BeautifulSoup(page)
    p=soup.find('p',{'id':'footerVersion'})  
    ver=re.search('(\d+\.)+\d+',p.contents[0])
    vers=['9.2.3.0','9.2.4.0','10.0.0.0','10.0.1.0','10.0.2.0','10.2.6.0','10.3.0.0','10.3.1.0','10.3.2.0','10.3.4.0','10.3.5.0','12.1.1.0']
    if ver.group() in vers:
        return 1
    return 0
    
        
def scan_deserial_weblogics(paras):
    """wlgds [-h host] [--object=objs]"""
    try:
        pd=lib_func.getparasdict(paras,"h:",['object='])
    except Exception:
        lib_func.printstr(scan_deserial_weblogics.__doc__,1)
        return
    ddict={'h':'','object':''}
    lib_func.setparas(pd,ddict)
    if ddict['h']:
        if scan_deserial_weblogic(ddict['h']):
            lib_func.printstr(ddict['h'],'Host:')
    elif ddict['object']:
        obj=mainobj.getobj(ddict['object'])
        if obj and obj.__doc__[:4]=='dict':
            for zl in obj:
                if scan_deserial_weblogic(zl['address']):
                    lib_func.printstr(ddict['h'],'Host:')
            
        