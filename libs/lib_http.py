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
import re
import math

flock=lib_TheardPool2.getlock()
curlopts={pycurl.USERAGENT:"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",\
          pycurl.HTTPHEADER:["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
                         "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",\
                         "Accept-Encoding: gzip, deflate",\
                         "Connection: keep-alive"]
          }

class bmdownload:
    """blackmoon download class"""
    def __init__(self,log=1):
        self.log=log
        self.flock=lib_TheardPool2.getlock()
       
    def download(self,address,savepath,savename="",opts={},thread=1):
        if not address:
            lib_func.printstr("You should input vaild urls",2)
            return
        objc=self.initobjc(opts)
        try:
            finfo=self.getfileinfo(objc,address)
        except Exception as e:
            lib_func.printstr(str(e),"DD:Get ddinfo faile:")
            return
        opts=lib_func.copydict(opts,(pycurl.URL,finfo[0]))
        
        if finfo[1]==0:
            lib_func.printstr("Have error in download",2)
            return
        block=self.getblock(finfo[1])
        fname=savepath+'/'+savename
        dlinfo={'url':finfo[0],'save':fname,'size':finfo[1],'block':block,'status':[0 for i in range(int(math.ceil(float(finfo[1])/block)))]}
        self.printdd(dlinfo)
        f=self.getfp(dlinfo['save'],dlinfo['size'])
        pool=lib_TheardPool2.threadpool(thread,start=False)
        pool.initsubthead(self.initsub,(opts,))
        [pool.addtask(self.getbytes,(dlinfo,i,f))for i in range(len(dlinfo['status']))]
        pool.start()
        pool.waitPoolComplete(self.getspeed)
        f.close()
    
    def getspeed(self,pool):
        speed=0
        for thread in pool.threads:
            #print "%.2f kb/s" %(thread.threadvars['speed']/1024),
            speed+=thread.threadvars['speed']
        #print ''
        if self.log:
            lib_func.printstr("%.2f kb/s" %(speed/1024),"DD:Speed:")
        else:
            pass
        
    def getfp(self,savepath,size):
        if os.path.isfile(savepath+'.bmcache'):
            f=None
            pass
        else:
            f=open(savepath,'wb')
            f.seek(size-3)
            f.write('EOF')
            f.flush()
        return f

    def printdd(self,dlinfo):
        lib_func.printstr(dlinfo['url'],"DD:URL:")
        lib_func.printstr(dlinfo['save'],"DD:SAVE:")
        lib_func.printstr(dlinfo['size'],"DD:SIZE:")
        
    def initobjc(self,opts):
        objc=pycurl.Curl()
        for key,value in curlopts.iteritems():
            objc.setopt(key,value)
        for key,value in opts.iteritems():
            objc.setopt(key,value)
        objc.setopt(pycurl.SSL_VERIFYPEER, 0)
        objc.setopt(pycurl.SSL_VERIFYHOST, 0)
        #objc.setopt(pycurl.TIMEOUT,10)
        return objc
    
    def initsub(self,opts,pool):
        for thread in pool.threads:
            thread.threadvars['objc']=self.initobjc(opts)
            thread.threadvars['speed']=0
    
    def write2file(self,objs,dlinfo,index,fp):
        self.flock.acquire()
        fp.seek(index*dlinfo['block'])
        fp.write(objs.getvalue())
        self.flock.release()

    def getbytes(self,dlinfo,index,fp,threadvar):
        objc=threadvar['objc']
        objs=StringIO.StringIO()
        objc.setopt(pycurl.WRITEFUNCTION, objs.write)
        objc.setopt(pycurl.RANGE,"%d-%d" %(index*dlinfo['block'],(index+1)*dlinfo['block']-1))
        for i in range(3):
            try:
                objc.perform()
                threadvar['speed']=objc.getinfo(pycurl.SPEED_DOWNLOAD)
                self.write2file(objs,dlinfo,index,fp)
                return
            except Exception as e:
                lib_func.printstr(str(e),"DD:Exception:")

        lib_func.printstr("Time out ,can't download",2)
    
    def getblock(self,size):
        if size<=10*1024:
            block=1024 #1KB
        elif size<=100*1024:
            block=1024*10 #10KB
        elif size<=1024*1024:
            block=1024*100 #100KB
        else:
            block=1024*500 #500KB
        '''
        elif size<=1024*1024*10:
            block=1024*1024 #1M
        else:
            block=1024*1024*1 #2M
        '''
        return block
 
    def getfileinfo(self,objc,url,follow=3):
        #get real download link and file size
        head=list()
        head.extend(curlopts[pycurl.HTTPHEADER])
        head.append('Range: bytes=0-0')
        objc.setopt(pycurl.HTTPHEADER,head)
        
        eurl=geteffectiveurl(objc,url,5)
        size=0
        name=""
        head,body=get4url(eurl,{},objc)
        parseh=parsehttphead(head)
        if parseh.has_key('content-range'):
            size=int(parseh['content-range'].split('/')[1])
  
        if parseh.has_key('content-disposition'):
            m=re.search(r'filename=\"(.*?)\"',parseh['content-disposition'])
            if m:
                name=m.groups()[0]
            
        return eurl,size,name
     

def getdata4info(url,opts={},objc=None,objs=None,objh=None,timeout=5):
    if not objc:
        objc=pycurl.Curl()
        objc.setopt(objc.SSL_VERIFYPEER, 0)     # https
        objc.setopt(objc.SSL_VERIFYHOST, 0)
    if not objs:
        objs=StringIO.StringIO()
    if not objh:
        objh=StringIO.StringIO()
    objc.setopt(pycurl.URL,url.strip())
    objc.setopt(pycurl.TIMEOUT,timeout)
    objc.setopt(pycurl.WRITEFUNCTION, objs.write)
    objc.setopt(pycurl.HEADERFUNCTION,objh.write)  
    for key,value in opts.iteritems():
        objc.setopt(key,value)  
    objc.perform()
    return objh.getvalue(),objs.getvalue()


def get4url(url,curlopts={},objc=None,timeout=5):
    if url:
        return getdata4info(url,curlopts,objc,timeout=timeout)


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
            hdt[key.lower()]=value.strip()
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

def u28quote(string):
    return urllib2.quote(string.encode('utf8'))



def geteffectiveurl(objc,url,nums=3):
    objc.setopt(pycurl.FOLLOWLOCATION,0)
    for i in range(nums):
        head,body=get4url(url,{},objc)
        hdict=parsehttphead(head)
        if hdict.has_key('location'):
            url=hdict['location']
            continue
        return url.strip()
    return None
    
    
    
"""
  def downdata4info(downinfo,fhand,num,threadvars):
        objc=threadvars['objc']
        #objs=threadvars['objs']
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
        threadvars['speed']=objc.getinfo(objc.SPEED_DOWNLOAD)/1024
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
    
"""