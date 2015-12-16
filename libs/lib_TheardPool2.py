import threading
import sys
import time
import Queue
import httplib2
#=============================================================================

def getlock():
    return threading.RLock()


class taskclass(threading.Thread):
    def __init__(self,debug=False,name=None,waitime=1):
        threading.Thread.__init__(self)
        self.queue=Queue.Queue()
        self.stop=False
        self.debug=debug
        self.waitime=waitime
        if name:
            self.setName(name)
        self.theadvars={}
        
    def run(self):
        while True:
            try:
                if self.stop:
                    break
                func,args=self.queue.get(timeout=self.waitime)
                args=list(args)
                args.append(self.theadvars)
                func(*args)
            except Queue.Empty:
                if self.debug:
                    print "\nSubThread task queue is empty"
                break 
            
    def addtask(self,func_args):
        self.queue.put(func_args)
        
    def __del__(self):
        if self.debug:
            print "thead:%s is finish" %self.getName()
            
class threadpool(threading.Thread):

    #----------------------------------------------------------------------
    def __init__(self,tmax=20,tasks=0,start=True,debug=False,waitime=1):
        threading.Thread.__init__(self)
        self.queue=Queue.Queue()
        self.debug=debug
        self.threads=[taskclass(debug=self.debug) for i in range(tmax)]
        self.waitime=waitime
        self.stop=False
        self.tasks=tasks
        self.currentasks=0        
        if start:
            self.start()
            
    def initsubthead(self,func,args):
        args=list(args)
        args.append(self)
        func(*args)
        

    def run(self):
        while True:
            try:
                if self.tasks>0 and self.currentasks>=self.tasks:
                    print "\nspecify task number is complete!!!"
                    break
                if self.stop:
                    break
                func_args=self.queue.get(timeout=self.waitime)
                for thead in self.threads:
                    thead.addtask(func_args)
                    self.currentasks+=1
                    if self.debug:
                        print func_args
                    if not thead.is_alive():
                        thead.start()
                
            except Queue.Empty:
                if self.debug:
                    print "\nThread Pool is empty"
                break
            
        self.waitsubcomplete()
        self.stop=True
        
            
    def addtask(self,func,args):
        self.queue.put((func,args))
    
    def waitsubcomplete(self):
        if self.debug:
            print "Wait all subthread complete..."
        for thead in self.threads:
            if  thead.isAlive():
                thead.join()
                
    def waitPoolComplete(self,func=None):
        while not self.stop:
            if func:
                func(self)
            time.sleep(1)
        if self.debug:
            print "This Pool subthead is all finish  succfully!!!"
########################################################################


  
                    
        
                
            
                
        
        
        
        
        
    
    