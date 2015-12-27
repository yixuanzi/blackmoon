import pycurl
import os
import sys
import StringIO
import urllib2
import lib_TheardPool2
import lib_func
import shutil
import gzip
import urlparse


flock=lib_TheardPool2.getlock()

class bmdownload:
    """blackmoon download class"""
    def __init__(self,thread=1,bg=1,log=0):
        self.thread=thread
        self.bg=bg
        self.log=log
        
    def download(self,address,savepath):
        if address:
            addr=address
        else:
            lib_func.printstr("You should input vaild urls",2)
            return
    
    def getfileinfo(self,address):
        pass
    
def downdata4info(downinfo,fhand,num,theadvars):
    objc=theadvars['objc']
    #objs=theadvars['objs']
    objc.setopt(objc.SSL_VERIFYPEER, 0)     # https
    objc.setopt(objc.SSL_VERIFYHOST, 0)    
    objc.setopt(pycurl.URL,downinfo['location'])
    objs=StringIO.StringIO()
    #objc.setopt(objc.VERBOSE, 1)
    #objc.setopt(objc.DEBUGFUNCTION, test)
    objc.setopt(pycurl.WRITEFUNCTION, objs.write)
    #objc.setopt(pycurl.HEADERFUNCTION,objh.write)
    #objc.setopt(pycurl.FOLLOWLOCATION, 1)
    #objc.setopt(pycurl.HTTPHEADER,['Range: 0-1024'])
    #objc.setopt(pycurl.HEADER,True) #get head and body from stringio
    #objc.setopt(pycurl.WRITEHEADER,h)
    objc.setopt(pycurl.RANGE,"%d-%d" %(num*downinfo['block'],(num+1)*downinfo['block']-1))
  
    #objc.setopt(pycurl.USERAGENT,"netdisk;5.3.4.5;PC;PC-Windows;6.2.9200;WindowsBaiduYunGuanJia")
    #objc.setopt(pycurl.PROXY,"http://127.0.0.1:8088")
    objc.perform()
    flock.acquire()
    fhand.seek(num*downinfo['block'])
    fhand.write(objs.getvalue())
    downinfo['status'][num]=1
    flock.release()
    objs.close()
    theadvars['speed']=objc.getinfo(objc.SPEED_DOWNLOAD)/1024
    '''
    print "HTTP-code:", objc.getinfo(objc.HTTP_CODE) 
    print "Total-time:", objc.getinfo(objc.TOTAL_TIME)
    print "Download speed: %.2f bytes/second" % objc.getinfo(objc.SPEED_DOWNLOAD)
    print "Document size: %d bytes" % objc.getinfo(objc.SIZE_DOWNLOAD)
    print "Effective URL:", objc.getinfo(objc.EFFECTIVE_URL)
    print "Content-type:", objc.getinfo(objc.CONTENT_TYPE)
    print "Namelookup-time:", objc.getinfo(objc.NAMELOOKUP_TIME)
    print "Redirect-time:", objc.getinfo(objc.REDIRECT_TIME)
    print "Redirect-count:", objc.getinfo(objc.REDIRECT_COUNT)
    print "====================="
    '''
    
def getdata4info(url,opts={},objc=None,objs=None,objh=None,timeout=5):
    if not objc:
        objc=pycurl.Curl()
        objc.setopt(objc.SSL_VERIFYPEER, 0)     # https
        objc.setopt(objc.SSL_VERIFYHOST, 0)
    if not objs:
        objs=StringIO.StringIO()
    if not objh:
        objh=StringIO.StringIO()
    objc.setopt(pycurl.URL,url)
    objc.setopt(pycurl.TIMEOUT,timeout)
    objc.setopt(pycurl.WRITEFUNCTION, objs.write)
    objc.setopt(pycurl.HEADERFUNCTION,objh.write)  
    for key,value in opts.iteritems():
        objc.setopt(key,value)  
    objc.perform()
    return objh.getvalue(),objs.getvalue()


def download4info(downinfo,theads=5):
    if os.path.isfile(downinfo['savename']):
        fhand=open(downinfo['savename'],'wb+')
    else:
        fhand=open(downinfo['savename'],'w')
        fhand.seek(downinfo['size']-3)
        fhand.write('EOF')
        fhand.flush()
        fhand=open(downinfo['savename'],'wb+')
    pool=lib_TheardPool2.threadpool(theads,debug=0,start=False)
    for i in range(len(downinfo['status'])):
        if not downinfo['status'][i]:
            pool.addtask(downdata4info,(downinfo,fhand,i))
    pool.initsubthead(setsubthead,[{pycurl.USERAGENT:"netdisk;5.3.4.5;PC;PC-Windows;6.2.9200;WindowsBaiduYunGuanJia"}])
    pool.start()
    pool.waitPoolComplete(getspeed)
    fhand.close()
    shutil.move(downinfo['savename'],os.path.splitext(downinfo['savename'])[0])

def parsehttphead(head):
    heads=head.split('\r\n')
    hdt={}
    for dt in heads:
        dt=dt.strip()
        if dt[:4]=="HTTP":
            lt=dt.split(' ')
            hdt['version']=lt[0]
            hdt['code']=lt[1]
            if len(lt)==3:
                hdt['status']=lt[2]
            else:
                hdt['status']=''
        elif dt:
            key,value=dt.split(':',1)
            hdt[key.lower()]=value
    return hdt

def gethttpresponse(hhead,hbody):
    if hhead.has_key('content-encoding') and hhead['content-encoding'].find('gzip')>=0:
        return gzip.GzipFile(fileobj=StringIO.StringIO(hbody)).read()
    else:
        return hbody
    

def getpyurl(copt={},proxy=None,ffx=None):
    """ffx can set 'sgcc' and other,mean set the ffx head to this type"""
    obj=pycurl.Curl()
    obj.setopt(pycurl.SSL_VERIFYPEER, 0)     # https
    obj.setopt(pycurl.SSL_VERIFYHOST, 0)
    if ffx:
        ffxip=getrandomip(ffx)
    opts={pycurl.USERAGENT:"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",\
          pycurl.HTTPHEADER:["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
                             "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",\
                             "Accept-Encoding: gzip, deflate",\
                             "Connection: keep-alive"]
          }
    
    if ffx:
        opts[pycurl.HTTPHEADER].append("X-Forwarded-For: %s" %ffxip)
        
    for key,value in opts.iteritems():
        obj.setopt(key,value)
    if obj:
        for key,value in copt.iteritems():
            obj.setopt(key,value)
    if proxy:
        obj.setopt(pycurl.PROXY,proxy)
    
    return obj

def getrandomip(flag='net'):
    import random
    if flag=='sgcc':
        p1=10
    else:
        p1=random.randint(1,254)
    p2=random.randint(1,254)
    p3=random.randint(1,254)
    p4=random.randint(1,254)
    return "%d.%d.%d.%d" %(p1,p2,p3,p4)

def getlinks4soup(soup,filter='link|.*',host=None):
    lks=[]
    import re
    tags={'a':'href','img':'src','link':'src','javascript':'src'}
    filter=filter.split('|')
    for key,value in tags.iteritems():
        links=soup.findAll(key)
        for link in links:
            lk=link[value].strip()
            if host and lk[:4]=='http':
                lk=host+lk
            
            if filter[0]=='link' and  re.search(filter[1],lk):
                lks.append(lk)
            elif filter[0]=='type':
                inx=lk.rfind('.')
                if inx and re.search(filter,lk[inx+1:]):
                    lks.append(lk)
    return lks

def getdomain4url(urls):
    up=urlparse.urlsplit(urls)
    return "%s://%s" %(up.scheme,up.netloc)