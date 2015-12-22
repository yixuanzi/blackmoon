#BLACKMOON
#author:Gbuyi
#email: yeying0311@126.com
#version v2_bate


#一个开放式漏洞利用平台，支持动态加载插件
	内置如下交互式命令
	* load	load [-o objname] filename
	* search	search plugin for you key
	* varobj	list objection in the space
	* help	print help msg for you question
	* dump	dump [-o filename] [--space=space] objname
	* clear	clear [-a] [-s space.name] 
	* eval	eval python_segment
	* plugins	list loaded plugins
	* example	this is example plugin


#插件样例
	根据功能要求加载自身需要模块
	import pycurl
	import sys
	import urllib2
	import gzip
	import StringIO
	from bs4 import *
	
	必须加载模块，由程序提供
	from bmplugin import *

	info={'desc':"this is a example for you",
		'cve':'',
		'link':"help link"} 

	def init_plugin(main):
		'''命令名，命令触发函数，命令功能描述，推荐固定参数__file__'''
		active.regcommand('example',test_func,"this is example plugin",__file__)

	def test_func(paras):
		命令帮助文档，通过使用 htlp command 可调出此处帮助文字
		"""example test_string"""
		print "you can do everything"


	
#基础函数库

#lib_config
    class bmconfig
     |########################################################################
     |  
     |  Methods defined here:
     |  
     |  __del__(self)
     |  
     |  __init__(self, path)
     |      Constructor
     |  
     |  getconfig(self, section, key)
     |  
     |  setconfig(self, section, key, value)
	 
	 
#lib_func
	FUNCTIONS
    dumpobj(obj, path)
    
    execShell(cmd)
    
    getMD5(fname)
    
    getmin(a, b)
    
    getparasdict(matparas, formats, formatm=[])
    
    getrandomstr(i=4)
    
    loadobj(path)
    
    mystrip(s, c='-')
    
    printlist(ablist, flag=0)
    
    printstr(s, flag=0)
    
    runjs(js)

#lib_interactive

    class interactive
     |  ########################################################################
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      my interactive for buyi
     |  
     |  defaultprefix(self)
     |  
     |  getcmddict(self)
     |  
     |  getfunction(self, name, groups=None, tp=0)
     |      0 function       1 desc message  2 help message
     |  
     |  getgvars(self, key)
     |  
     |  regcommand(self, cmd, func, msg='No desc msg', sfile='buildins')
     |      plugin sfile must be __file__
     |  
     |  reggvars(self, key, value)
     |  
     |  setdefaultgroups(self, groups)
     |  
     |  start(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  welcome = "The interctive is start\nYou can use 'exit' 'quit' to quit ...

	 
#lib_http

FUNCTIONS
    downdata4info(downinfo, fhand, num, theadvars)
    
    download4info(downinfo, theads=5)
    
    getdata4info(url, opts={}, objc=None, objs=None, objh=None, timeout=5)
    
    gethttpresponse(hhead, hbody)
    
    getspeed(obj)
    
    parsehttphead(head)
    
    setsubthead(opts, obj)

#lib_ThreadPool2

CLASSES
    threading.Thread(threading._Verbose)
        taskclass
        threadpool
    
    class taskclass(threading.Thread)
     |  Method resolution order:
     |      taskclass
     |      threading.Thread
     |      threading._Verbose
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __del__(self)
     |  
     |  __init__(self, debug=False, name=None, waitime=1)
     |  
     |  addtask(self, func_args)
     |  
     |  run(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from threading.Thread:
     |  
     |  __repr__(self)
     |  
     |  getName(self)
     |  
     |  isAlive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  isDaemon(self)
     |  
     |  is_alive = isAlive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  join(self, timeout=None)
     |      Wait until the thread terminates.
     |      
     |      This blocks the calling thread until the thread whose join() method is
     |      called terminates -- either normally or through an unhandled exception
     |      or until the optional timeout occurs.
     |      
     |      When the timeout argument is present and not None, it should be a
     |      floating point number specifying a timeout for the operation in seconds
     |      (or fractions thereof). As join() always returns None, you must call
     |      isAlive() after join() to decide whether a timeout happened -- if the
     |      thread is still alive, the join() call timed out.
     |      
     |      When the timeout argument is not present or None, the operation will
     |      block until the thread terminates.
     |      
     |      A thread can be join()ed many times.
     |      
     |      join() raises a RuntimeError if an attempt is made to join the current
     |      thread as that would cause a deadlock. It is also an error to join() a
     |      thread before it has been started and attempts to do so raises the same
     |      exception.
     |  
     |  setDaemon(self, daemonic)
     |  
     |  setName(self, name)
     |  
     |  start(self)
     |      Start the thread's activity.
     |      
     |      It must be called at most once per thread object. It arranges for the
     |      object's run() method to be invoked in a separate thread of control.
     |      
     |      This method will raise a RuntimeError if called more than once on the
     |      same thread object.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from threading.Thread:
     |  
     |  daemon
     |      A boolean value indicating whether this thread is a daemon thread (True) or not (False).
     |      
     |      This must be set before start() is called, otherwise RuntimeError is
     |      raised. Its initial value is inherited from the creating thread; the
     |      main thread is not a daemon thread and therefore all threads created in
     |      the main thread default to daemon = False.
     |      
     |      The entire Python program exits when no alive non-daemon threads are
     |      left.
     |  
     |  ident
     |      Thread identifier of this thread or None if it has not been started.
     |      
     |      This is a nonzero integer. See the thread.get_ident() function. Thread
     |      identifiers may be recycled when a thread exits and another thread is
     |      created. The identifier is available even after the thread has exited.
     |  
     |  name
     |      A string used for identification purposes only.
     |      
     |      It has no semantics. Multiple threads may be given the same name. The
     |      initial name is set by the constructor.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from threading._Verbose:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class threadpool(threading.Thread)
     |  Method resolution order:
     |      threadpool
     |      threading.Thread
     |      threading._Verbose
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, tmax=20, tasks=0, start=True, debug=False, waitime=1)
     |      #----------------------------------------------------------------------
     |  
     |  addtask(self, func, args)
     |  
     |  initsubthead(self, func, args)
     |  
     |  run(self)
     |  
     |  waitPoolComplete(self, func=None)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from threading.Thread:
     |  
     |  __repr__(self)
     |  
     |  getName(self)
     |  
     |  isAlive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  isDaemon(self)
     |  
     |  is_alive = isAlive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  join(self, timeout=None)
     |      Wait until the thread terminates.
     |      
     |      This blocks the calling thread until the thread whose join() method is
     |      called terminates -- either normally or through an unhandled exception
     |      or until the optional timeout occurs.
     |      
     |      When the timeout argument is present and not None, it should be a
     |      floating point number specifying a timeout for the operation in seconds
     |      (or fractions thereof). As join() always returns None, you must call
     |      isAlive() after join() to decide whether a timeout happened -- if the
     |      thread is still alive, the join() call timed out.
     |      
     |      When the timeout argument is not present or None, the operation will
     |      block until the thread terminates.
     |      
     |      A thread can be join()ed many times.
     |      
     |      join() raises a RuntimeError if an attempt is made to join the current
     |      thread as that would cause a deadlock. It is also an error to join() a
     |      thread before it has been started and attempts to do so raises the same
     |      exception.
     |  
     |  setDaemon(self, daemonic)
     |  
     |  setName(self, name)
     |  
     |  start(self)
     |      Start the thread's activity.
     |      
     |      It must be called at most once per thread object. It arranges for the
     |      object's run() method to be invoked in a separate thread of control.
     |      
     |      This method will raise a RuntimeError if called more than once on the
     |      same thread object.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from threading.Thread:
     |  
     |  daemon
     |      A boolean value indicating whether this thread is a daemon thread (True) or not (False).
     |      
     |      This must be set before start() is called, otherwise RuntimeError is
     |      raised. Its initial value is inherited from the creating thread; the
     |      main thread is not a daemon thread and therefore all threads created in
     |      the main thread default to daemon = False.
     |      
     |      The entire Python program exits when no alive non-daemon threads are
     |      left.
     |  
     |  ident
     |      Thread identifier of this thread or None if it has not been started.
     |      
     |      This is a nonzero integer. See the thread.get_ident() function. Thread
     |      identifiers may be recycled when a thread exits and another thread is
     |      created. The identifier is available even after the thread has exited.
     |  
     |  name
     |      A string used for identification purposes only.
     |      
     |      It has no semantics. Multiple threads may be given the same name. The
     |      initial name is set by the constructor.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from threading._Verbose:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

	FUNCTIONS
		getlock()