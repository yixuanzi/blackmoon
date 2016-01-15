import os
import pickle
import math
import sys
import time
import StringIO
import json
from bdcloud_interface import baidupcsi

from bmplugin import *



class bdcloud: #path must unicode
    main=None
    pcsi=baidupcsi()
    def __init__(self,flag=None):
        bdcloud.main.reloadconfig()
        self.config={'token':bdcloud.main.pcf.getconfig('baidu','token'),'useragent':bdcloud.main.pcf.getconfig('bdpcs','useragent')}
        self.opts={pycurl.USERAGENT:self.config['useragent'],pycurl.COOKIE:"BDUSS=%s" %self.config['token']}
        if flag=='debug':
            self.opts[pycurl.PROXY]="http://127.0.0.1:8088"
        self.currentdir=u'/'
        self.tree={}
        self.intertive=lib_interactive.interactive()
        self.prefix=self.intertive.prefix[:-1]
        self.calltable={'ls':self.ls,'pwd':self.pwd,'put':self.put,'get':self.get,\
                        'cd':self.cd,'del':self.delete,'login':self.login,'logout':self.logout}
        self.dd=lib_http.bmdownload()
        for name,func in self.calltable.iteritems():
            self.intertive.regcommand(name,func,func.__doc__)
        self.changeprefix()
        
    def login(self,paras):
        """ login username passwd"""
        pass
    
    def logout(self,paras):
        """logout"""
        self.config={}
        
    def changeprefix(self):
        self.intertive.setdefaultprefix("%s$%s>" %(self.prefix,self.currentdir))
        
    def putsecond(self,srcfile,dst=None):
        md5s=lib_func.getMD5(srcfile)
        size=os.path.getsize(srcfile)
        d,n=os.path.split(srcfile)
        if not dst:
            dst=self.currentdir+'/'+n
        else:
            dst=self.getrealpath(dst)+'/'+n
            
        objc=self.pcsi.getputsobj(dst,size,md5s)
        objs=StringIO.StringIO()
        objc.setopt(pycurl.WRITEFUNCTION,objs.write)
        objc.perform()
        js=json.loads(objs.getvalue())
        if js['errno']==0:
            return 1
        else:
            return 0
        
    
    def delfile(self,plist):
        objc=self.pcsi.getdelobj(plist)
        objs=StringIO.StringIO()
        objc.setopt(pycurl.WRITEFUNCTION,objs.write)
        objc.perform()
        js=json.loads(objs.getvalue())
        if js['errno']==0:
            print "Del file list succfully"
        else:
            print "Del file list failed"
    
    def download(self,srcfile,ddir,threads=1,kp=True):
        start=time.time()
        fname=os.path.split(srcfile)[1]
        if kp and os.path.isfile(ddir+'/'+fname+'.bmcache') and os.path.isfile(ddir+'/'+fname+'.downinfo'):
            pass
        else:
            daddr=self.pcsi.getdownlink(srcfile)
            self.dd.download(daddr,ddir,fname,self.opts,threads)
        end=time.time()
        print "INFO: Download file %s succfulliy" %srcfile
        print "TIME:%.2f s" %(end-start)

    def printlist(self,flist):
        for fp in flist:
            if fp['isdir']:
                print "DIR %s\t%s\t%s" %(fp['server_filename'],"None",time.ctime(fp['local_mtime']))
            else:
                print "FILE %s\t%s\t%s" %(fp['server_filename'],fp['size'],time.ctime(fp['local_mtime']))
                
    def getlist(self,path):
        path=self.getrealpath(path)
        url=self.pcsi.getlistlink(path)
        if self.tree.has_key(path):
            return self.tree[path]
        head,body=lib_http.getdata4info(url,self.opts)
        js=json.loads(body)
        if js['errno']==0:
            self.tree[path]=js['list']
            return js['list']
        else:
            return None
    
    def getrealpath(self,path):
        if not path:
            path=self.currentdir
        elif path=='..':
            if self.currentdir=='/':
                return self.currentdir
            else:
                return os.path.split(self.currentdir)[0]
        elif path[0]!='/':
            if self.currentdir=='/':
                path=self.currentdir+path
            else:
                path=self.currentdir+'/'+path
        return path
    
    def isdir(self,path): # 1 dir 2 file 0 none
        path=self.getrealpath(path)
        if (self.tree.has_key(path) and self.tree[path]) or self.getlist(path):
            return 1
        return 0
    
    def download_dir(self,src,dst,threads):
        start=time.time()
        flist=self.getlist(src)
        for fp in flist:
            if fp['isdir']:
                nextsrc=src+'/'+fp['server_filename']
                nextdst=dst+'/'+fp['server_filename']
                os.mkdir(nextdst)
                self.download_dir(nextsrc,nextdst,threads)
            else:
                self.download(fp['path'],dst,threads)
        end=time.time()
        print "TIME:%.2f s" %(end-start)

    def ls(self,paras):
        """ls [path]"""
        ddict={}
        try:
            pd=lib_func.getparasdict(paras,"")
        except Exception:
            lib_func.printstr(self.ls.__doc__,1)
            return
        lib_func.setparas(pd,ddict)
        if ddict.has_key('args'):
            path=ddict['args'][0]
        else:
            path=None
        path=self.getrealpath(path)
        flist=self.getlist(path)
        if flist:
            self.printlist(flist)
        else:
            print "Error: have not exist %s" %path
    
    def vaildtoken(self):
        if self.getlist('/'):
            return 0
        return -1
        
    def pwd(self,paras):
        print self.currentdir
    
    def cd(self,paras):
        """cd [path]"""
        ddict={}
        try:
            pd=lib_func.getparasdict(paras,"")
        except Exception:
            lib_func.printstr(self.cd.__doc__,1)
            return
        lib_func.setparas(pd,ddict)
        if ddict.has_key('args'):
            path=ddict['args'][0]
        else:
            path=None
        path=self.getrealpath(path)
        if self.tree.has_key(path) or self.getlist(path):
            self.currentdir=path
            self.changeprefix()
            return
        else:
            print "Error:%s is not exist" %path
    
    def get(self,paras):
        """get [-t thread] src dst"""
        ddict={'t':1}
        try:
            pd=lib_func.getparasdict(paras,"t:")
        except Exception:
            lib_func.printstr(self.get.__doc__,1)
            return
        lib_func.setparas(pd,ddict,2)
        src=ddict['args'][0]
        dst=ddict['args'][1]
        threads=int(ddict['t'])
        
        src=self.getrealpath(src)
        if self.isdir(src):
            dst=dst+'/'+os.path.split(src)[1]
            os.mkdir(dst)
            self.download_dir(src,dst,threads)
        else:
            self.download(src,dst,threads)
    
    def upload(self,srcfile,dst):
        pass
    
    def putfile(self,srcfile,dst):
        if not self.putsecond(srcfile,dst):
            self.upload(srcfile,dst)
        
    
    def putdir(self,src,dst):
        pass
    
    def put(self,args):
        """put [-t thread] src dst"""
        ddict={'t':1}
        try:
            pd=lib_func.getparasdict(paras,"t:")
        except Exception:
            lib_func.printstr(self.put.__doc__,1)
            return
        lib_func.setparas(pd,ddict,2)
        
        if os.path.isfile(ddict['args'][0]):
            self.putfile(ddict['args'][0],ddict['args'][1])
        else:
            self.putdir(ddict['args'][0],ddict['args'][1])
    
    def delete(self,path):
        """del path"""
        ddict={}
        try:
            pd=lib_func.getparasdict(paras,"")
        except Exception:
            lib_func.printstr(self.delete.__doc__,1)
            return
        if lib_func.setparas(pd,ddict,1):
            path=self.getrealpath(ddict['args'][0])
            self.delfile([path])   
    
    def start(self):
        self.intertive.start()
                     
def start(paras):
    bdc=bdcloud(flag=paras)
    if bdc.vaildtoken()==0:
        bdc.start()
    else:
        lib_func.printstr("You must config vaild token for baidu pcs token in plugins.ini",1)
