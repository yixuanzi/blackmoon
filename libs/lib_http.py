import pycurl
import os
import sys
import StringIO
import urllib2
import lib_TheardPool2
import shutil
import gzip



flock=lib_TheardPool2.getlock()
  
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


def setsubthead(opts,obj):
    if type(obj)==lib_TheardPool2.threadpool:
        for i in range(len(obj.threads)):
            obj.threads[i].theadvars['speed']=0
            obj.threads[i].theadvars['objc']=pycurl.Curl()
            for key,value in opts.iteritems():
                obj.threads[i].theadvars['objc'].setopt(key,value)         
                obj.threads[i].theadvars['objs']=StringIO.StringIO()
 
    else:
        print "parameter error!!!"
        exit(1)
    
def getspeed(obj):
    speed=0
    for thread in obj.threads:
        speed+=thread.theadvars['speed']
    print "Now download speed is %.2f kb/second" %speed 


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
    