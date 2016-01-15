import threading
import sys
import time
import Queue
import httplib2
#=============================================================================
#create thread pool,set number of thead and others
#init variable for every subthread of job if you want
#add task into pool
#wait all of subthread is over in the pool 
#!!!at the end of callback function(task function) parameters list is the subthread variable

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
        self.threadvars={}
        
    def run(self):
        while True:
            if not self.queue.empty():
                if self.stop:
                    break
                func,args=self.queue.get(timeout=self.waitime)
                args=list(args)
                args.append(self.threadvars)
                func(*args)
            else:
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
        flag=0
        while True:
            if self.tasks>0 and self.currentasks>=self.tasks:
                print "\nspecify task number is complete!!!"
                break
            if self.stop:
                break
            for thead in self.threads:
                if not self.queue.empty():
                    func_args=self.queue.get(timeout=self.waitime)
                else:
                    flag=1
                    break
                thead.addtask(func_args)
                self.currentasks+=1
                if self.debug:
                    print func_args
                if not thead.is_alive():
                    thead.start()  
            if flag:
                if self.debug:
                    print "\nThreadPool task queue is empty"                
                break
            
        self.__waitsubcomplete()
        self.stop=True
        
            
    def addtask(self,func,args):
        self.queue.put((func,args))
    
    def __waitsubcomplete(self):
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


  
                    
        
                
            
                
        
        
        
        
        
    
    