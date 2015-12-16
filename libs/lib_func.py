#coding : utf-8
import md5
import hashlib 
import os
import subprocess
import sys

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
    print fd[flag],s
    
def printlist(ablist,flag=0):
    for i in ablist:
        if flag:
            print i
        else:
            print i,
    print ''