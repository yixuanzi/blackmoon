import sys
import os
import lib_http
import lib_func
import lib_interactive

class bmplugin:
    
    def __init__(self,main_interactive):
        self.main_interactive=main_interactive
    
    def getmaintive(self):
        return self.main_interactive