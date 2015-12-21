import sys
import os
import lib_http
import lib_func
import lib_interactive
import lib_config
import lib_TheardPool2

PWD_PATH=os.getcwd()

TOOL_PATH=PWD_PATH+'/plugins/tool'

CONFIG_PATH=PWD_PATH+'/plugins/config/plugins.ini'

PLUGINS_PATH=[PWD_PATH+'/plugins/auxiliary',\
              PWD_PATH+'/plugins/exploit',\
              PWD_PATH+'/plugins/misc']

PLUGINS_GROUPS=['buildins','exploit','misc','auxiliary']