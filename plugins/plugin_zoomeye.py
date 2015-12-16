#https://www.zoomeye.org/help/manual
import lib_http
import pycurl
import sys
import urllib2
import gzip
import StringIO
from bs4 import *


class zoomeye:
    def __init__(self):
        self.helplink="https://www.zoomeye.org/help/manual"
        self.zoomc=zoomeye=pycurl.Curl()
        self.zoomc.setopt(pycurl.SSL_VERIFYPEER, 0)     # https
        self.zoomc.setopt(pycurl.SSL_VERIFYHOST, 0)
        opts={pycurl.USERAGENT:"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",\
              pycurl.COOKIE:"Hm_lvt_e58da53564b1ec3fb2539178e6db042e=1449477404,1449796789,1450150933; csrftoken=Tt2v0u4KEdcawjRAJw6ZKn94nM4bpWMd; sessionid=osdpz6v4fk6cxgr6813mxnxr6lnikv14; __jsluid=18350d75c69ee18b1ab16c96da836eb9; Hm_lpvt_e58da53564b1ec3fb2539178e6db042e=1450158229; __jsl_clearance=1450161556.988|0|SMRt%2FXvdqf7fxCeD6xZpY8RP3T4%3D",\
              pycurl.HTTPHEADER:["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
                                 "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",\
                                 "Accept-Encoding: gzip, deflate",\
                                 "Connection: keep-alive"]\
              }
        for key,value in opts.iteritems():
            self.zoomc.setopt(key,value)  
        self.zoomc.setopt(pycurl.PROXY,"http://127.0.0.1:8088")
        self.initzoomeye()
        
    def getzoomtoken(self):
        useragent=raw_input("please input the User-Agent:")
        if useragent:
            self.zoomc.setopt(pycurl.USERAGENT,useragent)
        cookie=raw_input("please input the zoom cookie token:")
        if cookie:
            self.zoomc.setopt(pycurl.COOKIE,cookie)
    
    def isvaildzoom(self):
        head,body=lib_http.getdata4info("https://www.zoomeye.org",objc=self.zoomc)
        #print head
        hdt=lib_http.parsehttphead(head)
        if hdt['code']=='521':
            return 0
        return 1
        
    def initzoomeye(self):
        while 1:
            if not self.isvaildzoom():
                self.getzoomtoken()
            else:
                break
            
    def zoomsearch(self,sstr,limit=20):
        sstr=urllib2.quote(sstr)
        surl="https://www.zoomeye.org/search?q="+sstr
        devices=self.getzoomsrs(surl,limit)
        return devices
    
    def getzoomsrs(self,surl,limit):
        p=1
        deviceALL=[]
        while 1:
            url="%s&p=%d" %(surl,p)
            body=self.getzoom4url(url)
            zoomdevs=self.parsezoom4body(body)
            if len(zoomdevs)<10 or (len(deviceALL)+10)>limit:
                deviceALL.extend(zoomdevs)
                return deviceALL
            deviceALL.extend(zoomdevs)
            p+=1
            
    def getzoom4url(self,url):
        while 1:
            head,body=lib_http.getdata4info(url,{pycurl.URL:url},self.zoomc)
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
            devdit['ip']=device.find('a',{"class":"ip"}).contents[0]
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

#zoom=zoomeye()
#devs=zoom.zoomsearch("esgcc.com.cn")
#zoom.printdevinfo(devs)
