import os
import sys
import urllib2
import pycurl
import StringIO
import json
import copy

from bmplugin import *

thread=1 # numbers of download threads



def setobjc(objc,opts):
    for key,value in opts.iteritems():
        objc.setopt(key,value)
    return objc

########################################################################
class baidupcsi:
    """"""
    #----------------------------------------------------------------------
    __useragent="netdisk;5.3.4.5;PC;PC-Windows;6.2.9200;WindowsBaiduYunGuanJia"
    def getinitobj(self,token):
        opts={pycurl.USERAGENT:self.__useragent,pycurl.COOKIE:"BDUSS=%s" %token}
        objc=pycurl.Curl()
        objc=setobjc(objc,opts)
        #objc.setopt(pycurl.PROXY,"http://127.0.0.1:8088")
        return objc

    def getinfolink(self,path):
        return "http://d.pcs.baidu.com/rest/2.0/pcs/file?app_id=250528&method=download&check_blue=1&ec=1&path="+lib_http.u28quote(path)
    
    def getlistlink(self,path):
        return "http://pan.baidu.com/api/list?dir="+lib_http.u28quote(path)+"&page=1&num=1000&clienttype=8"
    
    def getuseragent(self):
        return self.__useragent
    
    def getdelobj(self,flist):
        filelist="filelist="+str([lib_http.u28quote(f) for f in flist]).replace("'",'"')
        opts={pycurl.URL:"http://pan.baidu.com/api/filemanager?opera=delete&clienttype=8",pycurl.POST:1,pycurl.POSTFIELDS:filelist}
        objc=setobjc(self.getinitobj(),opts)
        return objc
    
    def getputsobj(self,dst,size,md5):
        post='path=%s&size=%d&isdir=0&block_list=["%s"]&method=post&rtype=2' %(dst,size,md5)
        opts={pycurl.URL:"http://pan.baidu.com/api/create?a=commit&clienttype=8",pycurl.POST:1,pycurl.POSTFIELDS:post}
        objc=setobjc(self.getinitobj(),opts)
        return objc
    
    def getuploadid(self,dstfile,size,md5s):
        post='path=%s&size=%d&isdir=0&block_list=["%s"]&autoinit=1&method=post' %(dstfile,size,md5s)
        objs=StringIO.StringIO()
        opts={pycurl.URL:"http://pan.baidu.com/api/precreate?clienttype=8",pycurl.POST:1,pycurl.POSTFIELDS:post,pycurl.WRITEFUNCTION:objs.write}
        objc=setobjc(self.getinitobj(),opts)
        objc.perform()
        js=json.loads(objs.getvalue())
        if js['errno']==0:
            return js['uploadid']
        else:
            print "Error:get uploadid fail"
        
    def getuoloadobj(self,dstfile,uploadid,srcfile):
        url="http://c2.pcs.baidu.com/rest/2.0/pcs/superfile2?app_id=250528&method=upload&path=%s&uploadid=%s&partseq=0" %(dstfile,uploadid)
        objs=StringIO.StringIO()
        opts={pycurl.URL:url,pycurl.POST:1,pycurl.HTTPPOST:[("theFile",(pycurl.FORM_FILE,srcfile))],pycurl.WRITEFUNCTION:objs.write}
        objc=setobjc(self.getinitobj(),opts)
        objc.perform()
        rs=objs.getvalue()
        
#cc=config()
#uid=cc.getuploadid('/TMP/test.txt',2710,'67b11e30c07ccb7bbd86a4336e79f2d8')
#cc.getuoloadobj('/TMP/tset.txt',uid,'z:\\info.txt')