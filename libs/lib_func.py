#coding : utf-8
import md5
import hashlib 
import os
import subprocess
import sys
import getopt
import pickle

import lib_func

def execShell(cmd):
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.stdout.read(),p.stderr.read()

def getMD5(fname):
    if sys.platform=='win32' and os.path.isfile(fname):
        rs=execShell('certutil -hashfile %s MD5' %fname)
        md5s=rs.split('\r\n')[1].replace(' ','')
        return md5s
    
def printstr(s,flag=0):
    
    fd={0:'INFO:',1:"WARING:",2:"ERROR:"}
    if type(flag)==str:
        print flag,s
        return
    print fd[flag],s
    
def printlist(ablist,flag=0):
    for i in ablist:
        if flag:
            print i
        else:
            print i,
    if not flag:
        print ''
    
def getparasdict(matparas,formats,formatm=[]):
    plist=matparas.split(' ')
    try:
        opts,args=getopt.getopt(plist,formats,formatm)
        pd={}
        for item in opts:
            pd[mystrip(item[0])]=item[1]
        if args and args[0]:
            pd['args']=args
        return pd
    except Exception:
        lib_func.printstr("parameter string is error for you formats",2)
        
def mystrip(s,c='-'):
    return s.replace(c,"")

def getrandomstr(i=4):
    import random
    cc='abcdefghijklmnopqrstuvwxzy'
    s=''
    for i in range(i):
        s+=cc[random.randint(0,25)]
    return s

def runjs(js):
    import PyV8
    v8=PyV8.JSContext()
    v8.enter()
    try:
        func=v8.eval(js)
    except Exception:
        lib_func.printstr("Javascript sytia error",2)
        return None
    return func()

def getmin(a,b):
    if a>b:
        return b
    return a

def loadobj(path):
    try:
        obj=pickle.load(file(path,'rb'))
        return obj
    except Exception:
        printstr("load object fail in %s" %path,1)
        return None

def dumpobj(obj,path):
    try:
        f=open(path,'wb')
        pickle.dump(obj,f)
    except Exception:
        printstr("dump object to %s fail" %path,2)
        return None

def isip(s):
    import re
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}$',s):
        return True
    return False

    
def setparas(pdict,ddict,args=0):
    """use paraster dict and default paraster dict to set the runtime variter"""
    for key in ddict.keys():
        if pdict.has_key(key):
            if pdict[key]:
                ddict[key]=pdict[key]
            else:
                ddict[key]=1
    
    if args and pdict.has_key('args') and args==len(pdict['args']):
        ddict['args']=pdict['args']
        return True
    elif args==0:
        if pdict.has_key('args'):
            ddict['args']=pdict['args']
        return True
    else:
        return False

def gethome():
    home=os.environ['HOMEPATH']
    if sys.platform=='win32':
        root=os.environ['SYSTEMROOT']
        return os.path.split(root)[0][:2]+home
    return home

def tounicode(string):
    try:
        s=string.decode('gbk')
    except UnicodeDecodeError:
        s=string.decode('utf8')
    return s

def getcwd4file(string):
    return os.path.split(string)[0]

def compereversion(v1,v2,sp='.',seg=3):
    v1s=v1.split(sp)
    v2s=v2.split(sp)
    try:
        for i in range(seg):
            vi1=int(v1s[i])
            vi2=int(v2s[i])
            if vi1>vi2:
                return 1
            elif vi1<vi2:
                return 2
        return 0
    except Exception:
        return -1

def copylist(objlist,value=None):
    obj=list()
    obj.extend(objlist)
    if value:
        obj.append(value)
    return obj

def copydict(objdict,kv=None):
    obj=dict()
    obj.update(objdict)
    if kv:
        obj[kv[0]]=kv[1]
    return obj
