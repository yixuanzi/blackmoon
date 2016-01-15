import pycurl
import sys
import urllib2
import gzip
import StringIO
import os
import re

from bmplugin import *

info={'desc':"This is a method scan vluns with deserial jenkins",
      'cve':'',
      'author':'wj',
      'link':"http://www.seclabx.com"} 

mainobj=None

def init_plugin(main):
    global mainobj
    mainobj=main
    active=main.maintive
    active.regcommand('jkds',scan_deserial_jenkinses,"scan unserial vulns with jenkins",__file__)

        
    
def scan_deserial_jenkins(testURL):
    r=urllib2.urlopen(testURL+'/login',timeout=5)
    page=r.read()
    soup=BeautifulSoup(page)
    lt=soup.find('a',{'href':'http://jenkins-ci.org/'})
    rfc=re.search('(\d+)\.(\d+)(\.\d)*',lt.contents[0])
    ver=rfc.group()
    if lib_func.compereversion('1.625.2',ver)==1:
        return 1
    else:
        return 0

def scan_deserial_jenkinses(paras):
    """jkds [-h host] [--object=objs]"""
    try:
        pd=lib_func.getparasdict(paras,"h:",['object='])
    except Exception:
        lib_func.printstr(scan_deserial_jenkins.__doc__,1)
        return
    ddict={'h':'','object':''}
    lib_func.setparas(pd,ddict)
    if ddict['h']:
        if scan_deserial_jenkins(ddict['h']):
            lib_func.printstr(ddict['h'],'Host:')
    elif ddict['object']:
        obj=mainobj.getobj(ddict['object'])
        if obj and obj.__doc__[:4]=='dict':
            for zl in obj:
                if scan_deserial_jenkins(zl['address']):
                    lib_func.printstr(ddict['h'],'Host:')
            
        