import sys
import os
import pycurl
import re
import lib_http
import lib_func
import lib_interactive
import lib_config
import lib_TheardPool2
from bs4 import *

PWD_PATH=os.getcwd()

TOOL_PATH=PWD_PATH+'/plugins/tool'

CONFIG_PATH=PWD_PATH+'/plugins/config/plugins.ini'

PLUGINS_PATH=[PWD_PATH+'/plugins/auxiliary',\
              PWD_PATH+'/plugins/exploit',\
              PWD_PATH+'/plugins/misc',\
              PWD_PATH+'/plugins/scan']

PLUGINS_GROUPS=['buildins','exploit','misc','auxiliary','scan']