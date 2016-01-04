#coding=utf8
import pycurl
import sys
import urllib2
import gzip
import StringIO
from bs4 import *
from bmplugin import *
import re


info={'desc':"get ip list object use www.zoomeye.org for search keys",
      'cve':'',
      'link':"https://www.zoomeye.org/help/manual"} 

zoom=None
lock=lib_TheardPool2.getlock()

def init_plugin(main):
    zoomeye.main=main
    active=main.maintive
    active.regcommand('zoomprint',zoom_search_print,"search result to print use zoomeye",__file__)
    active.regcommand('zoomeye',zoom_search_obj,"search result to object use zoomeye",__file__)

def getuseragent():
    return "Mozilla/5.0 (Windows NT 10.1; WOW64; rv:42.0) Gecko/20100101 Firefox/"+lib_func.getrandomstr(4)

class zoomeye:
    main=None
    zoomtoken={'__jsluid':"",'__jsl_clearance':"",'sessionid':""}
    useragent=getuseragent()
    def __init__(self,debugable=0,proxy=None):
        self.helplink="https://www.zoomeye.org/help/manual"
        self.zoomc=pycurl.Curl()
        zoomeye.zoomtoken['sessionid']=self.main.pcf.getconfig('zoomeye','token')
        self.zoomc.setopt(pycurl.SSL_VERIFYPEER, 0)     #https
        self.zoomc.setopt(pycurl.SSL_VERIFYHOST, 0)
        opts={pycurl.USERAGENT:self.useragent,\
              pycurl.HTTPHEADER:["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
                                 "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",\
                                 "Accept-Encoding: gzip, deflate",\
                                 "Connection: keep-alive"]\
              }
        for key,value in opts.iteritems():
            self.zoomc.setopt(key,value)
        if proxy:
            self.zoomc.setopt(pycurl.PROXY,proxy)
        #self.initzoomeye()
        
    def getzoomtoken(self):
        lib_func.printstr("Get Zoom token ing...")
        while 1:
            try:
                head,body=lib_http.getdata4info("https://www.zoomeye.org",objc=self.zoomc)
            except Exception:
                lib_func.printstr("Time Out",1)
                continue
            hdt=lib_http.parsehttphead(head)
            if hdt.has_key('set-cookie'):
                m=re.search('__jsluid=\w+;',hdt['set-cookie'])
                if m:
                    zoomeye.zoomtoken['__jsluid']=m.group()
            m=re.search(r"<script>(.+(eval\(.+\{\}\)\)\;).+)</script>",body)
            if m:
                js=m.groups()[1].replace('eval(','return(',1)
                js=lib_func.runjs("(function(){%s})" %js)
                js=js[:js.find('setTimeout')]
                js=re.sub(r"eval\(.+\{\}\)\)\;",js,m.groups()[0])
                js=js.replace('document.cookie=dc','return dc')
                rs=lib_func.runjs("(function(){%s})" %js)
                zoomeye.zoomtoken['__jsl_clearance']=re.search('__jsl_clearance=.+?;',rs).group()
            if self.isvaildzoom():
                lib_func.printstr("Get Zoom token OK")
                break
    def isvaildzoom(self):
        try:
            self.zoomc.setopt(pycurl.COOKIE,"%s %s" %(self.zoomtoken['__jsluid'],self.zoomtoken['__jsl_clearance']))
            head,body=lib_http.getdata4info("https://www.zoomeye.org",objc=self.zoomc)
        except Exception:
            lib_func.printstr("Time Out",1)
            return 0
        #print head
        hdt=lib_http.parsehttphead(head)
        if hdt['code']=='521':
            return 0
        return 1
        
    def initzoomeye(self):
        lock.acquire()
        if not self.isvaildzoom():
            self.getzoomtoken()
        lock.release()
    
    def zoomsearch(self,sstr,limit=10,target='host'):
        sstr=urllib2.quote(sstr)
        surl="https://www.zoomeye.org/search?q=%s&h=%s" %(sstr,target)
        devices=self.getzoomsrs(surl,limit)
        return devices
    
    def getzoomsrs(self,surl,limit,flag=0):
        """flag 0 means get one page result then get next one ,1 is not"""
        p=1
        deviceALL=[]
        while 1:
            url="%s&p=%d" %(surl,p)
            body=self.getzoom4url(url)
            zoomdevs=self.parsezoom4body(body)
            if flag or len(zoomdevs)<10 or ((len(deviceALL)+10)>=limit and limit>0):
                deviceALL.extend(zoomdevs)
                '''
                if len(zoomdevs)==0:
                    tp=BeautifulSoup(body)
                    if tp.find('span',{'class':'text-muted'}):
                        zoomeye.useragent=getuseragent()
                        return self.getzoomsrs(surl,limit,flag)
                '''
                return deviceALL
            deviceALL.extend(zoomdevs)
            p+=1
            
    def getzoomnumbers(self,url):
        body=self.getzoom4url(url)
        soup=BeautifulSoup(body)
        try:
            return int(soup.find('div',{'class':'result-summary'}).strong.contents[0].strip())
        except Exception:
            return -1
    
    def getzoom4url(self,url):
        while 1:
            try:
                head,body=lib_http.getdata4info(url,{pycurl.URL:url},self.zoomc)
            except Exception:
                lib_func.printstr("Time Out",1)
                continue
            hdt=lib_http.parsehttphead(head)
            if hdt['code']=='521':
                self.initzoomeye()
            else:
                return lib_http.gethttpresponse(hdt,body)
            
     
        
    def parsezoom4body(self,body):
        soup=BeautifulSoup(body)
        zoomdevs=[]
        #rs=soup.find("ul",{"class":"result device"})
        #devices=rs.findAll('li')
        ips=soup.findAll('a',{'class':'ip'})
        for ip in ips:
            device=ip.parent.parent
            zoomdevs.append(self.parsedevice2dict(device))
        return zoomdevs
    
    def parsedevice2dict(self,device):
        devdit={}
        try:
            devdit['ip']=str(device.find('a',{"class":"ip"}).contents[0])
            devdit['app']=device.find('li',{"class":"app"}).a.contents[0].strip()
            devdit['country']=device.find('a',{"class":"country"}).contents[2].strip()
            devdit['city']=device.find('a',{"class":"city"}).contents[0].strip()
            devdit['server']=device.header.s.a.contents[0].strip()
            devdit['port']=device.header.i.a.contents[0].strip()
            devdit['address']="%s:%s" %(devdit['ip'],devdit['port'])
        except Exception:
            pass
        return devdit
    
    def printdevinfo(self,devs):
        print "==============="
        print "Found about %d results" %len(devs)
        for dev in devs:
            for key,value in dev.iteritems():
                print key,value
            print  '============'

def init_zoom():
    global zoom
    if not zoom:
        zoom=zoomeye()
    
def zoom_search_print(paras):
    """zoomprint search_string"""
    init_zoom()
    if not paras:
        paras="port:6379"
    devs=zoom.zoomsearch(paras,10)
    zoom.printdevinfo(devs)
    
def zoom_search_obj(paras):
    """zoomeye [-o objname] [-t threads] [--max=limit] search_string"""
    init_zoom()
    try:
        pd=lib_func.getparasdict(paras,"o:t:",['max='])
    except Exception:
        lib_func.printstr(zoom_search_obj.__doc__,1)
        return    
    key=pd['args'][0]
    mmx=10
    threads=1
    if pd.has_key('max'):
        mmx=int(pd['max'])
    if pd.has_key('t'):
        threads=int(pd['t'])
    devs=zoomsearch(key,mmx,threads)
    if pd.has_key('o'):
        name=pd['o']
    else:
        name='zoom_rs_'+lib_func.getrandomstr()
    zoom.main.regobj(devs,name,__name__)

def initsubthread(pool):
    if type(pool)==lib_TheardPool2.threadpool:
        for i in range(len(pool.threads)):
            pool.threads[i].threadvars['zoom']=zoomeye()

def zoomwork(devs,url,lock,threadvar):
    subdevs=threadvar['zoom'].getzoomsrs(url,0,1)
    lock.acquire()
    devs.extend(subdevs)
    lib_func.printstr(url)
    print len(devs),len(subdevs)    
    lock.release()
    
def zoomsearch(key,limit,threads,target='host'):
    if threads==1:
        devs=zoom.zoomsearch(key,limit)
    else:
        import math
        devs=[]
        sstr=urllib2.quote(key)
        nm=zoom.getzoomnumbers("https://www.zoomeye.org/search?q=%s&h=%s" %(sstr,target))
        lib_func.printstr("Found result %d" %nm)
        if nm<=0:
            lib_func.printstr("This summary is emtry",1)
            return
        lock=lib_TheardPool2.getlock()
        pool=lib_TheardPool2.threadpool(tmax=threads,start=False)#,debug=True)
        pool.initsubthead(initsubthread,())
        ts=int(math.ceil(limit/10.0))
        total=int(math.ceil(nm/10.0))
        if ts:
            ts=lib_func.getmin(ts,total)
        else:
            ts=total
        for i in range(ts):
            surl="https://www.zoomeye.org/search?q=%s&h=%s&p=%d" %(sstr,target,i+1)
            pool.addtask(zoomwork,(devs,surl,lock))
        pool.start()
        pool.waitPoolComplete()
    return devs

#zoom=zoomeye()
#devs=zoom.zoomsearch("esgcc.com.cn")
#zoom.printdevinfo(devs)
