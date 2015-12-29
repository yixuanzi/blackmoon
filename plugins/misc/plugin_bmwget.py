import sys
import os
from bs4 import *
import pycurl
import gzip
import StringIO
import re
import urllib2


from bmplugin import *

info={'desc':"bmwget for this frametework",
      'cve':'',
      'link':''} 

def init_plugin(main): 
    active=main.maintive
    active.regcommand('bmwget',wgetaction,"get rec from http",__file__)
    
    


def wgetaction(paras):
    """bmwget [-m dd|batch] [-t thread] [-l] [-b] [--batch=batch_opts] [--download=download_opts] URL SAVE_PATH"""
    try:
        pd=lib_func.getparasdict(paras,"m:t:lb",['batch=','download='])
    except Exception:
        lib_func.printstr(wgetaction.__doc__,1)
        return
    
    runthime={'m':'dd','t':1,'l':0,'b':0,'batch':"link|.*",'download':"",'type':'1'}
    if not lib_func.setparas(pd,runthime,1):
        lib_func.printstr(wgetaction.__doc__,1)
        return   
    if runthime['m']=='dd':
        bmd=lib_http.bmdownload(runthime['t'],runthime['b'],runthime['l'])
        bmd.download(runthime['args'][0],runthime['args'][1])
        
    elif runthime['m']=='batch':
        head,body=lib_http.getdata4info(runthime['args'][0])
        soup=BeautifulSoup(body)
        lks=lib_http.getlinks4soup(soup,runthime['batch'],host=lib_http.getdomain4url(runthime['args'][0]))
        pool=lib_TheardPool2.threadpool(runthime['t'])
        pool.addtask(downREC,(runthime['args'][0],runthime['args'][1]))
        pool.waitPoolComplete()

def downREC(url,savepaht):
    bmd=lib_http.bmdownload(1,1,0)
    bmd.download(url,savepaht)